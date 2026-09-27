# W3_MultistageCableRoutingThroughHierarchica — Multi-Stage Cable Routing through Hierarchical Imitation Learning (2023, arXiv 2307.08927)
Setup: real Franka Panda; 2 Basler wrist cameras + side and top RealSense; low-level single-clip insertion policy trained on 1,442 teleop trajectories (<10 s each; ~800 successful + ~600 deliberate failure-then-recovery demos) collected at 5 Hz with a 3D mouse; action = 4-D Cartesian twist in the gripper frame; policy = ResNet18 (GroupNorm) per wrist cam + z-height -> MLP -> Gaussian; RandAugment (2 ops, magnitude 9). The high-level primitive selector uses wrist + side cams + a history of up to 6 primitives. Eval: 25 easy + 25 hard trials (low-level); 24 trials (full task).
Claim: learned primitives + a learned high-level selector with recovery beat flat BC/BeT/ACT and scripted state machines on multi-clip routing.
Evidence:
 - Low-level (Table I): learned 23/50 (18/25 easy, 5/25 hard) vs scripted waypoint policy with privileged clip pose 10/50.
 - Full task (Table IV, 24 trials): hierarchical ours 12/24; state machine 5/24; flat end-to-end BC 0/24; BeT 0/24; ACT 0/24 (ACT smoother but misses clip / drops cable).
 - Clips (Table III): 1 clip 19/24, 2 clips 14/24, 3 clips 12/24.
Ablations (low-level, Table II; full = 23/50):
 - No image augmentation -> 11/50 (easy 9/25, hard 2/25).
 - Side (external) camera instead of wrist cameras -> 6/50.
 - No correction/recovery demos -> 18/50 (failures = missing the clip and never lifting to retry).
 - Separate (non-shared) ResNet per wrist cam -> 21/50 (no real difference).
 - High-level without primitive history -> 0/24 vs 12/24 (Table V; it loops on go_next).
 - Interactive fine-tuning with 10 extra demos per config: in-distribution 20/40 -> 34/40; OOD 3-clip 6/30 -> 15/30; unseen 4-clip 0/10 -> 2/10 (Table VI).
Failure/limitations: >95% of full-task failures are the high-level policy declaring success when the cable sits just behind the clip, a perception ambiguity that the authors suggest better camera placement could fix. Low-level policy is Markovian and single-frame. Trial counts are modest (25–50). The ACT/BeT baselines were trained on long-horizon data that is much harder than a single pick-place.
Conflicts: agrees with ACT/DP literature on the value of wrist cameras and augmentation. ACT at 0/24 here is a long-horizon multi-stage failure, not a contradiction for short tasks. "History essential" applies to a high-level primitive selector with a visually ambiguous state, not to low-level control (the low-level policy is memoryless and works).
Relevance: high for our augmentation/wrist-cam/recovery-data choices. The single-clip policy is a small ResNet18 BC policy with wrist cams, which is close to what fits our 8 GB GPU. Wrist-frame actions + wrist cams made the skill invariant to clip placement. Strong photometric/geometric augmentation doubled success. Deliberate recovery demos (~40% of data) added ~+10 pts.
Decision impact:
 - Q05 augmentation: + strong RandAugment (photometric+geometric) doubles success 11/50 -> 23/50 — confidence H (clean real ablation)
 - Q11 cameras: + wrist cameras over external view (23/50 vs 6/50) for a local precision skill — confidence H
 - Q13 data: + include deliberate failure-and-recovery demos (18/50 -> 23/50) and targeted DAgger-style 10-demo top-ups (20/40 -> 34/40) — confidence M
 - Q02 action space: + end-effector/gripper-frame relative actions paired with wrist cams give placement invariance — confidence M (not ablated vs base-frame)
 - Q07 history: ~ history needed only for high-level stage tracking (0/24 vs 12/24); low-level Markovian policy fine — confidence M
 - Q06 chunking: ~ ACT chunking alone did not rescue a long multi-stage task (0/24) — confidence L
