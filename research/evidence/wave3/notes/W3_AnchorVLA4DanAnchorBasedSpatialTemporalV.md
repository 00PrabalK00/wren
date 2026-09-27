# W3_AnchorVLA4DanAnchorBasedSpatialTemporalV — AnchorVLA4D: an Anchor-Based Spatial-Temporal VLA (2025/26, arXiv n/a in text)
Setup: Qwen2.5-VL-3B + 400M ScaleDP diffusion head (4.4B total with Any4D spatial encoder), no robot-data pretraining except BridgeV2; inputs: current frame + first frame of the episode ("anchor") + proprio; predicts 5 actions, executes 1 in sim. Sim: SimplerEnv WidowX, 4 tasks × 24 trials. Real: xLerobot (low-cost dual-arm mobile robot built from SO-100/101-class Feetech arms), 3 tasks (bimanual box lift, open drawer, pour cup), 30 episodes per task, 3 cams 640×480 resized to 320×240 (+anchor view = 4 images), 10 trials per task, RTX 4090, ~300 ms/inference, 50-step chunk, executes 5 → ~17 Hz effective. Training on 8× Ascend 910B.
Claim: conditioning on the episode's first frame + a frozen pretrained 4D spatial encoder gives cheap spatio-temporal context; beats π0.5 on real xLerobot.
Evidence:
 - SimplerEnv avg (Table I): VanillaVLA 51.0 (10 denoise steps), AnchorVLA4D 64.6 (79.2 for starred ⋆ variant listed in table row — table order ambiguous, 64.6 is the text-reported number); MemoryVLA 7B 75.0 (per text SOTA). Latency 0.215 s vs 0.185 s vanilla (+16%).
 - Real: AnchorVLA4D 80% avg over 3 tasks vs π0.5 fine-tuned 50% (per-task figure only; 10 trials each). π0.5 performed better with executing all 50 actions than 5.
Ablations:
 - Table II: Vanilla 51.0 → +anchor 60.4 → +frozen spatial encoder 64.6; unfreezing SE 59.4; SE output removed after training 58.3.
 - Table III history format (4k-step continuation): anchor I0 55.2; past 3 frames (stride 1) 46.9; past 3 frames stride 20 21.9. SE injection: cross-attn before decoder 0%, cross-attn in action head 46.9, concatenation 64.6.
 - Table V proprio: sim w/o 40.6 vs w/ 51.0; REAL open drawer (5k steps, 10 trials) w/o 60% vs w/ 50% — authors: proprio lets the model memorize trajectories and hurts visual grounding with narrow real data.
 - Retries (Table IV): anchor reduces overall retries 1.54 → 1.40.
Failure/limitations: anchor biases the policy toward initial state; fails when gripper must move far from start or in long tasks (stale anchor). Critical: 10 real trials; π0.5 baseline tuned differently (chunk 50 vs 5); Table I ordering garbled so some sim numbers uncertain; proprio ablation is 1 task × 10 trials (60 vs 50 = 1 trial difference).
Conflicts: History result (more past frames hurts: 55→47→22) matches copycat/causal-confusion literature and DP's short obs horizon; proprio-hurts-in-real echoes reports (e.g., Octo/"shortcut" analyses, some SO-100 community findings) but conflicts with ACT/DP practice of always feeding joint state — difference is data narrowness (30 demos) and large VLA backbone.
Relevance: HIGH hardware match (xLerobot uses SO-101-type servos, 30 demos/task, 640×480 cams). Suggests: (1) don't stack past frames; (2) consider dropping or noising proprio when demos are few; (3) freezing pretrained geometric encoders beats fine-tuning them with low data; (4) 300 ms inference with 5-step execution gives 17 Hz on 4090 — our 8 GB laptop needs far smaller model.
Decision impact:
 - Q07 history: past 3 frames 46.9 / strided 21.9 vs first-frame anchor 55.2 (sim); proprio removal real drawer 50→60% — weakens frame stacking and (weakly) proprio input in low data — confidence L/M (sim N=96, real N=10)
 - Q03 vision/spatial encoder: frozen pretrained spatial encoder 64.6 vs unfrozen 59.4 — supports freezing pretrained encoders in low-data fine-tune — confidence L
 - Q04 3D: RGB-only 4D (Any4D) encoder adds +4.2 pts without depth sensors — ~ implicit 3D features from RGB — confidence L
 - Q06 chunking: π0.5 better executing full 50-step chunk than 5 on real xLerobot — ~ longer execution for slow VLAs — confidence L (stated, no numbers)
