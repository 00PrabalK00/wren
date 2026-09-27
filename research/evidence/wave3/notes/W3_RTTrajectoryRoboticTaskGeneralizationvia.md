# W3_RTTrajectoryRoboticTaskGeneralizationvia — RT-Trajectory: Robotic Task Generalization via Hindsight Trajectory Sketches (2023, arXiv 2311.01977)
Setup: Everyday Robots mobile manipulator; RT-1 architecture (EfficientNet-B3 ImageNet tokenizer, 6-frame history, discretized actions), trained on RT-1 dataset (~73K teleop demos, 542 tasks); conditioning = 2D (or 2.5D with height channel) end-effector trajectory sketch drawn on the head-camera image (hindsight-labelled from proprio + calibrated camera, color-coded time, grasp/release markers). Eval: 7 unseen skills, 64 trials total (human-drawn sketches).
Claim: coarse trajectory sketches as task conditioning generalize to new tasks/motions far better than language or goal images.
Evidence: unseen-skill success: RT-Trajectory 2.5D 67%, 2D 50% vs RT-1 (language) 16.7%, RT-2 11.1%, RT-1-Goal (goal image) 26%. From human video sketches: Pick 94% (2.5D) vs IK planner 42%; Fold towel 75% vs 25%. From LLM (code-as-policies) sketches: Pick 89% vs IK 83%; Open drawer 60% vs IK 71%.
Ablations: 2.5D (height) > 2D, esp. picking at unseen heights (Pick from Chair).
Failure/limitations: requires calibrated camera + sketch at test time; stationary arm assumption; large data regime; small number of trials per skill.
Conflicts: language conditioning only generalizes semantically, not to new motions — consistent with Anchor-Align's finding that BC-fine-tuned language grounding is weak.
Relevance: Low for our single/two-task SO-101 setup (we won't sketch trajectories at test time; 73K-demo regime). Only a weak point for Q08: when a second task is added, language alone will not induce new motions; each new behaviour needs its own demos.
Decision impact:
 - Q08 language conditioning: language-conditioned BC fails on unseen motions (16.7%) vs trajectory-conditioned (67%) — confidence L (large-data regime, different goal).
