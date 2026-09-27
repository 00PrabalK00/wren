# HiRobot — Hi Robot: Open-Ended Instruction Following with Hierarchical VLA Models (2025, arXiv 2502.19417, Physical Intelligence)
Setup: real only; 3 platforms (single-arm, dual-arm, dual-arm mobile); tasks table bussing, sandwich making, grocery shopping. High level = PaliGemma-3B VLM fine-tuned to output atomic language commands (+ verbal replies); low level = pi0 (PaliGemma-3B + flow-matching action expert). Demos segmented into 1–3 s skills; high-level training data augmented with VLM-generated synthetic user prompts/interjections. 20 trials per task per method, blind human evaluator; metrics Instruction Accuracy (IA) and Task Progress (TP).
Decision trigger: high level re-run "either when one second has elapsed, or when a new interaction with the user takes place" — authors "found a very simple strategy to work well"; completion detection mentioned only as a possible alternative.
Claim: a System-2 VLM emitting atomic commands to a System-1 VLA follows complex prompts and mid-task corrections better than flat VLA or GPT-4o as high level.
Evidence (all numbers figure-only except the text claim):
 - Hi Robot "averages over 40% higher instruction accuracy than GPT-4o"; beats flat pi0 on IA and TP in all 3 domains (Fig. 5).
 - Expert-human high level: low-level policy "executes nearly flawlessly" → failures stem from reasoning, not actuation.
 - GPT-4o high level loses state (commands new picks while gripper occupied); flat VLA "does not react to real-time feedback".
Ablations: (A) no synthetic data → ignores clarifications ("this is not trash"); (B) flat policy trained on same synthetic data < hierarchy (Fig. 8, figure-only).
Failure/limitations: two 3B models (no latency or GPU numbers reported); prompt engineering for synthetic data; high/low levels unaware of each other's capabilities (no feedback of low-level success to high level). Critical read: the hierarchy's benefit is about language/semantic steerability, NOT low-level reactivity to physical disturbances; no quantitative table in text.
Conflicts: consistent with RoboDual/GR00T that the slow level can run ~1 Hz; contrasts with StreamVLA/AsyncFastSlow which gate the slow level on completion rather than a fixed clock.
Relevance to SO-101: low. Our single pick-place task has no need for a semantic planner; the design lesson is the trigger rule (fixed ~1 s clock OR external event) which is trivial to copy for any slow module (e.g., a VLM success checker).
Decision impact:
 - Slow semantic layer for single-task SO-101: NOT NEEDED — M.
 - If a slow layer is added later (language, second object): re-query on fixed ~1 s clock + on events — supported by one real study — M.
