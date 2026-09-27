# iDP3 — Generalizable Humanoid Manipulation with 3D Diffusion Policies (2024, arXiv 2410.10803)
Setup: humanoid (upper body), head-mounted RealSense L515; 3 tasks (Pick&Place, Pour, Wipe), 10 demos × 10 rollouts = 100 episodes/task from ONE scene; >100 real trials for ablations; objects randomized in 10×10 cm; inference 15 Hz onboard.
Changes vs DP3: (1) egocentric point clouds in CAMERA frame — no calibration, no segmentation; (2) scale input to 4096 points instead of cropping; (3) conv + pyramid point encoder (smoother than MLP on human data); (4) longer prediction horizon (critical for jittery human demos).
Evidence:
 - In training scene: image DP with FINETUNED R3M (+random crop +color jitter) is the strongest method, slightly BETTER than iDP3; DP frozen R3M, vanilla DP, vanilla DP3 worse.
 - Out of distribution (10 trials each): new object Pick&Place/Pour: DP 3/10, 1/10 vs iDP3 9/10, 9/10; new view: DP 2/10, 0/10 vs iDP3 9/10, 9/10; new scene: DP 2/10, 1/10 vs iDP3 9/10, 9/10. Image DP fails in new scenes even WITH color-jitter augmentation.
 - Ablations (total successes/attempts): encoder Linear(DP3) 58/127 → Conv+Pyramid 75/139; points 1024 < 2048 < 4096 (saturating ~8192); without longer horizon DP3 fails to learn from human data.
 - Training time: iDP3 ~30 min vs DP ~80 min.
Failure/limitations: depth noise (they explicitly say D435-class depth is worse than L515); only 3 simple tasks; single-scene training; generalization trials small (10).
Conflicts/nuance: supports DP paper: fine-tuned pretrained image encoder wins IN distribution; 3D wins OUT of distribution. Color jitter alone did NOT fix image-policy scene/object shift.
Relevance: exactly our failure (new scene lighting + new pumpkin + moved camera). Camera-frame clouds remove need for calibration — works for our fixed scene cam. Our Jetson RealSense is likely a D4xx (stereo) → noisier depth; pumpkin is matte/large (good for stereo), gripper thin parts less so.
Decision impact:
 - 3d_input: SUPPORTED strongly for OOD robustness — M/H (100+ trials in-dist, 10 per OOD cell, consistent large gaps).
 - hybrid: image branch (fine-tuned) for in-distribution precision + point branch for robustness — suggested by the in-dist vs OOD split — M.
 - augmentation alone insufficient for scene/object shift — SUPPORTED — M.
 - prediction horizon: longer horizon needed for human demos — SUPPORTED — M.
