# Q07_history_proprio — 65 ledger lines
[fulltext] BAKU | history | no gain over current obs; last-step-loss history hurts | - history | M
[fulltext] CopycatAgents | Q07 history | BC-OH (H=2) lower held-out loss than H=1 but copies prev action; TCA+IB: Walker2d 592→1296, Hopper 293→1086 (MuJoCo, state-based) | + current obs only / no past-action input; + IB if history used | M
[fulltext] CopycatAgents | Q07 history | RNN history worse than frame stacking (Ant −311 vs 1750); dropout-on-history poor | - RNN / dropout fixes | L
[fulltext] BeT | Q07 history | no-history rel. 0.65 CARLA / 0.95 / 0.88 | + short history (sim, no chunking) | L/M
[fulltext] robomimic | Q07 history | BC-RNN vs BC (image, no chunking): Square PH 82.0 vs 62.0, Tool Hang PH 67.3 vs 20.0, Transport MH 42.0 vs 18.7; seq len 10≈30≈50 | + temporal context when NOT chunking; ~ when chunking | M
[fulltext] robomimic | proprio/obs space | +EEF vel or +joint pos/vel: −49–88% rel (low-dim), −2–29% (image) | - extra proprio features | M
[fulltext] WhatMattersLanguageIL | proprio | adding proprio 2.64→2.20 (causal confusion with initial pose) | - proprio when it can cue task | M
[fulltext] RT-1 | Q07 history | w/o 6-frame history: seen 97→82, unseen 76→62, distractors 83→50 (single-step, 3 Hz, 130k demos) | + history only for non-chunked/big-data; ~ for us | M
[fulltext] MDT | Q07 history | no history, chunk 10: SOTA CALVIN 4.52 | + current obs only | M
[fulltext] DiffusionTransformerPolicy | Q07 history | 2 obs 65.8 vs 1 obs 61.6 (chunk 32); 3 obs 35.4 | ~ 1-2 frames | L/M
[fulltext] BidirectionalDecoding | history | Push-T: extending obs context beyond few steps degrades | - long obs history | L/M
[fulltext] Seer-PIDM | Q07 history | uses 7–10-frame history but no ablation | ~ no evidence | L
[fulltext] RoboVLMs-WhatMatters | Q07 history | policy-head history 4.49 > interleaved 4.12 > one-step 4.09 (KosMos, window 16) | + history via separate policy head | M
[fulltext] Octo | Q07 history | 2 frames helps zero-shot, diminishing beyond; proprio input "generally worse" (causal confusion) in pretraining | ~ short history, caution proprio | L/M
[fulltext] HPT | Q07 history/proprio | scratch no-proprio 26.7 vs with proprio 43.3; pretrain w/o proprio 63.3 vs with 70.0 | + include current proprio | M
[fulltext] RDT-1B | Q07 history | 2-frame image history; proprio history excluded to avoid shortcut fixed motions (design, not ablated) | ~ no proprio history | L
[wave3] W3_CoarsetoFineImitationLearningRobotManipu | Q07 history | filtering predictions over frames 35.6% -> 44.4% vs per-frame | + temporal fusion of estimates | L
[wave3] W3_GivingRobotsaHandLearningGeneralizableMa | Q07 history/proprio | no grasp-state input 28.6 vs 54.3 (re-grasp loops) | + include gripper state | M
[wave3] W3_Instructiondrivenhistoryawarepoliciesfor | Q07 history | +history 78.1->81.8 (10 tasks); 74 tasks w/o hist 60.9 vs 65.4; keyframe actions | + history for non-Markovian keyframe tasks; ~ for dense control | L
[wave3] W3_MaskedImitationLearningDiscoveringEnviro | Q07 proprio/inputs | Robomimic Square: all low-dim modalities 12.7% vs masked (drop EEF vel/orientation) 56.7-71.3%; modality dropout 19.3% | + minimal proprio inputs | L
[wave3] W3_RealWorldOfflineReinforcementLearningwit | Q07 | joint velocity in state: BC PnP 0.632 -> 0.818, slide 0.623 -> 0.681 | + include velocity/short proprio history | L
[wave3] W3_ThinkingWhileMovingDeepReinforcementLear | Q07 history | frame stacking prior obs/actions nominal gain vs VTG (figure only) | ~ history less useful than explicit committed-action input | L
[wave3] W3_SPOCImitatingShortestPathsinSimulationEn | Q07 | context 100 vs shorter: avg 49.9 vs 27.8/39.9; Fetch 14.0 vs 2.3 (partially observable long-horizon) | ~ long history only for partially observable tasks | L
[wave3] W3_Seq2SeqImitationLearningforTactileFeedba | Q07 observation history | tactile POMDP, 50 demos: transformer-history seq2seq 76/84% vs LSTM-seq2seq 56/0% vs BC-LSTM 11/5% (sim/real) | + history only when state truly hidden | L
[wave3] W3_ActionEffectMemoryPretrainingforRobotMan | Q07 history | Place Shoe DP: 1 frame .40, DINOv2 stack 8f .52, 16f .40, AEM memory .76 | - raw frame stacking, + compact pretrained memory | L
[wave3] W3_CageCausalAttentionEnablesDataEfficientG | Q07 obs history | To=2/4/8 final 0.87/1.00/0.87 (L0, ~15 trials) | ~ short history (4) with causal compression | L
[wave3] W3_RobustVisualSimtoRealTransferforRoboticM | Q07 obs history | 3-frame history +28.5 pts, single-step policy, sim | + short frame history | L
[wave3] W3_WhyDoesActionChunkingImproveBehavioralCl | Q07 | history-conditioned policies "typically very poor" vs single delayed obs (no table) | - long observation history in low data | M
[wave3] W3_AnchorVLA4DanAnchorBasedSpatialTemporalV | Q07 history | SimplerEnv: first-frame anchor 55.2 vs past-3 frames 46.9 vs strided 21.9; real xLerobot drawer proprio w/ 50% vs w/o 60% (10 trials) | - frame stacking, - proprio in low data | L
[wave3] W3_OnBringingRobotsHome | Q07 history | single-frame policy on aliased shelves 0/10 vs 7/10 with distinguishing cue | + some history/context for aliased states | L
[wave3] W3_GeoPropGroundingRobotStateinVisionforGen | Q07 obs/proprio | DP-R18 sim vanilla proprio 66.8 vs no-proprio 68.1 vs grounded 75.3; real 38.8 / 28.8 / 50.0 (20 trials x 4 tasks) | + keep proprio, ground spatially; ~ copycat risk | M
[wave3] W3_AugInsertLearningRobustVisualForcePolici | Q07 history/proprio | real UR5e 20 rollouts: No-Proprio model better than full on all variations (figure only, 1 seed) | - raw proprio in narrow data | L
[wave3] W3_BAKUAnEfficientTransformerforMultiTaskPo | Q07 history | no history .90/.79/.70 vs last-step-loss history .54/.08/.37 vs multi-step-loss .90/.82/.68 | + current frame only | H
[wave3] W3_RoboVIPMultiViewVideoGenerationwithVisua | Q07 history | single-frame inpainting aug collapses Octo at 6-frame history (figure only) | ~ aug must be episode-consistent if using history | L
[wave3] W3_BestofSimandRealDecoupledVisuomotorManip | Q07 proprio | w/o proprio 71.7/48.3 vs full 91.7/71.7 | ~ proprio helps with sim-trained relative policy | L
[wave3] W3_SeedPolicyHorizonScalingviaSelfEvolvingD | Q07 history | DP frame stacking degrades with longer T_obs (fig); recurrent gated state: long task 33->73%, real ambiguous tasks e.g. 16->54% (100 rollouts) | - naive frame stacking; + recurrent state only for aliased/long tasks | M
[wave3] W3_PredVLAPredictiveSensorimotorModelingfor | Q07 history | removing multi-timescale hierarchy -17..-29 pts in predictive model, only -1.2 in plain BC | ~ recurrence helps only with predictive structure | L
[wave3] W3_PVIPluginVisualInjectionforVisionLanguag | Q07 history | V-JEPA2 frames@4fps: 2f 71.6, 4f 71.8, 8f 69.4, 16f 66.6 | + short history (0.5-1 s) via frozen video encoder; - long history | L
[wave3] W3_SelectivePerceptionforRobotTaskAwareAtte | Q07 history/proprio | router with raw state input 30% vs 83% without (acted as noise) | - raw proprio into gating modules | L
[wave3] W3_VIRALVisualSimtoRealatScaleforHumanoidLo | Q07 history | FF-history and LSTM > single-step (figure only) | + short history | L
[wave3] W3_VisionLanguageFoundationModelsasEffectiv | Q07 history | MLP no-history worst; LSTM/GPT history heads best (figure only) | + history via head | L
[wave3] W3_TaskAnchorGroundingTaskStateinReactiveVL | Q07 history | RMBench memory tasks: pi0.5 0.14 -> history+stage-coordinate 0.68; history-only 0.18, coordinate-only 0.31 (sim) | ~ structured task-state only for aliased/long tasks | L
[wave3] W3_VisualBacktrackingTeleoperationADataColl | Q07 history/copycat | success-only Q function relies on proprio (gripper closed+moving up) not image | ~ proprio shortcut risk in small datasets | L
[wave3] W3_ChainVLAChainingVisionLanguageActionQuer | Q07 history | w/o progress context 3.0; event readout removal Put Back 96->25 (memory-dependent sim tasks) | + recurrent/event memory for aliased tasks only | M
[wave3] W3_BlindfoldedExpertsGeneralizeBetterInsigh | Q07 history | GRU memory policy used to clone non-Markovian exploratory demos (not ablated) | + history when demos contain search | L
[wave3] W3_GeometricActionModelforRobotPolicyLearni | Q07 history | obs history H=1 89.7 vs H=2 84.4, H=4 85.1 (LIBERO-Plus Object) | - multi-frame history | M
[wave3] W3_TowardsAccessiblePhysicalAILoRABasedFine | Q07 copycat | 20 eps: zeroing images barely changes actions (0.8) -> proprio shortcut, oscillation near target | + test image-ablation sensitivity | L
[wave3] W3_ZETAAControlledStudyofZeroShotCrossEmbod | Q07 history/proprio | sim: AbsEEF state -> EEF-Delta state avg 64.6 -> 75.7 (ARM shift 39.9 -> 74.3) | ~ de-emphasize absolute proprio | L
[wave4] W4_FACTRForceAttendingCurriculumTrainingfor | Q07 history/proprio | excluding current joint state from input "greatly improves generalization" (stated, no numbers) | - proprio input | L
[wave4] W4_ImprovingGenerativeBehaviorCloningviaSel | Q07 | 2-frame history; prev obs as negative guidance gives future extrapolation | + short history usable at inference | L
[wave4] W4_ImprovingtheperformanceofAIpoweredAfford | Q07 history/memory | phase token (t/T) on ACT: fetching 50.0/69.9/79.9 → 83.3/86.6/93.3 (dims 128/256/512), trials unreported | + phase/progress signal | L
[wave4] W4_LIFDAnchoredDiffusionfor3DAwareSceneMemo | Q07 history/memory | no-memory ablation 93.6→74.8% LIBERO-Spatial (occlusion-style tasks) | ~ memory only for partial observability | L
[wave4] W4_MINERVAHowSmallCanaManipulationPolicyBea | Q07 history | 1→2 obs steps: +6 Goal, +4 Long (7M, single run) | + short history | L
[wave4] W4_ARWAMAVisualConditionedAgentReadyWorldAc | Q07 history/proprio | cross-attn relies 35.6% on proprio vs AdaLN 15.5% (shortcut) | ~ beware proprio shortcut | L
[wave4] W4_DoYouNeedProprioceptiveStatesinVisuomoto | Q07 history/state input | pi0 height gen w/ state 0 vs w/o 0.984; horiz 0 vs 0.584; ACT 0/0.084 vs 0.933/0.517; DP 0/0 vs 0.867/0.533; in-domain equal (1.0) | - proprio state input / + state-free or state-noise | M
[wave4] W4_CronusVLATowardsEfficientandRobustManipu | Q07 history | SimplerEnv: single-frame 31.0, naive 7-frame stack 32.4, cached-feature history+decoder 70.9; no current-frame modulator 63.5; frame count inverted-U (best 4-7) | + short cached feature history, - naive stacking | M
[wave4] W4_ChronosAPhysicsInformedFullHistoryFramew | Q07 history | real memory tasks pi0.5 0/150 vs full-history SSM 108/150; RMBench 11.2 vs 73.6% | + full history only for aliased/memory tasks | M
[wave4] W4_DreamGenUnlockingGeneralizationinRobotLe | Q07 | zero-state neural trajs → less proprio overfitting, fewer stuck-at-home failures on SO-100 (qualitative) | + proprio dropout/zeroing | L
[wave4] W4_GeoPredictLeveragingPredictiveKinematics | Q07 history | kinematic keypoint history encoder +2.5 pts RoboCasa | ~ low-dim history helps slightly | L
[wave4] W4_Learningathousandtasksinaday | Q07 | removing proprio from MT-ACT+ improved spatial generalization (preliminary, no numbers) | + drop/limit proprio | L
[wave4] W4_ReflexEnablingFastandPredictiveVisionLan | Q07 history | 2-frame fusion on intermediate ViT features 62.8 -> 71.7% (dynamic conveyor) | ~ short history for dynamic tasks only | L
[wave4] W4_UniVLALearningtoActAnywherewithTaskcentr | Q07 history | history latent actions: LIBERO-Long 88.1 -> 92.0, R2R 30.6 -> 47.1 | + compact action history | M
[wave4] W4_StageACTStageConditionedImitationforRobu | Q07 history/memory | ACT 20% vs ACT+5-frame history 10% vs stage-conditioned 55% SR (unseen door, 10-20 trials) | - raw frame history; + explicit low-dim stage signal | L
[wave4] W4_VODPSemanticGeometricAdaptiveDiffusionPo | Q07 history | RoboTwin T=1 64.6 vs T=3 63.9 | - obs history no gain | L
[wave4] W4_GlobalPriorMeetsLocalConsistencyDualMemo | Q07 history/memory | previous-action-chunk consistency module: removal -> LIBERO-Long -1.6 to -3.3, real -5.5 to -8 pts | + action-history conditioning | L
