# Wren

**A small, fast visuomotor policy for low-cost robot arms.** Wren looks through a scene camera and a wrist camera,
reads the joint angles, and outputs the next 1.6 s of motion for a 6-DoF SO-101 arm. The model has 61M trainable
parameters. It trains on one 8 GB laptop GPU in about 6 hours, and runs at about 110 ms per query on a Jetson Orin Nano.

Like a wren (a tiny, quick bird), it aims to be small enough for cheap hardware and fast enough to react.

> In code the policy type is still `so101flow` (package `so101_policy/`), because existing checkpoints are saved
> under that name. "Wren" is the project and model name.

This repo holds everything around it:
- the policy
- training scripts
- the real-time runner
- the Jetson inference server
- the recording/teleop app ("Episode Studio")
- the literature review behind the design
- experiment records

---

## 1. Architecture

```
 scene cam (640×480) ─┐                               ┌─ 80 scene tokens ─┐
                      ├─► DINOv2 ViT-S/14 (shared) ───┤                   │
 wrist cam (640×480) ─┘   pretrained, fine-tuned      └─ 80 wrist tokens ─┤
 6 joint angles ──────────► linear ──────────────────────  1 state token ─┼─► 6-layer transformer ─► memory (162 tokens)
                                                            1 task token ──┘        trunk                    │
                                                                                                             ▼
 noise (16 steps × 6 joints) ─► flow-matching DiT action expert (6 blocks, adaLN-zero, cross-attn) × 8 steps ─► 1.6 s of joint targets
                                  ▲ first d steps can be pinned to the plan already being executed (real-time chunking)
```

| Part | What it is | Params |
|---|---|---|
| Input | Both cameras resized and cropped to 210×280 (keeps 4:3, so the whole field of view survives), ImageNet-normalised. Joint state quantile-scaled to [-1, 1] (1st/99th percentile of our data). | – |
| Vision | **DINOv2 ViT-S/14**, pretrained by Meta and **shared by both cameras**. Frozen for the first 1k steps, then fine-tuned at 10× lower LR (1e-5). 15×20 patch tokens, average-pooled to **8×10 = 80 tokens per camera** (never pooled to one vector, so *where* things are is kept), plus a learned position embedding and a per-camera embedding. | 22.1M |
| Trunk | Transformer encoder: 6 layers, width 512, 8 heads, pre-LN, over 162 tokens = 80 scene + 80 wrist + 1 joint-state + 1 task. | 18.9M |
| Action expert | Flow-matching **DiT**: 6 blocks, width 384, 6 heads. 16 action tokens; each block has self-attention across the steps, cross-attention to the trunk memory, and an MLP. Flow time is injected per token via **adaLN-zero**, so each block starts as the identity. Output: velocity for 16 × 6 joint targets. | 19.4M |
| Sampling | Start from Gaussian noise; 8 Euler steps from τ=0 to τ=1. Committed prefix steps are pinned (τ=1) at every step. | – |

**Output:** a chunk of **16 absolute joint targets at 10 fps = 1.6 s**. The runner executes about 0.6 s of each chunk, then
switches to the next.

### What makes it different
- **Trained-in real-time chunking (training-time RTC).** During training, a random prefix of 0–4 steps is given
  *clean* (flow time 1) and excluded from the loss, so the model learns to *continue* a plan already under way. On the
  robot, each new chunk is pinned to what the arm will be doing when it lands. Consecutive chunks therefore join
  smoothly without blending: median switch jump 0.2° on the real arm, versus several degrees for ACT.
- **Robust to the scene camera, never blind at the gripper.** 30% of scene tokens are masked and occasionally the whole
  scene view; the wrist camera is never dropped. Joint angles get about 1° of noise and are hidden 30% of the time, so
  the model can't just copy them.
- **Hue-preserving augmentation.** Brightness, contrast, saturation and sharpness jitter, random crop, ±10 px shift and
  ±5° rotation, but no hue change (the pumpkin's colour is signal).
- **Edge-ready inference.** Sampling is shape-static, so the whole prediction is captured as **one CUDA graph**. On the
  Jetson this cut model time from 288 ms to 83 ms, because eager PyTorch there is limited by the slow ARM CPU issuing
  kernels, not by the GPU.

### Training recipe
- Conditional flow matching (linear path, v = action − noise), τ biased toward the noisy end (π0 practice).
  Four noise/time draws per image, sharing one encoder pass.
- AdamW (β 0.9/0.95, wd 1e-4, none on norms, biases or embeddings). LR 1e-4 with cosine decay to 1e-6 and
  1k warm-up; vision at 1e-5. Grad clip 1.0.
- **EMA** of the weights (0.999) is what runs on the robot.
- Batch 16, 60k steps, bf16 autocast in training (fp32 at inference).
- About 6 h on an RTX 5060 laptop (8 GB) while sharing the GPU with an ACT run.

### Why these choices
Every choice comes from a literature review: 7,162 abstracts screened, about 480 papers read in full. See
[`research/FINAL_REPORT.md`](research/FINAL_REPORT.md) (section 3 is the architecture, 4 the training recipe,
6 the real-time stack). In short:
- pretrained DINO patch tokens beat CLIP/SigLIP and robot-specific encoders for control;
- flow matching keeps multimodal actions that L1 regression averages away;
- ~50M parameters is the evidence-backed size for ~100 demos;
- chunk continuity should be trained in, not blended at inference.

### Prior art (honest novelty statement)
Every component has close prior work, and a September 2026 search found **no published model with this exact
combination**. Closest:
- **CT-VAM** (68M, DINOv3-S+ with two views and a flow decoder; smooth switching only at inference)
- **ABC-DiT** (the same recipe family, fine-tuned DINO + cross-attention DiT + RTC, but ~2B parameters on an
  $8k bimanual robot)
- **FlowDPG** (frozen DINOv2-B + DiT flow head)
- **MINERVA** (tiny from-scratch flow policy, simulation only)
- **Training-time RTC** (Black et al., shown on large VLA-style policies)

Wren's contribution is empirical: this large-scale recipe, scaled down about 30× to a $200 arm and a Jetson,
measured on real hardware.

---

## 2. Results so far (task: pick up a pumpkin, place it in a tray)

Data: 100 teleoperated episodes (19,832 frames at 10 fps) over two camera positions and several lighting setups.
Episodes 76 and 92 were excluded because the arm never moved. Details: [`experiments/episode_conditions.json`](experiments/episode_conditions.json).

**Offline** (recorded frames that were also in training, so optimistic; Jetson Orin Nano inference):

| checkpoint | error vs demo (mean over 1.6 s) | chunk-switch disagreement, plain → with RTC | round trip |
|---|---|---|---|
| Wren 5k | 5.1° | 13.0° → 2.6° | 321 ms (before CUDA graphs) |
| Wren 20k | 1.7° | 5.0° → 1.2° | 314 ms (before CUDA graphs) |
| Wren 60k | 1.0° | 1.7° → **0.7°** | **108 ms** |
| ACT 80k (baseline) | 1.4° | 1.7° (no RTC) | 92 ms |

**Real arm, 2026-09-27** ([`experiments/trials_2026-09-27.md`](experiments/trials_2026-09-27.md); scored from saved
frames; small n, not interleaved):

| policy | success | switch-jump p90 |
|---|---|---|
| **Wren 60k** | **7/10** | 0.7–4.2° |
| ACT 80k | 5/9 | 1.6–1.8° |
| SmolVLA (450M, fine-tuned) | completed the task in earlier informal runs; ~350 ms/query and needed RTC plus smoothing to stop jitter | – |

The difference isn't statistically significant yet. Both policies share the same failure: hovering at the grasp
without committing. The next step is an interleaved 10-spot trial round, then targeted demos at the failing spots.

---

## 3. Repo layout

| path | what |
|---|---|
| `so101_policy/` | **The model.** LeRobot plugin package (`configuration_so101flow.py`, `modeling_so101flow.py`, `processor_so101flow.py`). |
| `policy_runtime.py` | Loads any LeRobot chunking policy and turns one observation into one chunk; shared by the laptop runner and the Jetson server. `RemotePolicy` is the client for the Jetson. |
| `eval_real.py` | Real-time runner: async inference, timestamped chunks, RTC, 50 Hz servo executor, smoothing, per-query logs and frames in `policy_runs/`, `--remote` for the Jetson, `--no-arm` simulated follower. |
| `jetson/` | Jetson side: `policy_server.py` (ZMQ inference server) and its systemd unit; the scene-camera streaming script and unit; the (disabled) depth publisher and calibration dump. |
| `training/` | `train_wren.sh`, `train_act_baseline.sh`, `prune_checkpoints.py`. |
| `server.py`, `index.html`, `teleop_runner.py` | **Episode Studio**: web UI for 100 Hz teleoperation, LeRobot recording (NVENC, GOP 2) and live policy tests. |
| `deploy/` | systemd user unit for the Studio server. |
| `tools/bench_policy_latency.py` | Offline per-stage latency benchmark for any checkpoint. |
| `experiments/` | Episode conditions, trial records, overnight training log. |
| `research/` | Final report, executive summary, real-time tracks, and all evidence notes and ledgers. |

Weights and datasets are not in the repo (checkpoints are 0.2–0.5 GB each). They live in the training workspace
(`$SO101_WORKSPACE/outputs/train/…`, `$SO101_WORKSPACE/data/lerobot/so101_pumpkin_v1`).

## 4. Usage

```bash
# Train (LeRobot 0.4.4 venv; the plugin is found through a .pth file pointing at this repo)
bash training/train_wren.sh wren_run 60000 16 so101_pumpkin_v1 --dataset.episodes='[...]'

# Episode Studio (recording, teleop, policy tests; tick "Run on Jetson" to infer on the Jetson)
systemctl --user start so101-server        # http://127.0.0.1:8765

# Runner from a terminal
python eval_real.py --checkpoint <run>/checkpoints/060000/pretrained_model --remote 10.42.0.81:5557 --dry-run
python eval_real.py --checkpoint <...> --no-arm      # full pipeline against a simulated follower
```

Hardware:
- SO-101 leader and follower (Feetech STS3215)
- RealSense D435i as the scene camera, streamed from a Jetson Orin Nano (25 W mode, clocks pinned)
- USB wrist camera
- RTX 5060 laptop (8 GB)
