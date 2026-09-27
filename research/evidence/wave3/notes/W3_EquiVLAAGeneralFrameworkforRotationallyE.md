# W3_EquiVLAAGeneralFrameworkforRotationallyE — EquiVLA: A General Framework for Rotationally Equivariant Vision-Language-Action Models (2026, arXiv 2606.19784)
Setup: GR00T N1.5 (frozen VLM) + flow-matching DiT action head. EquiPerceptor: frame-averaging over C8 rotations of frozen ViT tokens (8 ViT passes); EquiActor: exactly SO(2)-equivariant steerable DiT (trained from scratch). LIBERO 4 suites (~40 demos/task, 50 rollouts/task, 2 seeds; both relative and absolute EE control), CALVIN ABCD→D (1000 chains), real Mobile ALOHA 5 tasks x 150 demos, 20 trials/task. Latency on H100: GR00T 64 ms/step, +EquiActor 147, EquiVLA(C8) 194 ms.
Claim: Injecting SO(2) equivariance into the perception adapter and action head of a pretrained VLA improves rotational generalization and data efficiency.
Evidence:
 - LIBERO relative control avg: GR00T N1.5 78.1; +EquiActor 91.0; EquiVLA 92.6 (pi0 published 86.0, SmolVLA published 65.6).
 - LIBERO absolute control avg: GR00T 62.6; +EquiActor 73.6; EquiVLA 76.1.
 - CALVIN avg len: 3.45 → 3.89 → 4.03.
 - Real ALOHA (/20, EquiVLA vs GR00T): Banana in Pot 15 vs 12; Block Storing 11 vs 9; House Building 10 vs 3; Letter Aligning 19 vs 13; Shorts Folding 17 vs 17; avg 72% vs 54%.
Ablations:
 - Data budget (LIBERO, 10% / 40% / 100% demos): GR00T 58.4/73.9/78.1; +EquiActor 58.8/84.1/91.0; EquiVLA 60.2/84.5/92.6.
 - Group size: C4 91.6 (161 ms), C8 92.6 (194 ms), C16 94.3 (243 ms).
 - Equivariance error: 7.75 → 0.84 (EquiActor) → 0.28 (full).
 - Control mode (not the paper's focus but controlled): relative EE control beats absolute EE by ~15 pts for every variant (78.1 vs 62.6; 92.6 vs 76.1).
Failure/limitations: SO(2) assumes a top-down-ish camera and planar rotation; the equivariant action head cannot reuse pretrained weights; 3x latency; equivariance only approximate from frozen ViT features; a lot of the gain may come from a better (from-scratch) action head rather than equivariance per se (EquiActor alone gives most of it; no non-equivariant from-scratch DiT control).
Conflicts: Relative > absolute EE on LIBERO agrees with ActionSpaceStudy 2026 (delta better) and conflicts with ACT's un-quantified claim that absolute joint targets are better on leader/follower rigs — note this is EE-space in sim with a large pretrained VLA, different from joint-space SO-101. Equivariance helping most with more data (gap widens 1.8 → 14.5) is the opposite of the usual "priors matter most in low data" claim.
Relevance: SO(2) equivariance is poorly matched to our oblique RealSense scene cam; the 3x ViT passes would hurt latency on the laptop. Main transferable signal is the action-space comparison (relative/delta EE > absolute) and a data point that a large frozen VLM + trained action head reaches only 54% real at 150 demos without extra priors.
Decision impact:
 - Q02 action space: relative EE control > absolute EE by ~13–16 pts across 3 model variants (LIBERO) — supports delta/relative actions — confidence M (sim, EE-space, controlled within paper).
 - Q14 robustness (object orientation): equivariant priors raise orientation-varied real tasks (House 3→10, Letter 13→19 /20) — supports rotational priors/augmentation for orientation variation — confidence L (20 trials, big VLA).
 - Q10 latency: frame averaging costs 3x inference (64→194 ms H100) — weakens heavy test-time symmetrization on laptop — confidence M.
