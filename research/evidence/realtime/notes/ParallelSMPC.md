# ParallelSMPC — Real-World Deployment of Massively Parallel Sampling-Based MPC for Contact-Rich Manipulation (2026, arXiv 2606.20712, TU Darmstadt)
Setup: JAX + MuJoCo MJX sampling MPC (MPPI, CEM, Predictive Sampling, Model Tensor Planning (MTP) with global structured samples). Real Franka Research 3 pushing a 3D-printed T (Push-T), object pose from OptiTrack mocap @100 Hz; planner on RTX 5090 at 8–10 Hz with 1024 samples; MoveIt2 Servo streams Cartesian velocity at 1 kHz and a control node picks the current horizon step at 50 Hz (servo interpolates within the published trajectory by elapsed time). Real eval: 6 seeds with small initial variations.
Evidence:
 - Sim Push-T (256 samples, 20 Hz): MTP lowest final pose error for long and short horizons; unimodal MPPI/CEM/PS get stuck in local minima (figure). Bugtrap: MTP escapes in all seeds.
 - Real: MTP lowest final pose error and variance (figure only).
 - Compute bottleneck: MJX physics dominates; integration steps > 0.025 s go unstable (deep penetration), forcing coarse steps and short horizons — "fundamental tension" between stable small timesteps and long horizons.
 - Online domain randomization (8 domains × 160 samples, 5 Hz): mass/friction gave no stable adaptation signal.
Failure/limitations: requires mocap state and a hand-built sim model of object; short paper, 6 seeds, figure-only results; RTX 5090 needed for 8–10 Hz.
Conflicts: shows the architecture used by learned systems too — slow planner (8–10 Hz) + time-indexed interpolation at the servo layer (50 Hz / 1 kHz) — same cascade as pi0-style chunk execution.
Relevance to SO-101: sampling MPC with physics is not feasible on 8 GB laptop GPU for a vision-only pumpkin pick (no object state, no mocap). The transferable part is the cascade: decouple planner publishing timed trajectories from a high-rate interpolating executor.
Decision impact:
 - Runtime physics-sampling MPC — INFEASIBLE for us — M/H.
 - Time-indexed trajectory publishing + interpolating executor — SUPPORTED as standard practice — M.
