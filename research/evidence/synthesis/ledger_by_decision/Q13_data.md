# Q13_data — 195 ledger lines
[fulltext] robomimic | Q13 data | MH 300 demos < PH 200 demos; adding 100 worse demos hurts BC (Square 58.7→46.7); Lift/Can 75–100% with 20% data | + quality over quantity | M/H
[fulltext] RT-1 | Q13 data | 75% tasks@97% data ≈ 51% data; ≤50 ep/task: unseen 14%, backgrounds 41 | + diversity > quantity | M/H
[fulltext] ConsistencyPolicy | Q10 steps_vs_quality | DDIM-15 ToolHang .14 vs DDPM-100 .79 vs CP-3 .77; low-var init +.04 | - naive step reduction on precise tasks | M
[fulltext] FLARE | Q13 data | novel objects: 10 demos 42.5 → 80.0 with 150 human ego videos/object (alignment loss only on videos) | + action-free video co-training | L/M
[fulltext] VC-1 | Q13 data | pretraining diversity > size (+Nav/+ImageNet +1.5–3.6; +800K frames +0.1) | + diverse pretraining | M
[fulltext] SmolVLA | data | SO-100 real: single-task no-PT 40 < ACT 48.3; multi-task 51.7; +community PT 78.3 | + in-embodiment pretraining + multi-task | M
[fulltext] X-VLA | data | PEFT 9M params LIBERO 92.8 @50 demos -> 91.1 @10 demos/task | + fine-tune pretrained VLA in low data | M
[fulltext] Seer-PIDM | Q13 data/pretraining | real 100 demos/task: scratch 60.0 → DROID-pretrained 78.4 SR; OXE (other robots) 53.3→56.7 | + same-embodiment pretraining only | M
[fulltext] DemoGen | data diversity | spatial success region ≈ union of demonstrated placements; no extrapolation; DP3 sim 25→400 demos 3→98%, fixed positions 100% | + spread demos over placement grid covering eval region | H
[fulltext] DemoGen | recovery data | disturbance resistance needs disturbance demos: 40.4 → 92.3 normalized (ADR) | + recovery/disturbance demos | M
[fulltext] DemoGen | demo count | 100→150 demos +37 pts, 150→200 +6 pts (precise peg, 40×40 cm) | + ~100–150 demos to cover workspace, diminishing after | M
[fulltext] RoboAgent-MT-ACT | data (new task) | add task with 50 demos ×4 aug + 10% replay of old data, no significant forgetting | + small new-task set + replay | L
[fulltext] RoboAgent-MT-ACT | co-training | universal (all activities) < single-activity policy on most tasks (negative transfer) | - indiscriminate unrelated-task mixing | L
[fulltext] DataScalingLaws | data diversity | 32 env-object pairs × 50 demos → 85–92.5% success in unseen envs+objects (4 tasks); per-env demo fraction 50% ≈ 100% | + many conditions, few demos each | H
[fulltext] DataScalingLaws | demo count | plateau at 400–800 total demos (16 env × 64 obj); ~50 demos per env-object pair; ≤100 total unstable | ~ 100–150 demos gives partial OOD only | M
[fulltext] DataScalingLaws | object diversity | 8 training objects → >0.8 on unseen objects; object gen easier than env gen | + 4–8 different pumpkins | H
[fulltext] DataScalingLaws | protocol | randomize initial gripper pose + object pose each demo; standardize strategy/speed across operators | + randomized starts, consistent strategy | M
[fulltext] MobileALOHA | co-training | 50/50 co-train with 825 same-embodiment off-task demos: whole-task +45/+20/+80/+95/+80 pts on 5 of 7 tasks, 0 on 2 | + co-train with public SO-100/101 data | M/H
[fulltext] MobileALOHA | co-training | 35 co-trained demos 70% > 50 plain 50%; mix 30/50/70% → 95/95/90; pre-train-then-FT no gain | + co-train (not pretrain), ratio insensitive | M
[fulltext] ALOHA-Unleashed | data quality | duration filtering (2164 eps): all 30%, shortest-50% 55%, shortest-25% 40% | ~ mild filtering, keep corrected mistakes | L/M
[fulltext] ALOHA-Unleashed | recovery data | retries emerge when in data; unseen states (face-down shirt, flipped shoe) never recovered | + explicit recovery / odd-state demos | M
[fulltext] ALOHA-Unleashed | demo count | ShirtMessy 0/20/70/70% at 25/50/75/100% (2164→8658 demos); ShirtEasy saturates at 25–50% | + narrow init first, widen with more data | M
[fulltext] UMI | data diversity | in-the-wild 1400 demos/30 envs: 71.7% unseen envs; narrow-domain data + same ViT-L: 0% | + vary scene conditions in collection | H
[fulltext] LBM-CarefulExamination | Q13 data | finetuned LBM with 15% task data beats single-task 100% (real SetBreakfastTable); 3–5× less data overall | + pretrain→finetune on own task | H
[fulltext] LBM-CarefulExamination | Q13 data_quality | unfiltered idle starts → policy never moves (89/200 rollouts); trim until 5 cm/15° motion | + trim low-motion prefixes | M
[fulltext] LBM-CarefulExamination | Q13 data_quantity | single-task sim SR 13.5–19.5% @49 demos, 50% @196, 68.5% @490 | ~ 50 demos is low for single-task | M
[fulltext] RoboVLMs-WhatMatters | Q13 cross_embodiment | OXE co-train ≈ no gain; same-robot other-task data > OXE; OXE pretrain → few-shot +17.2% SR | + in-domain data first | M
[fulltext] Dita | Q10 steps_vs_quality | DDIM steps 100/50/20/10/5/2 → Pick-Coke var 76.4/79.1/85.5/85.3/82.7/70.4; Move-Near var 52.1/66.0/73.0/69.5/63.5/51.6 | + ~10 steps; - 2 steps w/o distillation | M
[fulltext] Octo | Q13 data | pretrain mix: 25 datasets 83 vs 11 datasets 60 vs Bridge-only 43 | + diversity of pretraining data | M
[fulltext] HPT | Q13 data | cross-embodiment pretrain +27 pts over scratch at ~100 demos (43.3→70.0) | + pretrained trunk for 100-demo regime | L/M
[fulltext] RDT-1B | Q13 data | no-pretrain 1.2B: unseen object 0 vs 50, unseen scene 25 vs 62.5 | + pretraining for OOD objects/scenes | M
[fulltext] pi0 | Q13 data | pretrain+finetune up to ~2x vs scratch, largest on tasks similar to pretraining (figure only) | + pretraining + curated post-train | M
[fulltext] pi0.5 | Q13 data | 3->104 training locations: monotone gain, 104 ≈ model trained on test homes (40 trials/pt, figure only) | + maximize scene diversity over repetitions | M
[fulltext] FAST | Q13 data | idle all-zero frames filtered; stationary starts caused hovering (temp 0.7 workaround) | + trim idle frames | M
[fulltext] GR00T-N1 | Q13 data | 10% data GR00T 42.6 ≈ full-data DP 46.4; neural traj +4.2/+8.8/+6.8 sim, +5.8 real | + pretraining; + synthetic data | M
[wave3] W3_AffordDPGeneralizableDiffusionPolicywith | Q13 | sim 30 demos: all methods ~80% low variance, 13-53% high variance; image DP 0% real w/ 100 demos over 4 objects | + more demos needed as placement variance grows | L
[wave3] W3_ActionMapRobotPolicyLearningviaVoxelActi | Q13 data quantity | Insert 0/10 both heads at 50 demos, 5/10 at 275 | + more demos for multi-stage precision | M
[wave3] W3_BehaviorRetrievalFewShotImitationLearnin | Q13 | 10 target demos + VAE-retrieved prior data: sim avg 72% vs GC pretrain+FT 36%; real +>20 pts; naive mixing hurts | + filtered co-training with same-embodiment prior data | M
[wave3] W3_AnchorDreamRepurposingVideoDiffusionforE | Q13 data diversity | +-10 cm key-state perturbed trajectories give 2x real success at 50 seeds | + spatial coverage over raw count | M
[wave3] W3_IMLEPolicyFastandSampleEfficientVisuomot | Q13 data | Push-T reward 0.5 at <29% data vs DP ~43% vs FM >80%; real multimodal task from 17 demos | + generative 1-step head in low-data | L
[wave3] W3_BridgeDataBoostingGeneralizationofRoboti | Q13 data diversity | 50 target demos + 7.2k multi-domain demos: 66% vs 28% target-only (seen tasks); new tasks 50% vs 22% | + co-train with diverse same-robot data | M
[wave3] W3_BridgeDataBoostingGeneralizationofRoboti | Q13 training recipe | joint training >> pretrain+finetune (stated, no numbers); bridge weight 70-90% avoids overfitting 50 demos | + joint co-training | L
[wave3] W3_CACTIAFrameworkforScalableMultiTaskMulti | Q13 data diversity | sim held-out layouts: 10→100 training layouts R3M 9.5→33.1, MoCo 18.8→38.4 | + diversity over count | M
[wave3] W3_DABIEvaluationofDataAugmentationMethodsU | Q13 data quantity | 5 demos sufficient with 10x temporal augmentation for 1 Bi-ACT task | ~ | L
[wave3] W3_DecomposingtheGeneralizationGapinImitati | Q13 | sim gap 0.4 -> <0.1 from 5 to 100 training envs; out-of-domain robot data improves robustness | + environment diversity | M
[wave3] W3_GivingRobotsaHandLearningGeneralizableMa | Q13 data | env-gen avg: robot-only 5.2% / +play (larger) 23.8% / +diverse masked human wrist videos 63.6% | + scene diversity over volume | M
[wave3] W3_ElicitingCompatibleDemonstrationsforMult | Q13 | adding 5-10 demos from a different-style operator: Hammer 24.7->4.0%, Round Nut 13.3->7.3%; real food plating 60->30% naive vs 85% with compatibility feedback | + single consistent strategy / filter incompatible demos | M
[wave3] W3_EvaVLAEvaluatingVisionLanguageActionMode | Q13 data diversity | object orientation variation is dominant failure → demos must cover pose range | + pose diversity in demos | L
[wave3] W3_FurnitureVLALearningLongHorizonBimanualF | Q13 | 125/250/500 demos: 0.50/0.68/0.80 | ~ diminishing returns | L
[wave3] W3_HumanintheLoopImitationLearningusingRemo | Q13 data | 30 demos + intervention rounds (IWR, 50/50 balanced) 87.3/87.5% vs equal-budget full demos 76.7/64.9% vs HG-DAgger 75.3/69.6% (sim, low-dim) | + intervention/recovery data upweighted | M
[wave3] W3_IdentifyingExpertBehaviorinOfflineTraini | Q13 data | real TriFinger lift/mixed BC 489 -> 917 after filtering to expert episodes; BC on expert beats offline RL | + filter low-quality demos | L
[wave3] W3_ImmersiveDemonstrationsaretheKeytoImitat | Q13 | force-feedback demos: lower force variance and faster execution, mirrored by BC agent (sim, proprio-only, no success rates) | + consistent, feedback-rich teleop | L
[wave3] W3_ImperfectionforPrecisionUpcyclingImperfe | Q13 data quality | naive mixing of low-precision UMI demos: ATX 48.3->33.3, cable 78.3->25.0, sorting 81.7->75.0 (60 trials) | - mixing imprecise demos uniformly | H
[wave3] W3_ImperfectionforPrecisionUpcyclingImperfe | Q13 data reuse | flow-time routing: +Dpm ATX 73.3, cable 90.0 vs equal extra perfect data 75.0/91.7 (avg -4.2 pts) | + route imperfect data to high-noise flow times | M
[wave3] W3_LearningLatentPlansfromPlay | Q13 | sim 18 tasks: Play-LMP on 30 min play 71.8% vs 18 expert BC policies on 90 min 70.3%; 7 h play 85.5%; play-trained more robust to init perturbation | + coverage/varied-start data over narrow clean demos | M
[wave3] W3_LDA1BScalingLatentDynamicsActionModelvia | Q13 data quality | adding ~35% imperfect teleop demos: pi0.5 60→40 / 50→40; LDA 70→80 / 50→60 (10 trials) | - unfiltered imperfect demos for plain BC | L
[wave3] W3_LearningVisualRoboticControlEfficientlyw | Q13 data quantity | BC with 10 demos only solves reach/switch, fails move/pull/pickup (figure only) | - ~10 demos for plain BC | L
[wave3] W3_MimicPlayLongHorizonImitationLearningbyW | Q13 | Kitchen long-horizon 20->40 demos: 0.47->0.70; +10 min human play: 0.40->0.70 at 40 demos | + more demos / cheap human play for long-horizon | L
[wave3] W3_CLIPortWhatandWherePathwaysforRoboticMan | Q13 data | real 2-10 demos/task -> 55-75%; authors estimate 50-100 demos needed for robustness | ~ 50-100 demos | L
[wave3] W3_PolybotTrainingOnePolicyAcrossRobotsWhil | Q13 data | cross-robot data + 5 target demos 0.7-1.0 vs single-robot 0.0-0.3 | + cross-embodiment co-training with aligned spaces | L
[wave3] W3_RealWorldOfflineReinforcementLearningwit | Q13 | BC trained with other-task data drops (lift 0.823 -> 0.58-0.61) while IQL can gain | - naive multi-task mixing for BC | L
[wave3] W3_RoboMINDBenchmarkonMultiembodimentIntell | Q13 data quality | ACT failures dominated by inaccurate positioning (up to 48%) from non-random placements; gripper failures from too-fast closure (few frames) | + randomize placements, slow gripper actions during teleop | M
[wave3] W3_RoboMINDBenchmarkonMultiembodimentIntell | Q13 data quantity (sim co-train) | ACT 100 real + up to 500 digital-twin sim traj improves real success; sim-only 10% real (figure) | ~ sim co-training | L
[wave3] W3_SeeingAlltheAnglesLearningMultiviewManip | Q13 | same demo count spread over views: little/no penalty in fixed view | + diversity over repetition | L
[wave3] W3_RVTRoboticViewTransformerfor3DObjectMani | Q13 data quantity | real Franka ~10 demos/task keyframe: 56% overall, 82.5% excl. thin-marker tasks | ~ | L
[wave3] W3_SPOCImitatingShortestPathsinSimulationEn | Q13 | 100k episodes: 100 houses 43.5 vs 10k houses 57.0; 10k->100k episodes 19.0->57.0 | + environment diversity over repetition | M
[wave3] W3_Seq2SeqImitationLearningforTactileFeedba | Q13 data quantity | real snap-on success converges after ~50 demos (5–200 sweep, figure) | ~ 50 demos saturate narrow task | L
[wave3] W3_BayesianDisturbanceInjectionRobustImitat | Q13 data quality | noise-injected demos 51%→91% real (10 demos, low-dim) | + perturbation/recovery demos | M
[wave3] W3_EVLAEventAugmentedVisionLanguageActionMo | Q13 data diversity | multi-illumination training: image-only 40 lux 30%→80%, 75 lux 65%→100% | + collect demos under varied lighting | M
[wave3] W3_HumanintheLoopTaskandMotionPlanningforIm | Q13 data | learning only contact segments: Square Broad 80% vs 1.2% from 10 min data (sim) | + shorten learned segment | L
[wave3] W3_OfflinetoonlineReinforcementLearningforI | Q13 data quantity | 50→500 demos no gain without aug (~35%) | ~ more demos alone insufficient | L
[wave3] W3_RaCRobotLearningforLongHorizonTasksbySca | Q13 data quality | recover-then-correct interventions: sim 61/100 vs 23/100 full demos vs 22/100 HG-DAgger; real ≥2x data efficiency; shirt 78.3% w/ 5 h vs 75% w/ 89 h (cross-paper) | + human-in-loop recovery data | M
[wave3] W3_RobustVisualSimtoRealTransferforRoboticM | Q13 data diversity | appearance-diverse data avg 17.3 vs real-limited 13.2/20; + real FT 18.2 | + diversity over count | M
[wave3] W3_TransporterNetworksRearrangingtheVisualW | Q13 data quantity | 1-10 demos suffice with spatial equivariance (sim) | ~ | L
[wave3] W3_BridgeDataV2ADatasetforRobotLearningatSc | Q13 data | 13 skills vs 3 skills at ~27k traj: better unseen pick-place (figure only) | + skill/scene diversity | L
[wave3] W3_AdaptationofGeneralistRobotPolicieswithM | Q13 data | 1-demo BC real YAM 40%/27% (15 trials); object swap -> 0%; broader demos restore robustness | + demo coverage over positions | L
[wave3] W3_CanonicalPolicyLearningCanonical3DRepres | Q13 data | at 50 demos only CP non-zero; image policies flat 0-1/10 from 50 to 100 demos on UR5 | ~ 3D equivariance improves low-data | L
[wave3] W3_AhaRobotALowCostOpenSourceBimanualMobile | Q13 data | 50 demos box transfer 10/10 (10 trials); RoboPilot vs VR data 73 vs 70% | + ~50 demos for simple pick-place | L
[wave3] W3_ChicGraspImitationLearningbasedCustomize | Q13 data | 50 demos on variable carcasses: 25-65% per exemplar; failures at grasp height | ~ 50 demos marginal for high-variance objects | L
[wave3] W3_AnchorDP33DAffordanceGuidedSparseDiffusi | Q13 data | RoboTwin 98.7% headline; 10% DAgger off-trajectory frames claimed helpful, no ablation numbers | ~ recovery data | L
[wave3] W3_OnBringingRobotsHome | Q13 data | 24 demos/task -> 81% over 109 home tasks; novice demos 10%/0% first task -> 70%/90% second | ~ ~24-50 demos enough for short tasks; operator practice matters | M
[wave3] W3_OneACTPlaySingleDemonstrationBehaviorClo | Q05 synthetic demos | 1 VR demo -> transformed replays; real push 35/70/90% at 50/100/200 | + trajectory-transform augmentation | L
[wave3] W3_FromPlaytoPolicyConditionalBehaviorGener | Q13 data | 4.5 h play, no labels; goal-obs conditioning 0.98/0.90/2.80 ~= labels 1.0/0.89/2.75 | ~ play data usable | L
[wave3] W3_AStudyonEnhancingtheGeneralizationAbilit | Q13 data | trajectory-only (MimicGen) data fails on visual shifts; diversity-randomized data fixes | + diversity over count | M
[wave3] W3_GELLOAGeneralLowCostandIntuitiveTeleoper | Q13 data quality | teleop success GELLO .92 vs VR .72 vs SpaceMouse .63 (12 novices) | + joint-space leader teleop | M
[wave3] W3_CounterfactualBehaviorCloningOfflineImit | Q13 data quality | Counter-BC > BC on noisy human demos incl. Robomimic multi-human and real air hockey (figure only) | + denoising/smoothing noisy teleop actions | L
[wave3] W3_AsyncVLAAsynchronousFlowMatchingforVisio | Q13 data | pause intervals masked out of loss (no ablation) | ~ trim idle teleop frames | L
[wave3] W3_RobotSelfImprovementviaHumanVideoDynamic | Q13 data | real Stretch 5 tasks x15: BC 41.3 -> value-filtered rollout FT (RECAP/AWR) ~61 -> failure-repair DGAC 85.3 | + post-deployment rollout fine-tuning | L
[wave3] W3_DexterousImitationMadeEasyALearningBased | Q13 data | 30 demos, single-step state BC fails all 3 real tasks; kNN (INN/VINN) solves 2-3 (figure only); pauses <2 cm filtered | ~ single-step BC fails at 30 demos | L
[wave3] W3_GloVLALetGeometryMoveandLocalVLAInteract | Q13 data | local-only policy 100% @10 demos clean; 99.9 vs 48.5 perturbed @50 demos (LIBERO task 1) | + train on local interaction clips | L
[wave3] W3_RobotUtilityModelsGeneralPoliciesforZero | Q13 data | equal-size data: 5-6 envs x200 vs ~40 envs x25 -> ~50% drop on reorientation (figure); expert>non-expert, mixing can hurt | + diversity over repeats, + clean expert demos | M
[wave3] W3_P3POPrescriptivePointPriorsforVisuoSpati | Q13 data | 16-60 demos/task (8-15 per instance) -> 13/20-39/40 in-domain | ~ few demos OK with abstracted input | L
[wave3] W3_RoboTwin20AScalableDataGeneratorandBench | Q13 data | DR pretraining RDT 18.8->24.8, pi0 22.5->29.1; clean pretraining 14.6/24.9 (no gain) | + diversity over clean volume | M
[wave3] W3_EvaluatingtheEffectivenessofCorrectiveDe | Q13 data | Adroit relocate (DAPG sim): 10 orig + 20 corrective 66.6/92.7/97.9% vs 10 orig + 20 random 7.0/36.0/75.6% at 200/400/600 iters; no gain when corrective is minority; restrictive-only demos 69% in full space | + targeted corrective demos / wider initial-state coverage | L
[wave3] W3_BCZZeroShotTaskGeneralizationwithRobotic | Q13 data | equal data: manual 27%/23% vs 50% HG-DAgger 53%/47%; sim fixed scene 37 demos 97% vs randomized 40 demos 56% | + intervention/recovery data; variability raises demo need | M
[wave3] W3_BestofSimandRealDecoupledVisuomotorManip | Q13 data | end-to-end BC stack 30% ID -> 0% OOD position; BSR 75/35; K=10 BSR 73.3 vs e2e 20.0 | + demos covering workspace | M
[wave3] W3_HiWMHumanintheWorldModelforScalableRobot | Q13 data/recovery | real: human corrections in WM avg 94.3 vs self-generated successes 75.4 vs base 56.4 (DP & pi0, 3 tasks) | + failure-targeted corrective demos | M
[wave3] W3_FastandAccurateAnAdaptiveVLAInferenceFra | Q13 data quality | small policy trained on pi0-distilled rollouts +4.8 pts vs on human teleop | + consistent/clean demos | L
[wave3] W3_Pix2ActImageSpaceManipulationPolicieswit | Q13 data | real: 40 demos 55% vs DP 20%; 70 demos 85 vs 60 | ~ representation matters more at low data | L
[wave3] W3_SAVLASymmetryAwareVisionLanguageActionMo | Q13 data | 10%/25%/100% data: 48.3/66.1/86.5 baseline vs 57.1/71.9/91.6 equivariant | + structural priors matter more at low data | M
[wave3] W3_SeedPolicyHorizonScalingviaSelfEvolvingD | Q13 data | pauses in demos -> zero-velocity freeze failure (qualitative) | + trim idle pauses from teleop demos | L
[wave3] W3_KAIAKinematicAwareInterfaceforDataEffici | Q13 data | 100 demos: Ours 42.4 vs DP3 20.1, Seer 20.2; matches baselines with half data | + structured priors raise low-data efficiency | M
[wave3] W3_ItsNotJustMoreDemosCounterfactualActionS | Q13 data | single-factor targeted repair leaves worst-case 0.0; held-out best with random-500 (0.90) | + diversity/coverage over count | L
[wave3] W3_REBOOTFromFailuretoRecoveryADatasetandBe | Q13 data | 60 expert demos/task: install success 16% vs remove 56%; 54% failures at Align/Engage(place); recovery-data effect NOT measured | + collect phase-targeted recovery demos from own rollouts | L
[wave3] W3_REBOOTFromFailuretoRecoveryADatasetandBe | Q13 data | trailing static segments flagged; IL copies pauses (cited) | + trim idle segments | L
[wave3] W3_SelfSupervisedCorrespondenceinVisuomotor | Q13 data | real: ~50 demos -> 97-100% single-instance tasks; 146 demos -> 77% novel shoes | ~ 50 demos enough for fixed object; more for category | M
[wave3] W3_SPIRESynergisticPlanningImitationandRein | Q13 data | sim: KL-constrained RL on top of BC reaches >=80% with 10-50 demos vs BC >870 demos over 7 tasks; Tool Hang 10%->94% | ~ (needs sim/RL, not our pipeline) | L
[wave3] W3_SimulationDistillationPretrainingWorldMo | Q13 data | expert-only vs perturbed+suboptimal equal volume: 0.10/0.05 vs 0.90/0.85 (world model) | + recovery/perturbation coverage | L
[wave3] W3_StabilizetoActLearningtoCoordinateforBim | Q13 data | acting BC-RNN 20 -> 40 in-distribution demos: Hard OOD objects 28.8->23.1, 53.3->56.7, 26.6->30.0 (no gain) | + diversity over count for novel objects | L
[wave3] W3_TowardsEffectiveUtilizationofMixedQualit | Q13 data | real 50 mixed demos: DP Tissue 10->65%, ACT 0->25%, RISE Pen-3 40->60% after segment select+relabel; discarding low-quality < repairing | + clean/relabel noisy segments, keep mediocre demos | M
[wave3] W3_TowardsEffectiveUtilizationofMixedQualit | Q13 data | sim: trajectory-smoothing all demos -27.48% vs selected low-quality only +17.07% | - blanket smoothing of demos | M
[wave3] W3_TrainOfflineTestOnlineARealRobotLearning | Q13 data quality | BC scooping: successes-only 83.3% vs all incl. failures 72.2%; top5% 38.9, 25% 72.2, 50% 77.8 | + filter failed demos; diminishing returns | M
[wave3] W3_SIDSlidingintoDistributionforRobustFewDe | Q13 data | 2/10/50 raw demos after aug: ~19-23/25 all | ~ augmentation substitutes count | L
[wave3] W3_TheUnreasonableEffectivenessofDiscreteTi | Q13 data | real 5 demos: DP/LSTM/ARP 0.00, MiDiGaP 1.00 mild / 0.95 constrained | + structured object-frame policies cut demo need | M
[wave3] W3_VIRALVisualSimtoRealatScaleforHumanoidLo | Q13 data | 10-object vs 1-object training better on all objects (figure); pure BC brittle vs DAgger mix | + object diversity, + on-policy corrections | L
[wave3] W3_TunetoLearnHowControllerGainsShapeRobotP | Q13 data | compliant/overdamped gains give steeper BC scaling with #demos (fig); teleop success unchanged with tuned mapping | + tune gains before collecting more demos | L
[wave3] W3_WaypointBasedImitationLearningforRobotic | Q13 data | AWE relabelling: DP Square 30 demos 44.3->62.3, 50: 57.3->67.0, 200: 95.0->94.7; real ALOHA coffee ACT 36->64 | + waypoint relabelling in low-data regime | M
[wave3] W3_VisualBacktrackingTeleoperationADataColl | Q13 data | 60 min teleop each: in-episode fail->recover->success data BC 73% vs success-only BC 66%; IQL on it 79% (1437 A/B episodes) | + include recovery demos within same episode | M
[wave3] W3_VisualBacktrackingTeleoperationADataColl | Q13 data | separate failure/play episodes mixed in: OffRL 52-64% vs 67-69% success-only (spurious visual cues) | - mixing visually-dissimilar failure episodes | L
[wave3] W3_WhatistheBetterCurriculumControllerShape | Q13 data quality | 30 controller-consistent demos: ACT 95% stable vs 30 best-of-100 manual 15% (contact-screened 30%); pi0.5 95% vs 5% | + demo consistency over count/screening | M
[wave3] W3_VisuomotorControlinMultiObjectScenesUsin | Q13 data | representation priors' gain vanishes 1k->10k episodes (all ~95%) | ~ priors matter most in low-data regime | M
[wave3] W3_AXISAGrowableCommunityDrivenDataEnginefo | Q13 data quality | SG smoothing+resample: jerk -81% but replay success 100->86.2% | ~ smooth/trim idle carefully, verify replay | L
[wave3] W3_XDiffusionTrainingDiffusionPoliciesonCro | Q13 data quality | real Franka 5 robot+100 human demos: robot-only < naive co-train < manually filtered < noise-gated (fig only; +16% avg over baselines); ~50% human demos infeasible | + filter/down-weight infeasible or low-quality demos | L
[wave3] W3_ZevaEgoEgocentricMidTrainingwithInContex | Q13 data | real: 10 robot demos + 50 task-matched human videos (same cam) -> +55/+40 pts; 10K h ego ~ 2K h robot (75.3 vs 74.7%) | ~ human video helps only with latent-action VLA machinery | L
[wave3] W3_WhenShouldWePreferOfflineReinforcementLe | Q13 data | sim image manip: CQL on noisy-expert 86-92% vs BC on expert 15-33% (weak single-step BC) | ~ perturbed/recovery data valuable with reward weighting | L
[wave3] W3_BlindfoldedExpertsGeneralizeBetterInsigh | Q13 data | real peg insertion, 400 demos/shape: unseen shapes plus/ellipse 20/17% (standard expert) -> 100/96% (SAM2-masked operator view) and 96/79% (moderate pixel noise) | + exploratory/corrective demos over clean shortest-path demos | M
[wave3] W3_BeyondViewpointGeneralizationWhatMultiVi | Q13 data | 10->640 demos: single-view plateaus, multi-view keeps rising (figure only) | + view diversity over more same-view demos | L
[wave3] W3_CRAFTVideoDiffusionforBimanualRobotDataG | Q13 data | pose-only diversity (2x demos) camera-shift 6->13, lighting 3->5 (/20) | ~ spatial diversity helps a bit, not visual robustness | L
[wave3] W3_FrequencyGuidedActionDiffusionviaSubFreq | Q13 data quality | human-demo jitter inherited by DP; filtering high freqs improves SR & jerk (sim) | + smooth/filter teleop actions | L
[wave3] W3_ManiFlowAGeneralRobotManipulationPolicyv | Q13 data | Lift Pot: 50 demos 64.7, 100 ~90, 200 97.7 (pi0 94.0 needs 500) | ~ 100-200 demos saturate single task | M
[wave3] W3_RLDGRoboticGeneralistPolicyDistillationv | Q13 data quality | OpenVLA VGA insertion 100% with 45 RL eps vs 300 human; human plateaus 90% at 900 demos on unseen; relabeling human states with RL actions recovers most gap | + action consistency/quality over quantity; trim hesitation | M
[wave3] W3_MimicIntentNotJustTrajectories | Q13 data | learning curve: MINT-30M 0.95 vs ACT 0.65 at 10k iters | ~ sample-efficient head | L
[wave3] W3_HiFlowTokenizationFreeScaleWiseAutoregre | Q13 data | 50 demos placement tasks best method 42-58% real | ~ 50 demos marginal for precise placement | L
[wave3] W3_ROPASyntheticRobotPoseGenerationforRGBDB | Q13 data | +100 extra demos did not reliably help ACT (RGB-D CLB 56.7->33.3; RGB CPID 17.3->10.3) | - more nominal demos; + recovery states | L
[wave3] W3_TacSushiTactileGroundedWorldActionModeli | Q13 data quality | 50 failed trials used for consequence targets with imitation masked (not isolated) | + reuse failures for aux targets, mask their actions | L
[wave3] W3_ReconcilingRealitythroughSimulationAReal | Q13 data | real book-on-shelf: BC 15 demos 10/0/0%, BC 50 demos 40/30/20%, RialTo(15 demos+sim RL) 90/70/60% (pose/distractor/disturbance) | + diversity & recovery coverage over count | M
[wave3] W3_TowardsAccessiblePhysicalAILoRABasedFine | Q13 data | SO-101 button press VLA LoRA: 20 eps 18%, 50 eps 45-52%, 100 eps 68-72%, 200 eps 74-76% (no trial counts; dubious model description) | + plan 100+ demos for VLA fine-tune | L
[wave4] W4_0ResourceAwareRobustManipulationviaTamin | Q13 data | heuristic DAgger (staged failure states) ≈ DAgger >> base SR; data quality swings SR 20-60% | + recovery demos, replay-ability QA | M
[wave4] W4_ArmnetBenchv01ParallelRealWorldEvaluatio | Q13 data | 50 demos → 60-86% best-case on simple tasks, 0% on cable_clip for all 7 policies | ~ 50 demos OK for pick-place only | M
[wave4] W4_BridgeVLAInputOutputAlignmentforEfficien | Q13 | 3 demos/task 95.4% vs 10 demos 96.9% real | + very few demos suffice for 3D keyframe policy | M
[wave4] W4_FP3A3DFoundationPolicyforRoboticManipula | Q13 | 80 demos (10 x 8 envs): scratch DP/DP3 ~1-2.5% wild; pretrained 82.5% | ~ diversity only pays off with pretraining at 80 demos | M
[wave4] W4_LatentActionasIntentionEnablesEfficientF | Q13 | real avg 25/50/100% data (50/100/200 demos): 40.0/56.3/67.5 vs 8.8/20.0/33.8 | ~ 50 demos insufficient for high SR even with WAM | M
[wave4] W4_AdversarialDataCollectionHumanCollaborat | Q13 data quality/diversity | pi0 real: 20% ADC data avg 0.65 vs 100% traditional 0.24; 100% ADC 0.89; trad 0.0 on varied positions | + perturbation/recovery demos, full-workspace coverage | M
[wave4] W4_AdaptiveCapacityAllocationforVisionLangu | Q13 data | 120 demos/task, side+wrist cams → 80-100% SR (15 trials) with SmolVLA full FT | ~ 100+ demos adequate for simple tasks | L
[wave4] W4_MOVEASimpleMotionBasedDataCollectionPara | Q13 data | real orange→tray: static 3.3% vs MOVE 23.3% @35k steps; 23.3 vs 36.7% @75k; Meta-World avg 22.2→39.1% equal timesteps | + move objects during demos / max spatial diversity | M
[wave4] W4_BehaviorCloningforActivePerceptionwithLo | Q13 data quantity | delta reaches 5/5 at 4 demos, absolute at 8 | ~ action repr affects demo efficiency | L
[wave4] W4_AttentionfromActionforActionEmergentVisu | Q13 data | Most-diverse 25 demos 61.6 ≈ Full-100 62.0 > Least-diverse 25 58.4 (sim) | + spatial coverage over count | L
[wave4] W4_SEVOSemanticEnhancedVirtualObservationfo | Q13 data diversity | varied backgrounds/lighting/distractors in demos: +9..21 pts ACT, +10..23 SmolVLA; SO-101, 100 trials/cond | + diversify collection environment | M
[wave4] W4_BitVLA1bitVisionLanguageActionModelsforR | Q13 data | 3B VLM-policy w/o robot pretraining: near-zero real success with 50 demos (figure) | - large un-pretrained backbone on 50 demos | L
[wave4] W4_MolmoAct2ActionReasoningModelsforRealwor | Q13 | real SO-100 zero-shot novel objects/random cam: MolmoAct2-SO 56.7 vs pi0-SO 45.3 vs SmolVLA 2.3 (15 trials, partial credit) | + filtered community SO-100 pretraining data | M
[wave4] W4_DoYouNeedProprioceptiveStatesinVisuomoto | Q13 data | state-free holds success at 50-100 eps where state-based collapses (fig only); 300 eps diverse-height data only 0.117 height gen with state | ~ diversity does not fix state shortcut | L
[wave4] W4_ControlVLAFewshotObjectcentricAdaptation | Q13 data quantity | 6 real tasks 11-20 demos: ControlVLA 76.7% vs DP 20.8%, ACT 5.0%; ControlVLA 80% at 20 demos (OrganizeToy) | + pretrained prior + object-centric for few demos | M
[wave4] W4_BimanualManipulationWithinan8GBBudgetZer | Q13 data | 100 demos varied pose -> 95% | ~ 100 demos adequate for single task | L
[wave4] W4_RefinementofAcceleratedDemonstrationsvia | Q13 | 1 demo x 30 noisy robot replays -> ACT 100% peg-in-hole at seen and ±3 cm unseen (20 rollouts each) | + noisy replay augmentation for narrow tasks | L
[wave4] W4_DecouplingSemanticsandGeometricGrounding | Q13 data | RoboTwin 50 demos randomized train+eval: DP 14.9 vs clean 42.3 | - 50 demos insufficient to learn clutter/lighting invariance from randomized data | L
[wave4] W4_EMMAGeneralizingRealWorldRobotManipulati | Q13 data quality | AdaMix hard-sample reweighting +10.9 (pi0) / +7.5 (pi0.5) pts over uniform | ~ reweight hard samples | L
[wave4] W4_DCODADiffusionforCoordinatedDualArmDataA | Q13 | +100 extra scripted demos: Lift Ball 56→48, Push Box 36→29 (no gain) vs aug gains | + state coverage over raw count | L
[wave4] W4_EasyMimicALowCostFrameworkforRobotImitat | Q13 data | SO100+: robot-only 10/20 traj 0.26/0.51 vs +100 human videos co-train 0.88; saturates ~50 videos, ~10 robot traj | + human-video co-training when robot demos scarce | M
[wave4] W4_ExploringPoseGuidedImitationLearningforR | Q13 data quality | same task, noisier demos: 100% → 60% | + demo consistency matters | L
[wave4] W4_WARPEDWristAlignedRenderingforRobotPolic | Q13 | 15 teleop + 15 human-video demos: 19/20/17/11/20 vs teleop-only 16/19/16/15/19; collection 5-8x faster | + mixing cheap human-video demos | M
[wave4] W4_FromFixedtoFreeCamerasCalibrationFreeVie | Q13 data | 5 views × 100 demos/task/view still collapses at 15° | - camera-diverse data collection as sole fix | L
[wave4] W4_InContextVLAEndowingVisionLanguageAction | Q13 data quantity | LIBERO 5/10/25/50 demos: BC 50.6/63.1/77.4/90.4 vs VLA-Talker 71.4/84.6/92.8/97.4 | + explicit spatial cues improve data efficiency | L
[wave4] W4_FOCAFutureOrientedConditioningforDataEff | Q13 data | LIBERO avg drops 94.6->77.6 (pi0), 92.5->77.3 (SmolVLA) from ~43 to ~5 demos/task | ~ steep few-shot cliff below ~20 demos | M
[wave4] W4_FOCAFutureOrientedConditioningforDataEff | Q05 synthetic data | DreamGen video + implicit loss 95.7 @40% vs IDM pseudo-actions no gain | + synthetic video only as rep-level signal | L
[wave4] W4_DreamGenUnlockingGeneralizationinRobotLe | Q13 | SO-100 tic-tac-toe: 13 real+40 neural 65% vs 50 real 40% (table parse) | + state/scene diversity over count | L
[wave4] W4_HoloBrain0TechnicalReport | Q13 data diversity | co-training with diverse Grasp-Anything data 72.4→75.0% avg; test-driven 2–3 s recovery clips | + targeted recovery/diversity data | L
[wave4] W4_GuidedActionFlowQGuidedInferenceforFlowM | Q13 data | IQL critic on 100 rollouts (47 succ/53 fail): 47.5% -> 85.0%, timeouts 13 -> 3 | + use failed/succ rollouts via critic | L
[wave4] W4_InfiNoVAInfiniteNovelViewAugmentationfor | Q13 data diversity | views 1→5→dense: 6→24→40% random-view P&P | + viewpoint diversity in data | M
[wave4] W4_LearningtoMoveBeforeLearningtoDoTaskAgno | Q13 data | 30 h autonomous random play + 200 demos beats 200 demos alone; Stage-1 8k/14k/20k eps -> 24.5/30.2/33.3 | + cheap self-play data | M
[wave4] W4_LatentPolicySteeringAnEfficientandFlexib | Q13 data quantity | DP needs >100 demos to match LPS@50; gains saturate 200–300 | ~ | L
[wave4] W4_HumanEgoZeroShotRobotLearningfromMinutes | Q13 | same policy: 30 min teleop 65% vs 30 min diverse human video 95%; ACT teleop 52.5% | + diversity over count | M
[wave4] W4_MaxQSelectiveImitationforHumanintheLoopO | Q13 data/recovery | real USB insert, 20 demos + HIL interventions: MCBC 96% in 1 h, ACT Q-chunk 99% in 0.5 h vs HIL-SERL 5 h | + human intervention (DAgger-style) data | L
[wave4] W4_Learningathousandtasksinaday | Q13 | MT3 3 demos/task > monolithic BC at 50 demos/task; MT-ACT+ 150 demos over 50 tasks ≈ 600 over 12 tasks (figure) | + structure in tiny data; + diversity for BC | M
[wave4] W4_PipetteAnEmbodiedSimulationPlatformBench | Q13 data | 30 demos: precision placement ≤60% for all models even with aug | ~ 30 demos too few for precise placement | L
[wave4] W4_SKILSemanticKeypointImitationLearningfor | Q13 data quantity | 10 demos SKIL (Pick 50, Handle 70, Fold 60) > baselines at 20 (max 40/50/60) | + structured input cuts demos ~2x | M
[wave4] W4_InterleaveVLAEnhancingRobotManipulationw | Q13 data | 3B VLA fine-tuned on 60 demos/task w/o pretraining: Lift 2.8% vs 69.4% with interleaved pretraining | - big model from few demos without pretraining | M
[wave4] W4_PhysicallybasedLightingGenerationforRobo | Q13 | relighting 10 vs 100 source demos: reach 0.9 vs 1.0 (Red light, 10 trials) | + few lighting-diverse samples suffice | L
[wave4] W4_MasqueradeLearningfromInthewildHumanVide | Q13 data diversity | Stack Pots OOD: 0/10/50/100% edited human video co-train -> 2/26/47/68% (25 rollouts) | + diverse off-domain data via co-training | M
[wave4] W4_ReShootGenerativeVisualDomainRandomizati | Q13 data diversity | Gen-only 77.0 vs Rec 96.9 vs Mix 96.5 LIBERO; in-dist real 14/20→10/20 with aug | ~ keep real data anchor; diversity > count | M
[wave4] W4_TheCurseofPrecisionADataScalingLawforHig | Q13 data | Peg c (limit precision): cautious corrective expert 2.35mm vs direct unambiguous expert 1.27mm; SR-vs-N slope −0.72 at 10mm vs −0.19 at 4mm | + clean decisive demos over hesitant ones; ~ more demos give diminishing returns near precision limit | M
[wave4] W4_WhatMattersWhenDiagnosingandImprovingCon | Q13 data | 100 clean demos: color competitors drop P(pick) to 39.2% with motor skill intact (lift 93.8) | - clean-only demos for distractor robustness | M
[wave4] W4_SpotlightingTaskRelevantFeaturesObjectCe | Q13 data (pretraining mix) | slot pretraining mix D+B+F real 0.56 vs single dataset 0.26–0.45 | ~ | L
[wave4] W4_SSIPolicyLearningStructuredSceneInterfac | Q13 data | 10 demos: DP 54.50 vs SSI 80.42 LIBERO; real spatial avg DP 43.3 vs 80.0 (20 rollouts) | + structured interface raises few-demo efficiency | M
[wave4] W4_XR1TowardsVersatileVisionLanguageActionM | Q13 data quantity | stage-1 pretrain data 1→100%: 29.2→65.0% | ~ | L
[wave4] W4_TaskPrototypeGuidedFlowMatchingforFewSho | Q13 data | 1/2/4/6-shot support after source training: 66.8/73.4/79.6/82.1 | ~ few-shot conditioning (not needed for our case) | L
[wave4] W4_TraceGenWorldModelingin3DTraceSpaceEnabl | Q13 data | 5 target videos: pretrained 80% vs scratch 25%; 15 videos 82.5 vs 30%; human phone videos 67.5% (10 trials/task) | + strong prior makes few demos suffice | L
[wave4] W4_VODPSemanticGeometricAdaptiveDiffusionPo | Q13 data | Pick Apple Messy 20 demos 3.0 -> 100 demos 80.0; steeper scaling than DP/DP3 | ~ foundation features need ~50-100 demos | L
[wave4] W4_WhatMattersinLearningfromLargeScaleDatas | Q13 data quantity/diversity | real DROID co-train: all-DROID 0% on 6 tasks vs aligned retrieval up to 85%; bin can spatial reset small 30% -> large 60% | + spatial coverage & aligned data over raw quantity | M
[wave4] W4_DIALDecouplingIntentandActionviaLatentWo | Q13 data | real OOD 58.3 with human EgoDex pretrain vs 26.7 without (trials unreported) | ~ human video pretraining helps OOD but needs big corpus | L
[wave4] W4_NovelDemonstrationGenerationwithGaussian | Q13 data | 800 generated ~ 200 real (87.3%); 1800 generated 94.7%; pose-only data doesn't help camera shift (9.5%) | + diversity along shift axis > count | M
[wave4] W4_PriorVLAPriorPreservingAdaptationforVisi | Q13 data | few/std/large demos Hard: pi0.5 20/42/59, PriorVLA 31/53/65; ID gain vanishes at large data | ~ priors matter most in low data | M
[wave4] W4_VisualSimtoRealLearningforRoboticInserti | Q13 data quality/diversity | pure BC 68.9 vs DAgger mixture 96.1; object-geometry diversity 79.4 -> 96.6 on seen design | + on-policy/recovery data, object diversity | M
[wave4] W4_XSimCrossEmbodimentLearningviaRealtoSimt | Q13 data | 1 min human video (sim-expanded) 90% vs 10 min teleop BC 70% on wide init distribution | ~ synthetic coverage beats few real demos | L
[wave4] W4_RoBridgeAHierarchicalArchitectureBridgin | Q13 data quality | w/o DAgger 82.1 -> 65.1 mean | + corrective on-policy data | M
[wave4] W4_SimulationDrivenImitationLearningforBios | Q13 data diversity | sim ACT: train rooms 2->8 unseen-room SR 44.2 -> 57.4; objects 10->100 26.8 -> 42.2 (saturates ~75) | + scene & object diversity | M
