# W3_SpatialVAMSpatialAwareMultiViewVideoDiff — SpatialVAM: Spatial-Aware Multi-View Video Diffusion as a Data-Efficient Robot Policy (2026, arXiv 2604.03181)
Setup: Wan2.2 5B video diffusion model (LoRA) + 170M rotation/gripper head. Input: fused colored point cloud (cropped 1 m^3) rendered orthographically to 3 virtual views at 256x256 + EE pose rendered as Gaussian heatmaps; predicts future multi-view RGB + heatmap video (24 frames); EE position by back-projecting heatmap peaks, rotation (72-bin Euler) + gripper by classification. SE(3) point-cloud augmentation. Sim: Meta-World 7 tasks x 5 demos (25 trials/task), RoboCasa 10 tasks x 10 demos (50 rollouts). Real: Franka FR3, 3 calibrated ZED2i RGB-D, SpaceMouse teleop, ~10 demos/task, 3 base + 4 OOD variants, 10 trials each. Training 32 H20/H200 GPUs (~11 h real); inference >30 GB GPU memory, ~4.6 s per 24-frame chunk on A100 (5 denoise steps ~5 Hz claimed for Meta-World setting).
Claim: projecting 3D into multi-view images + heatmap actions aligns a video foundation model with action finetuning, giving strong data efficiency (10 demos) and OOD generalization.
Evidence:
 - Meta-World (5 demos/task): BC-Scratch 26.2, BC-R3M 35.4, DP 37.7, AVDC 58.9, DreamZero 61.1, Track2Act 67.4, SpatialVAM 89.1.
 - RoboCasa (10 demos): 3D Diffuser Actor 7.6, Cosmos Policy 20 (figure), SpatialVAM 35.8.
 - Real (10 demos, 10 trials/task; Put Lion, Push-T, Scoop, Put-B background cloth, Put-H height, Push-L lights off, Scoop-C new category): DP3 0.0 avg (0/10 everywhere), pi0.5 1.4 (1/10 Put Lion only), UVA 5.7, BridgeVLA 41.4 (9,0,4,8,7,0,1), SpatialVAM 57.1 (10,4,7,5,6,3,5).
Ablations (Meta-World unless noted):
 - Full finetune vs LoRA: 87.4 vs 89.1 (no gain).
 - Channel-concat heatmap+RGB instead of view-concat: 81.1.
 - Regress translation from latents (transformer) instead of heatmap back-projection: 76.6.
 - No pretrained video weights: 4.6 (cannot fit training set).
 - Additional predicted RGB views 0 -> 3: 61.1 -> 89.1 monotonic (joint RGB future prediction = large aux gain vs heatmap only).
 - Denoising steps N=1..50: 85.7–91.4, flat (1 step ~ as good).
 - Real: 1 physical camera instead of 3: 57.1 -> 50.0 with original virtual views, 60.0 with adapted virtual views.
 - Real calibration perturbation (20 mm / 2 deg): train-clean/test-perturbed 51.4; consistent perturbation 54.3 (vs 57.1).
 - Loss weight lambda +-80% -> ~3 pt change; heatmap sigma +-133% -> 2.5 pt.
Failure/limitations: authors: needs >=1 calibrated fixed RGB-D camera, 4.6 s/chunk on A100, >30 GB. Critical: 10 trials per real condition (one-trial = 10 pt); baselines at 10 demos are unfairly starved (DP3 training loss 1e-8 = extreme overfit, pi0.5 at 1.4% at 10 demos suggests poor fine-tune setup); OOD conditions are single variants; EE-space absolute positions from heatmaps.
Conflicts: pi0.5 near-zero at 10 demos contradicts reports of VLA data-efficiency at ~50 demos — regime difference (10 demos, multi-task). DP3 overfitting agrees with iDP3/other notes that simple MLP point encoders overfit with few demos. The "3D via multi-view virtual rendering" approach (RVT/BridgeVLA line) is robust to one-camera coverage and calibration noise, which differs from raw point-cloud policies.
Relevance: architecture itself is infeasible for us (5B, >30 GB, 4.6 s latency — worse than our SmolVLA 2 s). Transferable lessons: (i) a single calibrated RealSense RGB-D can suffice when rendered into virtual views (50–60% vs 57% three-cam); (ii) predicting future frames/heatmaps as auxiliary targets helped strongly (61 -> 89 in sim) but only with a huge pretrained video backbone; (iii) heatmap-peak position decoding beat direct latent regression.
Decision impact:
 - Q04 3D/depth: supports depth -> point cloud -> virtual-view projection as robust to single camera and ~2 cm calibration error (real 50–60 vs 57) — confidence L (10 trials, huge model).
 - Q09 aux objectives: supports future RGB prediction as co-target (sim 61.1 -> 89.1) but only with pretrained 5B video weights (scratch 4.6) — confidence L for our scale.
 - Q12 model size: weakens video-foundation-model VAMs for 8 GB/low-latency (>30 GB, 4.6 s/chunk) — confidence H (stated by authors).
 - Q14 robustness: lights-off/new category/background each 3–6/10 for best method at 10 demos; pi0.5 and DP3 ~0 — confidence L.
