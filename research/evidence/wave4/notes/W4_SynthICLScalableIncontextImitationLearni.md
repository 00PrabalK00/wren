# W4_SynthICLScalableIncontextImitationLearni — SynthICL: Scalable In-context Imitation Learning with Synthetic Data (2026, arXiv id not in text)
Setup: In-context IL: policy conditioned on 1 test-time demo (≤6 segmented multi-view context frames, no actions) + current segmented RGB (front + side + wrist), no proprio; frozen DINOv3 ViT-S/16+, spatio-temporal context encoder (8L), cross-attn state-context encoder (7L), ACT-style flow-matching action decoder (2L), horizon 8, delta EE (rotvec) + gripper, 10 Euler steps, temporal ensembling; aux subgoal-image MSE head (training only). Trained entirely on synthetic pseudo-demos (Isaac Sim, 3M trajs for real; PyBullet 100K for RLBench), with GraspNet grasps, lighting/camera/texture randomization, waypoint noise, color jitter. Eval: RLBench 12 unseen tasks × 100 rollouts; real Franka FR3, 16 unseen tasks × 20 rollouts; segmentation via SAM + Cutie.
Claim: RGB-only synthetic pseudo-demos + subgoal-image aux train a one-shot in-context policy that transfers zero-shot to real.
Evidence: Real avg: SynthICL 79.1%, w/o subgoal prediction 65.3%, Instant Policy (point cloud) 72.5%, ICRT 45.0%. RLBench avg: 75.0 / 72.2 (w/o SP) / IP 72.4 / ICRT 60.1. Appearance-disambiguation tasks (Stack Bowls/Cups) RGB >> point cloud (real Stack Bowls 20/20 vs IP 9/20).
Ablations:
 - Frozen DINOv3 75.0% vs LoRA-fine-tuned DINOv3 20.7% (sim) — shared encoder across very different views (wrist) degrades.
 - Cameras (sim): front+side+wrist 75.0; front+side (no wrist) 60.3; front+wrist 64.6. No wrist → poor grasp alignment; no side → depth/placement errors.
 - Execution (real Cube-in-Shape-Sorter, 20 trials): temporal ensembling 15/20 vs direct chunk exec H=1 12/20, H=2 13/20, H=4 13/20, H=8 11/20; direct = shakier near placement. Similar in sim.
 - Smaller model (dim 512→256, fewer layers) 75.0 → 64.8; only full model learns regrasp recovery.
 - Subgoal aux: +2.8 sim, +13.8 real, but hurts at small data (3K–10K trajs; figure only).
 - Data pipeline (real, figure only): without GraspNet grasps 9% / 11%; Isaac Sim vs PyBullet rendering +14%.
 - Spatio-temporal decomposed attention 75.0 vs full attention 63.4; separate vs joint subgoal decoder 75.0 vs 76.1.
 - Waypoint noise needed to prevent wrist-cam shortcut (gripper closes when wrist image matches context) — qualitative.
Failure/limitations: needs segmented RGB (background removed) — strong implicit background robustness; struggles with high precision/contact; targets far from external cams fail; collision. My read: 20 rollouts/task; ICIL setting differs from our single-task BC but ablations on encoder freezing, cameras, and temporal ensembling transfer.
Conflicts: Frozen > LoRA DINOv3 contradicts RayViT (this wave: full fine-tune of DINOv3 works) — difference: SynthICL trains on synthetic data then tests on real (fine-tuning overfits to sim appearance), and shares one encoder across views. Temporal ensembling beats direct chunk execution for precision — agrees with ACT; contradicts Diffusion-Policy-style "execute chunk open-loop". Excluding proprio improves generalization — agrees with Zhao et al. "Do you need proprioceptive states".
Relevance: Directly usable: (1) segmented-object RGB input as a robustness trick for lighting/background (needs SAM/Cutie at runtime — latency cost); (2) keep wrist cam (−15 pts without); (3) frozen DINOv3 small is enough and cheap on 8 GB; (4) temporal ensembling for smooth precise placement; (5) drop proprio to avoid shortcut.
Decision impact:
 - Q03 vision encoder: supports frozen DINOv3 ViT-S; LoRA fine-tuning of shared encoder collapsed (75 → 20.7) — confidence M (sim, synthetic-to-real setting)
 - Q11 cameras: wrist camera essential (75 vs 60.3 without); side view helps depth (64.6 without) — confidence M
 - Q06/Q10 chunking/smoothness: temporal ensembling 15/20 vs direct execution 11–13/20 real precision task — confidence L-M
 - Q09 aux objectives: subgoal-image prediction +13.8 real, but hurts in small-data regime — confidence M
 - Q05 augmentation/synthetic: RGB synthetic data with high-fidelity render + valid grasps transfers zero-shot; segmentation masks background — confidence M
 - Q12 model size: shrinking to 256-dim dropped 75 → 64.8 — confidence L
 - Q07 history/proprio: no proprio improves generalization (stated, no number) — confidence L
