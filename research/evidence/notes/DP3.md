# DP3 — 3D Diffusion Policy (2024, arXiv 2403.03954)
Setup: 72 sim tasks (7 domains, 10 demos/task) + 4 real tasks (Allegro hand ×3, gripper ×1), 40 demos/task, ONE RealSense L515 (LiDAR depth), 10 trials/task. Input: depth→point cloud (extrinsics+intrinsics), crop to workspace, FPS downsample to 512/1024 pts, NO color; tiny MLP point encoder (DP3 encoder, LayerNorm, max-pool, projection) + diffusion action head (DP backbone).
Claim: simple color-free point clouds + diffusion → +24.2% relative over image DP in sim; 85% real with 40 demos; generalizes across space/viewpoint/appearance/instance; fewer unsafe commands.
Evidence:
 - Real avg (4 tasks × 10 trials): image DP 35.0±25.0, depth-image DP 20.0±12.2, DP3 85.0±11.2.
 - Design ablation (Table VII): removing cropping hurts a lot; w/ color → no accuracy gain but loses appearance generalization; LayerNorm stabilizes; DPM-solver++ fails on high-dim control.
 - Encoder: simple DP3 MLP encoder beats PointNeXt / Point Transformer (heavier point nets worse in low-data).
 - Generalization tests are ANECDOTAL: spatial 4/5 unseen bowl positions (1 trial each); appearance: trained on green cube, 5 colors × 1 trial; instance 5 objects × 1 trial; view: small shifts.
Failure/limitations: depends on good depth + calibrated extrinsics; cropping a fixed workspace box; single camera; dexterous tasks mainly; generalization evaluation has 1 trial per condition; no lighting test per se (color-free input is lighting-invariant only insofar as depth is).
Conflicts: none direct; complements DP's claim that image methods need data aug for appearance generalization ("which could impede learning").
Relevance: our RealSense on the Jetson gives depth (D4xx active stereo; noisier than L515 on thin/dark/shiny objects; pumpkin is fine). Our failures (new pumpkin appearance, dark lighting) are exactly color/texture shifts → color-free point cloud branch directly targets them. Needs depth stream from Jetson + camera-to-robot extrinsics (one-time calibration) or at least consistent camera frame (policy can work in camera frame if camera fixed).
Decision impact:
 - 3d_input: add color-free point cloud from scene depth — SUPPORTED — M (strong in-distribution numbers; robustness claims anecdotal).
 - point encoder: small MLP/PointNet-style, not heavy point transformer — SUPPORTED — M.
