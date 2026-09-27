# W3_RoViAugRobotandViewpointAugmentationforC — RoVi-Aug: Robot and Viewpoint Augmentation for Cross-Embodiment Robot Learning (2024, arXiv 2409.03403)
Setup: Franka and UR5, single side-mounted ZED 2 third-person camera (NO wrist camera), teleop at 15 Hz, 150 demos per task, 5 tasks, Diffusion Policy (2-step history); 10 real trials per cell. Robot aug: LoRA-SAM robot segmentation + ControlNet SD robot-to-robot + E2FGVI inpainting + random brightness on pasted robot. Viewpoint aug: ZeroNVS novel-view synthesis with random SE(3) camera perturbation (per-trajectory "consistent" or per-frame "inconsistent"), done offline.
Claim: generative robot + viewpoint augmentation lets a policy deploy zero-shot on another robot and on shifted cameras.
Evidence:
 - Viewpoint (Place Tiger, Franka→Franka, test camera shifts Same / 10cm,20° / 25cm,35° / 35cm,45°): No aug 100/0/0/0. Vi-Aug 10cm consistent 100/30/0/0; 10cm inconsistent 100/70/10/0; 25cm consistent 100/80/30/30; 25cm inconsistent 90/80/50/30; 40cm consistent 70/70/60/20; 40cm inconsistent 80/80/50/40.
 - Cross-robot zero-shot same camera (5 tasks): no aug 0/0/0/0/40; Mirage 60/90/50/100/70; Ro-Aug 90/80/30/100/80; Ro-Aug w/o brightness randomization 90/50/10/40/60.
 - Cross-robot + camera shift (Table 4, 4 tasks × 2 shifts): RoVi-Aug ≥ Mirage and Ro-Aug at the larger shift (e.g. 50 vs 20 vs 30 etc.; Ro-Aug alone often 0–30).
 - Few-shot: 5-shot target demos 40/30/0/50/40 → Ro-Aug+5-shot 100/100/60/100/100.
 - Octo finetune (50 target demos): 30→60, 20→40 with RoVi-Aug pretraining data.
Ablations: brightness randomization of pasted robot matters (Place Tiger 80 vs 50, Sweep 100 vs 40); wider viewpoint range trades in-distribution accuracy (100→70–80%) for robustness; per-frame inconsistent aug ≥ consistent (with only 2-frame history).
Failure/limitations: 10 trials per cell; single side camera (no wrist); pipeline cascade artifacts; single task for viewpoint study; offline generation cost high; backgrounds unchanged.
Conflicts: The "no aug 100% → 0% with 10 cm/20° shift" is the starkest camera-brittleness number in our set; agrees with VGA (ACT 37→7% on unseen camera) though there the wrist camera softened it. Inconsistent-per-frame aug being fine here vs RoboVIP saying per-frame inconsistency collapses 6-frame-history Octo — reconciled by history length (2 vs 6 frames).
Relevance: Our "slightly moved camera" failure: a scene-camera-only BC policy can go to 0% with a ~10 cm shift. Mitigations: (a) wrist camera (not tested here), (b) viewpoint augmentation of the scene cam ±10–25 cm (cheap alternatives: random crop/shift/perspective warp, or depth-based reprojection from our RealSense since we have depth!), (c) brightness randomization. Keep a moderate range — too wide costs ~20 pts in-distribution.
Decision impact:
 - Q11 cameras: single fixed third-person camera policy 100%→0% at 10 cm/20° shift — confidence M/H (real, clean ablation, 10 trials).
 - Q05 augmentation: novel-view aug ±25 cm restores 0→80% (10cm,20°) and 0→50% (25cm,35°); cost −10 pts in-distribution — confidence M.
 - Q05 augmentation: brightness randomization of synthetic regions prevents overfitting (e.g. 40→100% sweep) — confidence M.
 - Q14 robustness: camera pose shift is catastrophic without aug — confidence M/H.
 - Q07 history: per-frame inconsistent aug OK with 2-frame history — confidence L.
