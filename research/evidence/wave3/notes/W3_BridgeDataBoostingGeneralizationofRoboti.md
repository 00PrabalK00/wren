# W3_BridgeDataBoostingGeneralizationofRoboti — Bridge Data: Boosting Generalization of Robotic Skills with Cross-Domain Datasets (2021, arXiv 2109.13396)
Setup: WidowX250s (6-DoF, low-cost, ~US$3600 setup), VR teleop via IK (EE control). Bridge dataset 7,200 demos, 71 tasks, 10 toy-kitchen/sink domains; 3-5 cams (webcams + RealSense), kitchen position randomized 0-20 cm and camera pose 0-10 cm / 0-30 deg every 25 trajectories, distractors every 5. Policy: task-id conditioned BC, ResNet-34 + spatial softmax + 3 FC, L2 loss, single-step (no chunking), single image. Target: ~50 demos per task in a new domain. Eval: 10 trials/task, object positions/distractors changed every trial, robot-vs-scene pose changed every 5 trials.
Claim: jointly training on a diverse multi-task multi-domain dataset plus 50 target demos ~doubles success on new tasks in new domains.
Evidence (Fig. 7 averages):
 - Scenario 1 (task in bridge + 50 target demos): joint 66% vs target-domain-only (multi-task) 28% vs single-task 18% vs direct transfer 14%.
 - Scenario 2 (import task not demoed in target domain): joint 44% vs direct transfer 30%.
 - Scenario 3 (new task, 50 demos, not in bridge): joint ~50% vs single task ~22% (6/10 tasks improved).
 - Fig. 9 per-task (joint vs single): wipe plate w/ sponge 70/?; put pear in bowl gains; flip orange pot upright 50 vs 60 (no gain: orange pot unlike metal pots); open box flaps 10 vs 10 (pushing absent in prior); pick screwdriver 0 vs 0 (visually unlike). (Fig. 9 cell alignment partly garbled in text; treat per-task numbers as approximate.)
Ablations:
 - Joint training vs pretrain-then-finetune: pretraining "significantly less effective" (no numbers).
 - Reweighting: 70/30 bridge/target (10:1 size) and 90/10 (60:1); lower bridge ratios overfit with 50 target demos (stated, no numbers).
Failure/limitations: transfer only helps when objects look like prior objects, motions are present in prior data, and scenes resemble prior scenes. Critical read: single-step L2 BC baseline is weak (single-task 18-22%), so relative gains are amplified; 10 trials/task; same robot type across data; 2021 architecture.
Conflicts: consistent with later OXE/Octo/pi0 co-training results; single-task numbers at 50 demos are much lower than ACT/DP at 50 demos, reflecting the old single-step regression policy rather than data limits.
Relevance: Suggests co-training our 50-100 pumpkin demos with community SO-100/101 LeRobot datasets (same embodiment, varied lighting/cameras) could improve robustness to lighting/camera shift — but only if visual/behavioural similarity exists; weight target data ~10-30%. The dataset's deliberate camera-pose randomization is a cheap data-collection recipe for our camera-shift failure.
Decision impact:
 - Q13 data diversity: supports co-training with diverse same-embodiment prior data over target-only 50 demos (66 vs 28; 50 vs 22) — confidence M (real, many tasks, but weak policy class, 10 trials).
 - Q14 robustness: supports randomizing camera pose / scene position during collection and adding multi-domain data for generalization to unseen configurations — L/M (not isolated as ablation).
 - Q12/training recipe: joint co-training > pretrain-finetune for small target data — L (no numbers).
