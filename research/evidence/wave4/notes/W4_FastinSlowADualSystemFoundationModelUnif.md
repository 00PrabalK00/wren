# W4_FastinSlowADualSystemFoundationModelUnif — Fast-in-Slow: A Dual-System Foundation Model Unifying Fast Manipulation within Slow Reasoning (2025, arXiv 2506.01953)
Setup: FiS-VLA: Prismatic 7B (LLaMA2) with SigLIP+DINOv2, pretrained on 860k OXE-style trajectories; System 1 = last 2 LLM blocks re-used as a diffusion action head, fed latest image + robot state + point cloud (1024 pts, via 3D tokenizer into the shared vision encoder), conditioned on System 2 intermediate features refreshed every n steps (1:4). Sim: 10 RLBench tasks, 100 scripted demos each (keyframes), 3x20 rollouts; trained 300 epochs on 8xA800. Real: Agilex (2x6-DoF, EEF control) and AlphaBot (2x7-DoF, joint control), 3 cams (exterior RealSense D435 + 2 wrist), 30 Hz, 100 teleop demos/task with randomized object positions, 4 tasks per robot, 20 rollouts each; baseline pi0.
Claim: Embedding a fast action module inside the VLM (partial parameter sharing) with asynchronous slow/fast rates gives higher success and 21.9 Hz control.
Evidence:
 - RLBench avg: ManipLLM 0.38, OpenVLA 0.40, pi0 0.55, CogACT 0.61, FiS 0.69 (+-0.03); speed 2.2 / 6.3 / 13.8 / 9.8 / 21.9 Hz (chunk=1, single GPU, sequential not parallel systems).
 - Real (Table 2, 20 trials, pi0 vs FiS): Agilex pick&place 0.70/0.80, lift ball 0.75/0.75, bottles at rack 0.55/0.70, wipe 0.35/0.45, mean 0.59/0.68; AlphaBot bowl 0.65/0.80, handover 0.75/0.80, pour 0.65/0.75, fold towel 0.40/0.60, mean 0.61/0.74.
 - Generalization (Table 3; orig / unseen object / cluttered background / lighting): Agilex bottles FiS 0.70/0.55/0.50/0.50 vs pi0 0.55/0.40/0.35/0.40; AlphaBot bowl FiS 0.80/0.65/0.60/0.55 vs pi0 0.65/0.40/0.40/0.35. Both models lose 19-46% relative under each shift.
Ablations (RLBench, 10 tasks x 60 rollouts):
 - System 1 inputs (Table 7): full 0.69; no point cloud 0.61; no PC + no image (only S2 latent + state) 0.44; latent only 0.22.
 - Shared blocks for System 1: 1 block 0.49, 2 blocks 0.69, 4 blocks 0.66, 8 blocks 0.64.
 - Slow:fast ratio: 1:1 0.60, 1:2 0.63, 1:4 0.69, 1:8 0.61.
 - Action chunk size H (Table 9): 1: 0.69, 2: 0.68, 4: 0.66, 8: 0.69 — flat, while theoretical control rate rises to 117.7 Hz at H=8.
 - Drop System-2 co-training loss: 0.69 -> 0.62.
 - Input variants (Table 10): moving PC to System 2 only 0.63; state in S2 0.61; images+PC in both 0.68.
Failure/limitations: authors: static sharing/frequency configuration. Failures: bimanual collision, wrong grasp height on thin towel, mislocalized banana, bad handover rotation. Critical read: 7B model, 8xA800 training — irrelevant compute regime for us; RLBench uses keyframe (waypoint) actions, so "chunk size" ablation there is not about dense teleop trajectories; real generalization only 20 trials per cell, no statistics; "Hz" numbers are model throughput, not closed-loop latency on robot.
Conflicts: Chunk-size-insensitivity contrasts with ACT/DP where chunking matters a lot for dense human teleop data — difference is RLBench keyframe actions. Point cloud helps (+8 pts) in line with DP3/iDP3 3D findings, but only as an extra input to a big VLA. Lighting still costs FiS ~29-31% relative despite point cloud input — point cloud does not immunize against lighting when RGB is also used.
Relevance: Low for architecture (too big for 8 GB). Useful data points: (1) adding a single-view depth point cloud from a RealSense D435 exterior camera to the action module helps in sim; (2) even strong pretrained VLAs with 100 randomized demos lose ~20-45% under new object/background/lighting — matches our SmolVLA failures, so pretraining scale alone does not buy robustness at 100 demos.
Decision impact:
 - Q04 3D input: supports adding point cloud to action module (0.61 -> 0.69 sim RLBench) — L (sim, keyframe actions, big VLA)
 - Q10 latency: dual-rate (slow semantic features refreshed every 4 action steps) keeps success (1:4 best 0.69 vs 1:1 0.60) while raising rate — L (sim)
 - Q06 chunking: chunk size 1-8 flat (0.66-0.69) on keyframe RLBench — L (not transferable to dense teleop)
 - Q14 robustness: 7B VLA with 100 demos still drops 19-46% relative on unseen object/background/lighting (20 trials) — L/M
 - Q12 model size: 7B not feasible on 8 GB; no small-model evidence — L
