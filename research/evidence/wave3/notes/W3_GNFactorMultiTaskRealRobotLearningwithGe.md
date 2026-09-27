# W3_GNFactorMultiTaskRealRobotLearningwithGe — GNFactor: Multi-Task Real Robot Learning with Generalizable Neural Feature Fields (2023, arXiv 2308.16891)
Setup: Keyframe (next-best-pose) voxel policy à la PerAct (Perceiver, 25.2M params) + a Generalizable Neural Feature Field that renders RGB and Stable-Diffusion features from a 100³ voxel grid built from ONE front RGB-D camera; extra views used only as rendering supervision at train time (19 in sim, 2 in real). Sim: 10 RLBench tasks, 20 demos/task, 128×128 RGB-D, 25 episodes × 3 seeds. Real: xArm7, 3 RealSense (front RGB-D for policy), 2 toy kitchens, 3 tasks, 5 VR demos/task, 10 trials per cell. 2×RTX3090, 2 days, batch 2.
Claim: distilling 2D foundation-model features into a 3D voxel representation via neural rendering improves multi-task few-shot BC and generalization.
Evidence:
 - RLBench multi-task avg (Table 1): PerAct 20.4, PerAct 4 cams 22.7, GNFactor 31.7.
 - RLBench generalization (larger/smaller obj, new position, distractor; Table 2): PerAct 18.0 vs GNFactor 28.3.
 - Real (Table 3, 10 trials each, avg of 12 cells): PerAct 22.5 vs GNFactor 43.3. Teapot (precise grasp): PerAct 0 in all 4 cells vs 30–40. With distractors, both drop (door k1: 40 → 30; k2: 50 → 20 for GNFactor).
Ablations (Table 4, 10-task avg): full 36.8; w/o GNF rendering objective 24.2; w/o RGB rendering loss 27.2; w/o diffusion features 30.0; diffusion → DINO 30.4; → CLIP 32.0; w/o depth-guided sampling 29.2; w/o skip 27.6; rendering views 19 → 9: 33.2; loss weights 0.01 → 1.0: 35.2.
 - More cameras as direct PerAct input (1 → 4): 20.4 → 22.7 only; using extra views as auxiliary rendering supervision helps more (24.2 → 36.8).
Failure/limitations: keyframe/motion-planner action space (not continuous teleop control); needs calibrated multi-camera for training; heavy (2 days on 2×3090); real 10 trials/cell; absolute success modest.
Conflicts: supports auxiliary reconstruction objectives as regularizers in low-data regimes (like 3D reconstruction / view-synthesis aux in other works); DINO vs SD features differ by only 0.4–2 pts here — contradicts papers finding DINOv2 best, but differences are within seed noise (std often ±5–15).
Relevance: low-medium. Keyframe voxel paradigm doesn't match our continuous joint-space chunking policy or 8 GB compute. Transferable idea: extra cameras as training-only auxiliary supervision rather than inference input; depth from the scene RealSense used to build 3D representation.
Decision impact:
 - Q09 auxiliary objectives: supports view-synthesis/feature-rendering aux loss (w/o it 24.2 vs 36.8, sim) — confidence M (sim ablation, 3 seeds; keyframe policy).
 - Q04 3D: supports 3D voxel + distilled 2D features for few-shot real (43.3 vs 22.5 PerAct, both 3D) — confidence L (both baselines 3D; no RGB-only 2D baseline).
 - Q11 cameras: adding 3 more input cameras to PerAct gives only +2.3 pts; wrist cam not studied — confidence L.
 - Q03 vision encoder: SD features > CLIP > DINO by small margins (36.8/32.0/30.4) — confidence L (within noise).
