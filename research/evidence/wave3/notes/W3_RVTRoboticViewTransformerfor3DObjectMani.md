# W3_RVTRoboticViewTransformerfor3DObjectMani — RVT: Robotic View Transformer for 3D Object Manipulation (2023, arXiv 2306.14896)
Setup: keyframe (next-best-pose) policy + motion planner. RGB-D → point cloud (robot base frame) → re-rendered into 5 ORTHOGRAPHIC virtual views (cube around workspace) with RGB, depth, xyz-correspondence channels → multi-view transformer predicts per-view translation heatmaps, rotation bins, gripper. Sim: RLBench 18 tasks, 100 demos/task, 4 RGB-D cams 128×128 (front, shoulders, wrist). Real: Franka, ONE third-person Azure Kinect RGB-D (calibrated), 5 tasks / 13 variations, 51 kinesthetic demos total (~10/task), 10 trials per variation set. Train 1 day on 8 V100 (vs PerAct 16 days).
Claim: view-based 3D (re-rendered virtual views) beats voxel 3D (PerAct) while being faster to train and infer.
Evidence:
 - RLBench avg (Table 1): Image-BC CNN 1.3, Image-BC ViT 1.3, C2F-ARM 20.1, PerAct 49.4, RVT 62.9. Inference 11.6 fps vs PerAct 4.9 fps; training 1 day vs 16 days.
 - Real (Table 2 right): stack blocks 100%, press sanitizer 80%, marker 0%, drawer 50%, shelf 50%; overall 56%, 82.5% excluding marker tasks. Marker failures blamed on sparse/noisy depth of thin objects.
Ablations (RLBench avg; full = 62.9):
 - Lower render resolution 51.1; no view-correspondence channel 59.7; no depth channel 60.3; no separate per-view processing 58.4; perspective instead of orthographic 40.2; no rotation aug 60.4; 3 views 60.2; single front view 35.8; views rotated 15° 59.9; using the REAL sensor camera views instead of re-rendered: 22.9 (orthographic) / 10.4 (perspective, no rot aug).
Failure/limitations: keyframe actions + motion planner (not continuous control, no chunk-boundary issues); requires calibrated depth → point cloud; thin objects (marker) fail due to depth noise.
Conflicts: agrees with iDP3/DP3 line that 3D input helps sample efficiency; image-only BC nearly 0 here, but that is a keyframe single-step image-BC baseline from PerAct's paper, not a modern chunked 2D policy (ACT/DP routinely do much better), so the 2D vs 3D gap is exaggerated.
Relevance: medium-low. Our policy is continuous chunked control; RVT's pipeline is not a drop-in. Transferable: (1) from ONE calibrated RealSense RGB-D, re-rendering canonical virtual views (e.g., top-down orthographic) is far better than raw sensor view (62.9 vs 22.9) — and makes the policy input invariant to physical camera placement, which directly targets our "slightly moved camera" failure (if re-calibrated); (2) point-cloud rotation/translation augmentation is only possible with a 3D representation; (3) thin objects suffer from depth noise (pumpkin is fine; gripper fingers less so).
Decision impact:
 - Q04 3D/depth: supports RGB-D point cloud → virtual orthographic views; single-sensor re-rendering 62.9 vs sensor views 22.9; depth channel +2.6 — confidence M (sim, keyframe setting).
 - Q11 cameras / viewpoint robustness: canonical re-rendered views decouple policy from physical camera pose (not directly tested for camera shift) — confidence L.
 - Q05 augmentation: 3D point-cloud rotation aug +2.5 (60.4 → 62.9) — confidence L.
 - Q13 data quantity: ~10 demos/task sufficient for simple keyframe tasks in real (82.5% excl. marker) — confidence L (keyframe ≠ continuous).
 - Q10 latency: 11.6 fps vs 4.9 fps PerAct — confidence L (keyframe inference only).
