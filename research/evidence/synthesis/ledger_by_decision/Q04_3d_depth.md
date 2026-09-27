# Q04_3d_depth — 94 ledger lines
[fulltext] DP3 | 3d_input | real 40 demos: DP3 85±11 vs image DP 35±25 vs depth-image DP 20±12 | + point cloud | M/H
[fulltext] iDP3 | 3d_input | OOD (new obj/view/scene): image DP(finetuned R3M+jitter) 0-3/10 vs iDP3 9/10 | + 3D for OOD | M/H
[fulltext] iDP3 | 3d_setup | camera-frame clouds, no calibration; 4096 pts; conv pyramid encoder | + | M
[fulltext] CopycatAgents | eval/checkpoint | test loss BC-OH < BC-SO and Ours > BC-OH, yet reward ordering opposite in several envs | - val loss as selection criterion | M
[fulltext] robomimic | eval/checkpoint | lowest-val-loss or last checkpoint 10–100% rel worse than best checkpoint | - val loss for checkpoint selection | H
[fulltext] RT-1 | eval/checkpoint | real-to-sim (RetinaGAN) success ordering directionally matches real; used for checkpoint selection | ~ proxy eval needed, not loss | L
[fulltext] FlowPolicy | Q04 3d_input | 2D DP 35.2 / CP 50.1 vs 3D DP3 68.7 / FlowPolicy 70.0 (sim, 10 demos) | + point cloud (sim) | L/M
[fulltext] MDT | eval/checkpoint | MT-ACT kept improving after val loss rose → authors used last epoch | - val loss for ACT-style ckpt selection | L
[fulltext] RoboMP-DINOv2 | Q04 3D | hard object-centric 3D filtering: obstacle task 3–7% vs full-scene 80–83% | - segmented-only point clouds | M
[fulltext] DemoGen | 3D | spatial gen at 100 demos: DP3 49, DP+DINOv2 61, DP+CLIP 53, DP scratch 22, R3M 9 | + 3D / pretrained encoders | M
[fulltext] 3DDiffuserActor | Q04 3d_input | RLBench same model: 3D tokens 81.3 vs 2D pooled 47.0; single front RGB-D 78.4 | + 3D (RGB features lifted to 3D) | H(sim)/L(real)
[fulltext] 3DDiffuserActor | Q04 fusion | CALVIN ABC→D: pooled point embedding (DP3) 0.31 vs tokenized lifted CLIP features 3.35; rel-attn 81.3 vs abs 71.3 | + lift pretrained 2D feats to 3D + relative attention | M
[fulltext] 3DDiffuserActor | Q04 depth_noise | trained clean; 3D noise σ²=0.01 → 72.4 (−6), σ²=0.03 → 50.1 (−28) | ~ needs moderate-quality depth / noise aug | M
[fulltext] Hyper-DP3 | Q04 3d_input | Piper + single D455 stereo, 50 demos, joint actions: HDP3 73/47/20% vs DP3 53/33/7% (15 trials) | + point-cloud policy works with stereo depth on low-cost arm | M
[fulltext] PointVLA | Q04 fusion | scratch conv point encoder → zero-init linear → additive into 5 late action-expert blocks; VLM 2D-only | + side-branch injection preserving pretrained 2D | M
[fulltext] PointVLA | Q04 3d_input | table height 3→52 mm: 2D VLAs 0/5, PointVLA 5/5; photo-vs-real 0/3 vs 3/3 | + 3D for geometry/height shift | L/M
[fulltext] PointVLA | Q04 rgb_concat | RoboTwin: DP3+RGB < DP3 in 12/13 tasks @20 demos (mean 15.6 vs 23.6) | - naive RGB concat into point cloud | M
[fulltext] PointVLA | Q04 encoder | pretrained 3D encoders hindered learning (no numbers) | + small scratch point encoder | L
[fulltext] EquivariantDP | Q04 3d_input | same DP: voxel 46.3 vs RGB 42.0 @100 demos (+4); equivariance bigger factor | ~ 3D alone modest in sim | M
[fulltext] EquivariantDP | Q04 equivariance | SO(2)-equi +21.9 pts @100 demos; real 80–95% vs voxel-DP 0–60% (20–60 demos, 20 trials) | + equivariant/rot-aug 3D (needs EE actions + calibration) | M/H
[fulltext] CONFLICT | 3d_input | iDP3/DP3 (camera-frame full-scene clouds robust OOD) vs CAGE/RISE (full-scene cloud 0.13 new background, 0 all shifts) & GROOT (only segmented object-centric 3D robust) — likely: robustness needs object-centric/cropped clouds; iDP3 scenes may have had less background clutter change | ~ object-centric 3D | OPEN
[wave3] W3_AffordDPGeneralizableDiffusionPolicywith | Q04 | real 100 demos/task: DP3 0-40% vs affordance-conditioned DP3 40-80%; DP3 overfits object positions | ~ point cloud alone insufficient; + explicit 3D object prior | L
[wave3] W3_DiffusionEDFsBiEquivariantDenoisingGener | Q04 3D input | sim: ~80% total success in unseen instances+poses+clutter from 10 demos vs ~0 for non-local baselines without segmentation (keyframe) | + point cloud / equivariance (keyframe) | L
[wave3] W3_EquivariantDescriptorFieldsSE3Equivarian | Q04 3D input | sim keyframe: 1.00 vs 0.84 (type-0 only) on unseen instances/poses/distractors, 5.1 s inference | + point cloud equivariance (not real-time) | L
[wave3] W3_DeFMLearningFoundationRepresentationsfro | Q04 depth | depth-pretrained ResNet-18 grasp 0.894 (FT) vs ImageNet 0.795 vs scratch 0.777 (sim RL, depth in all arms) | + depth-specific pretrained encoder if depth used | L
[wave3] W3_FurnitureVLALearningLongHorizonBimanualF | Q04 | front depth replacing rear RGB: 0.50 vs 0.80 | - depth as extra image channel in VLA (confounded) | L
[wave3] W3_GNFactorMultiTaskRealRobotLearningwithGe | Q04 3D | real xArm 5 demos/task: GNFactor 43.3 vs PerAct 22.5 (both voxel 3D, 10 trials/cell) | ~ 3D + foundation features | L
[wave3] W3_Instructiondrivenhistoryawarepoliciesfor | Q04 depth | point cloud tokens 73.1->77.1 | + depth/points | L
[wave3] W3_MakingSenseofVisionandTouchLearningMulti | Q04 | modality ablation: no-depth worst, no-RGB least harmful (figure, sim insertion) | + depth for geometric/contact tasks | L
[wave3] W3_CLIPortWhatandWherePathwaysforRoboticMan | Q04 depth | CLIP-only RGB ~76% vs two-stream RGB-D >90% (sim avg) | + depth/spatial stream for precision | L
[wave3] W3_PredictionwithActionVisualPolicyLearning | Q04 depth | real Panda (wrist cam, 50 rollouts/task): PAD 72 → PAD-Depth 78 | + depth as extra input | M
[wave3] W3_VistaBotViewRobustRobotManipulationviaSp | Q04 3D/depth | depth+pose reprojection to training view (GT geometry) VGS 0.79 vs estimated 0.67 vs ACT 0.24 | + geometric canonicalization via depth | M
[wave3] W3_RVTRoboticViewTransformerfor3DObjectMani | Q04 3D/depth | RLBench avg: RVT re-rendered orthographic virtual views 62.9 vs raw sensor views 22.9; PerAct voxels 49.4; image-BC 1.3; no depth channel 60.3 | + RGB-D → point cloud → virtual views | M
[wave3] W3_CageCausalAttentionEnablesDataEfficientG | Q04 3D vs RGB | RISE single-view point cloud best in-domain but bg 0.13, obj 0.00, L2 0 | - scene point cloud as robustness fix | M
[wave3] W3_LearningGeneralizableManipulationPolicie | Q04 3D vs RGB | segmented object point clouds in base frame: sim Cam-Hard 61.7 vs BC-RNN 0; Bg-Hard 63.3 vs 0 | + object-centric point cloud | M
[wave3] W3_LearningGeneralizableManipulationPolicie | Q04 3D vs RGB | naive RGB-D input fails all generalization settings (figure) | - raw RGB-D as robustness fix | M
[wave3] W3_TransporterNetworksRearrangingtheVisualW | Q04 3D vs RGB | top-down RGB-D heightmap pick-place from 1-10 demos (sim); real kit 98.9% | ~ structured primitive alternative, calibration-sensitive | L
[wave3] W3_CanonicalPolicyLearningCanonical3DRepres | Q04 depth/point cloud | UR5 shoe 50 demos: CP-SO2 4/10 & 6/10 vs ACT/DP/EquiDiff/DP3 0/10; Franka 100 demos CP 7/6/4/3 vs DP 2/1/4/0 | + xyz point cloud (canonicalized) | M
[wave3] W3_ConstrainedContextConditionalDiffusionMo | Q04 depth | depth height-map sim-to-real, 5 demos: C3DM 100% kitting/hang-cup; DP 0% (5 demos) | ~ depth helps sim2real keyframe | L
[wave3] W3_FourierFeaturesLetAgentsLearnHighPrecisi | Q04 3D/depth | real PointPatch+RGB 14.8 -> 40.2 with Fourier xyz; RoboCasa 13 -> 34; ablation no-FF 17.5 vs FF 39.9 | + point cloud only with Fourier pos-encoding; - raw xyz encoders | M
[wave3] W3_AnchorVLA4DanAnchorBasedSpatialTemporalV | Q04 3D | RGB-only Any4D encoder +4.2 pts (60.4->64.6) no depth sensor | ~ implicit 3D from RGB | L
[wave3] W3_OnBringingRobotsHome | Q04 depth | wrist RGB-D (median-pooled depth) > RGB-only on most tasks (figure); blinds-at-night depth 2/10 vs RGB 10/10 | + add depth, beware OOD depth | M
[wave3] W3_ContinuousVisionLanguageActionCoLearning | Q04 depth | RLBench avg: 2D CCoL 68.0 vs CCoL3D (RGB-D 3D tokens) 84.9 | + 3D tokens | L
[wave3] W3_RoboticManipulationisVisiontoGeometryMap | Q04 3D | RGB-only 3D prior (VGGT) beats depth-input GeoVLA 98.1 vs 97.7 LIBERO | ~ implicit 3D from RGB, no depth needed | L
[wave3] W3_P3POPrescriptivePointPriorsforVisuoSpati | Q04 3D/depth | naive RGB-D token ~RGB (pick mug 19/40 vs 13/40; novel 3/30 vs 6/30); 3D keypoints 39/40; monocular depth = camera depth (all 5/5) | + depth-lifted keypoints, ~ raw depth channel | M
[wave3] W3_RoboTwin20AScalableDataGeneratorandBench | Q04 3D | DP3 best clean (55.2) but 5.0 under DR despite perfect point clouds | ~ 3D helps in-distribution, not visual-shift robust via clutter | M
[wave3] W3_PerceiverActorAMultiTaskTransformerforRo | Q04 3D | voxel Perceiver 2.8x over C2FARM-BC, 34x over RGB-D Image-BC (RLBench, 10/100 demos) | + 3D fused input for few-demo multi-task | M
[wave3] W3_GLUEGlobalLocalUnifiedEncodingforImitati | Q04 3D | MimicGen DP3 34.4 vs RGB GLUE 52.4 vs ACT 34.8 | - plain DP3 | L
[wave3] W3_GroundedActionModel3DGroundingasaFoundat | Q04 3D/depth | DP3 whole-scene PC 55.2 Easy -> 5.0 Hard; det-only 16.0 / image-only 20.3 / both 46.8 | + RGB + object-cropped 3D; - raw scene point cloud for robustness | M
[wave3] W3_KAIAKinematicAwareInterfaceforDataEffici | Q04 3D | DP3 point cloud 37.3 sim avg vs ACT 58.5 RGB; fused DINOv2+PC 82.9 | - point-cloud-only; ~ fused RGB+3D | L
[wave3] W3_LaST0LatentSpatioTemporalChainofThoughtf | Q04 3D | latent modality alone: image 74%, point cloud 76%, proprio 75%, all 82% | ~ 3D small gain | L
[wave3] W3_PolarNet3DPointCloudsforLanguageGuidedRo | Q04 3D/depth | RLBench 10 tasks: XYZ-only 72.1 -> +RGB 91.3 -> all feats 92.1; crop table/background 81.6 -> 92.1; vs 2D Hiveformer 88.4 | + colored cropped point cloud | M
[wave3] W3_SelfSupervisedCorrespondenceinVisuomotor | Q04 3D/depth | 3D keypoints (depth) Push plate 98 vs 2D 87; better outside train convex hull | + depth-lifted features | L
[wave3] W3_SpatialVAMSpatialAwareMultiViewVideoDiff | Q04 3D/depth | real FR3 10 demos: RGB-D point cloud rendered to 3 virtual views; 1 camera 50.0 (orig views)/60.0 (adapted) vs 3 cams 57.1; 20mm/2deg calib error 51.4 | + single RGB-D via virtual-view projection is viable | L
[wave3] W3_TowardsEffectiveUtilizationofMixedQualit | Q04 3D | same 50 mixed demos: RISE 3D 90/90/87.5/70/50/40 vs DP 10/35/30/50/30/26.7 | + point cloud (uncontrolled arch) | L
[wave3] W3_SIDSlidingintoDistributionforRobustFewDe | Q04 3D | DP3 OOD 0-12% similar to ACT 0%; SID point-cloud egocentric works | ~ 3D alone not enough for spatial OOD | L
[wave3] W3_ToolFlowNetRoboticManipulationwithToolsv | Q04 3D/depth | sim tool tasks: RGBD 0.606 vs RGB 0.538 vs point-flow 0.892; flow gives no gain on translation-only variant | ~ 3D helps mainly rotation-heavy tasks | L
[wave3] W3_VisualThinkVLAVisualIntermediateReasonin | Q04 depth | Depth Anything V2 channel screened out as low-utility | ~ monocular depth cue | L
[wave3] W3_GeoVLAEmpowering3DRepresentationsinVisio | Q04 3D/depth | real WidowX+D435i: 86.3 vs CogACT 76.3; basket height H1 60 vs 20; EE-frame point token; DP3-MLP encoder 95.8 vs PEN 97.7 LIBERO | + depth branch in robot/EE frame | M
[wave3] W3_DeepSE3EquivariantGeometricReasoningforP | Q04 3D/depth | RLBench keyframe placement 10 demos: rot error 0.6-1.2 deg vs TAX-Pose 1.2-5.5 deg (segmented point clouds, planner execution) | ~ equivariant 3D helps precise placement, not closed-loop | L
[wave3] W3_ManiFlowAGeneralRobotManipulationPolicyv | Q04 3D/depth | clutter task @100 demos: xyz-only 57.3 vs +RGB 86.0; real point-cloud ManiFlow 71.0 vs DP3 37.6 | + colored point cloud | M
[wave3] W3_PRISMPerformerRSIMLEforSinglepassMultise | Q04 depth | dropping depth: 66.2 vs 65.2 full (no loss) | - depth input when wrist RGB present | L
[wave3] W3_ROPASyntheticRobotPoseGenerationforRGBDB | Q04 depth | ACT RGB->RGB-D single D415: CLB 41.3->56.7, CPB 43.3->49.7, BSR 21.3->26.7; real 13->15, 4->5, 14->17 /20 | + depth channel on scene cam | M
[wave3] W3_ReconcilingRealitythroughSimulationAReal | Q04 3D | single depth-cam point-cloud BC still 11% with distractors | ~ 3D alone not robust to distractors | L
[wave3] W3_VolumeDPModelingVolumetricRepresentation | Q04 3D/depth | RGB-only volume 90.7 vs 2D tokens 78.2 vs GT-depth occupancy selection 75.8 (LIBERO-Spatial) | + calibrated 3D lifting even without depth | M
[wave4] W4_3DCAVLALeveragingDepthand3DContexttoGene | Q04 | LIBERO w/o depth 97.0 vs 98.1 seen, 41.0 vs 45.2 unseen (sim only, 7B VLA) | + depth point-cloud branch | L
[wave4] W4_BridgeVLAInputOutputAlignmentforEfficien | Q04 | Real 10 demos/task, 13 tasks: BridgeVLA 96.9%, RVT-2 90% (3D) vs ACT 22.3%, pi0 3.8% (2D) — keyframe tasks | + 3D point-cloud input for low-data | M
[wave4] W4_FP3A3DFoundationPolicyforRoboticManipula | Q04 | Clean Table: FP3-Base point cloud 95/90 vs FP3-Base-Image (DINOv2) 90/55 in-domain/wild | + point cloud for OOD generalization | M
[wave4] W4_LIFDAnchoredDiffusionfor3DAwareSceneMemo | Q04 3D/depth | RGB geometry-aware (VGGT) features, real UR5e 10 demos: LIFD 56.0 vs Lift3D 34.5 vs DP 31.0 vs OpenVLA 40.5 | ~ RGB geometry priors vs depth | L
[wave4] W4_AttentionfromActionforActionEmergentVisu | Q04 3D | DP3 manual crop ≪ RGB DP on MimicGen at 200 demos; ROI filtering +24-42 pts | - point cloud (for rotation-heavy tasks) | L
[wave4] W4_CoLAFlowPolicyTemporallyCoherentImitatio | Q04 3D | single fixed L515 point cloud, 30 demos: own encoder 85% vs DP3 encoder 70% | ~ point cloud viable; encoder matters | L
[wave4] W4_ClutterRobustVisionLanguageActionModelst | Q04 | masked depth vs masked RGB: unseen objs 70→78 (2-stage), 57→69 (1-stage); seen clutter ~flat | + depth for novel-appearance objects | M
[wave4] W4_DepthCacheDepthGuidedTrainingFreeVisualT | Q04 3D/depth | depth-partitioned merging vs uniform: −18.2% if depth partition removed (LIBERO) | ~ depth as foveation prior | L
[wave4] W4_ChronosAPhysicsInformedFullHistoryFramew | Q04 depth | D435 point cloud too noisy for small blocks -> used single RGB + frozen ResNet18 in real | - D435 point clouds for small objects | L
[wave4] W4_GeneralizableHierarchicalSkillLearningvi | Q04 3D/depth | GemBench zero-shot mean 82.3 (3 demos, object point cloud) vs RVT-2 46.5, BridgeVLA 58.9 (100 demos); real 9/10 vs 4/10 w/ distractors | + segmented object point cloud from depth | M
[wave4] W4_ExploringPoseGuidedImitationLearningforR | Q04 3D/depth | relative 6D pose DP 81.7% ID vs RISE point cloud 3.3%, ACT 1.7% (sub-mm insertion, 10 trials) | ~ object-centric pose for precision only | L
[wave4] W4_HoloBrain0TechnicalReport | Q04 3D/depth | depth+camera-param 3D PE in VLA; no isolating ablation | ~ | L
[wave4] W4_LanguageGuidedObjectCentricDiffusionPoli | Q04 3D/depth | RLBench 21 tasks 40 demos: object-only point cloud 68.7 vs DP3 scene pc 43.6 vs RGB DP 39.3 | + segmented object point cloud | M
[wave4] W4_FastinSlowADualSystemFoundationModelUnif | Q04 3D input | RLBench System-1 input: +point cloud 0.69 vs no PC 0.61 vs no PC/no img 0.44 | + point cloud as extra input | L
[wave4] W4_OGVLAOrthographicImageGenerationfor3DAwa | Q04 3D/depth | real 3-5 demos: OG-VLA (RGB-D -> canonical ortho views + SE(3) aug) Pickup 100/80/90 (pose/obj/scene) vs pi0-FAST fails all tasks | + canonical 3D representation for few-demo keyframe policies | L
[wave4] W4_FoundationandSmallModelsCoordinationforV | Q04 depth | target mono-depth L1 vs L0 OOD: Microwave 83.6->90.9, Grill 73.5->81.8, Lift ~equal; S2-style depth channel much worse (48.7 vs 82.7 ID) | ~ depth helps contact tasks, encoding matters | M
[wave4] W4_HumanEgoZeroShotRobotLearningfromMinutes | Q04 | Water Flowers: RGB 7.5%, robot-RGB 32.5%, RGB+3D entity-pose tokens 85%, full 95% (40 trials) | + explicit 3D object-relative state from depth | M
[wave4] W4_RayViTRayConditionedVisualRepresentation | Q04 3D | point-map PMP-xyz 42.1->20.8, Adapt3R 41.7->28.5 under camera shift (no better than RGB) | - 3D input as viewpoint fix | M
[wave4] W4_GeoPredictLeveragingPredictiveKinematics | Q04 depth | depth as training supervision only; real geometry gen pi0 50 vs 95%, spatial 60 vs 85% (20 trials) | + depth as aux target, not input | L
[wave4] W4_JAMBJointActionMotionDiffusionforBimanua | Q04 | w/o 4D RoPE (depth positional grounding) 81.7→74.1; DP3 sim 58.1 vs DP 45.8 but DP3 real 35.6 | + depth as positional/aux, ~ raw point cloud | M
[wave4] W4_PocketDP3EfficientPocketScale3DVisuomoto | Q04 3D/depth | single D455 point cloud, 50 teleop demos, joint actions: Place 73.3, Bottle 46.7, Stack 20.0 (15 trials) | ~ point cloud works on low-cost arm, modest SR | L
[wave4] W4_Learningathousandtasksinaday | Q04 | segmented target-object point cloud (single RGB-D) → 1000 tasks 78.25% seen / 68% unseen from 1 demo each | + object-segmented depth input | M
[wave4] W4_SKILSemanticKeypointImitationLearningfor | Q04 3D/depth | 3D semantic keypoints vs DP3 full point cloud: unseen 72.8 vs 25.0; DP3 fails with distractors (1/10) | + sparse 3D object keypoints over scene point cloud | M
[wave4] W4_SSIPolicyLearningStructuredSceneInterfac | Q04 depth | LIBERO 10 demos: motion-only 63.42 -> +mono depth features 76.92 -> full SSI 80.42; depth-only 63.15 | + mono depth features as extra input | M
[wave4] W4_VODPSemanticGeometricAdaptiveDiffusionPo | Q04 3D vs RGB | single RGB + VGGT 87.9 vs L515 point-cloud DP3 67.5 real; sim 64.6 vs 64.0 | - raw point clouds; + 3D-aware RGB features | M
[wave4] W4_WhatstheMoveHybridImitationLearningviaSa | Q04 3D/depth | novel viewpoint: DP (RGB) 1/10 & 0/10 vs point-cloud waypoint SPHINX 9/10 & 9/10 (calibrated) | + calibrated 3D for reach phase | M
[wave4] W4_GaussianDreamEfficient3DGaussianWorldMod | Q04 3D/depth | training-only metric-depth loss: LIBERO-Plus Camera 76.5 -> 80.1; real camera-relocated 22.5 -> 42.5 (20 trials x2 tasks) | + depth as auxiliary supervision (no inference cost) | M
[wave4] W4_ManiVID3DGeneralizableViewInvariantReinf | Q04 3D/depth | view-randomized: w/o canonicalization 57.1 vs 92.9; DP3 (100 multi-view demos) 18.0 vs 78.4 with canonicalized encoder; real 103/140 vs 79/140 | + depth only if frame-canonicalized/calibrated | M
[wave4] W4_RoBridgeAHierarchicalArchitectureBridgin | Q04 3D/depth | raw depth vs masked depth: MT50 87.2 vs 85.4 but camera shift 60.8 vs 74.8 | ~ raw depth overfits viewpoint; mask/object-centric depth better | L
