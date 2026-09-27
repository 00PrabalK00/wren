# W3_CanonicalPolicyLearningCanonical3DRepres — Canonical Policy: Learning Canonical 3D Representation for SE(3)-Equivariant Policy (2025, arXiv n/a in text)
Setup: sim: 12 tasks (8 MimicGen, Push-T, 3 bimanual), success = mean of last 10 checkpoints × 50 inits. Real: Franka Panda (relative/OSC control) + UR5 (absolute EE control), ONE fixed RealSense D415 RGB-D, SpaceMouse teleop at 10 Hz, 100 demos/task on Franka (4 tasks), 50/100 demos on UR5 shoe task; point cloud cropped to workspace box, xyz only (no color), 256 points; diffusion head, DDIM 20 steps; image baselines at 230×230 crop. 10 trials per condition.
Claim: canonicalizing the point cloud (SO(2)/SO(3)-equivariant rotation estimate + translation removal) before a DP3-style diffusion policy gives better data efficiency and robustness to color/shape/viewpoint than image and plain point-cloud policies.
Evidence:
 - Real Franka (Table IX, 100 demos): Block/Shoe/Can/TableOrg — DP 2/1/4/0, EquiDiff 3/3/3/2, DP3 3/5/1/0, CP-SO2 7/6/4/3 (of 10).
 - Color variation (Table X): image DP/EquiDiff collapse to 0 on most tasks; CP-SO2 beats second best by 30/30/10/20 pts (xyz-only point clouds are color-blind by construction).
 - Color+shape (Table XI): leather shoes DP 0, EquiDiff 2, DP3 3, CP 5; hiking boots 0/0/2/2.
 - UR5 data efficiency (Table XII, trained black shoes): 50 demos — ACT, DP, EquiDiff, DP3 all 0/10; CP-SO2 4/10 black, 6/10 white. 100 demos — ACT 1/10 & 1/10, DP/EquiDiff 0, DP3 3/10 & 2/10, CP 6/10 & 7/10.
 - Viewpoint (Table XIII, 50 demos): training view CP 4/6; frontal (~15° rotation) CP 4/10 & 6/10, ACT/DP/EquiDiff 0; right-angled (~30°) CP 3/10 & 3/10.
Ablations:
 - Sim canonicalization vs DP3: Stack D1 DP3 23 → CP-SO3 71 / CP-SO2 79; Mug Cleanup 28 → 37/38; Nut Assembly 21 → 39/42.
 - Point-cloud encoder: PointNet++ and DGCNN drop MimicGen to ~0 under all policies; the simple DP3 MLP encoder is best; EquiBot with DP3 encoder improves a lot (Push-T 90%).
 - Scaling (SIM(3)) vs SE(3): mixed (2 tasks up, 2 down).
 - Frozen vs trained equivariant branch (Table VIII): CP-SO3 Stack D1 68 → 18 when frozen; CP-SO2 76 → 68.
 - Diffusion vs flow matching (Table VII): Stack D1 CP-SO2 76 vs 59, DP3 20 vs 17; Push-T CP-SO2 87 vs 97, DP3 70 vs 83 — task-dependent, no winner.
 - Equivariant branch only ~3.2% of params; larger branch → higher success.
Failure/limitations: neighborhood-processing encoders are slow; large viewpoint shift changes visible geometry (occlusion) → canonicalization fails (30° → 30%). Baselines worse on UR5 than Franka because UR5 has no OSC smoothing and "baseline policies frequently produced unstable motions" with a single camera and 50–100 demos. My read: 10 trials/cell, no wrist camera for image baselines, image baselines without strong augmentation; image baselines at 0/10 for 50–100 demos on UR5 looks like under-tuned baselines.
Conflicts: agrees with DP3/iDP3 that xyz-only point clouds are appearance-invariant and data-efficient; disagrees with papers where DP (RGB) beats DP3 in real (e.g. with wrist cams). Diffusion-vs-flow result supports "head choice is task-dependent, second-order".
Relevance: HIGH on the camera/appearance axis: our scene RealSense can provide exactly this cropped xyz point cloud; pumpkin color change is analogous to black→white shoe; our 50-demo regime is where image baselines failed here. SO-101 uses absolute joint targets without OSC smoothing — similar to UR5 case where jerky baselines failed. Caveat: pumpkin-in-tray is geometrically simple; neighborhood encoders cost latency.
Decision impact:
 - Q04 depth/point cloud: xyz-only point cloud + canonicalization 4–6/10 vs image policies 0/10 at 50 demos; color change robust — supports adding scene point-cloud branch — confidence M (10 trials, one task on UR5).
 - Q14 robustness: object color change kills image DP/EquiDiff (≈0) but not xyz point-cloud policies — supports color-free geometry input for object-appearance shift — confidence M.
 - Q11 cameras/viewpoint: ~15° camera rotation → image policies 0/10, CP 4–6/10; ~30° → 3/10 — supports 3D canonical input for camera shift; also shows even 3D degrades at large shifts — confidence M.
 - Q01 action head: diffusion vs flow matching task-dependent (Stack 76 vs 59, Push-T 87 vs 97) — neither dominates — confidence M (sim, many seeds).
 - Q03 encoder (point cloud): simple DP3 MLP encoder ≫ PointNet++/DGCNN (latter ~0 on MimicGen) — supports lightweight PC encoder — confidence M (sim).
 - Q13 data: CP only method non-zero at 50 demos; baselines need >100 — confidence L.
