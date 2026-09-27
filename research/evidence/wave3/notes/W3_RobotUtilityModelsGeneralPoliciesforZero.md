# W3_RobotUtilityModelsGeneralPoliciesforZero — Robot Utility Models: General Policies for Zero-Shot Deployment in New Environments (RUM) (2024, arXiv 2409.05865)
Setup: Hello Robot Stretch with iPhone wrist camera (wrist-only observation; RGB); data from handheld Stick-v2 (iPhone ARKit pose); 5 tasks (door, drawer, reorient, tissue pick, bag pick); ~1,000 demos/task over ~40 environments (~25 demos/env; door 1,200, drawer 525). ResNet34 encoder initialized from HPR (home-pretrained) + transformer trunk; VQ-BeT final (3.75 Hz subsampled data, 6-frame history), actions = relative 6D EE pose + absolute gripper; 2×A100 24–48 h; runs on robot CPU. Eval: 25 unseen envs (5/task) × 10 trials; 2,950 real rollouts total.
Claim: with ~1k diverse, high-quality demos, a small policy generalizes zero-shot to new homes/objects (90% with mLLM retry); data matters more than algorithm.
Evidence: zero-shot success with retry 90% avg (84–94% per task); without retry 74.4%; GPT-4o retry adds +15.6 pts, 1.31 tries on average, 4.8% false-positive success judgments. Transfer to xArm 7 / different wrist cam (RealSense D405 supported): ~10% drop without retry (figure: e.g. 84→76, 80→70-ish; figure only).
Ablations (mostly figure-only, qualitative):
 - Algorithm: VQ-BeT ≈ DP (overlapping error bars); ACT and MLP-BC "not far behind" → algorithm not make-or-break with good data.
 - Data scale: DP better on smaller subsets, VQ-BeT overtakes at 900–1,200 demos; VQ-BeT still improving at max size.
 - Diversity (equal size): ~40 envs × 25 demos vs 5–6 envs × ~200 demos: door opening both fine; reorientation — concentrated data suffers ~50% drop.
 - Quality (~500 demos): expert > non-expert on all tasks; co-training expert + non-expert sometimes HURTS.
Failure/limitations: wrist-only framing makes test-time scene variation "look" similar; tasks are short single-skill; robot assumed placed facing the task; retry assumes errors leave scene in-distribution and cheap reset. Most ablation numbers are in figures.
Conflicts: Supports "data > algorithm" (agrees with ALOHA-Unleashed / DROID style claims) but contrasts with ACT paper where CVAE vs L1 mattered hugely — difference is scale/quality (1k curated demos vs 50 human sim demos). DP > VQ-BeT at small data agrees with diffusion/flow being the safer choice at our 50–100 demo scale.
Relevance: For SO-101 with 50–100 demos: (1) spread demos over many variations (pumpkin appearance, positions, lighting, backgrounds) rather than many repeats of one setup; (2) keep demos clean/consistent — mixing sloppy demos can hurt; (3) wrist camera + relative EE actions enabled cross-camera/cross-robot transfer with ~10% loss; (4) success detector + retry is a cheap +15 pts system-level fix.
Decision impact:
 - Q13 data: diversity > quantity (concentrated data −50% on reorientation); expert-only > mixed quality — confidence M (real, many rollouts, but figure-only numbers).
 - Q01 action head: DP better at small data, VQ-BeT at ~1k; ACT/MLP close — confidence L/M.
 - Q11 cameras: wrist-camera-only policy generalizes to unseen homes and transfers across wrist cameras/robots with ~10% drop — confidence M.
 - Q14 robustness: 90% in 25 unseen environments with ~40-env diverse data + retry — confidence M.
 - Q02 action space: relative EE 6D actions used for cross-embodiment transfer (no ablation) — confidence L.
