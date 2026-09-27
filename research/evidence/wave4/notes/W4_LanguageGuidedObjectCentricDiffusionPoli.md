# W4_LanguageGuidedObjectCentricDiffusionPoli — Language-Guided Object-Centric Diffusion Policy for Generalizable and Collision-Aware Manipulation (Lan-o3dp) (2024/ICRA 2025, arXiv 2407.00451)
Setup: Sim: 21 RLBench tasks, single front camera 120×120, 40 demos/task, CNN diffusion policy conditioned (FiLM) on object-only point cloud (256 pts) from open-vocab segmentation; 20 eval episodes every 50 epochs, report mean of top-5 checkpoints. Real: Diana 7 arm, ONE RealSense D415, 4 tasks (pour, bottle upright, tape to drawer, brushing), 40 space-mouse demos/task; GroundingDINO → SAM → Cutie tracking for masks; EE-pose actions. GPT-4 parses instructions into policy/targets/obstacles. Inference RTX A6000 Ada: 100 DDPM steps ≈1 Hz, 16 steps ≈5 Hz.
Claim: segmented task-object point clouds as sole visual input make DP data-efficient and robust to background, instance change, clutter and camera view shift; A0|k-based cost guidance gives training-free obstacle avoidance.
Evidence:
 - RLBench 21 tasks, 40 demos: Lan-o3dp 68.7% vs DP (RGB) 39.3% vs DP3 (scene point cloud) 43.6%.
 - Real generalization: figure only, qualitative: higher base SR than DP; under camera view shift "no performance drop" whereas RGB DP "failed entirely"; instance change / multiple similar objects / clutter handled (numbers only in Fig. 5).
 - Obstacle avoidance (5 trials per obstacle): w/o guidance 0% everywhere; with guidance Pour: bottles 100, box 60, kettle 80, phone 100, laptop 60; Brush bottles 40; drawer bottles 20%.
Ablations (7 RLBench tasks): point encoder MLP 64.1%, PointNet 14.9%, MLP+residual 68.8% (sample prediction); epsilon prediction 65.7% vs sample 68.8%. Guidance on Ak vs A0|k without last-step guidance: 0% vs 60–100%.
Failure/limitations: assumes detection/segmentation succeeds; EE-only collision avoidance; eval protocol "top-5 of checkpoints" inflates sim numbers; real generalization numbers in figure only; few trials.
Conflicts: agrees with GSL, ControlVLA (object-centric → robustness), and with iDP3/DP3 notes that simple MLP point encoders beat PointNet in low data. Scene-level point cloud (DP3) only +4 pts over RGB here, object-level +29 — suggests the gain is from removing distractor/background, not from 3D per se.
Relevance: SO-101 with RealSense: segment pumpkin + tray (GroundingDINO/SAM2 + tracker), back-project with depth to ~256 points each, feed to small MLP encoder + DP/flow head. This directly attacks lighting/background/camera-shift failures (point cloud in camera frame still shifts with camera, but calibrated extrinsics transform to robot base frame). Cost: segmentation/tracking latency on laptop; tracking failure modes.
Decision impact:
 - Q04 3D/depth: object-centric point cloud 68.7 vs scene point cloud 43.6 vs RGB 39.3 (40 demos, 21 sim tasks) — supports segmented-object 3D input — confidence M.
 - Q14 robustness: camera view shift no drop vs RGB DP total failure (real, qualitative) — L/M.
 - Q03 encoder (point): simple MLP+residual 68.8 >> PointNet 14.9 — M.
 - Q01 head: sample (x0) prediction 68.8 vs epsilon 65.7 — L.
