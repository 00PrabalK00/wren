W4_3DCAVLALeveragingDepthand3DContexttoGene | Q04 | LIBERO w/o depth 97.0 vs 98.1 seen, 41.0 vs 45.2 unseen (sim only, 7B VLA) | + depth point-cloud branch | L
W4_3DCAVLALeveragingDepthand3DContexttoGene | Q08 | w/o CoT-expanded instruction 42.4 vs 45.2 unseen LIBERO | + LLM step decomposition in instruction | L
W4_3DCAVLALeveragingDepthand3DContexttoGene | Q14 | w/o ROI pooling 41.4 vs 45.2 unseen, 98.2 vs 98.1 seen; real unseen 38 vs OFT 30.2 vs DP 21.8 | + task-object mask pooling for generalization | L
W4_3DCAVLALeveragingDepthand3DContexttoGene | Q02 | SE(3) waypoints > velocities on real Franka (stated, no numbers) | + absolute EE pose over velocity | L
W4_3DCAVLALeveragingDepthand3DContexttoGene | Q12 | 7B OFT-based, 4.3 Hz on A100 | - large VLA for 8GB budget | M
W4_0ResourceAwareRobustManipulationviaTamin | Q10 latency/smoothness | chunk-wise smoothing (drop stale + linear cross-fade) > sync/async/TE/RTC in most settings; +RTC best (figure only, π0.5, 3 garment tasks) | + async+crossfade | M
W4_0ResourceAwareRobustManipulationviaTamin | Q02 action space | delta joint < absolute joint on Task B; Task C most sensitive (figure only) | + absolute joint | M
W4_0ResourceAwareRobustManipulationviaTamin | Q13 data | heuristic DAgger (staged failure states) ≈ DAgger >> base SR; data quality swings SR 20-60% | + recovery demos, replay-ability QA | M
W4_0ResourceAwareRobustManipulationviaTamin | Q05 augmentation | flip+arm-swap/frame-skip aug: no significant gain on Task A alone | ~ spatio-temporal aug | L
W4_0ResourceAwareRobustManipulationviaTamin | Q12 model size | OpenVLA/GO-1/XVLA/UniVLA ~0 SR after 20h fine-tune; only π0/π0.5 viable | ~ large VLA choice matters | L
W4_ArmnetBenchv01ParallelRealWorldEvaluatio | Q12 model size | SO-101, 50 demos, 12 tasks: π0.5 47.6, π0 35.1, GR00T 29.4, DP 26.7, ACT 19.2, Molmo 18.9, SmolVLA 15.0; pick-place: ACT 63 vs π0.5 67 vs SmolVLA 23 | + small ACT for simple pick-place; - SmolVLA | M
W4_ArmnetBenchv01ParallelRealWorldEvaluatio | Q01 action head | DP 26.7 vs ACT 19.2 pooled; ACT>DP on eye_drops_to_basket 63 vs 43; ACT 2.5% bimanual | ~ task-dependent | L
W4_ArmnetBenchv01ParallelRealWorldEvaluatio | Q13 data | 50 demos → 60-86% best-case on simple tasks, 0% on cable_clip for all 7 policies | ~ 50 demos OK for pick-place only | M
W4_ArmnetBenchv01ParallelRealWorldEvaluatio | Q02 action space | all policies use absolute target joint positions on SO-101 (not ablated) | ~ absolute joint | L
W4_BridgeVLAInputOutputAlignmentforEfficien | Q04 | Real 10 demos/task, 13 tasks: BridgeVLA 96.9%, RVT-2 90% (3D) vs ACT 22.3%, pi0 3.8% (2D) — keyframe tasks | + 3D point-cloud input for low-data | M
W4_BridgeVLAInputOutputAlignmentforEfficien | Q01 | heatmap output 88.2 vs direct MSE position regression 31.4 (RLBench) | + spatial heatmap/classification head for keyframe pose | M
W4_BridgeVLAInputOutputAlignmentforEfficien | Q03 | adding per-pixel 3D pos features into VLM image tokens 88.2 -> 56.2 | - modifying pretrained encoder input distribution | M
W4_BridgeVLAInputOutputAlignmentforEfficien | Q13 | 3 demos/task 95.4% vs 10 demos 96.9% real | + very few demos suffice for 3D keyframe policy | M
W4_BridgeVLAInputOutputAlignmentforEfficien | Q14 | COLOSSEUM 64.0 vs RVT-2 56.7; camera-pose axis 51.8 vs RVT-2 64.4 (worst axis) | ~ 3D robust to lighting/bg, not camera shift | M
W4_BridgeVLAInputOutputAlignmentforEfficien | Q11 | single static ZED depth cam, real 96.9% | + single scene depth cam enough for keyframe pick-place | L
W4_FACTRForceAttendingCurriculumTrainingfor | Q07 history/proprio | excluding current joint state from input "greatly improves generalization" (stated, no numbers) | - proprio input | L
W4_FACTRForceAttendingCurriculumTrainingfor | Q14 robustness | vision-only ACT unseen objects 21.3% avg vs V+F 61.2% vs FACTR 87.5% (50 demos, 4 real tasks) | + non-visual contact signal/curriculum | M
W4_FACTRForceAttendingCurriculumTrainingfor | Q05 augmentation | best vision-noise aug 65% vs decaying-blur curriculum 77.7% test (pivot); constant blur 15-17/25 vs curriculum 17-21/25 | ~ noise aug; + curriculum | L
W4_FACTRForceAttendingCurriculumTrainingfor | Q01 action head | MSE regression on absolute joint chunk k=100, ACT arch w/o CVAE works at 50 demos | ~ regression | L
W4_FP3A3DFoundationPolicyforRoboticManipula | Q04 | Clean Table: FP3-Base point cloud 95/90 vs FP3-Base-Image (DINOv2) 90/55 in-domain/wild | + point cloud for OOD generalization | M
W4_FP3A3DFoundationPolicyforRoboticManipula | Q03 | pretrained FP3 95/82.5 vs scratch 30/1.25 in-domain/wild, 4 real tasks, 80 demos | + large-scale pretrained policy/encoder over scratch | H
W4_FP3A3DFoundationPolicyforRoboticManipula | Q12 | 365M 95/90 vs 1.3B 100/95 (Clean Table) | ~ mid-size nearly matches large | L
W4_FP3A3DFoundationPolicyforRoboticManipula | Q13 | 80 demos (10 x 8 envs): scratch DP/DP3 ~1-2.5% wild; pretrained 82.5% | ~ diversity only pays off with pretraining at 80 demos | M
W4_FP3A3DFoundationPolicyforRoboticManipula | Q14 | DP fails completely at ~30 deg camera shift; calibrated point cloud robust (figure only) | + world-frame 3D for camera shift | M
W4_FP3A3DFoundationPolicyforRoboticManipula | Q06 | chunk 16 / execute 8 at 15 Hz; no ablation | ~ | L
W4_GroundingSimtoRealGeneralizationinRoboti | Q05 augmentation | camera-pose/table-height DR largest real gains (e.g. Click Bell clean 2.7 → CP 23.5, TH 36.9, all 49.7%); frame-wise > episode-wise (CP +2.7..8.4, BG up to +12.9 pts) | + geometric/viewpoint aug, per-frame | M
W4_GroundingSimtoRealGeneralizationinRoboti | Q14 robustness | distractors largest real drop, lighting smallest (OpenVLA-OFT, >10k real trials) | ~ lighting less critical for big pretrained encoders | M
W4_GroundingSimtoRealGeneralizationinRoboti | Q11 cameras | ±1cm camera pose randomization gives +10-20 pts real SR vs clean | + viewpoint randomization | M
W4_ImprovingGenerativeBehaviorCloningviaSel | Q10 | SG+adaptive chunking: +23.25% avg over DP, +12.27% over BID (6 sim tasks, 3 seeds); real SO-100 moving-cup 70%; BID 16 Hz halting vs ours 29 Hz smooth | + similarity-gated chunk switching / self-guidance | M
W4_ImprovingGenerativeBehaviorCloningviaSel | Q06 | EMA temporal ensembling 0.456 vs vanilla 0.496 Push-T; EMA below vanilla on real SO-100; EMA lambda task-sensitive | - temporal ensembling with diffusion heads | M
W4_ImprovingGenerativeBehaviorCloningviaSel | Q01 | Push-T: CFG 0.070, vanilla 0.496, AutoGuidance 0.735, self-guidance 0.873 | ~ diffusion head + past-obs guidance; avoid CFG | M
W4_ImprovingGenerativeBehaviorCloningviaSel | Q07 | 2-frame history; prev obs as negative guidance gives future extrapolation | + short history usable at inference | L
W4_ImprovingtheperformanceofAIpoweredAfford | Q07 history/memory | phase token (t/T) on ACT: fetching 50.0/69.9/79.9 → 83.3/86.6/93.3 (dims 128/256/512), trials unreported | + phase/progress signal | L
W4_ImprovingtheperformanceofAIpoweredAfford | Q12 model size | ACT d=32/64 unstable w/o TE; gains saturate ~128-256 (SO-100-class arm, ~45 demos) | ~ don't shrink ACT below d=128 | L
W4_ImprovingtheperformanceofAIpoweredAfford | Q10 smoothness | TE removes jitter of small models but slows motion | ~ TE | L
W4_LIFDAnchoredDiffusionfor3DAwareSceneMemo | Q07 history/memory | no-memory ablation 93.6→74.8% LIBERO-Spatial (occlusion-style tasks) | ~ memory only for partial observability | L
W4_LIFDAnchoredDiffusionfor3DAwareSceneMemo | Q14 robustness | RoboTwin clean-trained: Easy 63.2% → randomized Hard 19.4% | + diverse demos/aug needed | M
W4_LIFDAnchoredDiffusionfor3DAwareSceneMemo | Q04 3D/depth | RGB geometry-aware (VGGT) features, real UR5e 10 demos: LIFD 56.0 vs Lift3D 34.5 vs DP 31.0 vs OpenVLA 40.5 | ~ RGB geometry priors vs depth | L
W4_LatentActionasIntentionEnablesEfficientF | Q09 | latent-action intention aux: RoboCasa few-shot 65.6 vs Fast-WAM 56.0; real 50 demos 40.0 vs 8.8; perturbing latents 80.8->52.2 | + future latent-action prediction used at test time | M
W4_LatentActionasIntentionEnablesEfficientF | Q14 | LIBERO-Plus camera shift 69.2 vs Fast-WAM 24.9, Joint-WAM 47.2, pi0 13.8 | + future-aware aux for viewpoint robustness | L
W4_LatentActionasIntentionEnablesEfficientF | Q13 | real avg 25/50/100% data (50/100/200 demos): 40.0/56.3/67.5 vs 8.8/20.0/33.8 | ~ 50 demos insufficient for high SR even with WAM | M
W4_LatentActionasIntentionEnablesEfficientF | Q10 | latency/chunk A800: 196.5 (Fast-WAM), 338.5 (LAWA), 593.1 ms (Joint-WAM) | - video-DiT WAMs for laptop | M
W4_MINERVAHowSmallCanaManipulationPolicyBea | Q01 action head | flow→L1 regression +0.34 (95.63±1.08 → 95.97±0.80, 3 seeds), L1 3.8x faster | + L1 regression (small model) | M
W4_MINERVAHowSmallCanaManipulationPolicyBea | Q06 chunking | chunk 16 best; 8: -3.16, 32: -2.20; exec 1-2 steps > 4 > 8 | + chunk ~0.8s, execute 1-2 + TE | M
W4_MINERVAHowSmallCanaManipulationPolicyBea | Q10 latency/smoothness | TE 96.3 > BID 95.0 > plain 94.1 > RTC 91.8; 0.54M L1: 2.2 ms GPU / 5.1 ms CPU vs SmolVLA 118/1010 ms | + tiny model + replan-every-step + TE | M
W4_MINERVAHowSmallCanaManipulationPolicyBea | Q12 model size | 0.54M 95.05, 1M 96.75, 10M 97.45 vs π0.5 97.5; 5M: new objects 62→96 on LIBERO-Plus | + small (1-10M) specialist | M
W4_MINERVAHowSmallCanaManipulationPolicyBea | Q03 vision encoder | scratch CNN LIBERO-Plus light 1.1-6.5%, background 4.7-9.3%, camera 11.5-34.6% | - scratch encoder for robustness | M
W4_MINERVAHowSmallCanaManipulationPolicyBea | Q05 augmentation | random crop only → photometric robustness ≈0 at all scales | + photometric aug needed | M
W4_MINERVAHowSmallCanaManipulationPolicyBea | Q07 history | 1→2 obs steps: +6 Goal, +4 Long (7M, single run) | + short history | L
W4_MINERVAHowSmallCanaManipulationPolicyBea | Q08 language | task-ID embedding matches language VLAs; permutation → 6.5% | + task ID for closed task set | M
W4_AdversarialDataCollectionHumanCollaborat | Q13 data quality/diversity | pi0 real: 20% ADC data avg 0.65 vs 100% traditional 0.24; 100% ADC 0.89; trad 0.0 on varied positions | + perturbation/recovery demos, full-workspace coverage | M
W4_AdversarialDataCollectionHumanCollaborat | Q14 robustness | dynamic object moves: trad 0.0 vs ADC 0.88 (10 trials) | + data-side robustness via perturbations | M
W4_AdversarialDataCollectionHumanCollaborat | Q11 cameras | masked camera avg: trad 0.0 vs ADC 0.55 | + occlusion-rich data for camera redundancy | L
W4_AdversarialDataCollectionHumanCollaborat | Q12 model size | ACT on ADC data: oscillatory grasping (qualitative) attributed to small capacity | ~ small models vs very diverse data | L
W4_AdaptiveCapacityAllocationforVisionLangu | Q12 model size/FT | SmolVLA single-task PiPER 120 demos: LoRA r=8 0-27% vs r=128 80-100% vs Full FT 87-100%; SmolVLA FullFT ≈ π0 FullFT | + full FT / high-rank adapters of small VLA; - low-rank LoRA | M
W4_AdaptiveCapacityAllocationforVisionLangu | Q03 vision encoder | learned adapter rank highest in vision tower (fig); OOD embodiment needs higher rank | + fine-tune vision encoder for new robot/cameras | L
W4_AdaptiveCapacityAllocationforVisionLangu | Q13 data | 120 demos/task, side+wrist cams → 80-100% SR (15 trials) with SmolVLA full FT | ~ 100+ demos adequate for simple tasks | L
W4_ArtificialFoveatedPerceptionforMitigatin | Q09 auxiliary objectives | attention-mask aux loss: real π0.5 OOD Drawer 0.30→0.67, Lamp 0.20→0.53 (30 trials); sim SmolVLA Kitchen OOD 0.18→0.51 | + attention grounding aux loss (PCGrad) | M
W4_ArtificialFoveatedPerceptionforMitigatin | Q14 robustness | direct fine-tune loses 0.3–0.6 abs under distractors across SmolVLA/OpenVLA/π0.5/Motus | + explicit task-relevance grounding | M
W4_ArtificialFoveatedPerceptionforMitigatin | Q03 vision encoder | SmolVLA attention Soft-IoU w/ task mask only 0.12 after fine-tune; pretrained VLM backbones still shortcut | - "pretrained VLM = robust" | M
W4_ArtificialFoveatedPerceptionforMitigatin | Q12 model size | SmolVLA vs π0.5 similar OOD drops (Stack3 0.52 vs 0.61) | ~ size not the fix | L
W4_LookWhereItMattersAdaptiveVisualRefineme | Q03 | pi0 LIBERO avg 94.2 -> +4 registers ~97.2; removing learned registers -4.45 avg; <4 registers can be below baseline | + register tokens when fine-tuning ViT encoder | L
W4_LookWhereItMattersAdaptiveVisualRefineme | Q11 | single third-person RealSense: uncertainty-gated high-res crop 46.5 -> 69.0% real (with registers) | + close-range/high-res detail of interaction region matters | L
W4_LookWhereItMattersAdaptiveVisualRefineme | Q12 | 3B pi0 base, deploy on 24 GB 4090 | - large VLA for 8GB | M
W4_LookWhereItMattersAdaptiveVisualRefineme | Q10 | crop triggered ~30% of replans, ~1.4-1.6x compute | ~ uncertainty-gated extra compute | L
W4_ASystematicStudyofDataModalitiesandStrat | Q10 | real jerky chunk boundaries fixed by uniform avg of last 4 overlapping chunks, 0.146 s latency (qualitative) | + temporal ensembling | M
W4_ASystematicStudyofDataModalitiesandStrat | Q08 | robot-only VLA training loses all language generation / VLM benchmark ability; VL co-train (9:1) restores | - robot-only finetune of VLM when language needed | M
W4_ASystematicStudyofDataModalitiesandStrat | Q01 | FAST/VQ/latent-action token co-training no significant gain, FAST hurts unseen tasks | + continuous flow head, - discrete token aux | M
W4_ASystematicStudyofDataModalitiesandStrat | Q14 | final co-trained model 72.6% sim unseen (+36.4%); DS gains from VL+cross-embodiment data | ~ needs large co-train data | L
W4_ASystematicStudyofDataModalitiesandStrat | Q12 | 200-demo finetune: co-trained pretrain 90.2% vs scratch single-task -42.9% | + pretrained backbone | M
W4_MOVEASimpleMotionBasedDataCollectionPara | Q13 data | real orange→tray: static 3.3% vs MOVE 23.3% @35k steps; 23.3 vs 36.7% @75k; Meta-World avg 22.2→39.1% equal timesteps | + move objects during demos / max spatial diversity | M
W4_MOVEASimpleMotionBasedDataCollectionPara | Q14 robustness | static DP: randomizing obj 67.5 → +target 44.7 → +camera 31.7% (sim) | + camera/pose diversity in data | L
W4_BehaviorCloningforActivePerceptionwithLo | Q02 action space | toy wrist-cam task: 4 demos delta 5/5 vs absolute 0/5 (test MSE 6.2 vs 189 e-3); both 5/5 at >=8 demos; absolute snaps to trained poses | + step-wise joint delta | L
W4_BehaviorCloningforActivePerceptionwithLo | Q13 data quantity | delta reaches 5/5 at 4 demos, absolute at 8 | ~ action repr affects demo efficiency | L
W4_BehaviorCloningforActivePerceptionwithLo | Q11 cameras | 64x64 wrist RGB only suffices for centering task (5/5) | + low-res wrist cam | L
W4_BeyondImplicitForceEvaluatingExplicitFor | Q02 action space | leader-target ACT vs follower-state target: Wipe 60→15%, Bottle 50→25%, Plug 30→0% (real ALOHA, 10–20 trials) | + absolute leader joint targets | M
W4_BeyondImplicitForceEvaluatingExplicitFor | Q09 aux inputs (torque) | motor-current torque in state: Wipe 60→90, Plug 30→70, Bottle 50→70 | + log/add servo current for contact phases | L
W4_BeyondImplicitForceEvaluatingExplicitFor | Q12 model size | ACT d=512, chunk 100@50Hz works on real contact tasks | ~ | L
W4_AttentionfromActionforActionEmergentVisu | Q05 augmentation | real xArm: Seeker mask-guided overlay+crop OOD avg 60.0 vs MirrorAug 11.7 vs RVT2-crop 20.0 (20 trials) | + foreground-preserving/mask-guided overlay over uniform overlay | M
W4_AttentionfromActionforActionEmergentVisu | Q14 robustness | real ID 76.7 vs 48.3; lighting+bg OOD 60.0 vs 20.0; retention 78% vs 41% | + ROI crop of scene cam from frozen DINO attention | M
W4_AttentionfromActionforActionEmergentVisu | Q03 vision encoder | frozen DINOv3 readout alone → near-0 control success; good as ROI localizer; FiLM-only box 39.4 vs crop 61.2 | ~ frozen DINO for where-to-look, trainable encoder for control | L
W4_AttentionfromActionforActionEmergentVisu | Q11 cameras | wrist view not cropped; wrist fragile under over-exposure, needs scene view | ~ keep scene+wrist | L
W4_AttentionfromActionforActionEmergentVisu | Q13 data | Most-diverse 25 demos 61.6 ≈ Full-100 62.0 > Least-diverse 25 58.4 (sim) | + spatial coverage over count | L
W4_AttentionfromActionforActionEmergentVisu | Q04 3D | DP3 manual crop ≪ RGB DP on MimicGen at 200 demos; ROI filtering +24-42 pts | - point cloud (for rotation-heavy tasks) | L
W4_BFAHierarchicalBestFeatureAwareTokenPrun | Q10 | pi0 real 5.8→9.4 Hz with 768→241 visual tokens, SR 0.27→0.48 (5 tasks x20) | + supervised token pruning for speed | M
W4_BFAHierarchicalBestFeatureAwareTokenPrun | Q14 | RoboTwin2 OOD lighting/bg/clutter pi0 0.328→0.405; unsupervised DART 0.208 | + suppress background tokens (supervised) | M
W4_BFAHierarchicalBestFeatureAwareTokenPrun | Q09 | object/gripper mask BCE aux; w/o Intra-IP Cup 0.48→0.35 | + object-grounding aux loss | L
W4_BFAHierarchicalBestFeatureAwareTokenPrun | Q11 | wrist occlusion only fatal during manipulation phase; dropping wrist tokens Hammer 0.84→0.73 | + wrist cam | M
W4_BreakingtheVisionActionShortcutLatentInt | Q14 robustness | LIT real MolmoAct2 (100 demos/task): lighting OOD 53.3->70.0, camera OOD 30.0->46.7, distractors 50.0->63.3; LIBERO-Plus +3.9..+10.7 over 4 archs | + pose-supervised visual bottleneck / image-free action prior | M
W4_BreakingtheVisionActionShortcutLatentInt | Q09 aux objectives | LIBERO-Plus: baseline+pose aux 65.45 vs base 63.62 vs full LIT 71.92; removing pose loss from LIT 68.86 | ~ aux pose target only works with restricted pathway | M
W4_BreakingtheVisionActionShortcutLatentInt | Q11 cameras | camera-config shift still weakest: real 46.7% (LIT) vs 30.0% base; sim camera 39.4->48.4 (MolmoAct2) | ~ viewpoint shift remains hard | L
W4_ARWAMAVisualConditionedAgentReadyWorldAc | Q08 language | RoboTwin avg SR: bbox+skill token 87.2 vs text 74.2 vs box+text 84.6; AdaLN 87.2 vs cross-attn 73.4 | + spatial prompt / AdaLN, - raw text | M
W4_ARWAMAVisualConditionedAgentReadyWorldAc | Q09 aux objectives | no foresight 78.6, no reasoning 79.4, raw-patch future target 76.4 vs full 87.2 | + compressed latent future aux, - raw feature recon | M
W4_ARWAMAVisualConditionedAgentReadyWorldAc | Q03 encoder | frozen DINOv3 0.3B + 0.2B trainable reaches 87.2 sim / 71.7 real | ~ frozen DINO ok (no ablation) | L
W4_ARWAMAVisualConditionedAgentReadyWorldAc | Q07 history/proprio | cross-attn relies 35.6% on proprio vs AdaLN 15.5% (shortcut) | ~ beware proprio shortcut | L
W4_ARWAMAVisualConditionedAgentReadyWorldAc | Q10 latency | 14.09 ms/chunk (4090) vs pi0.5 62 ms via KV-cache reuse | + compact flow w/ KV reuse | M
W4_SEVOSemanticEnhancedVirtualObservationfo | Q13 data diversity | varied backgrounds/lighting/distractors in demos: +9..21 pts ACT, +10..23 SmolVLA; SO-101, 100 trials/cond | + diversify collection environment | M
W4_SEVOSemanticEnhancedVirtualObservationfo | Q14 robustness | no-SEVO ACT 75→30→0% (train/novel/extreme), SEVO ACT 95/85/10 | + diverse data + object overlay | M
W4_SEVOSemanticEnhancedVirtualObservationfo | Q12 model size | ACT 51.6M 95% (80 eps) vs SmolVLA 450M 83% (120 eps); SmolVLA fails <80 eps | + ACT-size over SmolVLA | M
W4_SEVOSemanticEnhancedVirtualObservationfo | Q03 vision encoder | fully trainable ResNet-18 (ACT) adapts better than frozen SigLIP (SmolVLA) at ~100 demos | + trainable/fine-tuned encoder | L
W4_SEVOSemanticEnhancedVirtualObservationfo | Q11 cameras | adding wrist cam: ACT 90→86, SmolVLA 79→12 (mobile base, oscillation/grasp-release failures) | - wrist cam (mobile-base caveat) | L
W4_SEVOSemanticEnhancedVirtualObservationfo | Q05 augmentation | YOLO mask overlay +3 pts, generalizes to other bottle brands (qualitative) | + detector-mask object highlight | L
W4_SEVOSemanticEnhancedVirtualObservationfo | Q10 latency | SmolVLA ~2 min/grasp on Orin NX, ACT real-time | - SmolVLA on edge | M
W4_BitVLA1bitVisionLanguageActionModelsforR | Q12 model size | LIBERO: BitVLA 3B/1.4GB 96.0 ≈ OFT 7.7B 97.1; OFT INT4 PTQ 96.9 at 4.7GB; SmolVLA 88.8 (Long 77.0) | + quantize a pretrained VLA; ~ SmolVLA weakest small VLA | L
W4_BitVLA1bitVisionLanguageActionModelsforR | Q10 latency | A100 latency: BitVLA 73ms, π0 86ms, DP 90ms, RDT 297ms, OFT+ 321ms | + low-bit inference for VLAs | M
W4_BitVLA1bitVisionLanguageActionModelsforR | Q01 action head | L1 chunk regression (OFT parallel decoding) 96% LIBERO with pretrained 3B backbone | ~ L1 regression ok with big pretrained backbone | L
W4_BitVLA1bitVisionLanguageActionModelsforR | Q13 data | 3B VLM-policy w/o robot pretraining: near-zero real success with 50 demos (figure) | - large un-pretrained backbone on 50 demos | L
W4_MolmoAct2ActionReasoningModelsforRealwor | Q10 | CUDA Graphs + cache: flow VLA 23.0 -> 55.8 Hz on H100; discrete token path 3.94x slower | + CUDA-graph/caching of flow loop; continuous head for speed | H
W4_MolmoAct2ActionReasoningModelsforRealwor | Q01 | per-layer KV-conditioned flow expert 95.9 vs hidden-state 94.0; flow samples K=8 95.9 vs K=1 94.15 (LIBERO) | + flow expert with multiple flow-time samples | M
W4_MolmoAct2ActionReasoningModelsforRealwor | Q03 | action-expert-only tuning (frozen VLM) 93.05 vs full FT 97.20; LoRA 96.25 | - frozen backbone for control | M
W4_MolmoAct2ActionReasoningModelsforRealwor | Q13 | real SO-100 zero-shot novel objects/random cam: MolmoAct2-SO 56.7 vs pi0-SO 45.3 vs SmolVLA 2.3 (15 trials, partial credit) | + filtered community SO-100 pretraining data | M
W4_MolmoAct2ActionReasoningModelsforRealwor | Q14 | OOD overall 50.69 vs OFT 39.89 vs pi0.5 27.01; lighting 62.05; spatial placement 26.25 (worst) | ~ lighting robustness via diverse pretraining+color aug; spatial OOD hard | L
W4_MolmoAct2ActionReasoningModelsforRealwor | Q02 | absolute joint pose, 1 s chunks (30 steps @30 Hz) for SO-100 | + absolute joint targets | L
W4_DoYouNeedProprioceptiveStatesinVisuomoto | Q07 history/state input | pi0 height gen w/ state 0 vs w/o 0.984; horiz 0 vs 0.584; ACT 0/0.084 vs 0.933/0.517; DP 0/0 vs 0.867/0.533; in-domain equal (1.0) | - proprio state input / + state-free or state-noise | M
W4_DoYouNeedProprioceptiveStatesinVisuomoto | Q02 action space | state-free: rel EEF 0.984/0.584 height/horiz vs abs EEF, rel joint, abs joint all 0/0 | + relative EEF delta | M
W4_DoYouNeedProprioceptiveStatesinVisuomoto | Q11 cameras | dual wide wrist w/o overhead 1.0/1.0 vs with overhead 0.983/0.583; overhead-only 0.217/0.133; 20 cm holder shift 0.80 w/o vs 0 with overhead | + wide-FoV wrist cam, - scene cam under placement shift | M
W4_DoYouNeedProprioceptiveStatesinVisuomoto | Q14 robustness | avg height gen 0->85%, horizontal 6->64% removing state; background change still needs re-finetune | + state-free for spatial shift | M
W4_DoYouNeedProprioceptiveStatesinVisuomoto | Q13 data | state-free holds success at 50-100 eps where state-based collapses (fig only); 300 eps diverse-height data only 0.117 height gen with state | ~ diversity does not fix state shortcut | L
W4_ControlVLAFewshotObjectcentricAdaptation | Q14 robustness | 20 demos OrganizeToy ID 90%; unseen objects avg 70%, unseen background 60% with SAM2 mask object-centric condition | + object-centric mask conditioning | M
W4_ControlVLAFewshotObjectcentricAdaptation | Q13 data quantity | 6 real tasks 11-20 demos: ControlVLA 76.7% vs DP 20.8%, ACT 5.0%; ControlVLA 80% at 20 demos (OrganizeToy) | + pretrained prior + object-centric for few demos | M
W4_ControlVLAFewshotObjectcentricAdaptation | Q01 action head | 11-20 demos: DP 20.8% vs ACT 5.0% vs Octo 1.6% | + diffusion over CVAE/regression in tiny data | L
W4_ControlVLAFewshotObjectcentricAdaptation | Q12 model size | 29M DiT DROID-pretrained + 5M adapter; pi0 38.6% -> ControlVLA@pi0 81.3% | + small pretrained policy w/ adapters | L
W4_BimanualManipulationWithinan8GBBudgetZer | Q01 action head | SO-101 bimanual, 100 demos: ACT 19/20 @100k steps vs Diffusion Policy 0/10 @200k (LeRobot defaults) | + ACT/CVAE under compute budget, - DP w/o tuning | M
W4_BimanualManipulationWithinan8GBBudgetZer | Q12 model size | ACT 52.6M reaches 95% on SO-101 pick-place, 100 demos | + ~50M model sufficient | M
W4_BimanualManipulationWithinan8GBBudgetZer | Q10 latency | Orin Nano: FP32 114 ms -> TRT FP16 17.9 ms -> INT8 12.7 ms; success 19/18/19 of 20 | + TensorRT FP16 | M
W4_BimanualManipulationWithinan8GBBudgetZer | Q06 chunking | chunk 100 fully executed (10 s open loop @10Hz) -> 95% on quasi-static task | ~ long exec horizon ok for static pick-place | L
W4_BimanualManipulationWithinan8GBBudgetZer | Q13 data | 100 demos varied pose -> 95% | ~ 100 demos adequate for single task | L
W4_ViewpointAgnosticManipulationPolicieswit | Q11 cameras | DP Pick&Place across viewpoints: base 37.0 → Vantage 83.2; VR 8 random views 42.6 (< VR-1 63.8); real ACT reach 44 vs 30-36 | + few targeted extra viewpoints, - many random views | L
W4_ViewpointAgnosticManipulationPolicieswit | Q05 augmentation | generated novel-view aug (5 views) 52.3 < Vantage 83.2 (sim DP) | ~ generative view aug | L
W4_CLASSContrastiveLearningviaActionSequenc | Q09 auxiliary objectives | DTW action-seq contrastive pretrain: real random-camera DP 0.10→0.60, 0.00→0.65, 0.05→0.55 (20 trials) | + action-similarity contrastive aux | M
W4_CLASSContrastiveLearningviaActionSequenc | Q11 cameras | +wrist cam Dyn-Cam Square: BC 21→66%, CLASS 68→90% | + wrist camera | M
W4_CLASSContrastiveLearningviaActionSequenc | Q03 vision encoder | DP random-init vs ImageNet: 3-Stack DynCam 0.28 vs 0.61; PushT rand-color 0.16 vs 0.53; R3M < ImageNet | + ImageNet-pretrained ResNet over scratch/R3M | M
W4_CLASSContrastiveLearningviaActionSequenc | Q05 augmentation | color jitter on rand-color Push-T: BC 53→78% | + photometric aug | M
W4_CLASSContrastiveLearningviaActionSequenc | Q14 robustness | camera-varied training data alone: real ImageNet-DP final ≤0.10 on 3 tasks | - relying on data diversity alone | M
W4_RefinementofAcceleratedDemonstrationsvia | Q13 | 1 demo x 30 noisy robot replays -> ACT 100% peg-in-hole at seen and ±3 cm unseen (20 rollouts each) | + noisy replay augmentation for narrow tasks | L
W4_RefinementofAcceleratedDemonstrationsvia | Q06 | erasing ~65% vs better direct playback; temporal ensembling suspected to damp corrections (no ablation) | - temporal ensembling for fast reactive motion | L
W4_CoLAFlowPolicyTemporallyCoherentImitatio | Q01 action head | long-horizon real: raw 1-step Flow 20%, VQ-latent flow 70%, continuous GRU-VAE latent flow 80%; real avg 77.5 vs RDP 70.0 vs DP3 57.9 | + generative head in continuous latent action space | M
W4_CoLAFlowPolicyTemporallyCoherentImitatio | Q10 latency/smoothness | latency 8.6ms (latent flow) vs 6.5 raw flow vs ~30ms DP3/RDP (4080); smoothness −93.7% vs raw flow | + latent-space 1-step flow for smooth real-time; - raw 1-step flow | M
W4_CoLAFlowPolicyTemporallyCoherentImitatio | Q04 3D | single fixed L515 point cloud, 30 demos: own encoder 85% vs DP3 encoder 70% | ~ point cloud viable; encoder matters | L
W4_CoLAFlowPolicyTemporallyCoherentImitatio | Q11 cameras | removing wrist cam: perturbation recovery 90% → 30% | + wrist camera | M
W4_AugmentedRealityforRObotsARROPointingVis | Q14 robustness | DP vanilla collapses (~0-0.3) under background/distractor shift vs ARRO ~0.75-1.0 (fig, 10 trials); pi0 distractor cube 30->90%; cross-emb DP 0->99% | + segment gripper+object onto fixed background | L
W4_AugmentedRealityforRObotsARROPointingVis | Q05 augmentation | grid background ARRO > black mask in real (pi0 90 vs 70%); does not fix lighting | + segmentation-based background canonicalization | L
W4_AugmentedRealityforRObotsARROPointingVis | Q10 latency | GroundingDINO+GPT-4o init + SAM2 tracking per frame; no latency reported | - extra perception in loop | L
W4_DecouplingVisionLanguageandActionforEffi | Q01 action head | params-matched heads on DINOv3+NeoBERT: DP 53.8, FM 54.7, ACT 52.4, MeanFlow 55.6 (18 RoboCasa tasks x100) | ~ head choice minor; + one-step MeanFlow for speed | M
W4_DecouplingVisionLanguageandActionforEffi | Q03 vision encoder | DINOv3 ConvNeXt-B frozen 32.6 vs fine-tuned 55.6; DINOv3 ViT-B 54.1, SigLIP-400M 53.9, Qwen3-VL ViT 51.8 | + fine-tuned DINOv3 | H
W4_DecouplingVisionLanguageandActionforEffi | Q08 language | none 11.3, one-hot 37.4, T5 44.5, BERT 47.8, NeoBERT frozen 55.6, Gemma2 55.0 (held-out paraphrases) | + frozen modern text encoder, cached tokens | M
W4_DecouplingVisionLanguageandActionforEffi | Q06 chunking | H16/replan8 55.6, H8/4 55.9, H4/2 52.7, H1 50.6 | + chunk 8-16 replan half; per-step only -5 | M
W4_DecouplingVisionLanguageandActionforEffi | Q10 latency | forward pass DEM 6.1 ms vs SmolVLA 99.3, pi0.5 103.3, GR00T 51.8 ms (RTX PRO 6000) | + decoupled small policy + 1-step head | H
W4_DecouplingVisionLanguageandActionforEffi | Q12 model size | 417M total/195M active: 55.6 sim, 66.0 real vs GR00T 3B 56.9/68.0; SmolVLA 450M 39.2 | + ~200M decoupled policy | M
W4_ClutterRobustVisionLanguageActionModelst | Q14 | pi0 4-distractor 5%→85%, unseen objs 11%→78% with object masking+masked depth (100 real trials) | + object-centric input masking | H
W4_ClutterRobustVisionLanguageActionModelst | Q04 | masked depth vs masked RGB: unseen objs 70→78 (2-stage), 57→69 (1-stage); seen clutter ~flat | + depth for novel-appearance objects | M
W4_ClutterRobustVisionLanguageActionModelst | Q05 | simple single-stage masking alone: 5→71 (seen clutter), 11→57 (unseen) without clutter data | + background/distractor removal by segmentation | M
W4_ClutterRobustVisionLanguageActionModelst | Q06 | 10 Hz exec horizon H=5/10/15/20 → pick-place 81/85/76/56 | + ~1 s execution horizon | M
W4_ClutterRobustVisionLanguageActionModelst | Q08 | fine-tuned pi0/pi0-FAST/pi0.5 grasp absent-target >75% (ignore instruction); OBEYED ~95% rejection | - relying on VLA FT for language grounding | H
W4_ClutterRobustVisionLanguageActionModelst | Q10 | perception adds seg 0.04+VLM 0.41+depth 0.18 s; pi0 0.15 s; cycle 0.62-0.78 s | ~ cost of modular grounding | M
W4_CrossViewActionConsistencyforCameraRobus | Q11 cameras | nominal-only VLA camera-track 16.8% vs multi-view 79.8–87.2%; real held-out cam 53.3→74.4% (90 rollouts) | + synchronized multi-view scene cams in training | M
W4_CrossViewActionConsistencyforCameraRobus | Q09 auxiliary objectives | cross-view flow-velocity consistency +7.4pp sim (3 seeds), shuffled pairs collapse to 25.8% | + cross-view action consistency loss | M
W4_CrossViewActionConsistencyforCameraRobus | Q14 robustness | mixed-camera SFT 74.7% vs consistency 87.2%; fails to extrapolate to 15° elevation | ~ data diversity alone insufficient | M
W4_CrossViewActionConsistencyforCameraRobus | Q05 augmentation | pair-consistent spatial aug 84.9 vs independent 80.9 | ~ | L
W4_DecouplingSemanticsandGeometricGrounding | Q08 language | real Aloha 100 demos: SVP-IL (SAM3 mask feature-fusion into DP) 60.0 vs π0 FT 31.7 vs DP 28.3; sim custom lang tasks 39.5 vs π0 24.0 vs ACT 2.8 | + decoupled segmenter-mask grounding over end-to-end language | M
W4_DecouplingSemanticsandGeometricGrounding | Q13 data | RoboTwin 50 demos randomized train+eval: DP 14.9 vs clean 42.3 | - 50 demos insufficient to learn clutter/lighting invariance from randomized data | L
W4_DecouplingSemanticsandGeometricGrounding | Q14 robustness | randomized scenes: SVP-IL 24.0 vs DP 14.9 | ~ masks help but not sufficient | L
W4_DecouplingSemanticsandGeometricGrounding | Q03 vision encoder | mask via early 4-ch concat 43.4 / pixel overlay 50.1 vs mid-feature addition 67.8 (sim) | - early channel fusion into pretrained stem | L
W4_CronusVLATowardsEfficientandRobustManipu | Q07 history | SimplerEnv: single-frame 31.0, naive 7-frame stack 32.4, cached-feature history+decoder 70.9; no current-frame modulator 63.5; frame count inverted-U (best 4-7) | + short cached feature history, - naive stacking | M
W4_CronusVLATowardsEfficientandRobustManipu | Q14 robustness | SimplerEnv-OR R-Score 86.9 vs CogACT 72.1, pi0 49.4; cyclic full-occlusion 35.4 vs 4.2 | + history for transient occlusion | M
W4_CronusVLATowardsEfficientandRobustManipu | Q01 action head | DiT diffusion 70.9 vs SiT flow 67.6 vs MLP 51.8 (large data) | ~ generative > MLP at scale | L
W4_CronusVLATowardsEfficientandRobustManipu | Q10 latency | cached features 8.73 Hz vs naive multi-frame 3.09 Hz (7B) | + feature caching | M
W4_EMMAGeneralizingRealWorldRobotManipulati | Q05 augmentation | unseen object appearance, avg SR 3 real tasks: pi0 no-aug 30% vs Cosmos-Transfer 50% vs DreamTransfer 65% vs +AdaMix 79.2%; best at 50% generated ratio | + generative appearance augmentation (<=50% synthetic) | M
W4_EMMAGeneralizingRealWorldRobotManipulati | Q14 robustness | Fold Clothes (50 demos, 1 shirt) unseen shirts: 10% -> 65% (pi0) with generated appearance variety | + data-side appearance diversity for novel objects | M
W4_EMMAGeneralizingRealWorldRobotManipulati | Q13 data quality | AdaMix hard-sample reweighting +10.9 (pi0) / +7.5 (pi0.5) pts over uniform | ~ reweight hard samples | L
W4_SLIM05BLearningActionGroundedPredictiveL | Q09 | latent IDM+FDM stage w/ EMA target: LIBERO-Plus 77.45 vs 66.82 no-EMA; CALVIN 4.556 vs 4.382; Stage1>Stage2-only (fig) | + latent forward/inverse dynamics pretraining on own demos | M
W4_SLIM05BLearningActionGroundedPredictiveL | Q12 | 0.47B: LIBERO 97.5 (OFT-7B 97.1), LIBERO-Plus 77.45 (OFT 69.6, pi0 69.3), CALVIN 4.556 | + ~0.5B compact policy sufficient | M
W4_SLIM05BLearningActionGroundedPredictiveL | Q10 | H100 latency 60.6 ms/4.26 GiB vs pi0.5 193 ms/7.94 GiB vs Fast-WAM 361 ms/13.6 GiB | + compact non-VLM flow policy for latency | M
W4_SLIM05BLearningActionGroundedPredictiveL | Q03 | fine-tuned DINOv2-B/14 (lr 1e-5) scene+wrist, no ablation | + fine-tuned DINOv2 | L
W4_SLIM05BLearningActionGroundedPredictiveL | Q14 | LIBERO-Plus camera 70.73 vs pi0 61.0, OFT 56.4; real background SLIM 49 vs pi0.5 54 vs Fast-WAM 2 | ~ latent predictive aux helps camera/light; background still hard | L
W4_DissectingMotionPriorRegularizationforDa | Q10 smoothness | 15 demos insertion: min-jerk loss 70/80 vs none 66/80 vs generic smooth 67/80 (CIs overlap); intra-chunk only | ~ jerk penalty small/non-sig, no boundary fix | L
W4_DissectingMotionPriorRegularizationforDa | Q09 aux objectives | speed-curvature prior +0 on top of min-jerk (70 vs 70/80) | ~ motion priors weak | L
W4_DepthCacheDepthGuidedTrainingFreeVisualT | Q10 latency | π0.5 191→143 ms (1.33×), real 55/60→52/60; perturbation recovery 17.4→13.7 s | ~ token compression small gain; small model better for 2 s gap | L
W4_DepthCacheDepthGuidedTrainingFreeVisualT | Q04 3D/depth | depth-partitioned merging vs uniform: −18.2% if depth partition removed (LIBERO) | ~ depth as foveation prior | L
W4_ChronosAPhysicsInformedFullHistoryFramew | Q01 action head | ALOHA insertion 50 demos, same encoder: diffusion 66 / flow 72 / regression 76 / IMLE 86 / IMLE+2nd-order bridge 90% | ~ regression >= flow/diffusion in low data | L
W4_ChronosAPhysicsInformedFullHistoryFramew | Q07 history | real memory tasks pi0.5 0/150 vs full-history SSM 108/150; RMBench 11.2 vs 73.6% | + full history only for aliased/memory tasks | M
W4_ChronosAPhysicsInformedFullHistoryFramew | Q10 smoothness | pi0.5 stop-and-go jitter vs acceleration-field chunks smooth (qualitative); 1-step 84 vs 3-5 steps 90% | + second-order/smooth action parameterization | L
W4_ChronosAPhysicsInformedFullHistoryFramew | Q04 depth | D435 point cloud too noisy for small blocks -> used single RGB + frozen ResNet18 in real | - D435 point clouds for small objects | L
W4_ChronosAPhysicsInformedFullHistoryFramew | Q12 model size | 0.3B (frozen backbone) 78% real vs pi0.5 7%; RoboTwin 70.0 vs pi0 48.8 (reported baselines) | + small model w/ frozen backbone | L
W4_DCODADiffusionforCoordinatedDualArmDataA | Q05 | wrist-view diffusion aug + corrective labels: ACT sim Lift Ball 56→73.3, Push Box 36→56; real Lift Drawer 7→14/20 | + generative recovery-state aug | M
W4_DCODADiffusionforCoordinatedDualArmDataA | Q13 | +100 extra scripted demos: Lift Ball 56→48, Push Box 36→29 (no gain) vs aug gains | + state coverage over raw count | L
W4_DCODADiffusionforCoordinatedDualArmDataA | Q12 | ~32 real demos: ACT 15/20 vs pi0-FAST LoRA 2/20 (Lift Ball) | + small model in low data | M
W4_DCODADiffusionforCoordinatedDualArmDataA | Q01 | pi0-FAST produced sudden large actions on augmented OOD states | - discrete action tokens | L
W4_GeneralizableHierarchicalSkillLearningvi | Q04 3D/depth | GemBench zero-shot mean 82.3 (3 demos, object point cloud) vs RVT-2 46.5, BridgeVLA 58.9 (100 demos); real 9/10 vs 4/10 w/ distractors | + segmented object point cloud from depth | M
W4_GeneralizableHierarchicalSkillLearningvi | Q02 action space | object-frame canonicalized trajectories: 0.83 vs no canonicalization 0.12 (5-task ablation) | + object-relative actions | M
W4_GeneralizableHierarchicalSkillLearningvi | Q14 robustness | real novel teabag 9/10 vs 6/10; with distractors 9/10 vs 4/10 (3 vs 30 demos) | + object-centric input | L
W4_EasyMimicALowCostFrameworkforRobotImitat | Q13 data | SO100+: robot-only 10/20 traj 0.26/0.51 vs +100 human videos co-train 0.88; saturates ~50 videos, ~10 robot traj | + human-video co-training when robot demos scarce | M
W4_EasyMimicALowCostFrameworkforRobotImitat | Q05 augmentation | hand recolor removed 0.87->0.40; partial mask 0.27 | + full visual randomization of embodiment gap | L
W4_EasyMimicALowCostFrameworkforRobotImitat | Q14 robustness | unseen green duck 0.50->0.80, pink cube 0.20->0.50 with human data | + data diversity via human video | L
W4_EasyMimicALowCostFrameworkforRobotImitat | Q02 action space | shared vs separate human/robot action heads 0.47 vs 0.87 (abs EE pose) | ~ embodiment-specific heads | L
W4_EasyMimicALowCostFrameworkforRobotImitat | Q08 language | LC 4-combo task 0.40 (20 robot) -> 0.90 (co-train) | ~ language ok w/ pretrained VLA | L
W4_E0EnhancingGeneralizationandFineGrainedC | Q14 robustness | LIBERO camera perturbation avg: π0 19.7→50.8, E0 66.5→83.9 with spherical warp view augmentation | + geometric view (camera-rotation warp) augmentation | M
W4_E0EnhancingGeneralizationandFineGrainedC | Q05 augmentation | spherical warp aug +31.1 (π0) / +22.6 (E0) pts under camera shift, no extra data | + camera-warp augmentation | M
W4_E0EnhancingGeneralizationandFineGrainedC | Q01 action head | discrete Tweedie diffusion vs π0 flow: LIBERO-Long 92.2 vs 85.2; real 8 tasks avg 45.6 vs 43.1 (mixed per task); π0-FAST AR 10.0 real | ~ discrete diffusion ≈ flow; - AR tokens | L
W4_E0EnhancingGeneralizationandFineGrainedC | Q06 chunking | action horizon 10–20 steps best on LIBERO (fig) | ~ moderate horizon | L
W4_ExploringPoseGuidedImitationLearningforR | Q04 3D/depth | relative 6D pose DP 81.7% ID vs RISE point cloud 3.3%, ACT 1.7% (sub-mm insertion, 10 trials) | ~ object-centric pose for precision only | L
W4_ExploringPoseGuidedImitationLearningforR | Q13 data quality | same task, noisier demos: 100% → 60% | + demo consistency matters | L
W4_ExploringPoseGuidedImitationLearningforR | Q12 model size | DP 70 ms / RGBD-gated 140 ms on RTX 4060 | ~ DP feasible on 8 GB | L
W4_WARPEDWristAlignedRenderingforRobotPolic | Q05 | rendered demos without aug: 0/20 on 3 of 5 tasks, Can 8 vs 17/20 with object/gripper/camera-extrinsic/appearance aug | + pose/appearance/camera augmentation | M
W4_WARPEDWristAlignedRenderingforRobotPolic | Q11 | wrist-only DP: WARPED 20/18/17/11/17 vs teleop 16/19/16/15/19 (x/20); novel obj Rotate Obj2 8/10 vs teleop 2/10 | + wrist camera for object-instance generalization | L
W4_WARPEDWristAlignedRenderingforRobotPolic | Q13 | 15 teleop + 15 human-video demos: 19/20/17/11/20 vs teleop-only 16/19/16/15/19; collection 5-8x faster | + mixing cheap human-video demos | M
W4_WARPEDWristAlignedRenderingforRobotPolic | Q14 | bg distractors small drop (Pour 18->15, Wipe 11->9); unseen scenes 16/20 with 50 demos over 20 tabletops | + scene diversity in demos for OOD scenes | L
W4_FromFixedtoFreeCamerasCalibrationFreeVie | Q14 robustness | real Franka: π0 63.3→53.3→39.3→16.0 at 0/5/10/15° cam rotation (5-view trained); CamVLA 79.0→29.3; sim single-view π0 65.3→6.3 at 15° | - relying on model to tolerate camera shift; + fixed camera mount / geometry-aware methods | H
W4_FromFixedtoFreeCamerasCalibrationFreeVie | Q02 action space | RLBench unseen views: camera-frame delta EE 51.4 vs base-frame delta 33.2 | + camera-frame deltas (needs EE control) | L
W4_FromFixedtoFreeCamerasCalibrationFreeVie | Q11 cameras | train-view spacing 15/30/45°: π0 33.2/25.5/16.8, CamVLA 51.4/34.0/21.2 | + dense viewpoint coverage if multi-view training | M
W4_FromFixedtoFreeCamerasCalibrationFreeVie | Q13 data | 5 views × 100 demos/task/view still collapses at 15° | - camera-diverse data collection as sole fix | L
W4_InContextVLAEndowingVisionLanguageAction | Q14 robustness | sim held-out: unseen obj BC 54.8 vs tool-evidence 85.1; +distractors 47.6 vs 80.3 | + explicit object localization input | L
W4_InContextVLAEndowingVisionLanguageAction | Q08 language | LIBERO: generate CoT 81.5 (359 ms) vs inject evidence action-only loss 97.4 (73 ms) | - generative CoT; + injected grounded text | M
W4_InContextVLAEndowingVisionLanguageAction | Q13 data quantity | LIBERO 5/10/25/50 demos: BC 50.6/63.1/77.4/90.4 vs VLA-Talker 71.4/84.6/92.8/97.4 | + explicit spatial cues improve data efficiency | L
W4_CTVAMACerebelloThalamicInspiredVisionAct | Q10 latency/async | FCI async: RTX 4080 56.8 ms fully hidden (20 Hz eff.), exec 8.33->6.41 s, success 100 vs 95% (20 trials); Jetson 200 ms, exec 10.24->7.23 s | + async + flow-consistent overlap inpainting | M
W4_CTVAMACerebelloThalamicInspiredVisionAct | Q12 model size | FM 68M 65.8 / 227M 76.9 / 758M 77.3 LIBERO; 68M CT-VAM 82.1 vs pi0 3.3B 86.0; real 100% vs pi0 95% | + ~70-230M policy | M
W4_CTVAMACerebelloThalamicInspiredVisionAct | Q06 chunking | H=8, overlap 4 @20 Hz with 30 demos real; not ablated | ~ short chunk + overlap | L
W4_CTVAMACerebelloThalamicInspiredVisionAct | Q08 language | one-hot task token instead of LM, LIBERO 82.1 | + compact task token for few tasks | L
W4_CTVAMACerebelloThalamicInspiredVisionAct | Q03 vision encoder | DINOv3-S+ backbone, 30 demos, 100% pouring (20 trials); not ablated | + pretrained DINO small backbone | L
W4_FOCAFutureOrientedConditioningforDataEff | Q09 aux objectives | LIBERO 10% data: pi0 77.6 -> FOCA 85.3; 40%: 89.9 -> 94.0; latent obj-centric > pixel (91.4/90.9 vs 93.3 explicit-only) | + latent future aux, - pixel prediction | M
W4_FOCAFutureOrientedConditioningforDataEff | Q13 data | LIBERO avg drops 94.6->77.6 (pi0), 92.5->77.3 (SmolVLA) from ~43 to ~5 demos/task | ~ steep few-shot cliff below ~20 demos | M
W4_FOCAFutureOrientedConditioningforDataEff | Q05 synthetic data | DreamGen video + implicit loss 95.7 @40% vs IDM pseudo-actions no gain | + synthetic video only as rep-level signal | L
W4_FOCAFutureOrientedConditioningforDataEff | Q12 model size | SmolVLA 92.5/90.3/77.3 vs pi0 94.6/89.9/77.6 at 100/40/10% | + small VLA ~ large in-distribution | M
W4_DreamGenUnlockingGeneralizationinRobotLe | Q05 | SO-100 GR00T N1 10-13 real demos: 21→45.5% avg with video-model neural trajectories (10 trials/task) | + generative synthetic demos (if compute) | L
W4_DreamGenUnlockingGeneralizationinRobotLe | Q07 | zero-state neural trajs → less proprio overfitting, fewer stuck-at-home failures on SO-100 (qualitative) | + proprio dropout/zeroing | L
W4_DreamGenUnlockingGeneralizationinRobotLe | Q13 | SO-100 tic-tac-toe: 13 real+40 neural 65% vs 50 real 40% (table parse) | + state/scene diversity over count | L
W4_GeneralizableRoboticInsertionwithWorldMo | Q11 cameras | sim RL: wrist cam placement with more occlusion of socket lowers success (figure only); blind policy much worse | ~ place wrist cam to avoid object occluding target | L
W4_HoloBrain0TechnicalReport | Q10 latency/smoothness | SimpleRTC async (prefix inpaint first d steps + blend) beats sync on cloth folding; teacher-forcing 5% hurts, 25% default | + async + prefix-inpainting + TF training | M
W4_HoloBrain0TechnicalReport | Q12 model size | real 10 tasks: 0.2B 74.8% vs 1.1B 77.2% vs π0.5 69.2% vs π0 45.4% | + small (~0.2B) pretrained model enough | M
W4_HoloBrain0TechnicalReport | Q13 data diversity | co-training with diverse Grasp-Anything data 72.4→75.0% avg; test-driven 2–3 s recovery clips | + targeted recovery/diversity data | L
W4_HoloBrain0TechnicalReport | Q04 3D/depth | depth+camera-param 3D PE in VLA; no isolating ablation | ~ | L
W4_HybridFlowA2NFEGenerativePolicyforRealTi | Q01 action head | real Franka ~300 demos: MeanFlow-1NFE 0%, DDIM-2 ≈0%, ReFlow-2 5.0%, DDIM-16 42.1%, HybridFlow-2NFE 70.1% (M-avg) | + generative head with enough/structured steps; - naive 1-2 step flow/diffusion | M
W4_HybridFlowA2NFEGenerativePolicyforRealTi | Q10 latency | Jetson Thor action-gen 19ms vs 152ms (DDIM-16); static PP 86.3 vs 63.8 under async execution | + minimize action-generation latency even for static tasks | M
W4_HybridFlowA2NFEGenerativePolicyforRealTi | Q03 vision encoder | DINOv3-base fine-tuned end-to-end, wrist fisheye only, works in real (no ablation) | ~ fine-tuned DINOv3 viable | L
W4_HybridFlowA2NFEGenerativePolicyforRealTi | Q14 robustness | unseen object color: 68.8 vs 86.3 ID (HybridFlow); 47.5 vs 63.8 (DDIM-16) | ~ ~20-pt drop on color shift | L
W4_LanguageGuidedObjectCentricDiffusionPoli | Q04 3D/depth | RLBench 21 tasks 40 demos: object-only point cloud 68.7 vs DP3 scene pc 43.6 vs RGB DP 39.3 | + segmented object point cloud | M
W4_LanguageGuidedObjectCentricDiffusionPoli | Q14 robustness | real camera view shift: object-centric no drop vs RGB DP fails entirely (figure/qualitative) | + object-centric 3D for camera shift | L
W4_LanguageGuidedObjectCentricDiffusionPoli | Q03 vision encoder | point encoders: MLP+res 68.8, MLP 64.1, PointNet 14.9 (7 tasks) | + simple MLP point encoder | M
W4_GuidedActionFlowQGuidedInferenceforFlowM | Q14 robustness | frozen SmolVLA with 1 distractor 0/11 vs QGF 6/12; nominal 19/40 -> 34/40 | - SmolVLA brittle to distractors; + critic guidance | L
W4_GuidedActionFlowQGuidedInferenceforFlowM | Q13 data | IQL critic on 100 rollouts (47 succ/53 fail): 47.5% -> 85.0%, timeouts 13 -> 3 | + use failed/succ rollouts via critic | L
W4_GuidedActionFlowQGuidedInferenceforFlowM | Q01 action head | flow head allows Q-gradient guidance at sampling, beta=2 | ~ generative head enables test-time steering | L
W4_FastinSlowADualSystemFoundationModelUnif | Q04 3D input | RLBench System-1 input: +point cloud 0.69 vs no PC 0.61 vs no PC/no img 0.44 | + point cloud as extra input | L
W4_FastinSlowADualSystemFoundationModelUnif | Q10 latency | slow:fast 1:1 0.60 / 1:2 0.63 / 1:4 0.69 / 1:8 0.61; 21.9 Hz vs pi0 13.8 Hz | + dual-rate (slow features reused over steps) | L
W4_FastinSlowADualSystemFoundationModelUnif | Q06 chunking | H=1/2/4/8: 0.69/0.68/0.66/0.69 on keyframe RLBench | ~ chunk size irrelevant for keyframe actions | L
W4_FastinSlowADualSystemFoundationModelUnif | Q14 robustness | real 20 trials: FiS 0.80 -> obj 0.65 / bg 0.60 / light 0.55; pi0 0.65 -> 0.40/0.40/0.35 | - pretraining scale alone does not give robustness at 100 demos | L
W4_InfiNoVAInfiniteNovelViewAugmentationfor | Q11 cameras | SO-101+SmolVLA (wrist+scene), 70 demos: ref view 65.3% → random views 7.5%; 5 physical views 24% (P&P) | + multi-view training / rigid camera mount | H
W4_InfiNoVAInfiniteNovelViewAugmentationfor | Q05 augmentation | 3DGS novel-view aug 40.5% vs VISTA generative NVS 7.5% vs none 7.5% (100 rollouts) | + geometry-consistent NVS; - single-image generative NVS | M
W4_InfiNoVAInfiniteNovelViewAugmentationfor | Q14 robustness | SmolVLA −88.5% relative under unseen viewpoints | - relying on VLA pretraining for camera robustness | H
W4_InfiNoVAInfiniteNovelViewAugmentationfor | Q13 data diversity | views 1→5→dense: 6→24→40% random-view P&P | + viewpoint diversity in data | M
W4_LiMABridgingLongtermImaginationtoRealtim | Q10 latency | H100 chunk latency: Cosmos-Policy 600 ms vs LiMA 325 ms; w/o async 450 ms same SR 80% | - video WAMs for laptop; + async slow/fast split | M
W4_LiMABridgingLongtermImaginationtoRealtim | Q09 aux objectives | w/o future visual intent: Cook Rice 61.7 vs 78.3, Stack Cup 76.7 vs 93.3 (3 seeds x 20) | ~ future-prediction helps in large WAM | L
W4_LiMABridgingLongtermImaginationtoRealtim | Q12 model size | 2B+1B LiMA vs GR00T N1.6 on Stack cup 90 vs 85, Assemble 50 vs 50 | - big WAM no gain on short tasks | L
W4_FLASHEfficientVisuomotorPolicyviaSparseS | Q10 | C1-continuous Legendre chunks: tracking err 4.7x lower than FM-DiT (spikes at chunk boundaries); 31.4 ms per episode inference | + continuity-constrained chunk param. | M
W4_FLASHEfficientVisuomotorPolicyviaSparseS | Q01 | history-anchored 1-step flow 96.8% vs Gaussian-start flow 79.2% (5 sim tasks) | + informative-prior 1-step flow | M
W4_FLASHEfficientVisuomotorPolicyviaSparseS | Q06 | sparse stride k=1 24% → k=4 96%, k≥13 collapse (Stack Cube) | + long bounded horizon | M
W4_FLASHEfficientVisuomotorPolicyviaSparseS | Q02 | polynomial coefficient trajectory + dense upsampling, analytic velocity | ~ smooth param. over raw points | L
W4_LearningtoMoveBeforeLearningtoDoTaskAgno | Q09 aux objectives | inverse-dynamics pretraining: SIMPLER 23.15 -> 33.32; real avg carrot 9 -> 28, pumpkin 21 -> 61 (200 demos) | + inverse dynamics on play data | M
W4_LearningtoMoveBeforeLearningtoDoTaskAgno | Q14 robustness | minor camera extrinsic shift: scratch 0/0, NORA 0/0, TAP 15/25%; background texture: scratch 0/0, NORA 10/55, TAP 25/65 | + dynamics pretraining; - reliance on big pretrained VLA for viewpoint | M
W4_LearningtoMoveBeforeLearningtoDoTaskAgno | Q13 data | 30 h autonomous random play + 200 demos beats 200 demos alone; Stage-1 8k/14k/20k eps -> 24.5/30.2/33.3 | + cheap self-play data | M
W4_LearningtoMoveBeforeLearningtoDoTaskAgno | Q11 cameras | single third-person view: viewpoint shift catastrophic, depth ambiguity failures | ~ need viewpoint robustness measures (wrist cam / aug) | L
W4_JEPAPolicyDiffusionFreeImitationLearning | Q01 action head | real ARX-5 100 demos: DP-100 18.7%, DP-16 31.8%, MIP (deterministic 2-pass) 54.7%, JEPA 66.9%; sim 9-task MIP 77.4 vs DP 75.1 | + deterministic few-pass regression w/ training noise; - "generative head required" | M
W4_JEPAPolicyDiffusionFreeImitationLearning | Q09 auxiliary | future-latent (0.2s) loss in shared stack +5.6 sim (83.0 vs 77.4); separate branch 76.3/77.6 (no gain); back-cut removes gain | + future-latent prediction only if it shares the action stack | M
W4_JEPAPolicyDiffusionFreeImitationLearning | Q10 latency | 13.2 ms (2 pass) vs 439.5 ms DP-100; real median 20 ms vs 316 ms | + few-pass heads | M
W4_JEPAPolicyDiffusionFreeImitationLearning | Q11 cameras | sim single seed: fixed+wrist beats wrist-only / fixed-only (Tool Hang 65 vs 27.5/35; 3-Piece 60 vs 15/42.5) | + scene+wrist | L
W4_JEPAPolicyDiffusionFreeImitationLearning | Q12 model size | 44M params from scratch, <6 GiB train, 128px, 100 demos → 67% real | + small from-scratch model on 8GB | M
W4_OGVLAOrthographicImageGenerationfor3DAwa | Q04 3D/depth | real 3-5 demos: OG-VLA (RGB-D -> canonical ortho views + SE(3) aug) Pickup 100/80/90 (pose/obj/scene) vs pi0-FAST fails all tasks | + canonical 3D representation for few-demo keyframe policies | L
W4_OGVLAOrthographicImageGenerationfor3DAwa | Q14 robustness | ARNOLD novel scene 28.8 vs PerAct 21.0; COLOSSEUM all-perturbation 10.5 vs PerAct 7.2 | ~ 3D+VLM priors help but absolute low | L
W4_FoundationandSmallModelsCoordinationforV | Q14 robustness | real ReachX RGB 61.7/21.7/25.0 vs L0 88.3/83.3/81.7; CloseCabinet RGB 85/45/48.3 vs L1 81.7/78.3/75; SmolVLA Microwave OOD RGB 4-8 vs L1 76-78 | + SAM mask role-color canonical input | M
W4_FoundationandSmallModelsCoordinationforV | Q05 augmentation | role-color repaint vs masked RGB (ARRO-style) same masks: Lift 89.5 vs 75.5, Microwave 85.3 vs 12.7 | + remove texture/color, not just background | M
W4_FoundationandSmallModelsCoordinationforV | Q04 depth | target mono-depth L1 vs L0 OOD: Microwave 83.6->90.9, Grill 73.5->81.8, Lift ~equal; S2-style depth channel much worse (48.7 vs 82.7 ID) | ~ depth helps contact tasks, encoding matters | M
W4_FoundationandSmallModelsCoordinationforV | Q03 vision encoder | SAM3 LoRA on ID data: gripper IoU 0 -> 99, object 14-33 -> 99; gripper mask essential (7.3 vs 98.7) | + frozen seg FM front-end, LoRA-adapted | M
W4_FoundationandSmallModelsCoordinationforV | Q10 latency | SAM3 15 ms/prompt, DA3 52 ms/frame on RTX 4060 Ti | ~ acceptable perception overhead | L
W4_LatentPolicySteeringAnEfficientandFlexib | Q09 world model aux | WM best-of-N steering real: DP 46.2→75.0%, π0.5 68.8→80.0% (50 demos, 20 trials×4) | + WM/value test-time steering (costs ~100 ms) | M
W4_LatentPolicySteeringAnEfficientandFlexib | Q12 model size | sim: DP 550K 57.2% vs π0.5 3.6B 60.9%; real: DP 46.2% vs π0.5 68.8% at 50 demos | ~ real pretrained VLA helps; small DP competitive in sim | M
W4_LatentPolicySteeringAnEfficientandFlexib | Q13 data quantity | DP needs >100 demos to match LPS@50; gains saturate 200–300 | ~ | L
W4_LatentPolicySteeringAnEfficientandFlexib | Q06 chunking | horizon 4–16 OK, 24 degrades LPS (Can) | ~ | L
W4_LightsCameraMalfunctionWhenIlluminationR | Q05 augmentation | real SO-101 SmolVLA: hue-fixed jitter color-task 97.5/92.5 (benign/attack) vs full HSV jitter 47.5/40.0 vs none 77.5/27.5 | + sat/value/contrast/sharpness jitter with hue fixed; - hue jitter | H
W4_LightsCameraMalfunctionWhenIlluminationR | Q14 robustness | real SO-101 50 demos: SmolVLA no-aug 70→0% under colored spotlight; with aug 80→70%; sim optimized light → 0% all suites | + photometric aug essential for lighting shift | M
W4_LightsCameraMalfunctionWhenIlluminationR | Q08 language | color-dependent 240 demos: SmolVLA+CG 97.5%, π0.5+CG 55.0% (66.7% failures wrong color) | ~ color grounding needs color-preserving aug; SmolVLA fine | M
W4_LightsCameraMalfunctionWhenIlluminationR | Q12 model size | SmolVLA > π0.5 on real color task (77.5 vs 47.5 no-aug) | + small VLA sufficient | L
W4_HumanEgoZeroShotRobotLearningfromMinutes | Q04 | Water Flowers: RGB 7.5%, robot-RGB 32.5%, RGB+3D entity-pose tokens 85%, full 95% (40 trials) | + explicit 3D object-relative state from depth | M
W4_HumanEgoZeroShotRobotLearningfromMinutes | Q09 | aux at 15 min: obj motion +17.5, latent future +12.5, 2D trace +5, all +25 pp; no gain ≥18 min | + future object-motion aux in low data | M
W4_HumanEgoZeroShotRobotLearningfromMinutes | Q14 | zero-shot bg/light/viewpoint/distractor/new instance 85–91.25% | + object-centric representation | M
W4_HumanEgoZeroShotRobotLearningfromMinutes | Q13 | same policy: 30 min teleop 65% vs 30 min diverse human video 95%; ACT teleop 52.5% | + diversity over count | M
W4_RayViTRayConditionedVisualRepresentation | Q14 robustness | RoboCasa camera perturbation: RGB 42.5->24.0 vs RayViT 39.8->37.3; real stages 2.44->0.91 vs 2.81->2.69 | + ray-map camera conditioning (needs calibration) | M
W4_RayViTRayConditionedVisualRepresentation | Q04 3D | point-map PMP-xyz 42.1->20.8, Adapt3R 41.7->28.5 under camera shift (no better than RGB) | - 3D input as viewpoint fix | M
W4_RayViTRayConditionedVisualRepresentation | Q03 encoder | DINOv3 ViT-S pretrained 42.5 vs scratch 29.2 (default), fine-tuned end-to-end | + pretrained DINOv3 small, fine-tuned | M
W4_RayViTRayConditionedVisualRepresentation | Q09 aux objectives | cross-view cosine loss +3.7/+6.4 on RayViT-cls; no stable gain on plain RGB | ~ view-consistency aux only with geometry tokens | L
W4_RayViTRayConditionedVisualRepresentation | Q11 cameras | 2 static + wrist (D405) cams; wrist view used as anchor | ~ wrist as stable reference view | L
W4_MaxQSelectiveImitationforHumanintheLoopO | Q13 data/recovery | real USB insert, 20 demos + HIL interventions: MCBC 96% in 1 h, ACT Q-chunk 99% in 0.5 h vs HIL-SERL 5 h | + human intervention (DAgger-style) data | L
W4_MaxQSelectiveImitationforHumanintheLoopO | Q01 action head | ACT 99% vs flow 96% actors in HIL RL | ~ | L
W4_GeoPredictLeveragingPredictiveKinematics | Q09 auxiliary | RoboCasa pi0 42.3 -> +track enc 44.8 -> +future track 47.2 -> +future depth 49.4 -> full 52.4; depth-only render 49.4 vs +color 49.2 | + training-only future track/depth prediction | M
W4_GeoPredictLeveragingPredictiveKinematics | Q04 depth | depth as training supervision only; real geometry gen pi0 50 vs 95%, spatial 60 vs 85% (20 trials) | + depth as aux target, not input | L
W4_GeoPredictLeveragingPredictiveKinematics | Q07 history | kinematic keypoint history encoder +2.5 pts RoboCasa | ~ low-dim history helps slightly | L
W4_GeoPredictLeveragingPredictiveKinematics | Q14 robustness | real novel-background distractors pi0 35 vs 90% (20 trials) | + 3D aux supervision aids distractor robustness | L
W4_JAMBJointActionMotionDiffusionforBimanua | Q09 | 8 sim tasks: action-only 61.4 → track-regression aux 73.9 → joint action+3D-track denoising 81.7; real 50 demos JAMB 85.6 vs GAP 64.4 vs DP3 35.6 | + future 3D track aux/joint prediction | M
W4_JAMBJointActionMotionDiffusionforBimanua | Q04 | w/o 4D RoPE (depth positional grounding) 81.7→74.1; DP3 sim 58.1 vs DP 45.8 but DP3 real 35.6 | + depth as positional/aux, ~ raw point cloud | M
W4_JAMBJointActionMotionDiffusionforBimanua | Q14 | Easy→Hard (unseen texture+clutter): DP3 1.7, GAP 4.3, JAMB 17.9 | ~ future-motion aux helps but insufficient for appearance shift | M
W4_MResTMultiResolutionSensingforRealTimeCo | Q11 cameras | real Franka: full 75.0/67.5 (pickup/insert) vs no-wrist 7.5/10.0 vs no-scene 20.0/12.5 | + scene + wrist both | M
W4_MResTMultiResolutionSensingforRealTimeCo | Q03 vision encoder | heldout objects: frozen VLM (MDETR) 72.3 vs fine-tuned VLM 45.6 (train 82.0 vs 82.4) | + frozen language-grounded encoder for global view generalization | M
W4_MResTMultiResolutionSensingforRealTimeCo | Q05 augmentation | asymmetric: color jitter+grayscale on wrist only, crop on scene: ≈+15% heldout (fig) | + asymmetric per-camera aug | L
W4_MResTMultiResolutionSensingforRealTimeCo | Q10 latency | real insert: 5Hz 45.0, 20Hz 62.5, multi-rate 67.5; sim dynamic 4.2/12.2/73.6 | + multi-rate cached slow encoder + fast head | M
W4_MResTMultiResolutionSensingforRealTimeCo | Q14 robustness | real pickup on 8 unseen objects 71.1 vs BC-Z 5.0, RT-1 0 (120 demos, 2 train objects) | + pretrained frozen VLM features for novel objects | M
W4_PocketDP3EfficientPocketScale3DVisuomoto | Q12 model size | 1.73M-param DiM decoder: RoboTwin avg 71.6 vs DP3 (255M U-Net) 50.8; real Piper 50 demos avg +15.3 pts over DP3 | + tiny decoder in low-data | M
W4_PocketDP3EfficientPocketScale3DVisuomoto | Q10 latency | 2-NFE PocketDP3 4.2-4.8 ms vs DP3 51.4 ms vs DP 460 ms; real inference on RTX 4060 | + tiny 3D policy with 2-step sampling | H
W4_PocketDP3EfficientPocketScale3DVisuomoto | Q01 action head | NFE 1/2/5/10: 53.0/58.2/57.7/58.0 (Adroit, 5000 eps); plain MLP decoder fails (0%) | + diffusion x0-pred with 2 steps; need mixer/residual structure | M
W4_PocketDP3EfficientPocketScale3DVisuomoto | Q04 3D/depth | single D455 point cloud, 50 teleop demos, joint actions: Place 73.3, Bottle 46.7, Stack 20.0 (15 trials) | ~ point cloud works on low-cost arm, modest SR | L
W4_SensingWhichModalityMattersEvidenceGated | Q14 robustness | real bimanual pi0.5: physical distractors 12/40 -> 34/40; irrelevant-cam corruption 21/40 -> 36/40; clean 28 -> 32/40 n.s. | + evidence-gated camera invariance/sufficiency loss | M
W4_SensingWhichModalityMattersEvidenceGated | Q05 augmentation | uniform ModDrop: sim MAN Full SR 12.5 -> 7.5, NoUseless 9.4 -> 6.8 (worse than vanilla) | - naive random camera dropout | M
W4_SensingWhichModalityMattersEvidenceGated | Q11 cameras | single useful camera only: 10/40 -> 29/40 with EGR; policies depend on uninformative wrist/head views | + train each cam to be sufficient when it sees the object | M
W4_SensingWhichModalityMattersEvidenceGated | Q09 aux objectives | action-MSE increase under UsefulOnly 158% vanilla vs 122% EGR | + consistency aux losses | L
W4_Learningathousandtasksinaday | Q13 | MT3 3 demos/task > monolithic BC at 50 demos/task; MT-ACT+ 150 demos over 50 tasks ≈ 600 over 12 tasks (figure) | + structure in tiny data; + diversity for BC | M
W4_Learningathousandtasksinaday | Q07 | removing proprio from MT-ACT+ improved spatial generalization (preliminary, no numbers) | + drop/limit proprio | L
W4_Learningathousandtasksinaday | Q04 | segmented target-object point cloud (single RGB-D) → 1000 tasks 78.25% seen / 68% unseen from 1 demo each | + object-segmented depth input | M
W4_Learningathousandtasksinaday | Q14 | 5-20 distractors + varied lighting: 78.25%/68% with segmentation-based inputs | + segmentation for distractor/lighting robustness | M
W4_PipetteAnEmbodiedSimulationPlatformBench | Q05 augmentation | sim 30 demos: re-simulated light/camera/speed/action replay aug SmolVLA 40.4→71.8, π0 37.3→44.1; ACT placement 42.3→24.3 | + appearance/camera aug for VLA; - action/speed perturbation on precise tasks | L
W4_PipetteAnEmbodiedSimulationPlatformBench | Q13 data | 30 demos: precision placement ≤60% for all models even with aug | ~ 30 demos too few for precise placement | L
W4_PipetteAnEmbodiedSimulationPlatformBench | Q12 model size | SmolVLA 71.8 vs π0 44.1 (augmented, 30 demos, sim) | + SmolVLA-size adequate/better than π0 in low data | L
W4_SKILSemanticKeypointImitationLearningfor | Q14 robustness | real unseen objects avg: SKIL 72.8 vs DP 23.0, DP3 25.0, GenDP-S 30.0; background+distractors 8/10 vs DP 0/10, DP3 0/10 | + semantic keypoint representation | M
W4_SKILSemanticKeypointImitationLearningfor | Q04 3D/depth | 3D semantic keypoints vs DP3 full point cloud: unseen 72.8 vs 25.0; DP3 fails with distractors (1/10) | + sparse 3D object keypoints over scene point cloud | M
W4_SKILSemanticKeypointImitationLearningfor | Q03 vision encoder | keypoint matching: DINOv2 far worse (mismatches under occlusion) than DiFT / RADIOv2.5-L/H (figure) | ~ correspondence features: DiFT/RADIO > DINOv2 | L
W4_SKILSemanticKeypointImitationLearningfor | Q13 data quantity | 10 demos SKIL (Pick 50, Handle 70, Fold 60) > baselines at 20 (max 40/50/60) | + structured input cuts demos ~2x | M
W4_InterleaveVLAEnhancingRobotManipulationw | Q08 language | SimplerEnv OOD avg text pi0 40.9 vs image+text 60.7; real Lift 36.1 vs 69.4% (12 trials/object) | + image-of-target conditioning for novel objects | L
W4_InterleaveVLAEnhancingRobotManipulationw | Q13 data | 3B VLA fine-tuned on 60 demos/task w/o pretraining: Lift 2.8% vs 69.4% with interleaved pretraining | - big model from few demos without pretraining | M
W4_InterleaveVLAEnhancingRobotManipulationw | Q14 robustness | visual OOD (lighting/tablecloth) text 71.4 vs interleave 73.4 — no appearance-robustness gain | ~ instruction format doesn't fix appearance shift | L
W4_MoEACTScalingMultiTaskBimanualManipulati | Q08 | decoder FiLM task conditioning: 53.1→62.0 avg over 16 sim tasks (50 trials each) | + FiLM task conditioning for multi-task | M
W4_MoEACTScalingMultiTaskBimanualManipulati | Q12 | dense ACT 84M 44.6 vs 0.9B 48.5; MoE-ACT 195M active 62.0 vs pi0 3.24B 56.9 (50 demos/task) | + small models; - dense scaling in low data | M
W4_SynthICLScalableIncontextImitationLearni | Q03 encoder | frozen DINOv3 ViT-S 75.0% vs LoRA-finetuned 20.7% (sim, shared across views) | + frozen DINOv3 | M
W4_SynthICLScalableIncontextImitationLearni | Q11 cameras | front+side+wrist 75.0 vs no wrist 60.3 vs no side 64.6 | + keep wrist cam + 2nd view | M
W4_SynthICLScalableIncontextImitationLearni | Q06 chunking | real precision task: temporal ensembling 15/20 vs direct exec H=1/2/4/8 12/13/13/11 of 20 | + temporal ensembling | L
W4_SynthICLScalableIncontextImitationLearni | Q09 aux objectives | subgoal image prediction real 65.3 -> 79.1; hurts at 3K-10K data | + subgoal aux at scale, ~ at small data | M
W4_SynthICLScalableIncontextImitationLearni | Q05 augmentation | synthetic RGB pseudo-demos: Isaac vs PyBullet +14%; no valid grasps 9-11%; segmented inputs | + high-fidelity synthetic + segmentation | M
W4_SynthICLScalableIncontextImitationLearni | Q12 model size | 512->256 dim smaller model 75.0 -> 64.8 | ~ too-small hurts | L
W4_PatchPolicyEfficientEmbodiedControlviaDe | Q03 vision encoder | frozen encoders (VQ-BeT Push-T/LIBERO): DINOv2 0.69/0.96, WebSSL 0.68/0.94, SigLIP2 0.51/0.83; real DINOv2-patch cable 0.70 vs ACT ResNet18-scratch 0.35 | + frozen DINOv2 patch tokens; - SigLIP for control | M
W4_PatchPolicyEfficientEmbodiedControlviaDe | Q03 pooling | Push-T 256→1 patch: 0.69→0.48; real CLS vs patch cable 0.60 vs 0.70, pen 0.65 vs 0.85 | - global CLS/avg pooling | M
W4_PatchPolicyEfficientEmbodiedControlviaDe | Q12 model size | ~50M policy beats 7.6B OpenVLA-OFT real (cable 0.70 vs 0.30, tool 0.90 vs 0.65) at 50–100 demos; DP trunk 22.8M→40.4M Push-T 0.07→0.83 | + small (~30–50M) policy on frozen features | M
W4_PatchPolicyEfficientEmbodiedControlviaDe | Q10 latency | VQ-BeT DINOv2 11 ms, ACT 8.6 ms, OFT 62 ms, DP ~420–450 ms (H200) | + single-pass/few-step heads | M
W4_PatchPolicyEfficientEmbodiedControlviaDe | Q01 action head | VQ-BeT vs DP on same patch features similar (BlockPush 1.68 vs 1.65) | ~ | L
W4_SemanticVLASemanticAlignedSparsification | Q10 latency | visual tokens 256→32: LIBERO 97.7 (vs OFT 97.1), 8.45→2.37 TFLOPs, 0.134→0.089 s; 32× pruning → 92.0 | + prune visual tokens ~8× | L
W4_SemanticVLASemanticAlignedSparsification | Q03 vision encoder | SigLIP(ID-prune)+DINOv2(aggregate) 97.1 vs same-pruner variants 91.9/94.6/95.0 | + combine semantic and geometric encoders | L
W4_SemanticVLASemanticAlignedSparsification | Q12 model size | 7B real AgileX 45-60 demos: 77.8 vs OFT 55.6 vs VQ-BeT/QueST 20 | ~ big-VLA only; no small-model data | L
W4_TimeFrequencyGeometricCrossAttentionforC | Q14 robustness | RoboTwin clean->randomized (trained clean): DP 28.3->0.2, ACT 40.2->0.8, DP3 57.0->5.8, pi0 44.2->18.7, pi0.5 61.3->14.2, +TFGCA 65.0->42.7 | - small from-scratch policies without aug collapse OOD | M
W4_TimeFrequencyGeometricCrossAttentionforC | Q01 action head | wavelet+geometric chunk attention on pi0.5: LIBERO-Plus 66.7->73.0; real AgiBot 50.0->61.7% (60 trials) | ~ structured chunk decoder helps big VLA | L
W4_TheGateNottheCacheGateProvenanceBoundsth | Q10 latency | token skipping: -18-22% latency; self-harvested gate at 0.9 skip -> success 0.68/0.31 vs dense 1.00; refresh -> 0.98 | - token skipping as main latency fix; + compute next chunk during execution | M
W4_TheGateNottheCacheGateProvenanceBoundsth | Q10 async | one-step observation delay (dense) -0.08 success on LIBERO-Spatial | ~ stale obs in async costs success | L
W4_PhysicallybasedLightingGenerationforRobo | Q05 | unseen real lighting (6 conds, 1000 trials): relit data +38.75 vs crop, +33.13 vs crop+color jitter, +41.88 vs IC-Light | + physically-based relighting; - color jitter alone | M
W4_PhysicallybasedLightingGenerationforRobo | Q14 | ResNet18 BC w/ crop/jitter reaches but fails pick-place under side/regional/RGB light | - photometric aug alone for lighting shift | M
W4_PhysicallybasedLightingGenerationforRobo | Q13 | relighting 10 vs 100 source demos: reach 0.9 vs 1.0 (Red light, 10 trials) | + few lighting-diverse samples suffice | L
W4_MasqueradeLearningfromInthewildHumanVide | Q13 data diversity | Stack Pots OOD: 0/10/50/100% edited human video co-train -> 2/26/47/68% (25 rollouts) | + diverse off-domain data via co-training | M
W4_MasqueradeLearningfromInthewildHumanVide | Q09 auxiliary | future 2D robot-keypoint aux loss; dropping co-training (pretrain only) = dramatic drop (fig) | + keep aux loss during fine-tuning | M
W4_MasqueradeLearningfromInthewildHumanVide | Q03 vision encoder | ImageNet/DINOv2/HRP ViT-B with 50 single-scene demos ~12% OOD avg vs 74% | - generic pretrained encoder alone for scene shift | M
W4_MasqueradeLearningfromInthewildHumanVide | Q14 robustness | 3 unseen scenes x 3 tasks: ~12% baselines vs ~74% (10 rollouts/scene) | + diverse visual co-training data | M
W4_MasqueradeLearningfromInthewildHumanVide | Q05 augmentation | robot overlay on human video essential (no-overlay steep drop, fig only) | + embodiment-consistent editing | L
W4_ReShootGenerativeVisualDomainRandomizati | Q05 augmentation | generative re-render of wrist+scene: novel-color real 0/40→19/40, 0/21→9/21; LIBERO-Plus +3.2 (camera +22.5, lighting −2.2) | + generative appearance re-render (offline); no lighting gain | M
W4_ReShootGenerativeVisualDomainRandomizati | Q14 robustness | recorded-only OpenVLA-OFT: object color change → 0% on 2 real robots | + appearance diversity mandatory | H
W4_ReShootGenerativeVisualDomainRandomizati | Q13 data diversity | Gen-only 77.0 vs Rec 96.9 vs Mix 96.5 LIBERO; in-dist real 14/20→10/20 with aug | ~ keep real data anchor; diversity > count | M
W4_ReShootGenerativeVisualDomainRandomizati | Q12 model size | 7B pretrained VLA still 0% under color shift | - size/pretraining gives appearance invariance | M
W4_TheCurseofPrecisionADataScalingLawforHig | Q13 data | Peg c (limit precision): cautious corrective expert 2.35mm vs direct unambiguous expert 1.27mm; SR-vs-N slope −0.72 at 10mm vs −0.19 at 4mm | + clean decisive demos over hesitant ones; ~ more demos give diminishing returns near precision limit | M
W4_TheCurseofPrecisionADataScalingLawforHig | Q11 cameras | removing wrist cam: c 2.35→3.85 mm (DP, sim) | + wrist camera for precision | M
W4_TheCurseofPrecisionADataScalingLawforHig | Q12 model size | U-Net width 64: no scaling (R²=0.22) vs width 256: R²=0.99 (Roll Ball, fig) | ~ adequate capacity needed | L
W4_WorldModelsforLearningDexterousHandObjec | Q09 aux objectives | hand-consistency keypoint loss in latent WM: PCK@20 at 4s 26 -> 60 | + structured keypoint aux target (WM setting) | L
W4_WorldModelsforLearningDexterousHandObjec | Q03 vision encoder | frozen-latent WM planning: DINOv2 strongest overall vs DINOv3/SigLIP2/V-JEPA2/Web-SSL (figure) | ~ DINOv2 as frozen latent | L
W4_RobustBimanualVisionLanguageActionModels | Q11 | mask both wrist views (keep ego) 64.0 vs mask ego 37.0 vs none 23.7 (3 sim tasks) | + wrist cam with structured wrist-dropout, scene cam as anchor | M
W4_RobustBimanualVisionLanguageActionModels | Q14 | real novel distractors 12.5→61.1, clean 44.4→69.4 (216 trials); sim Clean2Rand 3.7→15.1 | + training-time modality masking | M
W4_RobustBimanualVisionLanguageActionModels | Q05 | visual aug 22.3, region aug 23.0, token dropout 31.8 vs structured M3 64.0 (baseline 23.7) | - generic photometric aug for fusion robustness; + structured masking | M
W4_RobustBimanualVisionLanguageActionModels | Q12 | 0.5B VLA-Adapter+M3 62.7 vs pi0 39.5, RDT 30.2 (50 demos, clean) | + small VLA | L
W4_WhatMattersWhenDiagnosingandImprovingCon | Q05 augmentation | ACT sim full distractors: copy-paste distractor aug 39.5→100.0 (fixed receptacle), 14.0→64.0 (random receptacle) | + copy-paste distractor augmentation | M
W4_WhatMattersWhenDiagnosingandImprovingCon | Q14 robustness | UR3e with look-alike distractors: ACT 0/20 & 0/20 vs ACT+aug+attn-reg+prompt 13/20 & 12/20; clean equal (17/20) | + object-centric aug/regularization for distractors | M
W4_WhatMattersWhenDiagnosingandImprovingCon | Q08 language | target-crop prompt swap redirects selection 0-1%→35-91%; π0.5 routing 5/10→10/10 with cue | + visual target prompts for disambiguation | L
W4_WhatMattersWhenDiagnosingandImprovingCon | Q13 data | 100 clean demos: color competitors drop P(pick) to 39.2% with motor skill intact (lift 93.8) | - clean-only demos for distractor robustness | M
W4_SpotlightingTaskRelevantFeaturesObjectCe | Q03 vision encoder | frozen encoders real OOD: DINOv2 dense 0.07, ResNet-50 0.12, R3M 0.00, VC-1 0.03, DINOv2+slots 0.28, robot-pretrained slots 0.41 | ~ frozen dense brittle OOD; + object-centric bottleneck | M
W4_SpotlightingTaskRelevantFeaturesObjectCe | Q14 robustness | MetaWorld lighting DINOv2 0.39 vs slots 0.71; textures 0.03 vs 0.48 | + object-centric/task-relevant filtering | M
W4_SpotlightingTaskRelevantFeaturesObjectCe | Q05 augmentation | no aug baseline; frozen features only | ~ | L
W4_SpotlightingTaskRelevantFeaturesObjectCe | Q13 data (pretraining mix) | slot pretraining mix D+B+F real 0.56 vs single dataset 0.26–0.45 | ~ | L
W4_ReflexEnablingFastandPredictiveVisionLan | Q10 latency/async | SmolVLA: async < sync at low inference Hz, > sync near 20-30 Hz (fig); batched enc + CUDA Graph 125 -> 65 ms, SR 71.7 -> 73.8 | + cut latency first, async only when fast | M
W4_ReflexEnablingFastandPredictiveVisionLan | Q06 chunking | at 30 Hz async: bigger chunk (8-16) with short executed horizon (1-4) best (fig only); default chunk 8 exec 2 | + predict long, execute short | L
W4_ReflexEnablingFastandPredictiveVisionLan | Q09 auxiliary | future latent prediction vs frozen DINOv3: 36.8 -> 62.8%; trainable target 4.9% | + latent future pred with frozen target | M
W4_ReflexEnablingFastandPredictiveVisionLan | Q07 history | 2-frame fusion on intermediate ViT features 62.8 -> 71.7% (dynamic conveyor) | ~ short history for dynamic tasks only | L
W4_UniVLALearningtoActAnywherewithTaskcentr | Q01 action head | visual-query chunk decoder vs autoregressive discrete: +42.1 LIBERO-Long; w/o visual query 92.5 vs 95.2 | - discrete AR tokens, + chunked continuous | M
W4_UniVLALearningtoActAnywherewithTaskcentr | Q09 aux objectives | task-centric DINO latent actions 88.7 vs task-irrelevant 56.5 LIBERO avg (Long 79.4 vs 0.2) | + DINO-space inverse-dynamics pretraining | M
W4_UniVLALearningtoActAnywherewithTaskcentr | Q14 robustness | real lighting variation: UniVLA 66.7% vs DP 20.0%, OpenVLA 13.3%; novel object -6.6 pts | + pretrained DINO/latent-action features vs scratch DP | L
W4_UniVLALearningtoActAnywherewithTaskcentr | Q07 history | history latent actions: LIBERO-Long 88.1 -> 92.0, R2R 30.6 -> 47.1 | + compact action history | M
W4_UniVLALearningtoActAnywherewithTaskcentr | Q10 latency | OpenVLA 0.18 s/step (0.68 s/4-chunk) stutter -> 38.3% real avg | ~ latency hurts real performance | L
W4_TeachingTinyVLAModelsWheretoLookandHowto | Q01 | SmolVLA-0.25B + CVAE-latent flow (z=0 at test): LIBERO 82.8→87.4; full XS-VLA real multi-operator 21.7→65.0 (60 trials) | + CVAE latent on flow head for multi-style demos | M
W4_TeachingTinyVLAModelsWheretoLookandHowto | Q09 | coarse 3x3 target-location distillation: 82.8→88.8 (w/o LFM); image-only pretrain 87.0 vs spatial 90.3 (with LFM) | + spatial grounding aux/pretrain | M
W4_TeachingTinyVLAModelsWheretoLookandHowto | Q12 | 0.25B XS-VLA 90.3 vs SmolVLA 2.25B 88.8, 0.5B 87.3 (LIBERO) | + tiny model with structure | M
W4_UADUnsupervisedAffordanceDistillationfor | Q14 robustness | affordance-map input policy: novel instance/category gains figure-only; real 73% avg (10 demos, no baseline) | ~ relevance-map inputs | L
W4_UADUnsupervisedAffordanceDistillationfor | Q03 vision encoder | frozen DINOv2 + FiLM decoder affordance; DINOv2-3ch baseline worse (figure) | ~ | L
W4_Visionbasedmanipulationfromsinglehumanvi | Q14 | object-centric plan 60–93% vs hand-motion imitation ≤20% under new layouts/backgrounds (15 trials/task, non-learned) | + object-centric representation | L
W4_SSIPolicyLearningStructuredSceneInterfac | Q04 depth | LIBERO 10 demos: motion-only 63.42 -> +mono depth features 76.92 -> full SSI 80.42; depth-only 63.15 | + mono depth features as extra input | M
W4_SSIPolicyLearningStructuredSceneInterfac | Q13 data | 10 demos: DP 54.50 vs SSI 80.42 LIBERO; real spatial avg DP 43.3 vs 80.0 (20 rollouts) | + structured interface raises few-demo efficiency | M
W4_SSIPolicyLearningStructuredSceneInterfac | Q08 language | GroundingDINO layout from instruction + tracks; motion+layout Goal 81.5 vs motion-only 58.7-77.8 | + language-grounded layout maps | L
W4_SSIPolicyLearningStructuredSceneInterfac | Q14 robustness | real distractor/large-pose tasks DP 29 vs SSI 54% | + structured scene interface | L
W4_XR1TowardsVersatileVisionLanguageActionM | Q09 auxiliary objectives | UVMC (future visual dynamics + motion VQ codes): Light 42.5→57.5; vision-only codes 50.0 vs motion-only 35.0 (6 real tasks × 20) | + future-visual-prediction auxiliary | M
W4_XR1TowardsVersatileVisionLanguageActionM | Q12 model size | downstream-data only: 230M Light 42.5% vs full large 28.3% | + small model in low data | M
W4_XR1TowardsVersatileVisionLanguageActionM | Q14 robustness | illumination: π0 15%, XR-1 30%; dynamic distractors 5→55; novel objects 15→65 | - pretraining alone for lighting | M
W4_XR1TowardsVersatileVisionLanguageActionM | Q13 data quantity | stage-1 pretrain data 1→100%: 29.2→65.0% | ~ | L
W4_TaskPrototypeGuidedFlowMatchingforFewSho | Q01 action head | SO-101 SR@6: ACT 49.3, DP 55.6, FlowPolicy 59.8, TP-Flow 82.1 (trials/protocol unreported) | ~ flow >= diffusion > CVAE (weak evidence) | L
W4_TaskPrototypeGuidedFlowMatchingforFewSho | Q10 latency | SO-101 ResNet-18 flow policy, H=16, 8 ODE steps: 54.3 ms, 3.9 GB, 10 Hz | + small flow policy fits 8 GB budget | L
W4_TaskPrototypeGuidedFlowMatchingforFewSho | Q12 model size | OpenVLA 50.1 vs ResNet-18 flow 59.8-82.1 @6-shot on SO-101 | + small models suffice | L
W4_TaskPrototypeGuidedFlowMatchingforFewSho | Q13 data | 1/2/4/6-shot support after source training: 66.8/73.4/79.6/82.1 | ~ few-shot conditioning (not needed for our case) | L
W4_TraceGenWorldModelingin3DTraceSpaceEnabl | Q13 data | 5 target videos: pretrained 80% vs scratch 25%; 15 videos 82.5 vs 30%; human phone videos 67.5% (10 trials/task) | + strong prior makes few demos suffice | L
W4_TraceGenWorldModelingin3DTraceSpaceEnabl | Q09 auxiliary/world model | pretraining source: SSV2 25% / AgiBot 45% / mixed cross-embodiment 80% | + diverse 3D-trace world-model pretraining | L
W4_TraceGenWorldModelingin3DTraceSpaceEnabl | Q10 latency | 3D-trace planning 3.8x faster than trace baselines, >50x than video-gen models | ~ trace space cheaper than pixel world models | L
W4_StageACTStageConditionedImitationforRobu | Q07 history/memory | ACT 20% vs ACT+5-frame history 10% vs stage-conditioned 55% SR (unseen door, 10-20 trials) | - raw frame history; + explicit low-dim stage signal | L
W4_StageACTStageConditionedImitationforRobu | Q08 conditioning | stage GT 60% vs constant/random stage 0% (human gives stage at test time) | + one-hot subtask conditioning | L
W4_StageACTStageConditionedImitationforRobu | Q06 chunking | ACT chunk 100 steps (~3 s) + TE at 30 Hz used on real humanoid, no ablation | ~ | L
W4_VODPSemanticGeometricAdaptiveDiffusionPo | Q03 vision encoder | real 4 tasks x 60 trials: DP 11.2 / DP3 67.5 / VGGT-feature DP 87.9; sim sem-only 71.1, geo-only 63.9, fused 80.0 | + geometry-aware pretrained encoder (VGGT/DINOv2 fusion) | M
W4_VODPSemanticGeometricAdaptiveDiffusionPo | Q04 3D vs RGB | single RGB + VGGT 87.9 vs L515 point-cloud DP3 67.5 real; sim 64.6 vs 64.0 | - raw point clouds; + 3D-aware RGB features | M
W4_VODPSemanticGeometricAdaptiveDiffusionPo | Q14 robustness | lighting switch 80 / blink 85 vs 85; background 80-95; novel color blue 50 / green 40 vs 85; size 2.5cm 60, 5cm 50 (20 trials, no baseline) | ~ lighting/background OK, color shift still fails | L
W4_VODPSemanticGeometricAdaptiveDiffusionPo | Q07 history | RoboTwin T=1 64.6 vs T=3 63.9 | - obs history no gain | L
W4_VODPSemanticGeometricAdaptiveDiffusionPo | Q13 data | Pick Apple Messy 20 demos 3.0 -> 100 demos 80.0; steeper scaling than DP/DP3 | ~ foundation features need ~50-100 demos | L
W4_WhatMattersinLearningfromLargeScaleDatas | Q13 data quantity/diversity | real DROID co-train: all-DROID 0% on 6 tasks vs aligned retrieval up to 85%; bin can spatial reset small 30% -> large 60% | + spatial coverage & aligned data over raw quantity | M
W4_WhatMattersinLearningfromLargeScaleDatas | Q11 cameras | sim camPose-misaligned: target-only 16.7, low-var cotrain 43.3, camPose-diverse cotrain 90; real aligned camPose +25-50% | + viewpoint diversity/alignment critical | M
W4_WhatMattersinLearningfromLargeScaleDatas | Q14 robustness | objTex misaligned cotrain still 93.3% (sim), real +40-65% despite texture mismatch; no lighting tested | ~ texture diversity low priority vs viewpoint/spatial | L
W4_WhatMattersinLearningfromLargeScaleDatas | Q05 augmentation | camera-pose diversity rescues texture misalignment (tableTex 66.7 -> 80) | + viewpoint aug > color aug (indirect) | L
W4_DIALDecouplingIntentandActionviaLatentWo | Q09 auxiliary objectives | few-shot 100 demos/task RoboCasa: VLM-FT 30.6 -> +aux future-latent loss 51.9 -> future bottleneck (latent inverse dyn) 58.3 | + predict future frozen-encoder features | M
W4_DIALDecouplingIntentandActionviaLatentWo | Q03 vision encoder | foresight in DINOv2 space instead of native ViT: 58.3 -> 47.2 | ~ keep aux target in policy's own encoder space | L
W4_DIALDecouplingIntentandActionviaLatentWo | Q12 model size | frozen Qwen2.5-VL-3B + DiT (GR00T-style) only 21.8% few-shot | - big frozen VLM alone not sufficient | L
W4_DIALDecouplingIntentandActionviaLatentWo | Q13 data | real OOD 58.3 with human EgoDex pretrain vs 26.7 without (trials unreported) | ~ human video pretraining helps OOD but needs big corpus | L
W4_WhatstheMoveHybridImitationLearningviaSa | Q04 3D/depth | novel viewpoint: DP (RGB) 1/10 & 0/10 vs point-cloud waypoint SPHINX 9/10 & 9/10 (calibrated) | + calibrated 3D for reach phase | M
W4_WhatstheMoveHybridImitationLearningviaSa | Q11 cameras | wrist-only dense policy robust to distraction (1/10 -> 8/10); DP3 w/o wrist < DP with wrist | + wrist cam for precise phase | M
W4_WhatstheMoveHybridImitationLearningviaSa | Q09 auxiliary objectives | salient-point aux classification: Square 13% -> 65.5%, Can 70 -> 78 | + target-point/keypoint aux loss | M
W4_WhatstheMoveHybridImitationLearningviaSa | Q02 action space | object-relative waypoint offsets vs absolute waypoint regression: Can 70 -> 93.5, Square 13 -> 86.5 | + object-relative targets | L
W4_WhatstheMoveHybridImitationLearningviaSa | Q14 robustness | Cup Stack distractors DP 1/10 vs SPHINX 8/10 | + object-centric attention + wrist | L
W4_WhatstheMoveHybridImitationLearningviaSa | Q12 model size | fine-tuned OpenVLA worst on 3 precise real tasks (figure) | - large VLA for precise single-task | L
W4_NovelDemonstrationGenerationwithGaussian | Q05 augmentation | camera-shift avg SR: real 200 demos 6.1, VISTA 2D novel-view 40.6, 3DGS view aug 80.6 (30 trials, 3 tasks) | + 3D-consistent view/light/background aug | M
W4_NovelDemonstrationGenerationwithGaussian | Q14 robustness | lighting: 3DGS relight aug >80% avg vs ~+70pt over unaugmented; beats color jitter; novel objects 23.3 -> 76.7 | + targeted augmentation per shift axis | M
W4_NovelDemonstrationGenerationwithGaussian | Q11 cameras | no-aug policy novel view 0-17%, moving cam 0-13% | - relying on fixed scene cam without view aug | M
W4_NovelDemonstrationGenerationwithGaussian | Q13 data | 800 generated ~ 200 real (87.3%); 1800 generated 94.7%; pose-only data doesn't help camera shift (9.5%) | + diversity along shift axis > count | M
W4_NovelDemonstrationGenerationwithGaussian | Q12 model size | ResNet-18 + GPT2-style transformer, 128x128, chunk 10 + TE reaches 80-95% | + small model sufficient | L
W4_PriorVLAPriorPreservingAdaptationforVisi | Q12 model size / FT strategy | pi0.5 full FT vs frozen-prior adaptation: RoboTwin Hard 42 -> 53; real OOD 41 -> 57; real 10-demo OOD 10 -> 32 | + partial freezing of pretrained VLA over full FT | M
W4_PriorVLAPriorPreservingAdaptationforVisi | Q14 robustness | Diffusion Policy RoboTwin Easy 36% vs Hard (randomized light/bg/clutter) 0% on all 13 tasks | - from-scratch small policy without aug is brittle | M
W4_PriorVLAPriorPreservingAdaptationforVisi | Q13 data | few/std/large demos Hard: pi0.5 20/42/59, PriorVLA 31/53/65; ID gain vanishes at large data | ~ priors matter most in low data | M
W4_PriorVLAPriorPreservingAdaptationforVisi | Q03 vision encoder | trains vision encoder, freezes LLM + prior expert (not ablated alone) | ~ | L
W4_VisualSimtoRealLearningforRoboticInserti | Q05 augmentation | w/o appearance randomization 2.8% vs 96.1% (sim, randomized eval); w/o viewpoint rand 90.2 | + strong appearance randomization | M
W4_VisualSimtoRealLearningforRoboticInserti | Q13 data quality/diversity | pure BC 68.9 vs DAgger mixture 96.1; object-geometry diversity 79.4 -> 96.6 on seen design | + on-policy/recovery data, object diversity | M
W4_VisualSimtoRealLearningforRoboticInserti | Q14 robustness | real novel backgrounds/clutter 25/30 vs clean 6/6 | + appearance DR transfers to real bg shift | L
W4_VisualSimtoRealLearningforRoboticInserti | Q12 model size | ImageNet ResNet-18 shared across 8 views + MLP achieves 91.3% real (150 trials) | + small encoder sufficient | L
W4_XSimCrossEmbodimentLearningviaRealtoSimt | Q11 cameras | Shoe on Rack: side-only train -> frontal 23.3 / novel 33.3; side+frontal train -> 96.7/80.0/53.5 (10 trials) | + multi-viewpoint training data | L
W4_XSimCrossEmbodimentLearningviaRealtoSimt | Q05 augmentation | sim rendering with cam ±3cm + 4 lighting presets; real-sim InfoNCE calibration +8% task progress | + view/light randomization, encoder alignment | L
W4_XSimCrossEmbodimentLearningviaRealtoSimt | Q13 data | 1 min human video (sim-expanded) 90% vs 10 min teleop BC 70% on wide init distribution | ~ synthetic coverage beats few real demos | L
W4_GaussianDreamEfficient3DGaussianWorldMod | Q04 3D/depth | training-only metric-depth loss: LIBERO-Plus Camera 76.5 -> 80.1; real camera-relocated 22.5 -> 42.5 (20 trials x2 tasks) | + depth as auxiliary supervision (no inference cost) | M
W4_GaussianDreamEfficient3DGaussianWorldMod | Q09 auxiliary objectives | LIBERO-Plus Overall: tokens w/o supervision 86.3, +current recon 86.9, +future 87.2-87.8 (base 85.5) | + 3D recon/future aux losses, modest | M
W4_GaussianDreamEfficient3DGaussianWorldMod | Q14 robustness | real: standard 62.5 vs camera shift 42.5 vs layout 50.0 even for best model | ~ camera shift remains major failure | M
W4_GaussianDreamEfficient3DGaussianWorldMod | Q10 latency | pi0.5 286 ms vs 330 ms per chunk with 20 extra tokens (training heads removed) | ~ | L
W4_GlobalPriorMeetsLocalConsistencyDualMemo | Q10 latency/smoothness | flow init from retrieved trajectory prior: NFE 10 -> 3.2 (LIBERO 98.6 vs 96.9); real 85.0 vs 75.0 with 2.9x speedup | + informed prior / fewer NFE | L
W4_GlobalPriorMeetsLocalConsistencyDualMemo | Q07 history/memory | previous-action-chunk consistency module: removal -> LIBERO-Long -1.6 to -3.3, real -5.5 to -8 pts | + action-history conditioning | L
W4_GlobalPriorMeetsLocalConsistencyDualMemo | Q14 robustness | RoboTwin 2.0 Hard (DR light/texture/clutter): DP 20%, DP3 2%, ACT 1% vs VLAs 25-38% | - small scratch policies w/o aug | M
W4_GlobalPriorMeetsLocalConsistencyDualMemo | Q01 action head | flow matching from retrieved prior instead of N(0,I) | ~ | L
W4_ManiVID3DGeneralizableViewInvariantReinf | Q04 3D/depth | view-randomized: w/o canonicalization 57.1 vs 92.9; DP3 (100 multi-view demos) 18.0 vs 78.4 with canonicalized encoder; real 103/140 vs 79/140 | + depth only if frame-canonicalized/calibrated | M
W4_ManiVID3DGeneralizableViewInvariantReinf | Q11 cameras | RGB-D Maniwhere drop 3.9% at ±30° -> 31.5% at ±75° yaw; ManiVID-3D <6.7% | + view-invariant 3D representation for camera shift | L
W4_ManiVID3DGeneralizableViewInvariantReinf | Q05 augmentation | SRM image-aug baseline 12.1% avg under ±60° view randomization vs 94.5 | - image aug alone for large view shifts | L
W4_RoBridgeAHierarchicalArchitectureBridgin | Q14 robustness | MetaWorld unseen bg/light/color/cam: mask+masked-depth policy 84.6/82.6/83.2/74.8 vs RGB DrQ-v2 24.6/17.4/22.2/19.8 | + object-mask intermediate representation | M
W4_RoBridgeAHierarchicalArchitectureBridgin | Q03 vision encoder | frozen DINOv2 features instead of masks: mean 82.1 -> 50.4, camera pose 74.8 -> 30.6 | - frozen DINOv2 for small policy | L
W4_RoBridgeAHierarchicalArchitectureBridgin | Q04 3D/depth | raw depth vs masked depth: MT50 87.2 vs 85.4 but camera shift 60.8 vs 74.8 | ~ raw depth overfits viewpoint; mask/object-centric depth better | L
W4_RoBridgeAHierarchicalArchitectureBridgin | Q05 augmentation | w/o domain randomization: mean 82.1 -> 56.1, camera 74.8 -> 30.2 | + heavy DR incl. mask/depth corruption | M
W4_RoBridgeAHierarchicalArchitectureBridgin | Q13 data quality | w/o DAgger 82.1 -> 65.1 mean | + corrective on-policy data | M
W4_SimulationDrivenImitationLearningforBios | Q14 robustness | real single-scene-trained policy SR 0.98/0.99/0.00 across 3 table/wall scenes vs scene-diverse sim-trained 0.90/0.92/0.95 (1800 trials) | + background/scene diversity essential | M
W4_SimulationDrivenImitationLearningforBios | Q13 data diversity | sim ACT: train rooms 2->8 unseen-room SR 44.2 -> 57.4; objects 10->100 26.8 -> 42.2 (saturates ~75) | + scene & object diversity | M
W4_SimulationDrivenImitationLearningforBios | Q11 cameras | wrist-cam-only real-data policy collapses (0%) on new table color | - wrist cam alone not appearance-invariant | L
W4_SimulationDrivenImitationLearningforBios | Q01 action head | unseen-room SR: ACT 57.4, VTM-VAE 55.8, diffusion 49.0 (unseen obj 42.2/44.9/33.2) | ~ CVAE >= diffusion in small low-dim setting | L
