# W3_LearningVisualRoboticControlEfficientlyw — Learning Visual Robotic Control Efficiently with Contrastive Pre-training and Data Augmentation (CoDER / FERM) (2020, arXiv 2012.07975)
Setup: real xArm7, 6 short tasks (reach, pickup, move, pull, light switch, drawer), 2 RGB cams (RealSense over-shoulder + in-gripper Arducam), 100×100 crops; 10 joystick demos/task seeded into replay buffer; contrastive (CURL-style, random-crop) encoder pretraining on demo frames (<1 min on 2080Ti), then online SAC with random-crop augmentation and sparse reward; 15–50 min of real RL per task; 30 evaluation episodes.
Claim: demos + contrastive pretraining + augmentation make pixel RL on a real arm train in ~30 minutes.
Evidence: final success /30: reach 30, pickup 30, move 26, pull 28 (+ switch/drawer reported as perfect in caption); avg 96%. BC on the same 10 demos only succeeds on the easiest tasks (reach, switch) — figure only.
Ablations (figure only): 0 demos → no learning, 1 demo starts learning, 10 sufficient (sim pick-place); no contrastive pretraining → real move task essentially fails (1 success in an hour); no random-crop aug → SAC fails even on dense-reward FetchReach.
Failure/limitations: online RL with resets; short-horizon tasks; authors expect degradation under lighting/background change; no robustness tests.
Relevance: very low for our BC pipeline (no online RL planned). Only takeaways: random-crop augmentation is essential for pixel policies with little data; 10 demos are not enough for pure BC on non-trivial tasks. Note setup parallels ours (over-shoulder RealSense + gripper cam).
Decision impact:
 - Q05 augmentation: supports random-crop augmentation as essential in low-data pixel learning (no-aug RL fails) — confidence L (RL not BC, figure only).
 - Q13 data quantity: plain BC with 10 demos fails on move/pull/pickup-class tasks — confidence L (figure only, simple CNN BC).
