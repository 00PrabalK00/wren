# W3_DynamicExecutionHorizonPredictionforChun — Dynamic Execution Horizon Prediction for Chunk-based Robot Policies (DEHP) (2026, arXiv n/a in text)
Setup: SIM ONLY, STATE-based Diffusion Policy base (prediction horizon 16 in IsaacLab tasks), frozen; categorical horizon head h ∈ {1..H} conditioned on state + predicted chunk, trained with chunk-level PPO (distributional critic). Tasks: IsaacLab 3-stage peg insertion (2/4/6 mm clearance), bimanual needle–syringe insertion, FurnitureBench one-leg and round-table; 1,000 scripted demos with injected action noise; 1,000 envs × 3 seeds eval.
Claim: learned, state-dependent execution horizon beats the best tuned fixed horizon; it picks short horizons (≈1) in precision/contact phases and long ones in free space.
Evidence:
 - Fixed-horizon sweep (peg insertion, figure only): at low action noise executing 6 of 16 is best and success declines as execution horizon grows; at noise 0.15, executing 2 beats 6.
 - Table 1 (overall success, fixed-6 BC → DEHP): noise 0.00: 71.50 → 93.17; noise 0.05: 65.60 → 88.47 (Stage 1, tightest: 77.90 → 96.57 and 74.53 → 93.90). Average gain +23.03 pts across noise levels.
 - FurnitureBench one-leg: best fixed (24 actions/chunk) 70.30% → DEHP 95.18%; round-table low rand 29.90 → >93.80%; medium 18.50 → 53.03%. Needle–syringe: best fixed 10.20 → 29.00%.
 - Data scale 300/500/700/1000 demos: DEHP > all fixed horizons at every size (figure only).
Ablations: the horizon sweep itself; best fixed horizon differs by task (one-leg vs round-table) despite same controller.
Failure/limitations: state-based sim only, scripted demos; online RL required (thousands of env rollouts) — not feasible on our real SO-101 without sim; base policy capacity bounds gains.
Conflicts: agrees with BCP (W3_ContinueorReplan...) that stage-dependent replanning helps; slightly contrasts on whether fixed shorter horizons help — here shorter is better under noise (DEHP sweep), in BCP (VLA, RoboTwin) fixed 20/30/40 gave no gain over 50. Both agree optimal fixed horizon is task-dependent. Consistent with Diffusion Policy's choice of executing 8 of 16.
Relevance: moderate as design guidance: SO-101 has backlash/jitter ≈ "action noise" → favors shorter execution horizons (more frequent replanning) especially around grasp; a heuristic schedule (short near object/gripper events, long in transit) is a cheap approximation. Requires fast inference to replan often.
Decision impact:
 - Q06 execution horizon: under action/execution noise shorter execution (2 vs 6 of 16) is better; adaptive horizons +23 pts over best fixed (sim) — supports short execution horizon near contact + adaptive schedule — confidence M (sim, state-based, strong effect).
 - Q10 latency: benefit relies on cheap re-planning (h≈1 during insertion) — supports small fast policies enabling frequent replans — confidence L (inferred).
