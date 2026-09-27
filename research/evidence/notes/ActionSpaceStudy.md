# ActionSpaceStudy — Demystifying Action Space Design for Robotic Manipulation Policies (ICML 2026, arXiv 2602.23408)
Setup: 13,000+ real rollouts, 500+ models; single-arm AgileX PiPER (main; low-cost 6-DoF arm, similar class to SO-101), dual-arm AgileX, AIRBOT, RoboTwin-2.0 sim (10 tasks, 50 demos). Real: 4 tasks (touch cube, pick up cup, pick&place cup, bimanual cube transfer), 250 demos/task, 6×6 grid of initial positions for both data & eval, 3 trials × 10 rollouts. Base net: FiLM ResNet-18 + 6-layer transformer decoder; heads: MSE regression (ACT-like) and flow matching (DP-like); also π0 fine-tuning. 30 Hz, trained with k=60 (2 s) chunks.
Key findings:
 - Delta must be CHUNK-WISE (relative to robot state at chunk start, π0-style), NOT step-wise (relative to previous predicted step): chunk-wise > step-wise by ~10%+ average.
 - With chunk-wise delta, delta > absolute "consistently… across all platforms, task configurations, model variations" — but "albeit with marginal gains in certain settings".
 - Horizon couples with representation: absolute benefits from LONGER execution horizons; delta peaks at SHORTER horizons (drift sensitivity).
 - Joint space > task space in fixed-embodiment, more data/compute; task space better for cross-embodiment/transfer. Joint advantage grows with data/epochs (100 → 250 → 500 demos).
 - Delta risk: noise, latency, tracking errors accumulate → drift.
Resolution of the ACT/DP conflict: ACT's "delta degraded" and DP's "position > velocity" compare against STEP-WISE deltas/velocities (the legacy form). This study agrees step-wise is worse; its positive result is specifically for chunk-wise delta. So: chunk-wise delta (joint space) ≥ absolute, with shorter execution horizon.
Caveats for us: gains "marginal" in some settings; their data regime is 250 demos/task (we have ~50–100); SO-101 has notable tracking lag (low P gain 16, gravity sag ~6° wrist) — chunk-wise delta relative to follower state at chunk start will encode leader–follower offset; that is consistent at train and test, fine.
Decision impact:
 - action_space: joint-space, CHUNK-WISE delta (relative to follower state at chunk start) — SUPPORTED — M/H; keep absolute as ablation (cheap to switch).
 - execution horizon: shorter with delta (e.g., ~0.5 s) — SUPPORTED — M.
