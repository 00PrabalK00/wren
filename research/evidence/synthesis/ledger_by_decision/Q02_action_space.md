# Q02_action_space — 39 ledger lines
[fulltext] ACT | action_space | delta joint targets degraded vs absolute leader targets (no numbers) | - delta | M
[fulltext] DiffusionPolicy | action_space | position (absolute) > velocity for DP | - delta/velocity | M/H
[fulltext] OFT | action_space | absolute joint targets on ALOHA (leader/follower) succeed | + absolute | M
[fulltext] ActionSpaceStudy | action_space | chunk-wise delta > step-wise (~10%); chunk-wise delta ≥ absolute (sometimes marginal); joint > task in fixed embodiment | + chunk-wise delta joint | M/H
[fulltext] RESOLVED | action_space | ACT/DP negative results were vs step-wise delta/velocity; not in conflict with chunk-wise delta | | 
[fulltext] WhatMattersLanguageIL | Q02 action space | MCIL absolute 0.41 vs delta 1.82 avg len | + delta/relative actions | M
[fulltext] UMI | action space | relative-to-chunk-start 20/20, step delta 16/20, absolute 5/20 (calibration bias) | + chunk-wise relative | M
[fulltext] EquivariantDP | Q02 action_space | absolute EE > relative EE: DP 42.0 vs 33.3, EquiDiff 63.9 vs 48.8 @100 demos | + absolute pose | M
[fulltext] pi0.5 | Q02 action_space | absolute target joint/EE poses, per-dim 1–99% quantile norm to [-1,1] (not ablated) | ~ absolute + quantile norm | L
[wave3] W3_AxisGuideGroundingRobotActionCoordinateS | Q02 action space | relative-EEF policies fail to re-target to unseen positions without frame grounding | ~ delta EEF needs grounding | L
[wave3] W3_PolybotTrainingOnePolicyAcrossRobotsWhil | Q02 action space | per-robot heads on shared EE-delta vs shared blocking controller: shelf 0.9-1.0 vs 0.0 | ~ robot-specific action heads | L
[wave3] W3_RealWorldOfflineReinforcementLearningwit | Q02 | real Franka BC: absolute joint targets vs delta: slide 0.681 vs 0.551, lift 0.823 vs 0.721, PnP 0.818 vs 0.678; ORL prefers delta (abs crashes) | + absolute joint position for BC | M
[wave3] W3_AComparisonofActionSpacesforLearningMani | Q02 action space | RL sim, impedance (task-space) refs learn fastest > ID > PD > torque | ~ task-space targets (RL only, not BC) | L
[wave3] W3_GoalConditionedDualActionImitationLearni | Q02 action space | reactive delta for local precise phase + trajectory for transport: mean 0.870 vs 0.439 all-trajectory | ~ step-wise delta near contact | L
[wave3] W3_WhyDoesActionChunkingImproveBehavioralCl | Q02 | at 50-60 Hz delayed policies fail; 5-step sub-chunk actions (10-20 Hz effective) restore performance | ~ keep ~10-20 Hz effective action rate or chunk at high fps | L
[wave3] W3_AhaRobotALowCostOpenSourceBimanualMobile | Q02 action space | base velocity control from spiky teleop -> policy fails to move; position displacement -> smooth (qualitative); absolute joint cmds tolerate noise | + absolute position, - velocity | M
[wave3] W3_PerceiverActorAMultiTaskTransformerforRo | Q02 action space | keyframe next-best-pose + motion planner; random/fixed-interval keyframes -> 0% | ~ keyframe paradigm viable for quasi-static pick-place only | L
[wave3] W3_BCZZeroShotTaskGeneralizationwithRobotic | Q02 action space | 1-step delta targets @10 Hz: 3% vs adaptive multi-step state-diff 45% (same task, multi-task one-hot) | - step-wise small deltas; + look-ahead/absolute targets | M
[wave3] W3_Pix2ActImageSpaceManipulationPolicieswit | Q02 action space | MimicGen ablation: 3D absolute 41.5 vs 3D EE-relative 55.5 vs image-space 69.3 | + EE-relative over absolute | M
[wave3] W3_ProgVLAProgressAwareRobotManipulationSki | Q02 action space | delta joint displacement on real leader/follower PiPER, no ablation | ~ delta joints workable | L
[wave3] W3_TunetoLearnHowControllerGainsShapeRobotP | Q02 action space | real FR3 BC: compliant-overdamped 71% vs stiff 5-8%; sim 6 tasks significant; holds for abs & rel joints | + low-Kp/high-Kd servo gains under position actions | M
[wave3] W3_WhatistheBetterCurriculumControllerShape | Q02 action space | follower-realized state as action label in winning condition (confounded with reflex) | ~ follower vs leader labels unresolved | L
[wave3] W3_BenchmarkingActionSpacesinReinforcementL | Q02 action space | real Franka pick (12 trials): joint vel 100, joint pos-inc 100, EE pose-inc 41.7, EE vel 0; push dist 0.405/0.104/0.050/0.000 m | + joint space; - Cartesian IK-based | M
[wave3] W3_BenchmarkingActionSpacesinReinforcementL | Q02 action space | jerk m/s^3 pick: joint vel 16.0 vs joint pos-inc 52.6 | ~ velocity/integrated commands smoother (RL policy) | L
[wave3] W3_EquiVLAAGeneralFrameworkforRotationallyE | Q02 action space | LIBERO relative vs absolute EE: GR00T 78.1 vs 62.6; EquiVLA 92.6 vs 76.1 | + relative/delta EE | M
[wave3] W3_RoboticTableTennisACaseStudyintoaHighSpe | Q02 action space | task-space position actions train faster, survive frozen joints, morphology fix by residual; joint-velocity cannot | ~ (RL, industrial arm) | L
[wave3] W3_ZETAAControlledStudyofZeroShotCrossEmbod | Q02 action space | real (Franka, 50 demos/task): EEF-Delta state+EEF-Delta action 89.9 avg vs AbsEEF/World-Delta 56.0; on source robot 100 vs 87.5 | + gripper-frame relative actions and state | M
[wave4] W4_3DCAVLALeveragingDepthand3DContexttoGene | Q02 | SE(3) waypoints > velocities on real Franka (stated, no numbers) | + absolute EE pose over velocity | L
[wave4] W4_0ResourceAwareRobustManipulationviaTamin | Q02 action space | delta joint < absolute joint on Task B; Task C most sensitive (figure only) | + absolute joint | M
[wave4] W4_ArmnetBenchv01ParallelRealWorldEvaluatio | Q02 action space | all policies use absolute target joint positions on SO-101 (not ablated) | ~ absolute joint | L
[wave4] W4_BehaviorCloningforActivePerceptionwithLo | Q02 action space | toy wrist-cam task: 4 demos delta 5/5 vs absolute 0/5 (test MSE 6.2 vs 189 e-3); both 5/5 at >=8 demos; absolute snaps to trained poses | + step-wise joint delta | L
[wave4] W4_BeyondImplicitForceEvaluatingExplicitFor | Q02 action space | leader-target ACT vs follower-state target: Wipe 60→15%, Bottle 50→25%, Plug 30→0% (real ALOHA, 10–20 trials) | + absolute leader joint targets | M
[wave4] W4_MolmoAct2ActionReasoningModelsforRealwor | Q02 | absolute joint pose, 1 s chunks (30 steps @30 Hz) for SO-100 | + absolute joint targets | L
[wave4] W4_DoYouNeedProprioceptiveStatesinVisuomoto | Q02 action space | state-free: rel EEF 0.984/0.584 height/horiz vs abs EEF, rel joint, abs joint all 0/0 | + relative EEF delta | M
[wave4] W4_GeneralizableHierarchicalSkillLearningvi | Q02 action space | object-frame canonicalized trajectories: 0.83 vs no canonicalization 0.12 (5-task ablation) | + object-relative actions | M
[wave4] W4_EasyMimicALowCostFrameworkforRobotImitat | Q02 action space | shared vs separate human/robot action heads 0.47 vs 0.87 (abs EE pose) | ~ embodiment-specific heads | L
[wave4] W4_FromFixedtoFreeCamerasCalibrationFreeVie | Q02 action space | RLBench unseen views: camera-frame delta EE 51.4 vs base-frame delta 33.2 | + camera-frame deltas (needs EE control) | L
[wave4] W4_FLASHEfficientVisuomotorPolicyviaSparseS | Q02 | polynomial coefficient trajectory + dense upsampling, analytic velocity | ~ smooth param. over raw points | L
[wave4] W4_WhatstheMoveHybridImitationLearningviaSa | Q02 action space | object-relative waypoint offsets vs absolute waypoint regression: Can 70 -> 93.5, Square 13 -> 86.5 | + object-relative targets | L
