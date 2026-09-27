# W3_RoboticManipulationisVisiontoGeometryMap — Robotic Manipulation is Vision-to-Geometry Mapping: Vision-Geometry Backbones over Language and Video Models (VGA) (2026, arXiv 2604.12908)
Setup: VGGT (pretrained feed-forward 3D reconstruction transformer) as backbone, LoRA r=64, ~500M trainable params, 12-layer regression action head (OFT-style, L1-ish), chunk 8, aux camera+depth heads (sim only), A100s ≤60 GPU-h. Sim: LIBERO (~400 demos/suite, 500 rollouts/suite), RoboTwin2.0 (5 tasks), LIBERO-Plus (lighting/language/camera). Real: Franka + 3× RealSense D415 (wrist + fixed cam-1 for training/ID + unseen fixed cam-2 for OOD), 3 fine-grained tasks, 80–100 demos/task, 20 trials per task per condition; language grasp task 60 demos/object, 20 trials. RGB only (no depth input).
Claim: a pretrained 3D-geometry backbone (VGGT) beats VLM/video backbones, especially for viewpoint generalization, without depth sensors.
Evidence:
 - LIBERO avg 98.1% vs π0.5 96.9, OpenVLA-OFT 97.1, GeoVLA 97.7 (saturated benchmark).
 - RoboTwin2.0 Easy/Hard: VGA 80.4/77.6 vs π0 72.8/67.6, X-VLA 66.2/67.0.
 - LIBERO-Plus (zero-shot, light/language/camera): VGA 92.1/81.5/86.0; OpenVLA-OFT 85.8/81.5/59.7; π0 79.6/61.0/15.8; UniVLA 59.1/71.8/4.3.
 - Real (80–100 demos, 20 trials): ID avg ACT 37%, OpenVLA 18%, π0.5 77%, VGA 75%. Unseen camera (OOD) avg ACT 7%, OpenVLA 3%, π0.5 52%, VGA 58% (stack cube OOD: VGA 40 vs π0.5 50).
 - Language grasp among 3 similar vegetables: VGA 80% vs π0.5 76.7%.
Ablations (LIBERO avg): w/o PVM 95.7; w/o joint 3D-aux training 97.2 (vs 98.1); random init + full FT 86.6; random init + LoRA 6.4; VGGT init + full FT 87.1; VGGT init + LoRA 98.1 → pretrained 3D prior + keeping it frozen-ish (LoRA) worth ~11 points; full fine-tuning destroys most of the prior benefit.
Failure/limitations: real-world uses only action loss (no 3D aux). 20 trials/cond, 3 simple tasks; OOD gain over π0.5 is +6 pts (≈1 trial/task) — not significant. Wrist cam present in both ID/OOD, which likely carries much of OOD performance. 500M trainable, large compute; no latency reported. Stack cube OOD VGA < π0.5.
Conflicts: ACT (ImageNet ResNet18, scratch transformer) collapses under camera move 37→7% — consistent with LLaVA-VLA paper and RoViAug. Full-FT-destroys-prior agrees with papers favoring frozen/LoRA pretrained encoders in low data (e.g., Theia/VC-1 lines) and contrasts with ACT-style end-to-end FT.
Relevance: Directly our "slightly moved camera" failure: pretrained, geometry-aware representations + wrist cam give a large robustness gap vs ACT with ~same demo budget (80–100). VGGT backbone too heavy for our 8 GB inference loop likely; but the lesson "keep pretrained encoder largely frozen (LoRA), don't full-FT" is transferable. Auxiliary depth prediction gives only +0.9 in sim.
Decision impact:
 - Q03 vision encoder: supports pretrained + LoRA/frozen over full FT (98.1 vs 87.1) and over scratch — confidence M (sim ablation; real only vs baselines).
 - Q04 3D: supports implicit 3D priors from RGB (no depth sensor) — confidence L (no RGB-D comparison).
 - Q11 cameras: ACT drops 37→7% on unseen scene camera even with wrist cam; pretrained 3D backbone 75→58% — confidence M.
 - Q09 auxiliary: joint depth/camera prediction +0.9 pts (97.2→98.1) — confidence L (sim, saturated).
 - Q14 robustness: camera shift is the dominant failure for small scratch policies — confidence M.
