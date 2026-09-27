# W3_ToolFlowNetRoboticManipulationwithToolsv — ToolFlowNet: Robotic Manipulation with Tools via Predicting Tool Flow from Point Clouds (2022, CoRL 2022)
Setup: segmented point cloud (xyz + one-hot class) -> segmentation PointNet++ predicts per-point flow on the tool -> differentiable SVD -> SE(3) delta action; single-step BC (no chunking). Sim (SoftGym/FleX): ScoopBall (4D/6D action) and PourWater (3D/6D), scripted demonstrator, 500 epochs, 5 seeds, 25 test configs, normalized by demonstrator success (max over training history). Real: Sawyer + ladle (scanned tool model), top-down Azure Kinect depth for ball, 100 kinesthetic demos (~20 steps each), 50 trials.
Claim: predicting dense per-point tool flow and converting via SVD beats directly regressing an action vector from point clouds or images, mainly for rotations.
Evidence (normalized success, avg over 4 task variants, 5 seeds; ScoopBall4D / ScoopBall6D / PourWater3D / PourWater6D):
 - PCL Direct Vector MSE: 0.544/0.848/0.530/0.402 = 0.581; PM loss variant 0.124.
 - PCL Dense Transformation MSE 0.556, PM 0.340.
 - D direct 0.311; D+S (mask channel) 0.686; RGB 0.538; RGB+S 0.693; RGBD 0.606; RGBD+S 0.753.
 - ToolFlowNet 1.152/0.952/0.795/0.667 = 0.892.
 - Real: 41/50 (82%) scooping; all 9 failures = ladle colliding with container. No real baseline.
Ablations:
 - No skip connections: 0.323 (PourWater 0.000 — cannot predict rotations). MSE after SVD: 0.572. PM before SVD: 0.740. No consistency loss: 0.670 (all vs 0.892).
 - Translation-only ScoopBall variant: ToolFlowNet does NOT beat baselines -> benefit comes entirely from rotation prediction.
 - Direct-vector baselines with 4D/6D/9D/10D rotation reps (appendix) still below ToolFlowNet (not re-read in detail).
 - Adding a binary segmentation mask channel to image inputs: D 0.311 -> 0.686, RGB 0.538 -> 0.693, RGBD 0.606 -> 0.753 (a large, cheap gain).
Failure/limitations: needs ground-truth segmentation and a tool model (occlusion); actions required to compute flow; scripted sim demos (unimodal); only one real task without baseline; single-step policy. Critical: sim baseline numbers use max-over-training-history (optimistic for all).
Conflicts: agrees with other 3D papers that RGBD > RGB alone modestly (0.606 vs 0.538) but here RGB+mask ~ D+mask, i.e., knowing *where the object is* matters more than the depth modality. Old (2022) and pre-chunking/pre-diffusion.
Relevance: low. Our gripper does not hold a tool and the task is translation-dominated pick-place (the paper shows flow gives no benefit for translation-only). Useful side finding: object mask channels substantially help image policies — relevant as a cheap robustness prior (e.g., SAM mask of pumpkin/tray) for appearance shift.
Decision impact:
 - Q04 3D/depth: RGBD modestly > RGB (0.606 vs 0.538 sim); dense point-flow helps only for rotation-heavy tool tasks — confidence L (sim, scripted demos).
 - Q14/Q05 robustness: supports adding object segmentation masks as input channels (RGB 0.538 -> 0.693, D 0.311 -> 0.686) — confidence L (sim, GT masks).
