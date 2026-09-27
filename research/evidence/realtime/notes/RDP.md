# RDP — Reactive Diffusion Policy: Slow-Fast Visual-Tactile Policy Learning for Contact-Rich Manipulation (RSS 2025, arXiv 2503.02881)
Setup: real only; Flexiv Rizon arm(s), GelSight Mini / MCTac optical tactile or built-in joint torque ("Force"); RGB cams; TactAR AR teleop with tactile feedback (Quest 3). Tasks: Peeling (60 demos), Wiping (80), Bimanual Lifting (50); perturbations applied by evaluator before/after contact; ~10 trials per test variation (lifting stated). Slow = latent diffusion policy (CNN DP + FiLM) predicting a LATENT action chunk at 1–2 Hz; fast = Asymmetric Tokenizer decoder that decodes the latent chunk into actions every step conditioned on the latest tactile/force embedding (20–30 Hz; AT horizon 32 @ 24 Hz), actions interpolated to >500 Hz by robot controller. RTX 4090.
Latency (Table I): DP 120 ms; slow LDP 100 ms; fast AT < 1 ms.
Claim: keep chunking for multimodal/non-Markovian trajectory modeling, but close a fast inner loop on force/tactile inside the chunk.
Evidence (score; No perturb / Perturb before contact / Perturb after contact / All):
 - Peeling: DP 0.56/0.58/0.19/0.44; RDP (Force) 0.99/0.98/0.88/0.95; RDP GelSight/MCTac similar (0.98–1.00 unperturbed, 0.79–0.80 after-contact perturb).
 - Wiping: DP 0.75/0.70/0.25/0.57; DP+tactile emb 0.60/0.75/0.15/0.50; RDP GelSight 0.85/0.95/0.50/0.77; RDP Force 0.95/0.85/0.80/0.87.
 - Simply adding tactile to DP observations does NOT help (Q1) — reactivity needs the fast loop, not just the input.
Ablations:
 - Table V (Wiping, perturb after contact, grasp% / score): DP chunk 8: 100%/0.15; chunk 2: 20%/0.10 (small chunks break on non-Markovian pauses in demos); temporal ensembling τ=0.2/0.5/0.8: 30%/0.05, 0%/0.00, 100%/0.15; RDP 100%/0.50. → neither short chunks nor TE substitute for the slow-fast split.
 - Table VI (Peeling Force): only normal force 0.48; symmetric tokenizer 0.58; default 0.95.
 - Relative trajectory representation and latency matching (discard first actions covering inference+execution delay, as in UMI) both "essential" (Fig. 10, figure-only).
Failure/limitations: needs tactile/force sensors and TCP control; fast loop only reacts to tactile, not vision; ~10 trials per cell.
Conflicts: supports RTC/BID findings that temporal ensembling is fragile (very sensitive to τ). Agrees with Tube Diffusion Policy (W3) that a per-step feedback layer inside a chunk beats a pure chunk.
Relevance to SO-101: architecture pattern is directly relevant (slow chunk generator ~1–2 Hz + <1 ms fast decoder at control rate), and the model is small (DP-scale). But the fast signal must be something we have: Feetech servos report present position/load/current — a crude proxy, NOT tested in this paper. Visual fast signal (wrist cam) would need a cheap encoder. Latency matching (drop stale prefix) is a free, directly applicable trick.
Decision impact:
 - Latency matching (skip actions already "in the past" when a new chunk arrives) — SUPPORTED — M/H (also UMI).
 - Slow-fast latent chunk + fast feedback decoder — PROMISING — M (real, strong gains, but tactile-driven).
 - Short chunks / TE as reactivity fix — NOT SUPPORTED — M.
