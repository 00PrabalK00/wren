# GPC — Generative Predictive Control: Flow Matching Policies for Dynamic, Difficult-to-Demonstrate Tasks (2025/26, arXiv 2502.13406, Caltech)
Setup: SIM ONLY, state-based. Shows sampling-based predictive control (SPC: MPPI / predictive sampling / CEM) update is a Monte-Carlo score estimate of a noised cost-weighted distribution; trains flow-matching action-sequence policies from SPC data in cycles (policy samples bootstrap next SPC round). Deployment: GPC (policy alone, receding horizon, warm-started) or GPC+ (policy samples seed SPC rollouts in a simulator — needs state estimate). Seven systems from pendulum to humanoid standup; 100 ten-second sims per point.
Key mechanism: warm-start the flow from the previous plan: U0 = (1−α)ε + α·Ū_{k−1}; α=1 starts from the previous (shifted) plan → temporal consistency / mode commitment.
Evidence (figure-only values):
 - Inference 1–10 ms → feedback at 100–1000 Hz.
 - Warm-start (α=0.5 or 1.0) beats no warm-start; action inpainting (RTC-style soft-mask guidance) DEGRADES performance at these high feedback rates — authors: inpainting is designed for slow tasks with significant inference delay.
 - GPC outperforms PPO in many cases; GPC+ meets or exceeds others on all tasks; plain GPC fails on humanoid standup (scalability limit).
Failure/limitations: no hardware; no images; needs a fast simulator with state for training and for GPC+.
Conflicts: RTC/Legato (fulltext notes) show inpainting helps under 0.1–0.3 s delays on real robots; GPC shows it hurts when inference is ~ms and replanning every step. Consistent picture: the continuation method should match the delay regime — inpainting for large delay, warm-start/short exec for tiny delay.
Relevance to SO-101: warm-starting a flow head from the previous chunk is a zero-cost trick if our small flow policy runs fast enough to re-plan every 1–2 steps; SPC with a simulator is not realistic for our camera-based pick-place (no calibrated sim).
Decision impact:
 - Sampling-based MPC with physics sim at runtime — NOT FEASIBLE for our vision-based setup — M.
 - Flow warm-start from previous plan when replanning at high rate — PLAUSIBLE — L (sim only).
