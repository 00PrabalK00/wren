# W3_Pix2ActImageSpaceManipulationPolicieswit — Pix2Act: Image-Space Manipulation Policies with Equivariant Augmentation (2026, arXiv 2607.11167)
Setup: Two calibrated in-hand (wrist) cameras with intersecting optical axes + one agent-view camera. Action chunk expressed as 2D trajectories of 4 gripper keypoints in each in-hand image plane (continuous, unbounded) + gripper width; 3D EE pose recovered by triangulation. "Diffusion X-Net": ResBlock encoders from scratch (no pretrained encoder), multi-view transformer, shared per-view DiT diffusion head. Equivariant augmentation: independent SE(2) rotations of each in-hand image with matching rotation of its image-space actions. Sim: MimicGen 10 tasks, 128x128 images, 100 demos/task, chunk 12 execute 8, 50 test episodes, best checkpoint over evals. Real: UR5, 2 FLIR in-hand cams + RealSense D455 agent view, 4 tasks, 30-100 demos, 20 trials; DDIM for both methods.
Claim: grounding actions in image space of wrist cameras enables observation-action equivariant augmentation and yields better precision/generalization than SE(3) action chunks.
Evidence:
 - MimicGen avg (100 demos): Pix2Act 75.2% vs EquiDiff-Voxel 63.1%, EquiDiff-Img 53.6% (best image baseline); also beats DP, ACT, DP3, Motion Track; leads 9/10 tasks, biggest gains on high-precision/high-variation tasks.
 - Real (Table 3, %/20 trials, Pix2Act vs DP): Plug Flower (30 demos) 80 vs 55; Put in Drawer (60) 90 vs 50; Prepare Fruit Plate (70) 85 vs 60; Make Toast (100) 85 vs 60.
 - Reduced demos (Table 5): Prepare Fruit Plate 40 demos 55 vs 20, 70 demos 85 vs 60; Make Toast 70 demos 80 vs 55, 100 demos 85 vs 60.
 - Agent-view camera randomly perturbed at test time (Plug Flower, Put in Drawer): Pix2Act "unaffected", DP fails to complete either task (no exact numbers in text).
Ablations (Table 2, 4 MimicGen tasks StackThree/Hammer/Square/Threading, avg 69.3):
 - w/o equivariant aug: 51.0 (−18.3; −16 to −20 per task)
 - joint instead of shared per-view head: 49.5 (−19.8; Hammer −42)
 - predict 3D absolute action from same tokens: 41.5 (−27.8); 3D relative (EE-canonicalized) action: 55.5 (−13.8) → relative > absolute for SE(3) actions here
 - w/o agent-view camera: 66.5 (−2.8) — wrist cams carry most information
 - w/o proprioception: 68.0 (−1.3)
Failure/limitations: needs calibrated dual in-hand cameras; discontinuities when motion crosses camera plane; parallel grippers only; trained from scratch (no pretrained encoder). Critical read: sim numbers are best-checkpoint (optimistic for all methods); camera-perturbation result reported qualitatively; the agent-view shift test is easy for a policy that barely uses the agent view (ablation −2.8).
Conflicts: Relative (EE-frame) 3D actions beat absolute by 14 pts — agrees with ActionSpace studies favoring delta/relative and UMI's relative trajectories, contrasts with ACT's claim that absolute joints are better (different embodiment/control). The finding that agent view is nearly dispensable agrees with wrist-camera-centric results (UMI, Dobb-E).
Relevance: Medium. SO-101 has one wrist cam, not a stereo pair, so the full method doesn't apply. Transferable: (a) wrist views + EE-relative actions strongly reduce dependence on the scene camera → robustness to scene camera shift (our "slightly moved camera" failure); (b) equivariant (observation+action) augmentation is a big lever (+18 pts) when actions are expressed in the camera frame — with a single wrist cam, an in-plane rotation of wrist image + rotated EE-frame action is possible in principle; (c) from-scratch ResNet encoders are fine at 30-100 demos.
Decision impact:
 - Q02 action space: EE-relative actions beat absolute 3D (55.5 vs 41.5); image-space actions best (69.3) — M (sim ablation, 4 tasks)
 - Q05 augmentation: equivariant obs+action augmentation +18.3 pts avg — M
 - Q11 cameras: wrist cams dominant (removing agent view −2.8); agent-view perturbation breaks DP but not wrist-grounded policy — M
 - Q13 data: Pix2Act 55% vs DP 20% at 40 real demos; both improve at 70 — L/M
 - Q14 robustness: camera shift robustness via wrist-frame action grounding — L (qualitative)
