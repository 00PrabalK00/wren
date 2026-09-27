# W3_ChicGraspImitationLearningbasedCustomize — ChicGrasp: Imitation-Learning based Customized Dual-Jaw Gripper Control for Delicate, Irregular Bio-products Manipulation (2025, arXiv n/a in text)
Setup: UR10e + custom pneumatic dual-jaw gripper with eye-in-hand camera; 3× RealSense D435 RGB 640×480 @30 Hz (RGB only) + proprio; 50 SpaceMouse teleop demos (25–40 s each, varied carcass pose and lighting); action = xyz velocity + 2 binary jaw bits (5-DoF); Diffusion Policy (A100 80 GB, batch 32), IBC, LSTM-GMM, 600 epochs each; 3 chicken exemplars, ~50 pick trials per method (DP: 101 tries logged). Learned grasp → scripted rehang.
Claim: Diffusion Policy trained on 50 multi-view demos can grasp/lift raw carcasses; IBC and LSTM-GMM fail.
Evidence (Table I): DP 40.6% (41/101) grasp-and-lift, per-exemplar 25.3% (14/55) to 64.5% (20/31), ~38 s cycle; IBC 0% (erratic, fails to commit to a trajectory, times out ~60 s); LSTM-GMM 0% (smooth approach but never actuates jaws at the right position).
Ablations: none beyond the 3-way head comparison (no camera/history/horizon ablations).
Failure/limitations: most failures at pick stage; DP often stops slightly below the ideal grasp height; only 50 demos; slow (38 s vs human <2 s). My read: success counted per try, not per episode; baselines with default hyperparameters; binary gripper events are rare → LSTM-GMM failing to trigger gripper is a classic imbalance issue.
Conflicts: consistent with Diffusion Policy paper (DP ≫ IBC, LSTM-GMM on real tasks); binary-gripper-timing failure of GMM is an instance of the "gripper event underfitting" problem.
Relevance: moderate-low: 50-demo regime and multi-view + wrist cam matches ours; deformable irregular object, industrial arm. Gives one more real data point that a generative chunked head beats energy-based and GMM heads in 50-demo real data.
Decision impact:
 - Q01 action head: real 50-demo task: diffusion 40.6% vs IBC 0% vs LSTM-GMM 0% — supports diffusion over IBC/GMM — confidence M (single task, un-tuned baselines).
 - Q13 data: 50 demos gives only 25–65% on variable deformable objects; authors cite data diversity as main limit — confidence L.
