# W3_TaskAnchorGroundingTaskStateinReactiveVL — TaskAnchor: Grounding Task State in Reactive VLAs for Long-Horizon Manipulation (2026, arXiv 2609.23580)
Setup: SIM benchmarks only in the extracted text (abstract mentions real robots but no real-robot numbers/section appear in the text). Adapter (27.8M trainable) on pi0.5 (3.3B) and X-VLA: history-conditioned visual residual (test-time-training fast-weight memory over past frames) + milestone-supervised scalar "task-state coordinate" (fraction of milestones done) serialized into the language prompt. RMBench M(1): 5 memory-dependent bimanual tasks, 550 episodes jointly (baselines 50/task), 20-action chunks, execute 10, 100 seeds/task. RoboMemArena: 26 long tasks (~1076 steps), 100 demos/task.
Claim: Reactive VLAs fail on "task-state aliasing" (same observation, different stage); cheap history + stage-coordinate conditioning fixes much of it at +2 ms latency.
Evidence:
 - RMBench avg SR: DP/ACT/pi0.5/X-VLA roughly 0.06–0.14 (pi0.5 0.14, X-VLA 0.12), Mem-0 0.53, TaskAnchor-pi0.5 0.68, TaskAnchor-XVLA 0.66 (system-level; different training data volumes).
 - RoboMemArena avg TSR/CSR: pi0.5 21.5/38.7; PrediMem 38.5/55.2; TaskAnchor-pi0.5 44.4/60.5.
 - Latency per chunk: 62.00 → 64.08 ms (+3.35%).
Ablations (RMBench, same data/seeds): coordinate only 0.31; history-visual only 0.18; both 0.68. Coordinate only solves Swap Blocks (0.92) but not Swap T (0.09); history visual gives Swap T 0.16; both 0.24.
Failure/limitations: needs milestone annotations (or pseudo-milestones); comparisons to baselines are confounded by 11x more training episodes; sim only in text; 3.3B backbone irrelevant to 8 GB budget.
Conflicts: Agrees with the view that history helps only when the task is genuinely non-Markovian (aliased states); for Markovian short tasks, prior work (copycat/causal confusion, DP obs-horizon ablations) finds history can hurt. Consistent with SeedPolicy: structured/recurrent state beats naive frame stacking.
Relevance: Low for pumpkin pick-and-place (single-stage, Markovian: gripper state + scene disambiguate stage). Becomes relevant only if we add multi-step or "put back" style tasks. The stage-coordinate idea (predict progress scalar, feed as conditioning) is cheap and could help if the policy hesitates between reach and place phases.
Decision impact:
 - Q07 history/memory: history + explicit stage signal gives large gains only on memory-dependent tasks (0.14→0.68); either alone is weak (0.18/0.31) — supports "add structured task-state only if task is aliased; don't naively stack frames" — confidence L (sim, confounded, irrelevant task type for us).
 - Q10 latency: adapter cost negligible (+2 ms on 62 ms) — confidence L.
