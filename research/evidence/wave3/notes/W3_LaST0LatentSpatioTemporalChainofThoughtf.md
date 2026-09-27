# W3_LaST0LatentSpatioTemporalChainofThoughtf — LaST0: Latent Spatio-Temporal Chain-of-Thought for Robotic Vision-Language-Action Model (2026, arXiv id not in text)
Setup: 3.3B VLA (two Janus-Pro-initialised experts in a Mixture-of-Transformers), pretrained on >400K trajectories (OXE, DROID, RoboMIND), SFT 300 epochs on 8×A800. Sim: RLBench 10 tasks (100 keyframe demos/task, single front view RGB 384² + 1024-pt point cloud + proprio; 20 trials × 3 seeds), LIBERO (4 suites, 500 trials/suite, 2 views). Real: Franka single/dual-arm (6 tasks), AgileX mobile (2), TienKung humanoid hand (2); 200 teleop demos/task; 15 rollouts × 3 positions. Action head = flow matching. Inference 15.4 Hz on RTX 4090 without chunking.
Claim: predicting a few compact latent tokens of future image / point cloud / proprio (latent CoT) in a slow expert, and conditioning a fast flow-matching action expert on it, beats explicit CoT VLAs and π0.5 while being 14× faster than explicit CoT.
Evidence:
 - RLBench mean: LaST0 82% vs HybridVLA-7B 74%, π0.5-3B 65%, CogACT-7B 61%. Speed: LaST0 15.4 Hz vs CoT-VLA 1.1 Hz vs π0.5 13.8 Hz (4090).
 - LIBERO mean 98.1% (Spatial 99.2, Object 99.6, Long 95.6 vs OpenVLA-OFT 94.5, π0.5 92.4); CoT-VLA 81.1%.
 - Real Franka mean (6 tasks, 45 trials each): LaST0 0.72 vs π0.5 0.59, CoT-VLA 0.50, SpatialVLA 0.41. Long-horizon egg task steps 1/2/3: LaST0 0.66/0.47/0.33 vs π0.5 0.47/0.20/0.07.
Ablations (RLBench 10 tasks, figure values quoted in text):
 - Latent modality: image-only 74%, point-cloud-only 76%, proprio-only 75%, all three 82%.
 - Latent tokens per modality: 0 → 68%, 1 → 82%, more → no significant gain.
 - Latent temporal coverage (future keyframes): 0 → 68%, 4 → 82%, beyond 4 no gain.
 - Slow:fast ratio: 1:1/1:2/1:4 = 75–79%, 1:8 = 74%; training with mixed ratios then testing at 1:4 = 82%.
 - Single backbone instead of MoT two experts: 74% vs 82%.
Failure/limitations: authors: limited pretraining coverage for mobile/dexterous, complex object interactions hard. Critical read: all ablations in RLBench sim with keyframe/motion-planner demos (not human teleop); 3.3B params + 400K-traj pretraining — nowhere near 8 GB deployable; real eval is 45 trials per task, no lighting/camera-shift tests; "no latent" baseline (68%) still includes the large pretrained backbone, so the +14 pts is an auxiliary-future-prediction effect inside a big VLA.
Conflicts: agrees with other future-prediction-as-auxiliary papers (e.g. Seer/UP-VLA style) that predicting future state helps; differs from "Is Forward Prediction Enough" type critiques that pure pixel prediction adds little — here the gain comes from very compressed (1 token/modality) latents, not pixel reconstruction. Trained with mixed slow/fast delays → echoes async-training ideas (train with stale conditioning to be robust to latency).
Relevance: low-moderate for SO-101. Architecture too large for 8 GB. Transferable ideas: (1) a cheap auxiliary head predicting a few future latent tokens (incl. future proprio) could regularise a small policy; (2) run expensive perception at a lower rate than the action head and train with randomly stale conditioning so async execution is in-distribution.
Decision impact:
 - Q09 auxiliary objectives: supports compact future-latent prediction (image/3D/proprio) as auxiliary — confidence L (sim RLBench ablation, 3.3B VLA).
 - Q10 latency/async: supports training with randomly mixed stale-conditioning ratios for slow/fast decoupling — confidence L (sim only).
 - Q04 3D: point-cloud latent alone 76% vs image 74% — ~neutral, small effect — confidence L.
 - Q12 model size: no evidence for small models; 3.3B, 200 demos/task — n/a — L.
