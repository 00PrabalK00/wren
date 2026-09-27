# FastInSlow — Fast-in-Slow (FiS-VLA): A Dual-System Foundation Model Unifying Fast Manipulation within Slow Reasoning (2025, arXiv 2506.01953)
Setup: 7B VLM-based VLA; System 1 = the LAST transformer blocks of the System-2 LLM re-used (partial parameter sharing) as a diffusion action head, taking extra fast inputs (robot state, 2D image, 3D point cloud) while System 2 provides latent features from low-frequency calls. Pretrained on >860K trajectories (OXE mix + RoboMIND etc.), then fine-tuned. Sim: RLBench 10 tasks, 20 rollouts ×3. Real: Agilex (14-DoF EE pose) and AlphaBot (16-DoF joint position) dual-arm robots, 4 tasks each, 100 master-puppet demos per task, 3 cams @30 Hz (RealSense 435 overhead + wrist), 20 rollouts per task. Inference timed on one RTX 4090; both systems on the SAME GPU (no parallel deployment).
Claim: embedding System 1 inside the VLM (instead of a separate small model) lets it use pretrained knowledge while running at high rate.
Evidence:
 - RLBench mean SR / speed (Table 1, chunk=1): FiS 0.69 @21.9 Hz; CogACT 0.61 @9.8 Hz; pi0 0.55 @13.8 Hz; other baselines 0.38 @2.2 Hz, 0.40 @6.3 Hz. With chunk 8 "theoretical" 117.7 Hz; SR "stable across H".
 - Real: Agilex mean 68% vs pi0 59% (Place bottles at rack 70 vs 55); AlphaBot 74% vs pi0 61%.
 - Generalization (Table 3): unseen object / background / lighting cause drops of 25–46% relative for both FiS and pi0 (e.g., lighting: FiS 0.50 (−29%) on Place Bottles; pi0 0.35 (−46%) on AlphaBot task).
Ablations (RLBench):
 - System2:System1 frequency ratio 1:1 / 1:2 / 1:4 / 1:8 → 0.60 / 0.63 / 0.69 / 0.61 (Table 8). Too-stale System-2 latents (1:8) hurt.
 - Number of shared blocks for System 1: gains saturate at 2 blocks.
 - Inputs to System 1: latent only < +state < +2D < +3D point cloud (each adds, figure-only).
Failure/limitations: 7B model, large pretraining; no measured closed-loop reaction to disturbances; failure cases (bimanual collisions, handover rotation errors); authors: System 2 cannot yet recognize/correct failures. Critical read: "117.7 Hz" is chunk-8 throughput, not per-observation reaction frequency; ratio experiment is serial on one GPU.
Conflicts: RoboDual/GR00T keep System 1 as a separate small net; FiS argues sharing is better — but only vs pi0/CogACT at 7B scale. Agrees with RoboDual that the fast part must see fresh raw observations (state + image) not only slow latents.
Relevance to SO-101: low for direct use (7B, won't fit 8 GB at speed). Portable lessons: (1) fast path must take fresh proprio + camera; (2) slow-context staleness of ~4 fast steps was fine, 8 hurt; (3) depth/point cloud into the fast path helped (we have RealSense depth).
Decision impact:
 - Dual system with 7B slow model: INFEASIBLE on 8 GB — H.
 - If any slow context is used, refresh every ≤4 fast steps — L/M (sim ablation only).
