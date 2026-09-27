# W4_GeoPredictLeveragingPredictiveKinematics — GeoPredict: Leveraging Predictive Kinematics and 3D Gaussian Geometry for Precise VLA Manipulation (2025, arXiv 2512.16811)
Setup: pi0 (3B) backbone + (a) Track Encoder over history of 3D keypoints (joints + EEF via FK) and future-track queries predicting H=50 steps of keypoint trajectories; (b) predictive 3D Gaussian voxel decoder rendering FUTURE depth for the 2 environment cams (training-only supervision with masked L1 depth loss; not executed at inference). Obs: 2 environment + 1 wrist cam, 224x224. Sim: RoboCasa Human-50 (24 tasks, 50 demos, 50 trials/task, unseen objects/styles), LIBERO (50 demos/task, 500 trials/suite). Real: DISCOVER 6-DoF arm, 3 task categories x 50 demos, 20 trials each. Training 40k iters on 8x H20, batch 32; ~12-16 h/epoch reported in ablation.
Claim: Training-time auxiliary prediction of future 3D keypoint tracks and future depth (via 3DGS) improves a VLA's 3D precision/generalization with no inference cost for the geometry module.
Evidence:
 - RoboCasa avg: BC-Transformer 28.8, GWM 39.2, pi0 42.3, GeoPredict 52.4.
 - LIBERO avg: GeoPredict 96.5 (Spatial 98.0, Object 98.2, Goal 95.7, Long 94.0) vs OpenVLA 76.5 (reported).
 - Real (Table 5, 20 trials, pi0 vs GeoPredict): Spatial (plate at unseen positions) 60 vs 85; Geometry (unseen cube sizes/prism orientations) 50 vs 95; Visual robustness (novel background distractors) 35 vs 90.
Ablations (RoboCasa avg, Table 3/4):
 - pi0 42.3 -> +history track encoder 44.8 -> +future track prediction loss 47.2 -> +future depth loss 49.4 -> joint w/o refinement 50.5 -> full track-guided refinement 52.4.
 - Render color+depth 49.2 vs depth-only 49.4 (RGB reconstruction adds nothing). Gaussians/voxel 4 -> 8: 49.4 -> 51.4 but 12.0 -> 19.1 h/epoch; refined 4+64: 52.4 at 15.7 h/epoch.
Failure/limitations: authors: needs multi-view RGB-D + extrinsics for supervision. Critical read: history-track encoder is ALSO used at inference (adds history dependence); real eval only 20 trials/category with one baseline; distractor robustness gain large (35 -> 90) but unexplained mechanism; inference latency not reported; training compute (8xH20, ~hours per epoch) far beyond our setup; appendix (history real-world experiment) not in extracted text.
Conflicts: Supports auxiliary-future-prediction line (e.g. world-model/aux-loss papers) and 3D-awareness benefits; depth-only reconstruction >= RGB reconstruction agrees with papers that find pixel reconstruction auxiliary losses weak. Adding kinematic history HELPS (+2.5) here, unlike copycat warnings — but here history is low-dim keypoint tracks in a 3B model with 50-step prediction.
Relevance: The mechanism is portable in cheaper form: add an auxiliary head to a small policy predicting future EEF/keypoint trajectory and/or future depth from our RealSense (training-only, zero inference cost). Our scene RealSense provides depth labels for free. Evidence however is on a 3B VLA; unknown whether gains hold for a small ACT-size model. Full method infeasible on 8 GB.
Decision impact:
 - Q09 auxiliary objectives: supports training-only future-track + future-depth prediction (+10.1 pts RoboCasa; each piece +2-2.5) — M (sim 1200 trials, but a single backbone, pi0)
 - Q04 depth: depth used as training-time supervision only (no depth at inference) still gives 3D gains; real geometry-generalization 50 -> 95 — L/M
 - Q07 history: low-dim kinematic history encoder +2.5 pts (42.3 -> 44.8) — L
 - Q14 robustness: real distractor background 35 -> 90%, unseen positions 60 -> 85% (20 trials) — L
 - Q10 latency: geometry module dropped at inference -> no latency cost (not measured) — L
