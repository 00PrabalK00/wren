# W4_BreakingtheVisionActionShortcutLatentInt — Breaking the Vision–Action Shortcut: Latent Interface Training for Generalizable Robotics Foundation Models (2026, arXiv 2609.12641)
Setup: LIBERO (40 tasks, 50 rollouts/task) for ID, LIBERO-Plus (10,030 perturbed instances, 1 rollout each; 7 perturbation axes) zero-shot. Architectures: pi0.5, MolmoAct2, FAST-WAM, ImageWAM — all trained from pretrained BACKBONE with randomly-initialized action expert (no policy-pretrained checkpoints). Real: MolmoAct2, 3 tasks (Keep LEGOs, Wipe trash, Transfer egg), 100 demos/task, one multi-task policy; 25 ID rollouts/task, 10 per task per OOD condition. Flow matching action chunks. Robot/camera details for the real setup not given beyond "top camera" (Camera OOD = top camera only).
Claim: two-stage training — (1) action expert trained WITHOUT images, conditioned on language + state + terminal SE(3) EE pose of each chunk; (2) visual info enters only through K=100 latent tokens supervised (λ=0.3) to reconstruct that terminal pose — removes vision–action shortcuts and improves OOD robustness.
Evidence:
 - LIBERO ID avg (Base → LIT): pi0.5 87.75 → 91.80; MolmoAct2 93.50 → 94.10; FAST-WAM 97.60 → 98.10; ImageWAM 98.10 → 98.40.
 - LIBERO-Plus overall: pi0.5 68.97 → 79.67 (camera 58.29 → 80.30, sensor noise 79.89 → 91.94, lighting 82.40 → 90.11, language 52.15 → 71.50); MolmoAct2 63.62 → 71.92 (camera 39.40 → 48.41, noise 49.03 → 70.77, layout 55.90 → 71.61); FAST-WAM 51.44 → 60.63 (camera 16.40 → 43.83); ImageWAM 83.02 → 86.89. 26/28 cells improve, max drop −2.11.
 - Real (MolmoAct2, aggregated 3 tasks): ID 74.7 → 88.0; Lighting OOD 53.3 → 70.0; Camera OOD (top cam only) 30.0 → 46.7; Distractors 50.0 → 63.3. Transfer egg: ID 52 → 92, lighting 30 → 90, distractors 20 → 90. Wipe trash camera OOD 10 → 80. (per-task numbers from Fig. 6; 10 trials per OOD cell.)
Ablations (MolmoAct2, LIBERO-Plus overall; LIT 71.92, baseline 63.62):
 - no Stage 1 (random-init expert): 68.23 (−3.7).
 - no pose-reconstruction loss: 68.86 (−3.1); sensor noise 70.77 → 60.02, background 94.42 → 88.38.
 - allow direct visual access to action expert: 67.74 (−4.2) with same ID (94.25).
 - latent tokens only (no stage1, no pose): 65.70 (+2.1 over base) — a VLA-Adapter-style bottleneck alone helps little.
 - staged image-free pretraining only (LA4VLA-style): 65.46.
 - pose supervision added to baseline: 65.45.
 - Learning dynamics: Stage-2 action loss 0.025 @20k vs baseline 0.033 @30k at equal total budget.
Failure/limitations: authors: larger-scale real evaluation open. Critical: all results with big VLA/WAM backbones; real OOD trials 10 per task per condition; baselines trained without policy pretraining so absolute numbers below published; "Camera OOD" = dropping to the top camera only, i.e. camera configuration change, not a moved camera; requires EE pose (FK) for goal target — available for SO-101 via URDF.
Conflicts: consistent with causal-confusion/shortcut literature and with "bottleneck + auxiliary spatial target" ideas (object-centric / keypoint papers). Aux pose reconstruction ALONE gave only +1.8 — contrasts with papers claiming auxiliary objectives alone give large robustness gains; here the gain requires the restricted pathway + prior together.
Relevance: the recipe is architecture-agnostic and cheap in principle: for a small ACT/DP-style policy we could (a) predict chunk-terminal EE pose (or pumpkin/tray position) as an aux head from a bottleneck of a few tokens, (b) pretrain the action decoder conditioned on goal pose without images using our own demos. Directly targets our failures (lighting, camera shift, new-looking pumpkin). Unproven for small models / single-task / 50 demos.
Decision impact:
 - Q14 robustness: supports visual bottleneck + goal-pose supervision to cut shortcuts (real lighting 53→70, camera 30→47, distractors 50→63) — confidence M (4 architectures in sim, one in real, 10-trial OOD cells).
 - Q09 auxiliary objectives: pose-reconstruction aux helps only combined with restricted pathway (alone +1.8 pts) — M.
 - Q11 cameras: camera-configuration change remains the hardest shift even with LIT (46.7% real) — L.
 - Q13 data: 100 demos/task multi-task real regime; ID 88% with LIT — L.
