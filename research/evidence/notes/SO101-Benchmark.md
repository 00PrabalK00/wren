# SO101-Benchmark — Benchmarking VLAs on SO-101: Failure and Recovery Analysis (2026, arXiv 2606.08881)
Setup: SO-101 (our exact arm); 4 tasks (Pen Transfer, Selective Color Sorting, Multi-object Packing, Precision Pen Placement); 100 teleop demos/task with randomized poses/layouts; 20 real trials per model-task (320 total); policies fine-tuned with their own recipes: π0.5, SmolVLA, Wall-X, ACT. Datasets public.
Evidence: success avg ACT 33.75, SmolVLA 32.5, Wall-X 51.25, π0.5 56.25. Pen Transfer (simple pick-place) 70–95% for all; Color Sorting 0–10% for all. Failure taxonomy: grasp instability, repetition loop, state mismatch, precision misalignment. Execution-related failures (grasp instability + loops) dominate for ALL models; ACT also high state mismatch (continues after failed grasp); π0.5 lowest state mismatch. Recovery rate: π0.5 30.8%, Wall-X 20.5%, ACT 6.5%, SmolVLA 3.2%.
Hardware notes (from paper): SO-101 has actuator noise, joint backlash, control latency, trajectory jitter, limited repeatability, imperfect vision-action calibration → execution errors accumulate.
Limitations: 20 trials per cell (wide CIs); no hyperparameter parity guaranteed; no OOD tests.
Relevance: HIGH. Our pumpkin pick-place resembles Pen Transfer (all methods 70–95% in-dist) → in-distribution success is not the hard part; robustness + recovery + grasp stability are. Implications for us:
 - Grasp instability: LeRobot's SO follower config caps gripper torque at 50% (Max_Torque_Limit 500, Protection_Current 250) — hardware/config lever to test.
 - State mismatch / no recovery: small policies rarely recover → include recovery demonstrations (deliberate failed-grasp-then-regrasp episodes) in data; a gripper-state/progress signal may help.
 - Repetition loops: possibly aided by short history or progress token (contradicts BAKU's no-history finding in sim) — open question; test cheaply.
Decision impact:
 - evaluation protocol: ≥20 trials/condition, failure taxonomy + recovery rate — ADOPT — H.
 - data: add recovery demos — SUPPORTED (inferred from recovery gap) — L/M.
 - small from-scratch vs VLA: ACT ≈ SmolVLA on SO-101; bigger pretrained (π0.5, 3B) wins but doesn't fit our GPU — M.
