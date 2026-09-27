# W3_HermiteCurvesasTrajectoryPriorsforVision — Hermite Curves as Trajectory Priors for Vision-Language-Action Models (2026, IEEE TPAMI submission; arXiv id not in text)
Setup: pi-series backbones (pi0.5 ~3.3B flow matching, pi0-FAST AR), 8xH100, 30k steps, batch 256. Three variants: Hermite tokens (AR), Hermite scaffold + residual (flow), Hermite regularization = auxiliary 2-layer MLP head predicting K=2 cubic-Hermite boundary positions/velocities of the chunk, trajectory-space L2 loss, lambda=10, removed at inference. LIBERO (T=10, W=5), LIBERO-plus (10,030 perturbed instances), real: 4 three-stage tasks on Franka / Cybopal single & dual / ARX dual, 723-1,006 demos per task (3.2-6.3 h), 30 Hz EE control, chunk T=50, execute W=20, side/top + wrist cams, 15 rollouts per task.
Claim: treating the action chunk as a smooth curve (endpoint position+velocity) as a training-time inductive bias improves success and smoothness, with zero inference cost.
Evidence:
 - LIBERO avg: pi0.5 95.9 -> Reg 98.7 (LIBERO-10 91.4 -> 96.8); scaffold 97.7; pi0-FAST 85.5 -> Hermite tokens 95.4.
 - LIBERO-plus avg: 85.7 -> 90.9 (camera +13.4 [75.8->89.2], robot init +6.0, light +2.2, background +1.7). Scaffold variant 85.0 (worse than baseline on light/background/noise).
 - Real SR (Table 4, pi0-FAST / pi0.5 / tokens / scaffold / Reg): T1 60/86.7/80/86.7/100; T2 20/26.7/33.3/60/66.7; T3 40/46.7/46.7/80/93.3; T4 80/93.3/86.7/100/100; avg 50.0/63.4/61.7/81.7/90.0. Gain concentrated on precise placement stage.
 - Real seam discontinuity (median ||a_t - a_{t-1}|| at handover, W=20,T=50): Task 2 0.0056 -> 0.0040 (0.72x); Task 3 0.0059 -> 0.0028 (0.48x). Handover jumps are 5.5-8.6x larger than interior steps for all methods. Real jerk/accel RMS lower (p<1e-4); pi0.5 shows jitter right before grasp causing misses.
 - Latency (H100): pi0.5 48.4 ms, Reg 48.6, scaffold 49.4, Hermite tokens 28.9, pi0-FAST 238.2 ms; peak mem ~6.6-7.6 GB.
Ablations:
 - lambda 0/1/5/10/20: avg 95.9/97.4/98.2/98.7/97.5; median jerk 4.60e-4 -> 4.10e-4 at lambda=10.
 - K segments 1/2/3/4: 93.7/98.7/96.6/95.8 (K=2 best, lowest jerk).
 - Basis: global polynomial 96.7, Bernstein 96.9, B-spline 97.6, Hermite 98.7.
 - Scaffold supervision: theta-space LS 91.5, finite-diff 96.4, trajectory-space 96.2, +residual 97.7.
 - Failed rollouts are jerkier than successes for all variants (pi0.5 0.00046 vs 0.00070).
Failure/limitations: soft prior — narrows but does not eliminate seams; ignores vision side and non-smooth contact events. Critical read: sync execution only (no async/RTC comparison); 15 real rollouts per task; large models and ~800-1000 demos per task, not our 50-100 regime; real baseline pi0.5 unusually low on T2 (26.7).
Conflicts: Complements RTC/bidirectional-decoding/temporal-ensembling seam fixes (inference-time) with a training-time fix; agrees with ACT that jerky chunk boundaries hurt; LIBERO gains on saturated benchmark are small, the real gains are large.
Relevance: Directly targets our "jerky motion at chunk boundaries". The regularizer is a few lines (fixed linear basis + small MLP head), zero inference overhead, model-agnostic — easy to add to ACT/flow/diffusion training on SO-101 joint chunks (Dc=6 joints excluding gripper). Their real setup (30 Hz, T=50, W=20) also supports recording at 30 Hz and ~1.7 s chunks, executing ~0.7 s.
Decision impact:
 - Q10 smoothness at chunk boundaries: supports adding a trajectory-smoothness (Hermite) auxiliary loss — seams 0.48-0.72x, real SR 63.4 -> 90.0 — confidence M (4 real tasks x 15 trials, big model, big data).
 - Q09 auxiliary objectives: supports training-only trajectory-structure aux head over explicit output parameterization (Reg 98.7 > scaffold 97.7 on LIBERO; 90.0 vs 81.7 real) — M.
 - Q06 chunking: real setup T=50 / W=20 at 30 Hz; handover jumps 5.5-8.6x interior regardless of method — seams are inherent to chunked replanning — M.
 - Q01 action head: FAST AR decoding 238 ms vs flow 48 ms on H100; Hermite tokens 28.9 ms — L.
