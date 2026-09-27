# ActionControlNet (ACNet) — A Lightweight Delay-Aware Adapter for Smooth Asynchronous Control in VLA Models (Guo & Guo, Jun 2026, arXiv 2606.25985)
Setup: ControlNet-style side branch: the executed "delay action" suffix of the previous chunk (padded with learnable tokens) → small transformer encoder → residual injected into the LAST block of a mostly frozen flow action head (Evo-1 VLA, 8-layer DiT expert); backbone vision-language latent cached once per sample and reused over several sampled delays (cheap training). Kinetix (RTC protocol, d 0–4), Meta-World MT50 (H=50, e=25, d∈{0,5,10,15}, RTX 4080 SUPER), and REAL SO-ARM101: 50 training rollouts, 10 epochs, 2 tasks (cube into box, clean table with tabletop vacuum), 10 trials per task.
Evidence:
 - Kinetix (Table I, SR d=0/1/2/3/4; avg d>0; % params trained): Naive 0.89/0.74/0.69/0.55/0.46 (0.61; 0%); RTC 0.91/0.75/0.80/0.72/0.61 (0.72; 0%); Training-RTC 0.89/0.88/0.83/0.79/0.70 (0.80; 100%); ACNet 0.90/0.87/0.84/0.76/0.68 (0.79; ~20%).
 - Meta-World MT50 (Table II, SR d=0/5/10/15, avg, latency, Hz): Naive 0.80/0.71/0.70/0.70 (0.70, 73 ms, 13.6 Hz); RTC 0.79/0.72/0.72/0.71 (0.71, 159 ms, 6.28 Hz); Training-RTC 0.80/0.77/0.74/0.73 (0.74, 134 ms, 7.46 Hz); ACNet 0.81/0.76/0.74/0.73 (0.74, 91 ms, 11.0 Hz).
 - SO-ARM101 real (Table III): Naive async 9/10 cube-in-box, 8/10 clean table (17/20); ACNet 10/10, 10/10 (20/20). Qualitative: naive shows larger oscillations near chunk transitions.
 - Jerk plots (Meta-World, H=50, d=10): flatter jerk around handoffs (figure only).
 - Ablation: injecting only into the final block is best (Meta-World; numbers not extracted).
Failure/limitations: CONFOUNDED comparison — RTC/Training-RTC use π0-based implementations while ACNet uses Evo-1, so latency differences reflect backbones (authors acknowledge Evo-1's lower runtime). Real: 10 trials/task, only vs naive async, 17/20 vs 20/20 is not statistically separable. MT50 differences ≤0.05.
Conflicts: consistent with TT-RTC/REMAC that conditioning the action head on committed actions fixes handoff jitter; claims parity with full training-time RTC while training ~20% of params.
Relevance: HIGH (only paper found with SO-101 + 50 demos + async chunk-boundary evaluation). Shows the naive-async oscillation at chunk transitions we see on SO-101 is reproduced by others and removed by conditioning the head on the executed suffix. Adapter training on cached backbone features is cheap enough for an 8 GB laptop (not measured).
Decision impact:
 - Q10 async: condition the action head on the executed delay suffix (adapter or full TT-RTC) — SUPPORTED — M (sim + small SO-101 real).
 - Q10 cost: adapter ≈ full training-time RTC performance at ~20% trainable params — L/M (confounded backbones).
