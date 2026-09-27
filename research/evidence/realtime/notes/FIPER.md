# FIPER — Failure Prediction at Runtime for Generative Robot Policies (NeurIPS 2025, arXiv 2510.09459)
Setup: diffusion and flow-matching IL policies; sim Sorting, Stacking (Franka), PushT (Sentinel data); real Pretzel rope folding (Franka) and Push Chair (Sentinel data). Calibration/training on successful rollouts only: M=50 (sim), M=10 (real). 5 seeds.
Method: two scores, both conformally calibrated on successful rollouts: (i) RND-OE — random network distillation on the policy's own frozen observation embedding (novelty of what the policy "sees"); (ii) ACE — action-chunk entropy from a batch of sampled chunks. Scores aggregated over a SLIDING window (w≈5–25 steps); alarm only if BOTH exceed thresholds (AND).
Evidence:
 - Aggregate across 5 envs (Table 1): FIPER best timestep-wise accuracy TWA 0.65, accuracy 0.78, normalized detection time DT 0.30, overall TPR 0.92; individual RND-OE or ACE detect even earlier but with lower accuracy.
 - AND vs OR (Table 2): AND gives higher TWA/accuracy because far higher TNR (OR variants TNR 0.05–0.43) — needed to avoid alarms on benign OOD successes.
 - Sliding window vs cumulative (STAC-style): cumulative is more accurate but detects much later (length-driven); per-step score (w=1, as in FAIL-Detect logpZO) → very low TNR (flags most successes).
 - PCA-kmeans OOD baseline TNR 0.24 → novelty alone ≠ failure.
Ablations: window size, threshold type (CP constant / band / time-varying), operator.
Failure/limitations: separate RND model to train; runtime cost small in their envs (not quantified here), could grow with high-dim actions; real tests are 2 tasks.
Conflicts: argues against cumulative STAC (Sentinel) for EARLY warning, and against single-step thresholds (FAIL-Detect). Agrees with Sentinel that raw OOD/variance alone mis-fires.
Relevance to SO-101: Directly implementable with a small policy: reuse our policy's vision encoder embedding, train a tiny RND predictor on successful-run embeddings, sample a batch of chunks for entropy; calibrate on ~10 successful rollouts. Useful as a "stop/retry/ask-human" trigger rather than a re-plan trigger.
Decision impact:
 - Failure monitor = obs-novelty (RND on policy embedding) AND action entropy, windowed, conformal thresholds — SUPPORTED — M.
