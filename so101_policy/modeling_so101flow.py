"""SO-101 flow policy v1 (research/FINAL_REPORT.md sections 3-4).

    images -> DINOv2 ViT-S (shared, fine-tuned at 0.1x LR) -> 8x10 pooled patch tokens per camera
    [scene tokens, wrist tokens, state token, task token] -> 6-layer transformer trunk -> memory
    noisy action chunk + per-token flow time -> 6-block DiT expert (self-attn, cross-attn to memory) -> velocity

Flow matching convention: x_tau = tau * action + (1 - tau) * noise, tau = 1 is clean data, the expert predicts
v = action - noise and sampling integrates tau from 0 to 1 with Euler steps.

Training-time RTC: a random prefix of d clean steps (tau = 1, excluded from the loss) teaches the expert to
continue a committed prefix. At inference predict_action_chunk(prev_chunk_left_over=..., inference_delay=d)
pins the first d steps to the part of the previous chunk that will run while the model is thinking, so
consecutive chunks join without a jump and without blending.
"""

import copy
import math
from collections import deque

import torch
import torch.nn.functional as F  # noqa: N812
from torch import Tensor, nn

from lerobot.policies.pretrained import PreTrainedPolicy
from lerobot.utils.constants import ACTION, OBS_STATE

from .configuration_so101flow import So101FlowConfig

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)
WRIST_CAMERA = "observation.images.camera2"


def timestep_embedding(tau: Tensor, dim: int = 256) -> Tensor:
    """Sinusoidal embedding of flow time in [0, 1]; any shape -> shape + (dim,)."""
    half = dim // 2
    freqs = torch.exp(-math.log(10000) * torch.arange(half, device=tau.device, dtype=torch.float32) / half)
    args = tau.float()[..., None] * 1000 * freqs
    return torch.cat([torch.cos(args), torch.sin(args)], dim=-1)


def modulate(x: Tensor, shift: Tensor, scale: Tensor) -> Tensor:
    return x * (1 + scale) + shift


class DiTBlock(nn.Module):
    """Self-attention over action tokens, cross-attention to the trunk memory, MLP; each sub-layer is
    modulated per token by the flow-time embedding (adaLN-zero, so a fresh block starts as identity)."""

    def __init__(self, dim: int, heads: int, dropout: float, mlp_ratio: int):
        super().__init__()
        self.norm1 = nn.LayerNorm(dim, elementwise_affine=False)
        self.self_attn = nn.MultiheadAttention(dim, heads, dropout=dropout, batch_first=True)
        self.norm2 = nn.LayerNorm(dim, elementwise_affine=False)
        self.cross_attn = nn.MultiheadAttention(dim, heads, dropout=dropout, batch_first=True)
        self.norm3 = nn.LayerNorm(dim, elementwise_affine=False)
        self.mlp = nn.Sequential(nn.Linear(dim, mlp_ratio * dim), nn.GELU(), nn.Dropout(dropout),
                                 nn.Linear(mlp_ratio * dim, dim))
        self.mod = nn.Linear(dim, 9 * dim)
        nn.init.zeros_(self.mod.weight)
        nn.init.zeros_(self.mod.bias)

    def forward(self, h: Tensor, c: Tensor, memory: Tensor) -> Tensor:
        s1, g1, b1, s2, g2, b2, s3, g3, b3 = self.mod(F.silu(c)).chunk(9, dim=-1)
        x = modulate(self.norm1(h), b1, s1)
        h = h + g1 * self.self_attn(x, x, x, need_weights=False)[0]
        x = modulate(self.norm2(h), b2, s2)
        h = h + g2 * self.cross_attn(x, memory, memory, need_weights=False)[0]
        x = modulate(self.norm3(h), b3, s3)
        return h + g3 * self.mlp(x)


class FlowExpert(nn.Module):
    def __init__(self, config: So101FlowConfig, action_dim: int):
        super().__init__()
        dim = config.expert_dim
        self.in_proj = nn.Linear(action_dim, dim)
        self.pos = nn.Parameter(torch.randn(1, config.chunk_size, dim) * 0.02)
        self.mem_proj = nn.Linear(config.dim_model, dim)
        self.time_mlp = nn.Sequential(nn.Linear(256, dim), nn.SiLU(), nn.Linear(dim, dim))
        self.blocks = nn.ModuleList(
            DiTBlock(dim, config.expert_heads, config.dropout, config.expert_mlp_ratio)
            for _ in range(config.n_expert_layers))
        self.final_norm = nn.LayerNorm(dim, elementwise_affine=False)
        self.final_mod = nn.Linear(dim, 2 * dim)
        self.out = nn.Linear(dim, action_dim)
        for layer in (self.final_mod, self.out):
            nn.init.zeros_(layer.weight)
            nn.init.zeros_(layer.bias)

    def forward(self, x_t: Tensor, tau: Tensor, memory: Tensor) -> Tensor:
        """x_t (B, H, A), tau (B, H) per-token flow time, memory (B, N, D) -> velocity (B, H, A)."""
        h = self.in_proj(x_t) + self.pos[:, : x_t.shape[1]]
        c = self.time_mlp(timestep_embedding(tau))
        m = self.mem_proj(memory)
        for block in self.blocks:
            h = block(h, c, m)
        shift, scale = self.final_mod(F.silu(c)).chunk(2, dim=-1)
        return self.out(modulate(self.final_norm(h), shift, scale))


class FlowModel(nn.Module):
    def __init__(self, config: So101FlowConfig):
        super().__init__()
        from transformers import Dinov2Model

        self.config = config
        self.cameras = list(config.image_features)
        if WRIST_CAMERA not in self.cameras:
            raise ValueError(f"Expected the wrist camera at {WRIST_CAMERA}; got {self.cameras}")
        self.vision = Dinov2Model.from_pretrained(config.vision_model)
        if config.vision_grad_checkpointing:
            # Non-reentrant: the reentrant variant silently gives no gradients to the checkpointed layers
            # when their input doesn't require grad.
            self.vision.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
        vision_dim = self.vision.config.hidden_size
        dim = config.dim_model
        n_tokens = config.pooled_tokens[0] * config.pooled_tokens[1]
        self.vis_proj = nn.Linear(vision_dim, dim)
        self.cam_embed = nn.Parameter(torch.randn(len(self.cameras), 1, dim) * 0.02)
        self.pos_embed = nn.Parameter(torch.randn(1, n_tokens, dim) * 0.02)
        self.mask_token = nn.Parameter(torch.randn(1, 1, dim) * 0.02)
        state_dim = config.robot_state_feature.shape[0]
        self.state_proj = nn.Linear(state_dim, dim)
        self.no_state_token = nn.Parameter(torch.randn(1, 1, dim) * 0.02)
        self.task_token = nn.Parameter(torch.randn(1, 1, dim) * 0.02)
        layer = nn.TransformerEncoderLayer(dim, config.n_heads, config.dim_feedforward, config.dropout,
                                           activation="gelu", batch_first=True, norm_first=True)
        self.trunk = nn.TransformerEncoder(layer, config.n_trunk_layers, norm=nn.LayerNorm(dim),
                                           enable_nested_tensor=False)
        self.expert = FlowExpert(config, config.action_feature.shape[0])
        self.register_buffer("img_mean", torch.tensor(IMAGENET_MEAN).view(1, 3, 1, 1), persistent=False)
        self.register_buffer("img_std", torch.tensor(IMAGENET_STD).view(1, 3, 1, 1), persistent=False)

    def view(self, img: Tensor, wrist: bool) -> Tensor:
        """(B, 3, H, W) in [0, 1] -> (B, 3, *image_size), with a random crop/shift/rotation when training.
        The crop keeps the camera's aspect ratio so the whole field of view survives at eval."""
        cfg = self.config
        b, _, h, w = img.shape
        oh, ow = cfg.image_size
        # Antialiased downsample first so the (near 1:1) resampling below doesn't alias.
        img = F.interpolate(img, size=(round(oh / cfg.scene_crop[0]), round(ow / cfg.scene_crop[0])),
                            mode="bilinear", antialias=True, align_corners=False)
        lo, hi = cfg.wrist_crop if wrist else cfg.scene_crop
        dev = img.device
        if self.training:
            s = torch.empty(b, device=dev).uniform_(lo, hi)
            rot = torch.empty(b, device=dev).uniform_(-1, 1) * math.radians(cfg.max_rotation_deg)
            shift = (torch.empty(b, 2, device=dev).uniform_(-1, 1) * cfg.max_shift_px * (0 if wrist else 1)
                     / torch.tensor([w / 2, h / 2], device=dev))
        else:
            s = torch.full((b,), (lo + hi) / 2, device=dev)
            rot = torch.zeros(b, device=dev)
            shift = torch.zeros(b, 2, device=dev)
        cos, sin = torch.cos(rot) * s, torch.sin(rot) * s
        aspect = h / w
        theta = torch.stack([torch.stack([cos, -sin * aspect, shift[:, 0]], -1),
                             torch.stack([sin / aspect, cos, shift[:, 1]], -1)], 1)
        grid = F.affine_grid(theta, (b, 3, oh, ow), align_corners=False)
        return F.grid_sample(img, grid, mode="bilinear", padding_mode="reflection", align_corners=False)

    def encode(self, batch: dict[str, Tensor], freeze_vision: bool) -> Tensor:
        cfg = self.config
        b = batch[OBS_STATE].shape[0]
        views = torch.cat([self.view(batch[k], k == WRIST_CAMERA) for k in self.cameras])
        views = (views - self.img_mean) / self.img_std
        with torch.set_grad_enabled(torch.is_grad_enabled() and not freeze_vision):
            patches = self.vision(pixel_values=views).last_hidden_state[:, 1:]  # drop CLS
        gh, gw = cfg.image_size[0] // 14, cfg.image_size[1] // 14
        patches = patches.reshape(-1, gh, gw, patches.shape[-1]).permute(0, 3, 1, 2)
        pooled = F.adaptive_avg_pool2d(patches, cfg.pooled_tokens).flatten(2).transpose(1, 2)
        tokens = (self.vis_proj(pooled) + self.pos_embed).view(len(self.cameras), b, -1, cfg.dim_model)
        seq = []
        for i, key in enumerate(self.cameras):
            t = tokens[i] + self.cam_embed[i]
            if self.training and key != WRIST_CAMERA:
                drop = torch.rand(t.shape[:2], device=t.device) < cfg.scene_token_dropout
                drop |= (torch.rand(b, 1, device=t.device) < cfg.scene_view_dropout)
                t = torch.where(drop[..., None], self.mask_token.to(t.dtype), t)
            seq.append(t)
        state = batch[OBS_STATE]
        if self.training:
            state = state + cfg.state_noise * torch.randn_like(state)
        state_tok = self.state_proj(state)[:, None]
        if self.training:
            gone = torch.rand(b, 1, 1, device=state.device) < cfg.state_dropout
            state_tok = torch.where(gone, self.no_state_token.to(state_tok.dtype), state_tok)
        seq += [state_tok, self.task_token.expand(b, -1, -1)]
        return self.trunk(torch.cat(seq, dim=1))

    def loss(self, batch: dict[str, Tensor], freeze_vision: bool) -> tuple[Tensor, dict]:
        cfg = self.config
        memory = self.encode(batch, freeze_vision)
        k = cfg.flow_samples_per_obs
        actions = batch[ACTION].repeat_interleave(k, 0)
        pad = batch.get("action_is_pad")
        pad = (torch.zeros(actions.shape[:2], dtype=torch.bool, device=actions.device) if pad is None
               else pad.repeat_interleave(k, 0))
        memory = memory.repeat_interleave(k, 0)
        n, horizon = actions.shape[:2]
        dev = actions.device
        noise = torch.randn_like(actions)
        # Flow time biased toward the noisy end (pi0 practice).
        tau = 0.999 * (1 - torch.distributions.Beta(1.5, 1.0).sample((n, 1)).to(dev))
        # Training-time RTC: a clean committed prefix of d steps, d weighted toward small values.
        weights = torch.exp(-torch.arange(1, cfg.rtc_max_delay + 1, dtype=torch.float32))
        d = torch.multinomial(weights, n, replacement=True).to(dev) + 1
        d = torch.where(torch.rand(n, device=dev) < cfg.rtc_no_prefix_prob, torch.zeros_like(d), d)
        prefix = torch.arange(horizon, device=dev)[None] < d[:, None]
        tau_tok = torch.where(prefix, torch.ones_like(tau).expand(-1, horizon), tau.expand(-1, horizon))
        x_t = tau_tok[..., None] * actions + (1 - tau_tok[..., None]) * noise
        v = self.expert(x_t, tau_tok, memory)
        per_step = ((v.float() - (actions - noise)) ** 2).mean(-1)
        weight = (~prefix & ~pad).float()
        loss = (per_step * weight).sum() / weight.sum().clamp_min(1)
        return loss, {"flow_mse": loss.item(), "mean_prefix": d.float().mean().item()}

    @torch.no_grad()
    def sample(self, batch: dict[str, Tensor], prefix: Tensor, prefix_mask: Tensor) -> Tensor:
        """Integrate the flow from noise to an action chunk. prefix (B, H, A) holds committed steps where
        prefix_mask (B, H) is true; those are pinned and marked clean (tau = 1) at every step. Shapes don't
        depend on the prefix length, so the whole call can be captured once as a CUDA graph."""
        cfg = self.config
        memory = self.encode(batch, freeze_vision=True)
        b = memory.shape[0]
        x = torch.randn(b, cfg.chunk_size, cfg.action_feature.shape[0], device=memory.device)
        pin = prefix_mask[..., None]
        clean = torch.ones_like(prefix_mask, dtype=torch.float32)
        steps = cfg.num_inference_steps
        for i in range(steps):
            x = torch.where(pin, prefix, x)
            tau = torch.where(prefix_mask, clean, torch.full_like(clean, i / steps))
            x = x + self.expert(x, tau, memory).float() / steps
        return torch.where(pin, prefix, x)


class GraphSampler:
    """Replays FlowModel.sample as one CUDA graph. On the Jetson the eager call is bound by the CPU issuing
    ~thousands of small kernels (210 ms CPU time for 210 ms total); a graph replay issues them in one launch."""

    def __init__(self, model: FlowModel):
        self.model = model
        self.graph = None
        self.key = None

    def __call__(self, batch: dict[str, Tensor], prefix: Tensor, prefix_mask: Tensor) -> Tensor:
        inputs = {k: v for k, v in batch.items() if isinstance(v, Tensor)}
        key = tuple((k, tuple(v.shape), v.dtype) for k, v in sorted(inputs.items()))
        if key != self.key:
            self._capture(inputs, prefix, prefix_mask)
            self.key = key
        for k, v in inputs.items():
            self.static[k].copy_(v)
        self.static_prefix.copy_(prefix)
        self.static_mask.copy_(prefix_mask)
        self.graph.replay()
        return self.out.clone()

    def _capture(self, inputs, prefix, prefix_mask):
        self.static = {k: v.clone() for k, v in inputs.items()}
        self.static_prefix = prefix.clone()
        self.static_mask = prefix_mask.clone()
        stream = torch.cuda.Stream()
        stream.wait_stream(torch.cuda.current_stream())
        with torch.cuda.stream(stream):  # warm-up outside the graph (allocator, lazy init)
            for _ in range(3):
                self.model.sample(self.static, self.static_prefix, self.static_mask)
        torch.cuda.current_stream().wait_stream(stream)
        self.graph = torch.cuda.CUDAGraph()
        with torch.cuda.graph(self.graph):
            self.out = self.model.sample(self.static, self.static_prefix, self.static_mask)


class So101FlowPolicy(PreTrainedPolicy):
    config_class = So101FlowConfig
    name = "so101flow"
    native_rtc = True  # eval_real.py passes prev_chunk_left_over / inference_delay straight through

    def __init__(self, config: So101FlowConfig, **kwargs):
        super().__init__(config)
        config.validate_features()
        self.config = config
        self.model = FlowModel(config)
        self.ema = copy.deepcopy(self.model)
        self.ema.requires_grad_(False)
        self.register_buffer("train_steps", torch.zeros((), dtype=torch.long))
        self._graph = None
        self.reset()

    def enable_cuda_graph(self):
        """Run inference through a captured CUDA graph (big win where the CPU is slow, e.g. the Jetson)."""
        self._graph = GraphSampler(self._inference_model())

    def reset(self):
        self._queue = deque(maxlen=self.config.n_action_steps)

    def get_optim_params(self) -> list[dict]:
        vision, decay, no_decay = [], [], []
        for name, p in self.model.named_parameters():
            if not p.requires_grad:
                continue
            if name.startswith("vision."):
                vision.append(p)
            elif p.ndim < 2 or "norm" in name or name.endswith(("embed", "token", "pos")):
                no_decay.append(p)
            else:
                decay.append(p)
        cfg = self.config
        return [
            {"params": decay},
            {"params": no_decay, "weight_decay": 0.0},
            {"params": vision, "lr": cfg.optimizer_lr_vision},
        ]

    def _autocast(self):
        return torch.autocast("cuda", dtype=torch.bfloat16, enabled=self.config.device == "cuda")

    def forward(self, batch: dict[str, Tensor], reduction: str = "mean") -> tuple[Tensor, dict]:
        freeze = int(self.train_steps) < self.config.freeze_vision_steps
        with self._autocast():
            loss, info = self.model.loss(batch, freeze_vision=freeze)
        return loss, info

    @torch.no_grad()
    def update(self):
        """Called by lerobot-train after every optimizer step: EMA of the weights (warm-started)."""
        self.train_steps += 1
        step = int(self.train_steps)
        decay = min(self.config.ema_decay, (1 + step) / (10 + step))
        ema_params = list(self.ema.parameters())
        params = list(self.model.parameters())
        torch._foreach_lerp_(ema_params, params, 1 - decay)
        for be, b in zip(self.ema.buffers(), self.model.buffers()):
            be.copy_(b)

    def _inference_model(self) -> FlowModel:
        use_ema = self.config.use_ema_for_inference and int(self.train_steps) > 0
        return self.ema if use_ema else self.model

    @torch.no_grad()
    def predict_action_chunk(self, batch: dict[str, Tensor], prev_chunk_left_over: Tensor | None = None,
                             inference_delay: int | None = None, **kwargs) -> Tensor:
        """(B, chunk_size, action_dim) normalized actions. With prev_chunk_left_over (normalized, starting at
        this observation's time) and inference_delay d, the first d steps are pinned to it."""
        model = self._inference_model()
        model.eval()
        cfg = self.config
        state = batch[OBS_STATE]
        b = state.shape[0]
        prefix = torch.zeros(b, cfg.chunk_size, cfg.action_feature.shape[0], device=state.device)
        mask = torch.zeros(b, cfg.chunk_size, dtype=torch.bool, device=state.device)
        if prev_chunk_left_over is not None and inference_delay:
            left = prev_chunk_left_over if prev_chunk_left_over.ndim == 3 else prev_chunk_left_over[None]
            d = min(int(inference_delay), left.shape[1], cfg.chunk_size)
            if d > 0:
                prefix[:, :d] = left[:, :d].to(state.device, torch.float32)
                mask[:, :d] = True
        # Inference runs in fp32: autocast only added CPU overhead (Jetson 210 -> 296 ms) for no speed gain.
        if self._graph is not None and state.is_cuda:
            try:
                return self._graph(batch, prefix, mask)
            except (RuntimeError, torch.AcceleratorError) as exc:  # e.g. capture OOM on a GPU busy training
                print(f"so101flow: CUDA graph unavailable ({str(exc).splitlines()[0]}); running eagerly", flush=True)
                self._graph = None
                torch.cuda.empty_cache()
        return model.sample(batch, prefix, mask)

    @torch.no_grad()
    def select_action(self, batch: dict[str, Tensor], **kwargs) -> Tensor:
        if len(self._queue) == 0:
            chunk = self.predict_action_chunk(batch)[:, : self.config.n_action_steps]
            self._queue.extend(chunk.transpose(0, 1))
        return self._queue.popleft()
