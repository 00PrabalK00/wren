# AAC — Adaptive Action Chunking at Inference-time for Vision-Language-Action Models (2026, arXiv 2604.04161)
Setup: training-free, on GR00T N1.5 (flow DiT head) and pi0.5. Sample N candidate chunks in parallel (default N=20); per-step Gaussian differential entropy for translation/rotation + Bernoulli entropy for gripper; choose executed chunk size h* at the maximum differential point of average entropy vs h, subject to a minimum action magnitude (gripper change counts). Sim RoboCasa, LIBERO, LIBERO-Pro (position perturbations). Real: Realman single arm + Mycobot gripper, wrist + side RGB, 50 SpaceMouse demos per task, 3 tasks (banana pick-place, emergency button, toy-to-drawer + close); trials implied 20/task (5% granularity).
Claim: high entropy → execute fewer actions and re-plan sooner; low entropy → longer commitment.
Evidence:
 - Real (Table 5): GR00T vs GR00T+AAC: Banana 70 → 90; Button 65 → 75; Drawer 65 → 80; avg 67 → 82.
 - LIBERO with pi0.5 (Table 2): 97.0 → 97.9 avg. LIBERO-Pro perturbation (Table 3): pi0.5 30.9 → 34.8 avg; GR00T 3.9 → 6.3.
 - Samples vs cost (Table 4, A800): N=1 94.1% @83.0 ms; 5: 94.7 @83.5; 10: 94.4 @84.3; 20: 95.0 @106.0; 30: 95.0 @136.5; 40: 95.5 @157.0 — N≤10 nearly free, N=20 adds ~20 ms.
 - Chunk sizes chosen follow task phases: long in free transit, short near contact (figure).
Ablations: number of samples (above); fixed chunk sizes vary widely per task (Fig. 1).
Failure/limitations: needs stochastic generative head; gains in sim small (~1 pt); real trials small; no stop-go issue reported, unlike Knowing-When-to-Stop's multi-sample baseline (W3) that paused on a real robot.
Conflicts: BCP (W3) found entropy triggers "marginal gains, higher runtime"; Knowing-When-to-Stop (W3) found multi-sample truncation gave stop-go pauses (18.3%). AAC's minimum-magnitude constraint may be what avoids tiny chunks. HiPolicy supports entropy-gated execution.
Relevance to SO-101: feasible for a small flow head (batching N≤10 is near free). Real evidence: 50 demos/task, single arm — close to our regime. Must enforce a minimum executed length or smooth continuation to avoid stop-go.
Decision impact:
 - Entropy-adaptive execution horizon with min-length guard — PROMISING — M (real +15 pts avg, conflicting W3 evidence).
