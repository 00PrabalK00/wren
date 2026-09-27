# Q12_model_size — 109 ledger lines
[fulltext] BAKU | model_size | 4-31M equal; 114M severely worse on LIBERO-90 (50 demos/task) | - large from-scratch, + ~10-30M | M/H
[fulltext] OFT | from_scratch | DP from scratch ≥ RDT-1B on folding/scooping with 20-45 demos | + small from scratch viable | M
[fulltext] DP3 | encoder_size | tiny MLP point encoder > PointNeXt/PointTransformer | + small encoder | M
[fulltext] Theia | Q12 model size | 22–86M distilled encoder beats 300–630M VFMs on real WidowX | + small encoder | M
[fulltext] SmolVLA | model_size | 0.24/0.45/2.25B LIBERO 82.75/87.3/88.75; skip VLM top half ok | + ~0.45B frozen VLM | M
[fulltext] TinyVLA | model_size | real 5 tasks x100 demos: TinyVLA-S 0.4B 23.3 < DP 35.3 < B 77.4 < H 1.3B 94.0 (OpenVLA 68.3) | - <0.5B VLA from own VLM, + ~1B | M
[fulltext] VLA-Adapter | model_size | 0.5B no robot PT = 7B OFT (97.3 vs 97.1 LIBERO); 7B backbone +0.2 | + 0.5B VLM | M
[fulltext] X-VLA | model_size | LoRA 9M ~= pi0 full FT (LIBERO-Long 84.2 vs 85.2; WidowX 54.2 vs 55.7) | + ~0.9B + LoRA (8 GB-friendly, inferred) | M
[fulltext] Seer-PIDM | Q12 model size | OpenVLA-7B full FT at 100 demos 16.7% vs Seer 65M-trainable 60–78% | + small trainable (~65M) with frozen encoders | L/M
[fulltext] DataScalingLaws | model size | diffusion U-Net small/base/large 0.88/0.90/0.83 | + small action head | M
[fulltext] Hyper-DP3 | Q12 model_size | 2.52M params ≈ DP3 255.8M (5000-ep: 58.2 vs 59.3); RoboTwin 63.2 vs 55.2 | + tiny decoder (MLP-Mixer) | M/H
[fulltext] RoboVLMs-WhatMatters | Q12 model_size | Flamingo 0.1x data: 3B 0.13, 9B 0.83; but 2–3B KosMos/PaliGemma beat 9B VLMs | ~ pretraining quality > size | M
[fulltext] Octo | Q12 model size | zero-shot 10M<27M<93M; ~100-demo fine-tune avg Octo 72 vs 28M scratch 20 vs VC-1 15 | + pretrained 27–93M init; - big from-scratch transformer | M
[fulltext] HPT | Q12 model size | HPT-XL (227M) 76.7 vs HPT-B (12.6M) 70.0 finetuned | ~ small trunk sufficient, modest gain from size | L
[fulltext] OpenVLA | Q12 model size | fine-tuned 7B needs 60 GB (LoRA); int4 inference 7 GB at ~3 Hz; DP from scratch competitive on narrow tasks | - 7B VLA for 8 GB single-task | M
[fulltext] RDT-1B | Q12 model size | 166M vs 1.2B: unseen object 37.5 vs 50, scene 62.5 vs 62.5, instruction 25 vs 100 | ~ size matters mainly for language | L/M
[fulltext] CogACT | Q12 model size | action module 13M/89M/308M → 58.5/62.5/64.8 (log-linear, 7B backbone fixed) | ~ bigger head helps modestly | L/M
[fulltext] pi0 | Q12 model_size | pi0-small 470M from scratch viable only with 10k h; VLM-init gain confounded with size | ~ | L
[fulltext] GR00T-N1 | Q12 model_size | GR-1 sim 30/100/300 demos: GR00T 43.2/50.0/49.3 vs DP 21.3/32.7/40.4 | + pretrained large at low data (confounded by same embodiment) | M
[wave3] W3_AxisGuideGroundingRobotActionCoordinateS | Q12 model size / finetune | full-finetuned SmolVLA used as stronger baseline than frozen-VLM action-expert-only (figure only) | + full finetune of SmolVLA | L
[wave3] W3_DiffusionVLAGeneralizableandInterpretabl | Q12 model size | DiVLA 2B/7B/72B: sorting 66.2/74.9/82.4, bin-pick 63.7/66.7/75.9 (72B also more pretrain data) | + larger pretrained VLA (not feasible on 8GB) | M
[wave3] W3_LDA1BScalingLatentDynamicsActionModelvia | Q12 model size | LDA 0.5B 50.7 vs 1B 55.4; UWM 0.1B 14.2 vs 1B 19.3 (sim) | ~ (outside 8GB regime) | L
[wave3] W3_MaskedVisualPretrainingforMotorControl | Q12 model size | ViT-B encoder no better than ViT-S (figure only) | ~ small encoder enough | L
[wave3] W3_RecoveringAggressivelyPrunedVisionLangua | Q12 model size | 72%-pruned 7B student (1.86B) real PiPER 77.5% vs teacher 65.5% (200 eps, with KD); SFT-only 59.5% | + small backbones suffice for task-specific policies (with distillation) | M
[wave3] W3_PredictionwithActionVisualPolicyLearning | Q12 model size | B/2 128M 62.4, L/2 449M 68.4, XL/2 661M 72.5; XL/8 (17 tokens) 48.2 | ~ bigger helps in 50-task sim | L
[wave3] W3_RT2VisionLanguageActionModelsTransferWeb | Q12 | 5B from scratch "very poor"; co-FT > FT robot-only; 55B > 5B on unseen (figure-only) | + pretrained init; larger helps OOD but costs latency | M
[wave3] W3_VistaBotViewRobustRobotManipulationviaSp | Q12 model size | pi0 VGS 0.33 vs ACT 0.24 (sim), 0.27 vs 0.21 (real): large VLA barely more view-robust | - relying on VLA scale for viewpoint robustness | M
[wave3] W3_BeyondTaskSuccessBehavioralandRepresenta | Q12 model size | GPU mem at inference: pi0 8.6 GB, pi0.5 9.1 GB, X-VLA 7.1 GB, VLA-JEPA 5.5 GB | - pi0-class VLAs on 8 GB GPU | M
[wave3] W3_ADualProcessVLAEfficientRoboticManipulat | Q12 model size | BC-xfmr from scratch 0.476 vs fine-tuned OpenVLA-7B 0.098 (RoboCasa sim, 3000 demos/task) | + small from-scratch policy | L
[wave3] W3_CageCausalAttentionEnablesDataEfficientG | Q12 model size | DINOv2-L frozen+LoRA fine at 40-50 demos but 280 ms/step on RTX3090 | ~ large frozen encoder OK for data, bad for 8GB latency | L
[wave3] W3_WhatDoWeLearnfromaLargeScaleStudyofPreTr | Q12 model size | ViT-B > ViT-L in all 4 configs (best 73 vs 59) at 30-150 demos | + smaller encoder in low data | M
[wave3] W3_BridgeDataV2ADatasetforRobotLearningatSc | Q12 model size | larger GCBC image encoder strictly better at 60k traj (figure only) | ~ larger encoder at large data | L
[wave3] W3_TowardsSynergisticGeneralizedandEfficien | Q12 model size | 20M-param specialist + VLA prior: 5 demos 73.3% vs DP 20% vs ACT 0% (15 runs) | + small specialist | M
[wave3] W3_FlowingWithPurposeLatentActionGuidedFlow | Q12 model size | 0.11B scratch LAFM 86.7 > pi0 3.3B finetuned 71.7 (real, 15 trials/task) | + small task-specific policy | M
[wave3] W3_WhyDoesActionChunkingImproveBehavioralCl | Q12 | explicit ensemble of DPs: Transport 12.6 -> 41.5, ToolHang 75.2 -> 87.6 | + small ensembles if compute allows | M
[wave3] W3_FocusVLAFocusedVisualUtilizationforVisio | Q12 model size | 0.5B 98.7 LIBERO > 7B OpenVLA-OFT | + small | L
[wave3] W3_RethinkingthePracticalityofVisionlanguag | Q12 model size | CALVIN AvgLen 0.5B 3.65 vs 7B 3.75 (same arch) | + small (0.5B) VLA | M
[wave3] W3_OrderedActionTokensforVisuomotorPolicyLe | Q12 model size | 5M-param Transformer reaches 16/20 on 2 real tasks (single webcam, 10 Hz) | + tiny policies viable | L
[wave3] W3_PerceiverActorAMultiTaskTransformerforRo | Q12 model size | 8xV100 16 days training; real 53 demos/7 tasks 20-90% | - heavy voxel transformers for 8 GB | M
[wave3] W3_BAKUAnEfficientTransformerforMultiTaskPo | Q12 model size | LIBERO-90: 4.4M .85, 10M .90, 31M .87, 114M .19 | + ~10-30M policy for low data | M
[wave3] W3_pimathbfR2ReactiveRealtimeFlowPolicies | Q12 model size | GR00T-N1.7: VLM ~60 ms + 4-step DiT ~80 ms per call on A6000; needs 2 GPUs for async | + small policy to avoid latency | M
[wave3] W3_FastandAccurateAnAdaptiveVLAInferenceFra | Q12 model size | LIBERO 50 demos/task: BC-ViLT 86.95 vs pi0 94.15; full-workspace randomization 20 vs 56%; real dual-arm ACT 60% vs pi0 100% | ~ small ok in narrow distribution, large better under wide variation | M
[wave3] W3_SeedPolicyHorizonScalingviaSelfEvolvingD | Q12 model size | RoboTwin 50 demos: 33M SeedPolicy 40.1% clean vs 1.2B RDT 34.5%; Hard 4.3 vs 13.7 | + small for in-distribution; - small scratch for visual shift | M
[wave3] W3_PredVLAPredictiveSensorimotorModelingfor | Q12 model size | 0.68M trainable controller: 75.4% 4-suite LIBERO, 46 ms/step on 5090 | ~ tiny controllers viable on frozen features (sim only) | L
[wave3] W3_PolarNet3DPointCloudsforLanguageGuidedRo | Q12 model size | single-task de32 92.1 vs de64 91.0; multi-task de32 77.4 vs de64 89.3, L4 86.3 | ~ small for single task | L
[wave3] W3_ReasoningWithoutInferenceCostLatentSeman | Q12 model size | frozen 2B backbone at robot finetune -> 0% vs 85 full finetune | - freezing large VLA backbone | L
[wave3] W3_PVIPluginVisualInjectionforVisionLanguag | Q12 model size | 3B GR00T fine-tune on 50 demos only 35.7-39.8% sim avg | ~ big VLA not sufficient alone | L
[wave3] W3_ProgVLAProgressAwareRobotManipulationSki | Q12 model size | 0.1B no-robot-pretrain 91.1 LIBERO vs SmolVLA-2.25B 88.7; real PiPER 50 demos/task 68% (100 trials) | + ~100M model | M
[wave3] W3_SpatialVAMSpatialAwareMultiViewVideoDiff | Q12 model size | 5B Wan2.2 VAM needs >30 GB and 4.6 s/24-frame chunk on A100 | - video-foundation VAMs on 8 GB laptop | H
[wave3] W3_TunetoLearnHowControllerGainsShapeRobotP | Q12 model size | compliant gains -> higher val MSE but higher success | - select checkpoints by val loss | M
[wave3] W3_VisionLanguageFoundationModelsasEffectiv | Q12 model size | 10% data: 3B 0.05-0.13 vs 9B 0.83; full data 3B-IFT 4.09 vs 9B 3.97; full fine-tune 3B 0.50 vs partial 4.09 | ~ pretrained capacity helps, full FT collapses | L
[wave3] W3_VIMAGeneralRobotManipulationwithMultimod | Q12 model size | object tokens beat pixel tokenizers across 2M-200M, esp. low data (1% data ~ others 10%) (figure only) | + object-centric inputs for small models | L
[wave3] W3_vlasimdEfficientCPUInferenceforLanguageC | Q12 model size | SO-101, 44 demos/3 instr: 60M IMPACT 90/85/60% | + small (~60M) model | M
[wave3] W3_WhatistheBetterCurriculumControllerShape | Q12 model size | ACT 18M 95% = pi0.5 2B 95% ID with 30 demos (fragile cup) | + small model sufficient in-distribution | M
[wave3] W3_ActionControlNetALightweightDelayAwareAd | Q12 model size | Meta-World latency: Evo-1+ACNet 91 ms/11 Hz vs pi0 RTC 159 ms, Training-RTC 134 ms | + lightweight VLA for real-time | L
[wave3] W3_ContrastiveActionImagePretrainingforVisu | Q12 model size | frozen CAIP encoder ViT-B 47.9 / ViT-L 81.3 / SO400M 87.5 (3 tasks) | ~ bigger frozen encoder helps | L
[wave3] W3_XDistillCrossArchitectureVisionDistillat | Q12 model size | MW: ResNet18 90.7 vs ViT-S-Half(11M) 57.2 vs ConvNeXt 89M 86.6; real pi0 SFT 26.7 vs 75.6 | + small CNN encoder in low data | M
[wave3] W3_DecouplingtheDeclarativefromtheProcedura | Q12 model size | SO-101 in-domain: 55M-trainable w2VLA 95.1 vs pi0.5 (693M trainable) 95.8 | + small head over frozen encoders | M
[wave3] W3_ManiFlowAGeneralRobotManipulationPolicyv | Q12 model size | RoboTwin2 DR 50 demos: scratch ManiFlow 64.7/55.5/55.0/66.7 vs fine-tuned pi0 24.3/18.0/41.0/70.0 | + small scratch flow policy at 50 demos | M
[wave3] W3_MimicIntentNotJustTrajectories | Q12 model size | 30M scratch policy (frozen SigLIP+DINOv2): LIBERO 97.1 vs SmolVLA 88.8; LIBERO-Plus 69.5 vs pi0.5 65.0 | + small policy on frozen strong encoders | M
[wave3] W3_RealtimeVLAFLASHSpeculativeInferenceFram | Q12 model size | 110M regression draft w/ stale KV 58.4% vs 2.7B pi0 85.2% (LIBERO-10) | ~ tiny regression head weaker on long horizon | L
[wave3] W3_SutureBotAPrecisionFrameworkBenchmarkFor | Q12 model size | real dVRK, 10 trials: multitask ACT pickup/throw/knot 9/8/9, E2E 3/10 vs pi0 7/7/4, 0/10; GR00T 1/2/1; OpenVLA-OFT 0/0/0 | + small from-scratch ACT in out-of-domain low-data | M
[wave3] W3_SeeSelectivelyActAdaptivelyDualLevelStru | Q12 model size | LoRA 2x capacity 41.3 vs 41.9 baseline (no gain) | ~ capacity not bottleneck | L
[wave3] W3_TSMaskVLA2DTemporalSpatialMaskingforVisi | Q12 model size | 0.5B beats 7B OpenVLA-OFT on CALVIN (4.19 vs 4.10) | + small backbone | L
[wave4] W4_3DCAVLALeveragingDepthand3DContexttoGene | Q12 | 7B OFT-based, 4.3 Hz on A100 | - large VLA for 8GB budget | M
[wave4] W4_0ResourceAwareRobustManipulationviaTamin | Q12 model size | OpenVLA/GO-1/XVLA/UniVLA ~0 SR after 20h fine-tune; only π0/π0.5 viable | ~ large VLA choice matters | L
[wave4] W4_ArmnetBenchv01ParallelRealWorldEvaluatio | Q12 model size | SO-101, 50 demos, 12 tasks: π0.5 47.6, π0 35.1, GR00T 29.4, DP 26.7, ACT 19.2, Molmo 18.9, SmolVLA 15.0; pick-place: ACT 63 vs π0.5 67 vs SmolVLA 23 | + small ACT for simple pick-place; - SmolVLA | M
[wave4] W4_FP3A3DFoundationPolicyforRoboticManipula | Q12 | 365M 95/90 vs 1.3B 100/95 (Clean Table) | ~ mid-size nearly matches large | L
[wave4] W4_ImprovingtheperformanceofAIpoweredAfford | Q12 model size | ACT d=32/64 unstable w/o TE; gains saturate ~128-256 (SO-100-class arm, ~45 demos) | ~ don't shrink ACT below d=128 | L
[wave4] W4_MINERVAHowSmallCanaManipulationPolicyBea | Q12 model size | 0.54M 95.05, 1M 96.75, 10M 97.45 vs π0.5 97.5; 5M: new objects 62→96 on LIBERO-Plus | + small (1-10M) specialist | M
[wave4] W4_AdversarialDataCollectionHumanCollaborat | Q12 model size | ACT on ADC data: oscillatory grasping (qualitative) attributed to small capacity | ~ small models vs very diverse data | L
[wave4] W4_AdaptiveCapacityAllocationforVisionLangu | Q12 model size/FT | SmolVLA single-task PiPER 120 demos: LoRA r=8 0-27% vs r=128 80-100% vs Full FT 87-100%; SmolVLA FullFT ≈ π0 FullFT | + full FT / high-rank adapters of small VLA; - low-rank LoRA | M
[wave4] W4_ArtificialFoveatedPerceptionforMitigatin | Q12 model size | SmolVLA vs π0.5 similar OOD drops (Stack3 0.52 vs 0.61) | ~ size not the fix | L
[wave4] W4_LookWhereItMattersAdaptiveVisualRefineme | Q12 | 3B pi0 base, deploy on 24 GB 4090 | - large VLA for 8GB | M
[wave4] W4_ASystematicStudyofDataModalitiesandStrat | Q12 | 200-demo finetune: co-trained pretrain 90.2% vs scratch single-task -42.9% | + pretrained backbone | M
[wave4] W4_BeyondImplicitForceEvaluatingExplicitFor | Q12 model size | ACT d=512, chunk 100@50Hz works on real contact tasks | ~ | L
[wave4] W4_SEVOSemanticEnhancedVirtualObservationfo | Q12 model size | ACT 51.6M 95% (80 eps) vs SmolVLA 450M 83% (120 eps); SmolVLA fails <80 eps | + ACT-size over SmolVLA | M
[wave4] W4_BitVLA1bitVisionLanguageActionModelsforR | Q12 model size | LIBERO: BitVLA 3B/1.4GB 96.0 ≈ OFT 7.7B 97.1; OFT INT4 PTQ 96.9 at 4.7GB; SmolVLA 88.8 (Long 77.0) | + quantize a pretrained VLA; ~ SmolVLA weakest small VLA | L
[wave4] W4_ControlVLAFewshotObjectcentricAdaptation | Q12 model size | 29M DiT DROID-pretrained + 5M adapter; pi0 38.6% -> ControlVLA@pi0 81.3% | + small pretrained policy w/ adapters | L
[wave4] W4_BimanualManipulationWithinan8GBBudgetZer | Q12 model size | ACT 52.6M reaches 95% on SO-101 pick-place, 100 demos | + ~50M model sufficient | M
[wave4] W4_DecouplingVisionLanguageandActionforEffi | Q12 model size | 417M total/195M active: 55.6 sim, 66.0 real vs GR00T 3B 56.9/68.0; SmolVLA 450M 39.2 | + ~200M decoupled policy | M
[wave4] W4_SLIM05BLearningActionGroundedPredictiveL | Q12 | 0.47B: LIBERO 97.5 (OFT-7B 97.1), LIBERO-Plus 77.45 (OFT 69.6, pi0 69.3), CALVIN 4.556 | + ~0.5B compact policy sufficient | M
[wave4] W4_ChronosAPhysicsInformedFullHistoryFramew | Q12 model size | 0.3B (frozen backbone) 78% real vs pi0.5 7%; RoboTwin 70.0 vs pi0 48.8 (reported baselines) | + small model w/ frozen backbone | L
[wave4] W4_DCODADiffusionforCoordinatedDualArmDataA | Q12 | ~32 real demos: ACT 15/20 vs pi0-FAST LoRA 2/20 (Lift Ball) | + small model in low data | M
[wave4] W4_ExploringPoseGuidedImitationLearningforR | Q12 model size | DP 70 ms / RGBD-gated 140 ms on RTX 4060 | ~ DP feasible on 8 GB | L
[wave4] W4_CTVAMACerebelloThalamicInspiredVisionAct | Q12 model size | FM 68M 65.8 / 227M 76.9 / 758M 77.3 LIBERO; 68M CT-VAM 82.1 vs pi0 3.3B 86.0; real 100% vs pi0 95% | + ~70-230M policy | M
[wave4] W4_FOCAFutureOrientedConditioningforDataEff | Q12 model size | SmolVLA 92.5/90.3/77.3 vs pi0 94.6/89.9/77.6 at 100/40/10% | + small VLA ~ large in-distribution | M
[wave4] W4_HoloBrain0TechnicalReport | Q12 model size | real 10 tasks: 0.2B 74.8% vs 1.1B 77.2% vs π0.5 69.2% vs π0 45.4% | + small (~0.2B) pretrained model enough | M
[wave4] W4_LiMABridgingLongtermImaginationtoRealtim | Q12 model size | 2B+1B LiMA vs GR00T N1.6 on Stack cup 90 vs 85, Assemble 50 vs 50 | - big WAM no gain on short tasks | L
[wave4] W4_JEPAPolicyDiffusionFreeImitationLearning | Q12 model size | 44M params from scratch, <6 GiB train, 128px, 100 demos → 67% real | + small from-scratch model on 8GB | M
[wave4] W4_LatentPolicySteeringAnEfficientandFlexib | Q12 model size | sim: DP 550K 57.2% vs π0.5 3.6B 60.9%; real: DP 46.2% vs π0.5 68.8% at 50 demos | ~ real pretrained VLA helps; small DP competitive in sim | M
[wave4] W4_LightsCameraMalfunctionWhenIlluminationR | Q12 model size | SmolVLA > π0.5 on real color task (77.5 vs 47.5 no-aug) | + small VLA sufficient | L
[wave4] W4_PocketDP3EfficientPocketScale3DVisuomoto | Q12 model size | 1.73M-param DiM decoder: RoboTwin avg 71.6 vs DP3 (255M U-Net) 50.8; real Piper 50 demos avg +15.3 pts over DP3 | + tiny decoder in low-data | M
[wave4] W4_PipetteAnEmbodiedSimulationPlatformBench | Q12 model size | SmolVLA 71.8 vs π0 44.1 (augmented, 30 demos, sim) | + SmolVLA-size adequate/better than π0 in low data | L
[wave4] W4_MoEACTScalingMultiTaskBimanualManipulati | Q12 | dense ACT 84M 44.6 vs 0.9B 48.5; MoE-ACT 195M active 62.0 vs pi0 3.24B 56.9 (50 demos/task) | + small models; - dense scaling in low data | M
[wave4] W4_SynthICLScalableIncontextImitationLearni | Q12 model size | 512->256 dim smaller model 75.0 -> 64.8 | ~ too-small hurts | L
[wave4] W4_PatchPolicyEfficientEmbodiedControlviaDe | Q12 model size | ~50M policy beats 7.6B OpenVLA-OFT real (cable 0.70 vs 0.30, tool 0.90 vs 0.65) at 50–100 demos; DP trunk 22.8M→40.4M Push-T 0.07→0.83 | + small (~30–50M) policy on frozen features | M
[wave4] W4_SemanticVLASemanticAlignedSparsification | Q12 model size | 7B real AgileX 45-60 demos: 77.8 vs OFT 55.6 vs VQ-BeT/QueST 20 | ~ big-VLA only; no small-model data | L
[wave4] W4_ReShootGenerativeVisualDomainRandomizati | Q12 model size | 7B pretrained VLA still 0% under color shift | - size/pretraining gives appearance invariance | M
[wave4] W4_TheCurseofPrecisionADataScalingLawforHig | Q12 model size | U-Net width 64: no scaling (R²=0.22) vs width 256: R²=0.99 (Roll Ball, fig) | ~ adequate capacity needed | L
[wave4] W4_RobustBimanualVisionLanguageActionModels | Q12 | 0.5B VLA-Adapter+M3 62.7 vs pi0 39.5, RDT 30.2 (50 demos, clean) | + small VLA | L
[wave4] W4_TeachingTinyVLAModelsWheretoLookandHowto | Q12 | 0.25B XS-VLA 90.3 vs SmolVLA 2.25B 88.8, 0.5B 87.3 (LIBERO) | + tiny model with structure | M
[wave4] W4_XR1TowardsVersatileVisionLanguageActionM | Q12 model size | downstream-data only: 230M Light 42.5% vs full large 28.3% | + small model in low data | M
[wave4] W4_TaskPrototypeGuidedFlowMatchingforFewSho | Q12 model size | OpenVLA 50.1 vs ResNet-18 flow 59.8-82.1 @6-shot on SO-101 | + small models suffice | L
[wave4] W4_DIALDecouplingIntentandActionviaLatentWo | Q12 model size | frozen Qwen2.5-VL-3B + DiT (GR00T-style) only 21.8% few-shot | - big frozen VLM alone not sufficient | L
[wave4] W4_WhatstheMoveHybridImitationLearningviaSa | Q12 model size | fine-tuned OpenVLA worst on 3 precise real tasks (figure) | - large VLA for precise single-task | L
[wave4] W4_NovelDemonstrationGenerationwithGaussian | Q12 model size | ResNet-18 + GPT2-style transformer, 128x128, chunk 10 + TE reaches 80-95% | + small model sufficient | L
[wave4] W4_PriorVLAPriorPreservingAdaptationforVisi | Q12 model size / FT strategy | pi0.5 full FT vs frozen-prior adaptation: RoboTwin Hard 42 -> 53; real OOD 41 -> 57; real 10-demo OOD 10 -> 32 | + partial freezing of pretrained VLA over full FT | M
[wave4] W4_VisualSimtoRealLearningforRoboticInserti | Q12 model size | ImageNet ResNet-18 shared across 8 views + MLP achieves 91.3% real (150 trials) | + small encoder sufficient | L
