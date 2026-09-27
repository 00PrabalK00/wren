# W3_KnowingWhentoStopAdaptiveActionChunkingv — Knowing When to Stop: Adaptive Action Chunking via Internal Cross-Attention Dynamics in VLAs (2026, arXiv 2609.00908)
Setup: training-free inference rule on pi0.5 (Hp=50) and X-VLA (Hp=30). Sim: RoboTwin 2.0 (10 tasks, 50 Aloha-Agilex demos/task, pi0.5 fine-tuned 40k steps bs32; 3 seeds x 100 rollouts, clean mode) and LIBERO (public pi0.5 ckpt, Hp=10). Real: dual-arm ARX R5 + leader teleop, 2 wrist fisheye cams + head RGB cam, images 20 Hz, low-level control 60 Hz, 3 tasks (hang mug, stack cups, tidy pens), 50 demos/task, 20 trials per method per task. Latency measured on A100.
Claim: entropy of action-query->VLM-token cross-attention rises with index within a chunk and plateaus; truncating execution at the high-entropy plateau (k=5, tau=0.01, eta=0.95*ln N) beats every fixed execution horizon.
Evidence:
 - Offline: entropy vs per-step MSE Spearman rho=0.432 (partial r=0.214 after controlling for index); top-entropy quartile has 10.4x mean MSE of rest.
 - RoboTwin pi0.5 avg SR: fixed exec 10: 61.6, 15: 58.0, 20: 53.8, 25: 52.2; SA 57.6; MS 57.0; Ours 62.9 (avg executed length 18.11). Longer fixed horizons omitted "due to significantly degraded success".
 - RoboTwin X-VLA avg: fixed 15: 43.5, 20: 64.9, 25: 74.1, 30 (full): 76.1; Ours 79.0. (Opposite optimum from pi0.5: X-VLA prefers executing the whole chunk.)
 - LIBERO pi0.5 avg: fixed-2 93.00, -4 94.63, -6 94.88, -8 94.13, -10 94.75; Ours 97.25 (Long: best fixed 90.0 -> 94.5).
 - Real (20 trials/task, avg of 3): fixed exec 10: 45, 20: 46.7, 30: 51.7, 40: 46.7, 50: 41.7; SA 55; MS 18.3; Ours 61.7. Per task fixed optimum varies (tidy pens best at 20: 40%, worst at 50: 10%).
 - Latency per inference cycle (A100): fixed 0.2661 s, MS 0.2956, SA 0.2728, Ours 0.2725 (<7 ms overhead).
Ablations:
 - Execution horizon (fixed) swept: pi0.5 sim monotonic drop 61.6 -> 52.2 from 10 -> 25 steps; X-VLA monotonic rise 43.5 -> 76.1 from 15 -> 30; real pi0.5 inverted-U peaking at 30 steps (1.5 s at 20 Hz).
 - Multi-sampling uncertainty (MS) truncation produced very short chunks -> "intermittent pauses during movement" on real robot -> 18.3% (vs 41.7–51.7 fixed). Frequent re-planning without smoothing causes stop-go behaviour.
 - No ablation of k/tau/eta reported (one config for all, eta picked from the offline curve).
Failure/limitations: needs an explicit cross-attention path (flow/diffusion action expert over VLM tokens); not evaluated on WAMs. Critical read: gains over the best fixed horizon are small in sim (+1.3 pi0.5, +2.9 X-VLA, +2.4 LIBERO) and the real +10 pts rests on 20 trials x 3 tasks (~±11 pt CI per task); only fixed horizons, no temporal ensembling or RTC-style smoothing baseline; all synchronous execution; big models on A100 (0.27 s/chunk).
Conflicts: agrees with ACT/DP that the execution horizon matters a lot and has an interior optimum; shows the optimum is model- and task-specific (pi0.5 short, X-VLA full chunk), so "execute 8 of 16" style defaults do not transfer. MS failure echoes the chunk-boundary jerk problem: very short execution horizons without continuity constraints produce pauses.
Relevance: our jerk/latency problem is on SmolVLA (flow expert with cross-attention to VLM tokens) — this signal is computable for SmolVLA at ~zero cost, but it addresses *how many* steps to execute, not boundary discontinuity or 2 s latency. The main transferable lesson: sweep the execution horizon on the real robot (it moved real SR 41.7–51.7 with the same weights), expressed in seconds (~1–1.5 s best here at 20 Hz), and avoid very short horizons with async stop-go.
Decision impact:
 - Q06 chunking/execution horizon: supports tuning/adapting execution horizon per model and stage; fixed-horizon choice swings SR by ~10–30 pts — confidence M (sim 300 rollouts/config, real only 20 trials).
 - Q10 latency/smoothness: weakens very short re-planning horizons (MS short chunks -> pauses, 18.3% real) — confidence L (one baseline, qualitative cause).
