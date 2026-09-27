# W3_BCZZeroShotTaskGeneralizationwithRobotic — BC-Z: Zero-Shot Task Generalization with Robotic Imitation Learning (2021, arXiv 2202.02005)
Setup: Everyday Robots mobile manipulators (multiple robots, 1–4 locations, 7 operators, 5 months), single head-mounted monocular RGB camera, 10 Hz VR teleop; 100 training tasks, 25,877 demos (11,108 expert + 14,769 HG-DAgger interventions) + 18,726 human videos; ResNet-18 torso + FiLM conditioned on 512-D frozen multilingual sentence embedding (or video embedding), MLP heads for delta XYZ / delta axis-angle / gripper, Huber loss; random crop, downsample, photometric augmentation; auxiliary open-loop prediction of the next 10 actions, execute 1 closed-loop. Eval on 29 held-out tasks.
Claim: large-scale, diverse, HG-DAgger-collected data + language FiLM conditioning gives zero-shot generalization to unseen task compositions.
Evidence:
 - Held-out tasks: language 32% overall (non-zero on 24/29, 44% avg on those); video conditioning 4%.
 - Table 3: training tasks one-hot 42%, language 40%, video 24% → language embedding is as good as one-hot; held-out performance bottlenecked by control layer.
 - Most common failures: "last-centimeter" errors (gripper not closing/releasing, near misses).
 - Single-task: bin emptying 3.4 picks/min (human 6.3); door opening 87% train / 94% held-out scenes.
Ablations (Table 4, "place bottle in ceramic bowl"):
 - Multi-task language 52%, multi-task one-hot 45%, single-task 1000 demos 5%, multi-task one-hot WITHOUT adaptive state-diff (N=1 step delta) 3%.
 - Same data budget: 100% manual 27% (1-task) / 23% (8-task) vs 50% manual + 50% HG-DAgger 53% / 47%.
 - Appendix sim: deterministic scene 37 demos → 97.2%; randomized object positions 40 demos → 56% single-task.
 - Action labels: cloning 10 Hz one-step deltas → tiny actions, dithering, drift (3%); target = state difference to a pose N>1 steps ahead chosen adaptively by motion magnitude.
Failure/limitations: enormous data regime (25k demos) vs ours; single camera, no wrist cam; closed-loop single-step execution; precise last-cm errors dominate; evaluation std given but trial counts per task small.
Conflicts: Supports the ACT/DP finding that single-step small-delta targets at low rate fit teleop noise; BC-Z's fix (look-ahead targets) is the same principle as action chunking / absolute targets. Single-task 1000 demos → 5% shows high environment variability kills sample efficiency — consistent with data-scaling papers that diversity needs many more demos; contrasts with ACT's 50 demos in a fixed scene.
Relevance: For SO-101 at 10 Hz: do NOT train on one-step deltas; use absolute joint targets or chunks spanning ≥1 s. HG-DAgger-style corrective interventions doubled success at equal data — directly applicable with leader/follower teleop (take over when policy drifts). Frozen sentence encoder + FiLM is enough for a 2-object language switch. Sim appendix number (37 demos → 97% fixed scene vs 56% randomized) calibrates our 50–100-demo expectation when the pumpkin position varies.
Decision impact:
 - Q02 action space: 1-step deltas at 10 Hz 3% vs adaptive multi-step state-diff 45% — weakens step-wise delta targets at low control rate — confidence M (single task, large data)
 - Q13 data: HG-DAgger 50/50 vs manual 100% at equal data: 27→53% (1-task), 23→47% (8-task); sim 37 demos fixed scene 97% vs 40 demos randomized 56% — supports adding intervention/recovery data and expecting variability to raise demo needs — confidence M
 - Q08 language: frozen multilingual sentence embedding + FiLM ≈ one-hot on train tasks (40 vs 42%) and enables 32% zero-shot — supports frozen text encoder + FiLM — confidence M
 - Q05 augmentation: used random crop + photometric augmentation throughout (no ablation) — ~ — confidence L
