# W3_RoboMINDBenchmarkonMultiembodimentIntell — RoboMIND: Benchmark on Multi-embodiment Intelligence Normative Data for Robot Manipulation (2024, arXiv 2412.13877)
Setup: dataset paper: 107k real teleop trajectories, 479 tasks, 96 objects, 4 embodiments (Franka, UR5e, AgileX dual-arm, Tien Kung humanoid), 8-criterion quality assurance, plus 5k annotated FAILURE trajectories and a digital-twin sim. Benchmarks: single-task ACT / Diffusion Policy (DROID implementation) / BAKU trained from scratch on 45 tasks; VLAs (OpenVLA, RDT-1B, CrossFormer) fine-tuned multi-task; 10 real trials per task.
Claim: a large, quality-controlled, multi-embodiment dataset that trains strong single-task and VLA policies.
Evidence:
 - ACT avg success: AgileX 55.3% (15 tasks), UR5e 38.0% (5), Tien Kung 34.0% (10), Franka 30.7% (15). DP beats ACT on several Franka/Tien Kung tasks (figure only); BAKU lowest (attributed to sim-tuned hyperparameters).
 - VLAs: RDT-1B best overall, especially dual-arm (Table III, numbers not extracted cleanly).
 - Failure analysis for ACT (Fig. 15): "Inaccurate positioning" is the top failure reason on every embodiment, up to 48% of failures on humanoid; gripper failures (can't close, object drop) are next.
 - Sim+real co-training (ACT, FR-UprightBlueCup, 100 real + 0–500 digital-twin sim traj): more sim improves success in both real and sim (figure only); sim-only → 10% real; 100:500 → 90% in sim.
 - Sim/real correlation of single-task ACT/DP evals over 5 tasks: Pearson 0.83 (ACT) and 0.91 (DP) (as extracted).
Ablations: only real:sim ratio (figure only).
Failure/limitations & critical read: benchmark numbers are default-hyperparameter baselines with 10 trials; demos per task vary and not controlled; no systematic data-quantity ablation.
Data-quality lessons stated by authors: (1) inaccurate positioning traced to non-random object placement by collectors despite instructions → collect at neglected locations; (2) gripper failures because operators close the gripper too fast → too few frames of the gripper action → instruct slower gripper closure.
Conflicts: consistent with "data diversity of initial positions matters" and ACT/DP roughly comparable at single-task scale.
Relevance: practical collection advice directly applicable to our SO-101 pumpkin demos at 10 fps: slow the gripper close/open (at 10 fps a fast close spans 1–2 frames), and deliberately randomize pumpkin/tray placement including edges. ACT reaching only ~31% on Franka with defaults warns that off-the-shelf configs on real data are mediocre.
Decision impact:
 - Q13 data quality: slow gripper actions + truly randomized placements; positioning errors dominate failures (up to 48%) — confidence M (large real eval, qualitative attribution).
 - Q13 data quantity: digital-twin sim data added to 100 real demos improves ACT; sim-only fails (10% real) — confidence L (one task, figure).
 - Q01 action head: ACT vs DP split by embodiment/task, no clear winner at single-task scale — confidence L.
