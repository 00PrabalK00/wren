# W4_FLASHEfficientVisuomotorPolicyviaSparseS — FLASH: Efficient Visuomotor Policy via Sparse Sampling (2026, arXiv 2605.15492)
Setup: Franka; 5 sim tasks (RLBench Close Box, ManiSkill Pick/Stack Cube with 100 demos; LIBERO Pick-Place Bowl, Open Drawer with 40 demos) + 2 real (Place Cube, Insert Cube mm-tolerance, few rollouts: 5 for timing). All methods share ResNet-18 (GroupNorm) encoder, obs horizon, batch, 10k optimizer steps; 50 rollouts per sim task. RTX 5090. Action = joint trajectory as Legendre polynomial coefficients (degree K=6) fit over sparse stride k=4, DiT flow head started from coefficients fitted to action HISTORY (not noise), 1 Euler step + consistency loss; C1 continuity (KKT) between chunks; analytic velocity feed-forward to 1 kHz torque controller.
Claim: polynomial-coefficient chunks + history-anchored one-step flow → higher success, ~30 ms total episode inference, smooth chunk transitions and lower tracking error.
Evidence:
 - Sim avg success FLASH 96.8% vs FLASH-G (same but from Gaussian noise, NFE 10) 79.2%; +4.8 pp over A2A-Noise (1-step, action-space history prior); ≥92% on all 5 tasks; ties ACT on Pick Cube (Table 1 flattened – per-cell values not reliably parseable).
 - Training speed: Pick Cube 96% at 2.5k steps vs ACT needing 10k for comparable; Stack Cube 98% at 6.25k steps vs VITA 72%.
 - Inference (sum over episode, Stack Cube): FLASH 31.4 ms; A2A 69 ms; FLASH-G 159 ms; Score-UNet 5476 ms. Per-call 0.32 ms at NFE 1.
 - Tracking: sim mean/peak tracking error 4.70x/3.18x lower than FM-DiT, whose error spikes at every chunk boundary; real MAE 0.274±0.004° vs FM-DiT 0.460±0.028° (5 rollouts). Real Insert Cube 100%, average +47 pp over 7 baselines (radar chart). Place Cube wall time 8.00±0.24 s fastest.
Ablations:
 - Stride k (Stack Cube): k=1 24% → k=4 96%; sweet spot k∈[3,8] ≥93%; k≥13 collapses (too little visual feedback / polynomial expressivity).
 - Fit padding + KKT C1 continuity (Close Box): neither 75.0% → padding 86.0% → both 97.5%.
 - NFE (Close Box, 2.5k ckpt): NFE1 80%, NFE2 54%, 4 56%, 6 68%, ≥10 86-94% (consistency loss specializes to 1 step; mid NFE worse).
 - Velocity feed-forward off: J7 tracking MAE 1.33° → 2.90°.
 - Post-hoc playback speed 0.5x–1.33x keeps ≥93% on Stack Cube.
Failure/limitations: fixed polynomial degree may not fit sharp contact-rich motions; constant speed per rollout. Critical: sim-heavy, scripted/sim demos, real tasks with few trials; training budget capped at 10k steps favours fast-converging methods; history-anchoring relies on action history (copycat risk not studied); torque-controlled Franka — SO-101 servos are position controlled so velocity feed-forward benefit won't transfer.
Conflicts: Stride k=1 (dense) failing at 24% echoes ACT's k=1 → 1% result (longer horizon matters). History-anchored generation conflicts with literature warning that proprio/action history causes copycat shortcuts in low data (they add noise to history to mitigate). Agrees with RTC/A2A line that chunk-boundary discontinuities are a major source of jerk; here solved by C1 continuity constraints rather than ensembling.
Relevance: Medium. Our jerky chunk boundaries + 2 s latency: a compact trajectory parameterization (polynomial/B-spline chunk, C1 matching to executed trajectory) + 1-step flow on ResNet-18 is cheap on 8 GB and addresses both. Upsampling a coefficient chunk also decouples 10 fps data from 30+ Hz servo commands. But evidence mostly sim.
Decision impact:
 - Q10 smoothness/latency: C1-continuous polynomial chunks remove boundary spikes (tracking err 4.7x lower than FM-DiT), 1-step inference 0.32 ms/call — confidence M (sim + small real).
 - Q01 action head: flow from informative prior (history) with 1 step beats Gaussian-start flow (96.8 vs 79.2) — supports history-anchored/1-step flow — confidence M.
 - Q06 chunking: sparse stride k 3-8 over horizon best; k=1 24%, k≥13 collapse — supports long-but-bounded horizon — confidence M.
 - Q02 action space: continuous trajectory (coefficient) representation + upsampling beats discrete absolute chunks for smoothness — confidence L-M.
