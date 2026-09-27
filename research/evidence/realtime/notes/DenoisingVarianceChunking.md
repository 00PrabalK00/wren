# DenoisingVarianceChunking (DVAC) — Denoising Tells When to Replan: Denoising-Variance Adaptive Chunking for Flow-Based Robot Policies (Feng et al., Jun 2026, arXiv 2606.03847)
Setup: training-free, test-time. For each future action index, compute the variance of the clean-action estimates x̂0 over the last L (=5 or 3) Euler denoising steps; execute the low-variance prefix and replan before the first high-variance action; threshold = α × rolling mean of local variance (α=2, window m=5), N_min..N_max bounds. Sim: LIBERO (π0.5 action horizon 10, fixed exec 5; π0; Qwen2.5-VL-π; Qwen3-VL-GR00T; 100 episodes/suite), RoboTwin (16 tasks, π0.5, H=50), CALVIN-5. Real: Cobot Magic, 3 D435i (2 wrist + head), 3 tasks × 50 demos, 30 trials per method, N_max=40, two A6000.
Evidence:
 - LIBERO π0.5 avg SR / avg replans: fixed-5 baseline 0.948 / 32.6 → DVAC 0.980 / 18.6 (−43%). Fixed-horizon sweep (Table 7): fixed-1…10 range 0.910–0.970 (fixed-7 0.970 best fixed) — DVAC beats the best fixed with fewer replans.
 - π0 (H=50) LIBERO: fixed-25 0.675, fixed-50 0.635, DVAC τ=1e-4 0.715, α=2 0.637 (gains depend on threshold).
 - RoboTwin 16 tasks: π0.5 0.359 → DVAC 0.416 (fixed τ 0.367–0.385). CALVIN-5 avg subtasks 0.587 → 0.628.
 - Real (Table 5, SR / time s / replans): place cube Fix15 0.800/39.63/25.7, Fix40 0.533/30.36/9.4, DVAC 0.867/34.25/12.5; stack cubes 0.700/67.53/42.6, 0.433/52.83/17.2, 0.767/56.04/24.1; test tubes 0.433/80.30/61.8, 0.233/60.30/26.5, 0.533/64.28/31.2.
 - Phase analysis: variance higher in contact/precision ("operating") phases than free motion across all LIBERO suites; executed-length vs phase correlation r < −0.27 (p<0.05).
Ablations: fixed numeric thresholds not transferable across tasks/backbones (e.g., Qwen2.5-VL-π τ=1e-4 0.835 vs α-adaptive 0.983); adaptive scaling stabilises. Episode-level: DVAC rescues 21 LIBERO failures, introduces 8.
Failure/limitations: variance can stay low before a grasp → long chunk executed near contact → failure (authors' case study); requires multi-step flow sampling (≥L steps) — incompatible with 1-step generators; synchronous execution only.
Conflicts: agrees with DEHP/BCP/KnowingWhenToStop that adaptive horizons beat fixed; long fixed execution (Fix40) loses 20–27 pts on real tasks — agrees with SmolVLA's n_exec ablation. Interacts with async: chunk truncation must still respect the inference delay.
Relevance: moderate-high: zero-cost signal for our SmolVLA flow expert (10 steps) — shorten execution near grasp/place automatically; the real-robot sweep with 50 demos (Fix15 vs Fix40) is a direct warning against executing long chunks open-loop.
Decision impact:
 - Q06 execution horizon: adaptive (denoising-variance) truncation > best fixed horizon with ~40% fewer replans — M (sim large N; real 30 trials × 3 tasks).
 - Q06: long open-loop execution (40 steps) costs 20–27 pts real SR vs 15 — M.
