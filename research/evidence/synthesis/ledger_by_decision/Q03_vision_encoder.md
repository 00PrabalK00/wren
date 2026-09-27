# Q03_vision_encoder — 126 ledger lines
[fulltext] DiffusionPolicy | vision | frozen pretrained 0.40-0.70 vs finetuned 0.92-0.98 vs scratch R18 0.94 | - frozen, + finetune low LR | H(in-dist)
[fulltext] DP3 | encoder_size | tiny MLP point encoder > PointNeXt/PointTransformer | + small encoder | M
[fulltext] iDP3 | vision | in-dist: finetuned R3M image DP ≥ iDP3; frozen R3M worse | + finetune, - frozen | M
[fulltext] SPA | vision | frozen, 268 tasks: SPA > MAE > ... ; DINOv2 < MoCoV3/MAE; CLIP-style poor | - DINOv2/SigLIP as frozen, + SPA/MAE init | M
[fulltext] robomimic | Q03 vision | shallow conv vs ResNet-18: −25–62% rel; LR 1e-3 vs 1e-4: −35–63% (image) | + ResNet-18-class encoder, low LR | M
[fulltext] RT-1 | Q03 vision | no ImageNet pretraining: unseen 76→43, backgrounds 59→41 | + pretrained encoder | M/H
[fulltext] R3M | Q03 vision | frozen RN50, in-dist only: sim ~62% (+>10 pts vs CLIP/MoCo, +>20 vs scratch); real 20 demos 56% vs CLIP 24% | ~ R3M (in-dist only), + pretrained>scratch | M
[fulltext] VC-1 | Q03 vision | E2E fine-tune ViT-L on few-shot IL collapses: MW 88.8→22.7, Adroit 59.3→15.9, DMC 66.9→6.7 | - fine-tuning LARGE encoder on small data | H
[fulltext] VC-1 | Q03 vision | real Franka: frozen 70% vs E2E (enc LR 1e-5) 67.5% vs MAE-adapt-on-demo-frames 85% | + in-domain MAE adaptation, ~ low-LR fine-tune | M
[fulltext] VC-1 | Q03 vision | frozen VC-1 < frozen R3M on Adroit/MW/DMC (59/89/67 vs 73/96/81); no universal PVR | - VC-1 as pick | M
[fulltext] Theia | Q03 vision | spatial tokens 78.9 vs CLS 50.0; Theia-B 79.8 vs MVP-L 77.4, R3M 76.5, VC-1-L 69.6 (frozen) | + spatial tokens, + distilled small ViT | H/M
[fulltext] Theia | Q03 vision | real: frozen 0% on long-horizon microwave; drawer frozen→FT Theia 85→100, R3M 0→55, VC-1 0→45, but DINOv2-L 35→20 | + fine-tune (except DINOv2-L) | M
[fulltext] UnbiasedLookPVR | Q03 vision | real 50 demos, fine-tuned MAE ViT-B: ImageNet 41 / Kinetics 44 / DoH 38 vs Ego4D 28 / RoboNet 30 / VC-1 33 / MVP 25; Soup+DoH 60 | + ImageNet-style diverse init, - Ego4D/robot PVRs | M/H
[fulltext] UnbiasedLookPVR | Q03 vision | ViT-B from scratch = 0% on all 3 real tasks | + pretrained init mandatory | H
[fulltext] UnbiasedLookPVR | evaluation | sim vs real PVR performance R²=0.32 | - trust sim encoder rankings | M/H
[fulltext] WhatMakesPVRsRobust | Q03 vision | frozen, 9k sim evals: manipulation PVRs (R3M/MVP/VIP) best in-dist but best one ranks 7/15 OOD; DINO/MoCo-v3/sup-ViT better OOD | + ImageNet SSL ViT, - R3M/MVP/VIP for OOD | M
[fulltext] WhatMakesPVRsRobust | Q03 vision | DINOv2-S/14 worse in- and OOD than DINO v1 (frozen) | - plain frozen DINOv2 | L/M
[fulltext] RoboMP-DINOv2 | Q03 vision | fine-tuned DINOv2-B DP: spatial-OOD 50.7 → clutter 41.0; RoboMP 60.7/59.7 | ~ fine-tuned DINOv2 fragile | M
[fulltext] RESOLVED | Q03 vision | frozen-vs-FT tension: FT wins in-dist when encoder small/low-LR/aug (DP, Theia, Dasari); FT collapses only for ViT-L+MLP+tiny data (VC-1); OOD robustness depends on pretraining recipe (DINO/MoCo/ImageNet ViT > R3M/MVP/VC-1), not frozen-vs-FT; no 2D encoder survives camera/scene shift like 3D (iDP3) | |
[fulltext] VLA-Adapter | vision | LIBERO-Long bridge: last-layer raw 85.8 < query 90.2 < all-layer raw 90.6 < all query 92.6 < both 95.0; frozen VLM 86.4 vs SmolVLA 77.0 | + multi-layer VLM features + query tokens | M
[fulltext] FLOWER | vision | intermediate fusion 93.4 vs late 61.8 vs early 33.4 (LIBERO-Long); frozen VLM 2.65 vs 4.44; Florence-2 > SmolVLM | + fine-tuned grounding VLM, intermediate features | M
[fulltext] FLOWER | pretraining | Aloha joint-space: cross-action-space PT worse than scratch; droid-joint PT best | - mismatched-action PT | M
[fulltext] X-VLA | pretraining | naive heterogeneous PT: 39.6 -> 25.0 (-14.6); fixed by action alignment + soft prompts -> 73.8 | - naive cross-embodiment PT | M
[fulltext] Seer-PIDM | Q13 data/pretraining | real 100 demos/task: scratch 60.0 → DROID-pretrained 78.4 SR; OXE (other robots) 53.3→56.7 | + same-embodiment pretraining only | M
[fulltext] DemoGen | vision | DINOv2/CLIP init ≫ scratch ResNet ≫ R3M for spatial generalization | + pretrained init (not R3M) | M
[fulltext] DataScalingLaws | vision | fine-tuned DINOv2 ViT-L 0.90, LoRA 0.72, frozen 0.00, scratch 0.03; ViT-S/B/L 0.66/0.81/0.90 | + pretrained + full fine-tune; - frozen | H
[fulltext] UMI | vision | CLIP ViT-B fine-tuned 14/20 vs scratch ResNet-34 0/10 | + pretrained fine-tuned | M
[fulltext] PointVLA | Q04 encoder | pretrained 3D encoders hindered learning (no numbers) | + small scratch point encoder | L
[fulltext] RoboVLMs-WhatMatters | Q03 backbone | VL-pretrained KosMos P.H. ABC→D 4.25 vs no-VL 0.56; PaliGemma-3B 3.82 > Qwen-VL-9B 0.30 | + strong VL pretraining over size | H
[fulltext] Octo | Q03 vision | ~100 demos from scratch: ResNet beats ViT/patch transformer; big transformer overfits; ViT wins only on 800k-traj pretraining (83 vs ResNet-50 70) | + ResNet/CNN for small-data from scratch | M
[fulltext] HPT | Q03 vision | frozen ResNet-18 + pretrained 12.6M trunk 70.0 vs VC-1 53.3 / R3M 50.0 / Voltron 46.7 / scratch 43.3 (Sweep, ~100 demos) | + frozen small CNN + policy-level pretraining over vision-only pretraining | L/M
[fulltext] OpenVLA | Q03 vision | LoRA-era FT: frozen vision 47.0 vs full FT 69.7 vs last-layer 30.3 (7B, Franka 33 rollouts) | + fine-tune encoder when adapting a big pretrained VLA | M
[fulltext] KnowledgeInsulation | Q03 vision | frozen PaliGemma backbone + trained expert = 0% (drawer, shirt fold) | - fully frozen generic backbone for precise tasks; + fine-tune with protected gradients | M
[fulltext] GR00T-N1 | Q03 vision | frozen LLM + unfrozen vision encoder + middle-layer (12th) features "better and faster" (no numbers) | + fine-tune vision, mid-layer features | L/M
[fulltext] CONFLICT | vision | frozen DINOv2+LoRA with spatial tokens (CAGE) robust 0.87/0.80/0.80 vs DP ResNet-scratch 0/0/0.27; fine-tune WITHOUT aug worst, fine-tune WITH jitter+shift best (encoder study) | + pretrained, spatial tokens, aug mandatory | M
[wave3] W3_AxisGuideGroundingRobotActionCoordinateS | Q12 model size / finetune | full-finetuned SmolVLA used as stronger baseline than frozen-VLM action-expert-only (figure only) | + full finetune of SmolVLA | L
[wave3] W3_CACTIAFrameworkforScalableMultiTaskMulti | Q03 vision encoder | frozen out-of-domain R3M ≈ in-domain MoCo ≈ fine-tuned in real (figure only); sim in-domain MoCo > R3M (75.9 vs 62.0 train) | ~ frozen pretrained | L
[wave3] W3_CapturingVisualEnvironmentStructureCorre | Q03 | MetaWorld fine-tuned: DINOv2 0.767, CLIP 0.765, ViT-IN 0.683, MAE 0.648; frozen CLIP worst 0.562; best frozen encoder differs by env | + fine-tuned DINOv2/CLIP; - frozen CLIP | M
[wave3] W3_DecomposingtheGeneralizationGapinImitati | Q03 | frozen R3M/CLIP ResNet50 leave large gap, CLIP ~ scratch CNN except object texture | - frozen pretrained reps for robustness | L
[wave3] W3_GeneralizableVLAFinetuningviaRepresentat | Q03 vision encoder | LIBERO-PRO/Plus: frozen VLM 43.1/59.9, BC finetune 61.0/85.1, finetune + frozen-copy feature anchoring 68.1/87.3 (+align 71.9/90.3) | + finetune with anchoring; - frozen | M
[wave3] W3_DeFMLearningFoundationRepresentationsfro | Q03 vision encoder | fine-tuned > frozen for all encoders; Kinect-noise shift frozen DeFM 0.486 vs FT 0.876, frozen ImageNet 0.004 | + fine-tune encoder; - frozen | M
[wave3] W3_GNFactorMultiTaskRealRobotLearningwithGe | Q03 vision encoder | distilled SD 36.8 vs CLIP 32.0 vs DINO 30.4 (sim) | ~ | L
[wave3] W3_HInDexVisualReinforcementLearningwithHan | Q03 vision encoder | frozen encoders, 12 dexterous sim tasks avg success: ImageNet RN50 81.3, VC-1 70.8, MVP 63.1, R3M 42.3, hand-pose RN50+BN-adapt 91.3 | + ImageNet RN50 baseline; - R3M | L
[wave3] W3_HInDexVisualReinforcementLearningwithHan | Q03 finetune strategy | BN-only (0.18% params) adaptation beats full finetune; full finetune can be worse than frozen (figure only) | ~ partial adaptation | L
[wave3] W3_MaskedVisualPretrainingforMotorControl | Q03 vision encoder | frozen MAE(HOI) ViT-S > supervised ImageNet ViT on 7/8 PixMC RL tasks (up to +80 abs, figure only); random frozen fails 6/8 | + pretrained (SSL) > random; ~ vs ImageNet | L
[wave3] W3_MultiViewMaskedWorldModelsforVisualRobot | Q03 vision encoder | frozen CLIP/MAE world models far below in-domain MV-MAE (figure only) | - frozen generic encoders (RL, sim) | L
[wave3] W3_MimicPlayLongHorizonImitationLearningbyW | Q03 | R3M-BC (frozen pretrained) long-horizon 0.00/0.17 vs end-to-end ResNet18 hierarchical 0.47/0.70 | - frozen R3M | L
[wave3] W3_CLIPortWhatandWherePathwaysforRoboticMan | Q03 vision encoder | stack-pyramid seen n=10: CLIP 64.7 / ImageNet-RN50+BERT 35.0 / untrained 12.7; n=1000 98.8/97.5/51.2 | + pretrained VL encoder in low-data | M
[wave3] W3_RT2VisionLanguageActionModelsTransferWeb | Q03 | VLM-pretrained RT-2 ~6x frozen VC-1/R3M, ~2x RT-1 on unseen objects/backgrounds/envs | + web VLM pretrained vision; - frozen VC-1/R3M | M
[wave3] W3_SPOCImitatingShortestPathsinSimulationEn | Q03 | avg success CLIP-RN50 26.6, DINOv2 ViT-S 44.8, SigLIP ViT-B 49.9 (sim, language-conditioned nav+pick) | + SigLIP/DINOv2 over CLIP-ResNet | M
[wave3] W3_ActionEffectMemoryPretrainingforRobotMan | Q03 vision encoder | memory feats DINOv2 CLS .96/.76 > CLIP CLS .84/.44 > DINOv3 CLS .76/.52 | + DINOv2 | L
[wave3] W3_CageCausalAttentionEnablesDataEfficientG | Q03 vision encoder | frozen DINOv2-L+LoRA w/ spatial tokens: bg-change 0.87 vs ResNet-scratch 0.00; new object 0.80 vs 0.00 (50 demos, real) | + frozen pretrained ViT + LoRA, token-level | M
[wave3] W3_CageCausalAttentionEnablesDataEfficientG | Q03 vision encoder | mean-pooled DINOv2 tokens: L0 0.40 vs 1.00 with perceiver | - pooled VFM features | M
[wave3] W3_LIVLanguageImageRepresentationsandReward | Q03 vision encoder | frozen LIV > CLIP/R3M/VIP for frozen-backbone BC (figure only) | ~ control-aware VL pretraining | L
[wave3] W3_OfflinetoonlineReinforcementLearningforI | Q03 vision encoder | E2E > frozen pretrained asymptotically in O2O RL; frozen random fails (figure) | ~ | L
[wave3] W3_WhatDoWeLearnfromaLargeScaleStudyofPreTr | Q03 vision encoder | VC-1 Base real avg: frozen ≈71, FT no-aug ≈46.5, FT+aug ≈73 (30-150 demos) | + FT only with aug; frozen safe default | M
[wave3] W3_WhatDoWeLearnfromaLargeScaleStudyofPreTr | Q03 vision encoder | frozen real avg R3M 56, CLIP 47, MVP 53, VC-1B 69, VC-1L 63; no PVR best on all tasks | - CLIP for manipulation | L
[wave3] W3_AdaptationofGeneralistRobotPolicieswithM | Q03 vision encoder | residual RL on LIBERO: scratch ResNet collapses, frozen DINO slower, pi0.5 feats fastest (figure only) | + pretrained frozen features | L
[wave3] W3_FlowingWithPurposeLatentActionGuidedFlow | Q03 vision encoder | ImageNet ResNet18 end-to-end in 0.11B policy beats pi0 real (no ablation) | ~ ResNet18 sufficient | L
[wave3] W3_Ag2ManipLearningNovelManipulationSkillsw | Q03 vision encoder | real Franka 20 demos, 4 tasks x10: ImageNet R50 8/40, CLIP 10/40, R3M 16/40, VIP 20/40, Ag2Manip 31/40 | - frozen generic ImageNet/CLIP; + manipulation-pretrained | L
[wave3] W3_CanonicalPolicyLearningCanonical3DRepres | Q03 vision encoder | DP3 MLP point encoder >> PointNet++/DGCNN (~0 on MimicGen) | + simple MLP point encoder | M
[wave3] W3_FocusVLAFocusedVisualUtilizationforVisio | Q03 vision encoder | LIBERO avg DINOv2+SigLIP 98.4, VLM 98.2, VGGT 96.8; mixed->cascaded attn 93.6->97.0 | ~ fusion matters more than encoder (in-dist) | L
[wave3] W3_RethinkingthePracticalityofVisionlanguag | Q03 vision encoder | real DR (new tabletop+distractors), 200 demos: ACT 18.6->3.0% vs 0.5B VLA 44.2->30.7% | + pretrained VLM features, - scratch/ImageNet ResNet | M
[wave3] W3_AnchorVLA4DanAnchorBasedSpatialTemporalV | Q03 vision encoder | frozen spatial encoder 64.6 vs unfrozen 59.4 vs removed 58.3 | + freeze pretrained encoders | L
[wave3] W3_OnBringingRobotsHome | Q03 vision encoder | in-domain MoCo ResNet34 (HPR) >=23% over VC-1/MVP/R3M/IN-1K; VC-1 bimodal | + in-domain pretrain, full fine-tune small CNN | M
[wave3] W3_FromPlaytoPolicyConditionalBehaviorGener | Q03 vision encoder | frozen BYOL ResNet18 embeddings fail on knob state (knob 3/20, NN ~chance) | - frozen global SSL embeddings for fine details | L
[wave3] W3_RoboticManipulationisVisiontoGeometryMap | Q03 vision encoder | LIBERO VGGT-init+LoRA 98.1 vs VGGT-init full-FT 87.1 vs random init 86.6 | + pretrained, frozen/LoRA; - full fine-tune | M
[wave3] W3_P3POPrescriptivePointPriorsforVisuoSpati | Q03 vision encoder | frozen DIFT correspondence + CoTracker transfers points across instances | + frozen foundation features for object localization | L
[wave3] W3_RoboTwin20AScalableDataGeneratorandBench | Q03 vision encoder | Hard setting: pretrained RDT 13.7/pi0 16.3 vs scratch ACT 1.7/DP 0.6 | + pretrained backbones | M
[wave3] W3_GLUEGlobalLocalUnifiedEncodingforImitati | Q03 vision encoder | learnable CLIP global-only (GLUE-S) real 70.0 vs DP-R18 36.2 / ACT 48.8; OOD 30-50 vs 0-25 | + pretrained CLIP-class fine-tuned > ImageNet ResNet18 | M
[wave3] W3_RobustPoliciesviaMidLevelVisualRepresent | Q03 vision encoder | RLBench pick+place unseen colors: frozen mid-level features 100% vs scratch pixels+DR 20% | + frozen pretrained encoder | L
[wave3] W3_GroundedActionModel3DGroundingasaFoundat | Q03 vision encoder | frozen 3D-grounding backbone + trained flow head 55.3 avg vs fine-tuned pi0.5 45.0 (RoboTwin single-task) | + frozen strong perception + small head | M
[wave3] W3_BestofSimandRealDecoupledVisuomotorManip | Q03 vision encoder | frozen DINOv2 multi-layer 91.7/71.7 vs last-layer 78.3/55.0 (K=20); scratch BC worst | + frozen DINOv2 multi-scale | M
[wave3] W3_SAVLASymmetryAwareVisionLanguageActionMo | Q03 vision encoder | frozen GR00T N1.5 VLM + 100M head reaches 55-75% on 3 SO-101 tasks with 50 demos each | + frozen pretrained VLM backbone | M
[wave3] W3_PVIPluginVisualInjectionforVisionLanguag | Q03 encoder | GR00T 50 demos sim: 39.8 -> +frozen DINOv2 side-path 56.8 -> +frozen V-JEPA2 69.4 | + frozen dense SSL features injected to action head | M
[wave3] W3_SelfSupervisedCorrespondenceinVisuomotor | Q03 vision encoder | sim Reach T+R: dense-correspondence keypoints 97.8 vs E2E 32.2 vs AE 61.1; E2E ResNet34 3.3 | + pretrained/correspondence features over scratch E2E | M
[wave3] W3_ProgVLAProgressAwareRobotManipulationSki | Q03 vision encoder | LIBERO: fine-tuned DUNE ViT-S 91.1 vs frozen 77.6 (Long 88.6 vs 60.6); DINOv3 88.7 | + fine-tuned pretrained SSL ViT-S; - frozen | M
[wave3] W3_TrainOfflineTestOnlineARealRobotLearning | Q03 vision encoder | frozen+BC real Franka: in-domain MoCo 83.3/72.2%, BYOL 72.2/66.6 vs ImageNet ResNet50 47.2/50.0, MoCo generic 33.3/55.5, R3M 44.4/33.3 (scoop/pour) | - frozen generic (R3M/ImageNet); + in-domain adaptation | M
[wave3] W3_VIRALVisualSimtoRealatScaleforHumanoidLo | Q03 encoder | DINOv3 student backbone best (figure only) | + DINO-family | L
[wave3] W3_VisionLanguageFoundationModelsasEffectiv | Q03 vision encoder | CALVIN ABCD->D avg len: R3M frozen 0.10, Voltron frozen 0.11, Voltron fine-tuned 2.08, RoboFlamingo 4.09 | - frozen robotics encoders; + fine-tune | M
[wave3] W3_VisuomotorControlinMultiObjectScenesUsin | Q03 vision encoder | sim IBC: MoCo frozen global features did not converge; Slot (object-aware) 57.1 vs RGB 36.9 at 1k eps | - global-pooled contrastive features; + spatial/object-aware | L
[wave3] W3_VisualSpatialAttentionandProprioceptiveD | Q03 vision encoder | autoencoder-reconstruction global latent collapses under lighting (avg 56%) | - reconstruction-pretrained global features | L
[wave3] W3_ContrastiveActionImagePretrainingforVisu | Q03 vision encoder | frozen-encoder real avg: CAIP 76.0 vs SigLIP2 43.4, SigLIP 42.4, DINOv2 42.0, MVP 42.0, R3M 17.4 (6 tasks x12) | + action-aligned pretraining; ~ generic frozen encoders task-dependent | M
[wave3] W3_XDistillCrossArchitectureVisionDistillat | Q03 vision encoder | real xArm 20-25 demos DP: DINOv2-distilled ResNet18 75.6 vs scratch ResNet18 41.9 vs fine-tuned DINOv2 ViT-S 31.4; sim 34 tasks 87.2 vs 64.1 vs 66.2 | + pretrained-prior CNN fine-tuned e2e; - fine-tuned ViT at few demos | M
[wave3] W3_DecouplingtheDeclarativefromtheProcedura | Q03 encoder | frozen MetaCLIP2 ViT-L + frozen VFM, 55M trainable works at 16 demos/pair on SO-101 | + frozen pretrained encoders in low data | M
[wave3] W3_BeingH05ScalingHumanCentricRobotLearning | Q03 vision encoder | LIBERO 5-shot, frozen Und+ViT: manipulation-pretrained 77.1 vs generic VLM 51.3; full FT 85.1 vs 84.1 | ~ frozen only if robot-pretrained; FT closes gap | M
[wave3] W3_GeometricActionModelforRobotPolicyLearni | Q03 vision encoder | DA3 geometric backbone: LIBERO-Plus camera 83.1 vs best baseline 73.4, OFT 56.4; total 85.5 vs pi0.5 84.6 | + geometric foundation encoder for viewpoint robustness | M
[wave3] W3_MitigatingtheHumanRobotDomainDiscrepancy | Q03 encoder | frozen R3M Adroit 74.0 -> adapter-aligned 81.3 (full FT 77.7); RLBench D4R 55.3 -> 59.9; real +11-13% (fig) | - frozen human-video encoders as-is; + light last-layer adapter with robot-domain data | L
[wave3] W3_IsForwardPredictionEnoughPhysicalStateGr | Q03 encoder | frozen DINOv2 probes: EE-yaw r 0.50, gripper vel 0.20 vs grounded 0.98/0.69; fine-tuned DINOv2 80.1 vs 85.3 LIBERO-Goal | - frozen generic encoder w/o state grounding | L
[wave3] W3_MimicIntentNotJustTrajectories | Q03 vision encoder | frozen SigLIP+DINOv2 concat: LIBERO-Plus light 92.2, background 77.1, camera 61.4 | + frozen foundation features for photometric robustness | L
[wave3] W3_mimicvideoVideoActionModelsforGeneraliza | Q03 vision encoder | video-pretrained (Cosmos 2B) > PaliGemma 3B VLM features, 10x sample efficiency (LIBERO) | + video/dynamics pretraining (large scale) | M
[wave3] W3_TowardsAccessiblePhysicalAILoRABasedFine | Q03 vision encoder | frozen 74% vs LoRA-unfrozen 76% (200 eps); vision-influence 4.5 vs 6.2 | ~ freezing costs little at 200 demos | L
[wave4] W4_BridgeVLAInputOutputAlignmentforEfficien | Q03 | adding per-pixel 3D pos features into VLM image tokens 88.2 -> 56.2 | - modifying pretrained encoder input distribution | M
[wave4] W4_FP3A3DFoundationPolicyforRoboticManipula | Q03 | pretrained FP3 95/82.5 vs scratch 30/1.25 in-domain/wild, 4 real tasks, 80 demos | + large-scale pretrained policy/encoder over scratch | H
[wave4] W4_MINERVAHowSmallCanaManipulationPolicyBea | Q03 vision encoder | scratch CNN LIBERO-Plus light 1.1-6.5%, background 4.7-9.3%, camera 11.5-34.6% | - scratch encoder for robustness | M
[wave4] W4_AdaptiveCapacityAllocationforVisionLangu | Q03 vision encoder | learned adapter rank highest in vision tower (fig); OOD embodiment needs higher rank | + fine-tune vision encoder for new robot/cameras | L
[wave4] W4_ArtificialFoveatedPerceptionforMitigatin | Q03 vision encoder | SmolVLA attention Soft-IoU w/ task mask only 0.12 after fine-tune; pretrained VLM backbones still shortcut | - "pretrained VLM = robust" | M
[wave4] W4_LookWhereItMattersAdaptiveVisualRefineme | Q03 | pi0 LIBERO avg 94.2 -> +4 registers ~97.2; removing learned registers -4.45 avg; <4 registers can be below baseline | + register tokens when fine-tuning ViT encoder | L
[wave4] W4_AttentionfromActionforActionEmergentVisu | Q03 vision encoder | frozen DINOv3 readout alone → near-0 control success; good as ROI localizer; FiLM-only box 39.4 vs crop 61.2 | ~ frozen DINO for where-to-look, trainable encoder for control | L
[wave4] W4_ARWAMAVisualConditionedAgentReadyWorldAc | Q03 encoder | frozen DINOv3 0.3B + 0.2B trainable reaches 87.2 sim / 71.7 real | ~ frozen DINO ok (no ablation) | L
[wave4] W4_SEVOSemanticEnhancedVirtualObservationfo | Q03 vision encoder | fully trainable ResNet-18 (ACT) adapts better than frozen SigLIP (SmolVLA) at ~100 demos | + trainable/fine-tuned encoder | L
[wave4] W4_MolmoAct2ActionReasoningModelsforRealwor | Q03 | action-expert-only tuning (frozen VLM) 93.05 vs full FT 97.20; LoRA 96.25 | - frozen backbone for control | M
[wave4] W4_CLASSContrastiveLearningviaActionSequenc | Q03 vision encoder | DP random-init vs ImageNet: 3-Stack DynCam 0.28 vs 0.61; PushT rand-color 0.16 vs 0.53; R3M < ImageNet | + ImageNet-pretrained ResNet over scratch/R3M | M
[wave4] W4_DecouplingVisionLanguageandActionforEffi | Q03 vision encoder | DINOv3 ConvNeXt-B frozen 32.6 vs fine-tuned 55.6; DINOv3 ViT-B 54.1, SigLIP-400M 53.9, Qwen3-VL ViT 51.8 | + fine-tuned DINOv3 | H
[wave4] W4_DecouplingSemanticsandGeometricGrounding | Q03 vision encoder | mask via early 4-ch concat 43.4 / pixel overlay 50.1 vs mid-feature addition 67.8 (sim) | - early channel fusion into pretrained stem | L
[wave4] W4_SLIM05BLearningActionGroundedPredictiveL | Q03 | fine-tuned DINOv2-B/14 (lr 1e-5) scene+wrist, no ablation | + fine-tuned DINOv2 | L
[wave4] W4_CTVAMACerebelloThalamicInspiredVisionAct | Q03 vision encoder | DINOv3-S+ backbone, 30 demos, 100% pouring (20 trials); not ablated | + pretrained DINO small backbone | L
[wave4] W4_HybridFlowA2NFEGenerativePolicyforRealTi | Q03 vision encoder | DINOv3-base fine-tuned end-to-end, wrist fisheye only, works in real (no ablation) | ~ fine-tuned DINOv3 viable | L
[wave4] W4_LanguageGuidedObjectCentricDiffusionPoli | Q03 vision encoder | point encoders: MLP+res 68.8, MLP 64.1, PointNet 14.9 (7 tasks) | + simple MLP point encoder | M
[wave4] W4_FoundationandSmallModelsCoordinationforV | Q03 vision encoder | SAM3 LoRA on ID data: gripper IoU 0 -> 99, object 14-33 -> 99; gripper mask essential (7.3 vs 98.7) | + frozen seg FM front-end, LoRA-adapted | M
[wave4] W4_RayViTRayConditionedVisualRepresentation | Q03 encoder | DINOv3 ViT-S pretrained 42.5 vs scratch 29.2 (default), fine-tuned end-to-end | + pretrained DINOv3 small, fine-tuned | M
[wave4] W4_MResTMultiResolutionSensingforRealTimeCo | Q03 vision encoder | heldout objects: frozen VLM (MDETR) 72.3 vs fine-tuned VLM 45.6 (train 82.0 vs 82.4) | + frozen language-grounded encoder for global view generalization | M
[wave4] W4_SKILSemanticKeypointImitationLearningfor | Q03 vision encoder | keypoint matching: DINOv2 far worse (mismatches under occlusion) than DiFT / RADIOv2.5-L/H (figure) | ~ correspondence features: DiFT/RADIO > DINOv2 | L
[wave4] W4_SynthICLScalableIncontextImitationLearni | Q03 encoder | frozen DINOv3 ViT-S 75.0% vs LoRA-finetuned 20.7% (sim, shared across views) | + frozen DINOv3 | M
[wave4] W4_PatchPolicyEfficientEmbodiedControlviaDe | Q03 vision encoder | frozen encoders (VQ-BeT Push-T/LIBERO): DINOv2 0.69/0.96, WebSSL 0.68/0.94, SigLIP2 0.51/0.83; real DINOv2-patch cable 0.70 vs ACT ResNet18-scratch 0.35 | + frozen DINOv2 patch tokens; - SigLIP for control | M
[wave4] W4_PatchPolicyEfficientEmbodiedControlviaDe | Q03 pooling | Push-T 256→1 patch: 0.69→0.48; real CLS vs patch cable 0.60 vs 0.70, pen 0.65 vs 0.85 | - global CLS/avg pooling | M
[wave4] W4_SemanticVLASemanticAlignedSparsification | Q03 vision encoder | SigLIP(ID-prune)+DINOv2(aggregate) 97.1 vs same-pruner variants 91.9/94.6/95.0 | + combine semantic and geometric encoders | L
[wave4] W4_MasqueradeLearningfromInthewildHumanVide | Q03 vision encoder | ImageNet/DINOv2/HRP ViT-B with 50 single-scene demos ~12% OOD avg vs 74% | - generic pretrained encoder alone for scene shift | M
[wave4] W4_WorldModelsforLearningDexterousHandObjec | Q03 vision encoder | frozen-latent WM planning: DINOv2 strongest overall vs DINOv3/SigLIP2/V-JEPA2/Web-SSL (figure) | ~ DINOv2 as frozen latent | L
[wave4] W4_SpotlightingTaskRelevantFeaturesObjectCe | Q03 vision encoder | frozen encoders real OOD: DINOv2 dense 0.07, ResNet-50 0.12, R3M 0.00, VC-1 0.03, DINOv2+slots 0.28, robot-pretrained slots 0.41 | ~ frozen dense brittle OOD; + object-centric bottleneck | M
[wave4] W4_SpotlightingTaskRelevantFeaturesObjectCe | Q13 data (pretraining mix) | slot pretraining mix D+B+F real 0.56 vs single dataset 0.26–0.45 | ~ | L
[wave4] W4_UADUnsupervisedAffordanceDistillationfor | Q03 vision encoder | frozen DINOv2 + FiLM decoder affordance; DINOv2-3ch baseline worse (figure) | ~ | L
[wave4] W4_VODPSemanticGeometricAdaptiveDiffusionPo | Q03 vision encoder | real 4 tasks x 60 trials: DP 11.2 / DP3 67.5 / VGGT-feature DP 87.9; sim sem-only 71.1, geo-only 63.9, fused 80.0 | + geometry-aware pretrained encoder (VGGT/DINOv2 fusion) | M
[wave4] W4_DIALDecouplingIntentandActionviaLatentWo | Q03 vision encoder | foresight in DINOv2 space instead of native ViT: 58.3 -> 47.2 | ~ keep aux target in policy's own encoder space | L
[wave4] W4_PriorVLAPriorPreservingAdaptationforVisi | Q03 vision encoder | trains vision encoder, freezes LLM + prior expert (not ablated alone) | ~ | L
[wave4] W4_RoBridgeAHierarchicalArchitectureBridgin | Q03 vision encoder | frozen DINOv2 features instead of masks: mean 82.1 -> 50.4, camera pose 74.8 -> 30.6 | - frozen DINOv2 for small policy | L
