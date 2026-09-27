# W3_FasterVisuomotorPolicyLearningonActionMa — Faster Visuomotor Policy Learning on Action Manifolds via Riemannian MeanFlow (RMFP) (2026, arXiv id not in text)
Setup: sim benchmarks: spherical LASA (7 demos/shape), spherical Push-T, Robomimic Tool Hang (state) and Transport (vision, 14-DoF), Franka Kitchen with EE pose on R3 x S3 x R2; sweeps of 1/2/5/10 network function evaluations (NFE) per chunk; batch sizes/epochs follow Ding et al. (RFMP). Real: I2RT YAM 6-DoF arm, Jetson Thor inference, external Orbbec + wrist D405 RGB-D @30 Hz, 60 real demos, qualitative only (no success rate).
Claim: learning the flow map (MeanFlow average velocity, semigroup consistency + flow-matching anchor) on the action manifold gives 1-step generation competitive with multi-step flow/diffusion.
Evidence (success/score at NFE=1 unless stated):
 - Spherical Push-T: RMF-v 78.5, RFM 67.9, RDP-x 73.1, RDP-eps 15.0; at NFE=10 best RMF 85.0 vs 83.9.
 - Franka Kitchen: RMF variants 34.9-41.7 vs best baseline RDP-x 23.7; NFE=10 48.9 vs 48.6 (ceiling same).
 - Tool Hang: RMF-v 64.0 at 1 NFE (= DP at 5 NFE, RFM at 10); RMF-v 76.0 at 2 NFE; DP 0.0 at 1 NFE, 74.0 at 10; RFM 60 (1-5 NFE) -> 64.
 - Transport (vision): flow-based arms 86-94 at all budgets; RFM 94.0 at 1 NFE; DP 0.0 at 1 NFE.
 - LASA DTW at 1 NFE: RMF-x1 0.022 vs RFM 0.090; smoother (lower jerk).
Ablations: velocity vs endpoint head (no consistent order; endpoint better in higher-dim action); hemisphere vs uniform quaternion prior worth ~5.7 pts at NFE=1 for velocity heads. Consistency objective "buys the low-budget regime, not a higher ceiling".
Failure/limitations: all quantitative results in sim with single benchmark seeds/eval counts not emphasized; real-world only a qualitative rollout; training costs 4 NFEs per gradient step.
Conflicts: Supports prior results that flow matching tolerates very few steps far better than DDPM-style diffusion (DP collapses to 0 at 1 NFE; FM at 1 NFE loses only ~4 pts on Tool Hang and none on Transport). Note that 1-step FM ~ conditional mean regression, yet still performs well on Robomimic — consistent with regression heads being adequate on low-multimodality data (vs ACT's CVAE ablation on multimodal human data).
Relevance: For our 8 GB laptop and latency problem: flow-matching heads with 1-2 steps (or MeanFlow-style consistency) are nearly free at inference; diffusion with DDPM noise-prediction must not be run at 1 step. Manifold machinery is unnecessary for SO-101 joint-space actions (Euclidean) — Robomimic results are the relevant ones.
Decision impact:
 - Q01 action head: supports flow matching (or MeanFlow) over DDPM-style diffusion when few steps are needed: DP 0.0 at 1 NFE vs FM 60-94 — M (sim, several benchmarks)
 - Q10 latency: 1-2 NFE flow/MeanFlow heads match 10-NFE quality (Tool Hang 76 at 2 NFE) — M
