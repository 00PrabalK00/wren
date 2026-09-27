"""Config for "SO-101 flow policy v1" (research/FINAL_REPORT.md section 3).

DINOv2 ViT-S shared over the scene and wrist cameras -> transformer trunk over [scene tokens, wrist tokens,
state token, task token] -> flow-matching DiT action expert predicting a chunk of absolute joint targets,
trained with per-token flow time so the next chunk can be conditioned on the committed prefix of the
current one (training-time RTC).
"""

from dataclasses import dataclass, field

from lerobot.configs.policies import PreTrainedConfig
from lerobot.configs.types import NormalizationMode
from lerobot.optim.optimizers import AdamWConfig
from lerobot.optim.schedulers import CosineDecayWithWarmupSchedulerConfig


@PreTrainedConfig.register_subclass("so101flow")
@dataclass
class So101FlowConfig(PreTrainedConfig):
    # Chunking: 16 steps = 1.6 s at 10 fps (3.5); eval_real.py decides how much of each chunk runs.
    n_obs_steps: int = 1
    chunk_size: int = 16
    n_action_steps: int = 6

    normalization_mapping: dict[str, NormalizationMode] = field(
        default_factory=lambda: {
            "VISUAL": NormalizationMode.IDENTITY,  # ImageNet mean/std is applied inside the model
            "STATE": NormalizationMode.QUANTILES,
            "ACTION": NormalizationMode.QUANTILES,
        }
    )

    # Vision (3.1, 3.2): 4:3 input so the whole field of view is kept; 15x20 patches pooled to 8x10 tokens.
    vision_model: str = "facebook/dinov2-small"
    image_size: tuple[int, int] = (210, 280)
    pooled_tokens: tuple[int, int] = (8, 10)
    freeze_vision_steps: int = 1000  # fresh-head gradients stay out of the pretrained encoder at first
    vision_grad_checkpointing: bool = True
    scene_crop: tuple[float, float] = (0.90, 0.95)  # random crop fraction per frame (train); mean at eval
    wrist_crop: tuple[float, float] = (0.95, 0.95)
    max_shift_px: float = 10.0  # scene only
    max_rotation_deg: float = 5.0
    scene_token_dropout: float = 0.3
    scene_view_dropout: float = 0.1  # the wrist view is never dropped

    # Proprio (3.3, Q07): one token, noise ~1 deg in normalized units and dropout.
    state_noise: float = 0.02
    state_dropout: float = 0.3

    # Trunk (3.3)
    dim_model: int = 512
    n_heads: int = 8
    dim_feedforward: int = 2048
    n_trunk_layers: int = 6
    dropout: float = 0.1

    # Flow expert (3.4)
    expert_dim: int = 384
    expert_heads: int = 6
    n_expert_layers: int = 6
    expert_mlp_ratio: int = 2
    flow_samples_per_obs: int = 4  # noise/time draws per encoder pass in the loss
    num_inference_steps: int = 8
    rtc_max_delay: int = 4  # training-time RTC: prefix of up to this many clean steps
    rtc_no_prefix_prob: float = 0.3

    # Optimisation (4.3)
    optimizer_lr: float = 1e-4
    optimizer_lr_vision: float = 1e-5
    optimizer_betas: tuple[float, float] = (0.9, 0.95)
    optimizer_weight_decay: float = 1e-4
    optimizer_grad_clip_norm: float = 1.0
    scheduler_warmup_steps: int = 1000
    scheduler_decay_steps: int = 80000
    scheduler_decay_lr: float = 1e-6
    ema_decay: float = 0.999
    use_ema_for_inference: bool = True

    def __post_init__(self):
        super().__post_init__()
        if self.n_action_steps > self.chunk_size:
            raise ValueError("n_action_steps cannot exceed chunk_size")
        if self.n_obs_steps != 1:
            raise ValueError("so101flow uses a single observation step (no history)")

    def get_optimizer_preset(self) -> AdamWConfig:
        return AdamWConfig(lr=self.optimizer_lr, betas=self.optimizer_betas,
                           weight_decay=self.optimizer_weight_decay, grad_clip_norm=self.optimizer_grad_clip_norm)

    def get_scheduler_preset(self) -> CosineDecayWithWarmupSchedulerConfig:
        return CosineDecayWithWarmupSchedulerConfig(
            peak_lr=self.optimizer_lr, decay_lr=self.scheduler_decay_lr,
            num_warmup_steps=self.scheduler_warmup_steps, num_decay_steps=self.scheduler_decay_steps)

    def validate_features(self) -> None:
        if len(self.image_features) == 0:
            raise ValueError("so101flow needs at least one camera")
        if self.robot_state_feature is None:
            raise ValueError("so101flow needs observation.state")

    @property
    def observation_delta_indices(self) -> None:
        return None

    @property
    def action_delta_indices(self) -> list:
        return list(range(self.chunk_size))

    @property
    def reward_delta_indices(self) -> None:
        return None
