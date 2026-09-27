# Q11_cameras — 83 ledger lines
[fulltext] robomimic | Q11 cameras | real Can: 73.3% with wrist vs 43.3% without; sim Transport −43% rel | + wrist cam | H
[fulltext] X-VLA | cameras | wrist view to separate vision encoder, not VLM: 50/47.9 -> 64.6 | + separate wrist encoder | M
[fulltext] UMI | cameras | wrist fisheye 20/20 vs 69°-FoV crop 11/20 | + wide-FoV wrist cam | M
[fulltext] Dita | Q11 cameras | LIBERO +wrist cam 82.4 → 92.3 avg (LONG 63.8 → 83.6) | + wrist camera | M
[fulltext] VideoPredictionPolicy | Q11 cameras | static-only 3.58 vs static+wrist 4.33 | + wrist cam | M
[fulltext] Octo | Q11 cameras | FT often better with 3rd-person only than 3rd+wrist (only 27% pretrain data has wrist) | - relying on OXE-pretrained generalist for wrist view | M
[fulltext] RDT-1B | Q11 cameras | 10% independent modality masking to avoid over-reliance on exterior vs wrist (not ablated) | + modality dropout | L
[fulltext] FAST | Q11 cameras | DROID: random 1-of-2 external cams in training, no calibration -> works from unseen viewpoints (44 trials, partial credit) | + multi-view randomization for camera shift | L/M
[wave3] W3_AxisGuideGroundingRobotActionCoordinateS | Q11 cameras | real DP front-only→front+wrist: Flip Pot 36.65→73.33, Grape 83.33→93.39, Close Pot 33.33→36.66 (30 trials) | + wrist cam | M
[wave3] W3_CoarsetoFineImitationLearningRobotManipu | Q11 cameras | wrist-cam last-inch correction net: 44.4% -> 70.0% avg over 8 real tasks (1 demo) | + wrist camera for fine alignment | L
[wave3] W3_VisionBasedManipulatorsNeedtoAlsoSeefrom | Q11 cameras | real BC 360 demos: OOD mean wrist 52% vs third-person 20% (both 85% ID); MW IQM wrist 73.7 / third 56.6 / both 66.3 / both+VIB(third) 87.7 | + wrist cam primary; ~ naive scene+wrist fusion; + bottlenecked scene stream | H
[wave3] W3_DecomposingtheGeneralizationGapinImitati | Q11 | sim: camera range radius 2.5->5->7.5 cm roughly doubles gap each step; real new head pose 45.8% | + keep scene camera rigidly fixed / randomize pose in data | M
[wave3] W3_DiffusionVLAGeneralizableandInterpretabl | Q11 cameras | OpenVLA 3 views 45.3 vs 1 view 12.7; camera-position shift: DP 0, OpenVLA 0, DiVLA 60% (5 trials) | + multi-view incl wrist | M
[wave3] W3_GivingRobotsaHandLearningGeneralizableMa | Q11 cameras | wrist-only + top-36% mask allows human video transfer; no mask 24.3 vs 54.3 | + wrist cam | L
[wave3] W3_FurnitureVLALearningLongHorizonBimanualF | Q11 | removing rear camera 0.80 -> 0.47; resolution 224/300/448: 0.60/0.72/0.80 | + additional views covering occlusion; + resolution | M
[wave3] W3_GNFactorMultiTaskRealRobotLearningwithGe | Q11 cameras | PerAct 1→4 input cameras 20.4→22.7 only | ~ more static cams as input low value | L
[wave3] W3_Instructiondrivenhistoryawarepoliciesfor | Q11 cameras | 3 views 65.4 vs best single view 40.1 (74 RLBench tasks) | + multi-view | M
[wave3] W3_MaskedImitationLearningDiscoveringEnviro | Q11 cameras | real Franka reach: both views 54.2% vs masked spurious top view 95.2% (constructed correlation) | ~ extra views can add spurious cues | L
[wave3] W3_MultiViewMaskedWorldModelsforVisualRobot | Q11 cameras | viewpoint-randomized training + multi-view MAE: real uncalibrated-camera cup pick 74.7% vs 11.3% (MWM) vs 7.1% (MAE+WM) | + train with varied camera poses | M
[wave3] W3_PolybotTrainingOnePolicyAcrossRobotsWhil | Q11 cameras | wrist-cam multi-robot policy 0.7-1.0 vs exterior-cam naive multi-robot 0.0-0.4 (5 demos, 10 trials; confounded) | + wrist camera for viewpoint/embodiment invariance | L
[wave3] W3_SeeingAlltheAnglesLearningMultiviewManip | Q11 | 200 demos, randomized camera pose: multiview ~ fixed-view on fixed-view task; fixed-view policy drops sharply with small yaw change (figure only; sim 5 seeds x 50 eps, real 10 eps) | + randomize scene-camera pose during data collection | M
[wave3] W3_VistaBotViewRobustRobotManipulationviaSp | Q11 cameras | single-view-trained ACT: sim 0.83 -> 0.13-0.28 at +-30/45 deg; real 0.79 -> 0.15/0.18 at +-45 deg; VistaBot 0.53/0.61 | - single fixed scene camera without viewpoint diversity | H
[wave3] W3_RVTRoboticViewTransformerfor3DObjectMani | Q11 cameras | single virtual front view 35.8 vs 3 views 60.2 vs 5 views 62.9 (all re-rendered from same sensors) | + multi-view (virtual) | L
[wave3] W3_EVLAEventAugmentedVisionLanguageActionMo | Q11 cameras | wrist-only: stacking fails from occlusion by grasped object; wide FOV lens "critical" (qualitative) | + add scene cam / wide wrist FOV | L
[wave3] W3_LearningGeneralizableManipulationPolicie | Q11 cameras | residual real failures = mm grasp misses without wrist cam (qualitative) | + wrist camera | L
[wave3] W3_RobustVisualSimtoRealTransferforRoboticM | Q11 cameras | second viewpoint 44.97→65.43% avg (+50.4 assembling), sim | + multi-view | M
[wave3] W3_TowardsSynergisticGeneralizedandEfficien | Q11 cameras | adding gripper camera/depth/tactile to specialist improves CALVIN avg len (figure only) | + wrist cam | L
[wave3] W3_CanonicalPolicyLearningCanonical3DRepres | Q11 cameras | camera rotated ~15 deg: image policies 0/10, CP 4-6/10; ~30 deg: CP 3/10 | + 3D canonical input for viewpoint shift | M
[wave3] W3_ConstrainedContextConditionalDiffusionMo | Q11 cameras | single top-down cam occluded by arm prevents recovery (stated) | + wrist cam | L
[wave3] W3_FourierFeaturesLetAgentsLearnHighPrecisi | Q11 cameras | 2 static + wrist; RGB-only and PC-only failed on real color-goal tasks | ~ fuse RGB+3D | L
[wave3] W3_RethinkingthePracticalityofVisionlanguag | Q11 cameras | CALVIN separate view tokens 1.50 vs merged composite image 3.68 | + wrist+scene, + token-cheap fusion | L
[wave3] W3_AStudyonEnhancingtheGeneralizationAbilit | Q11 cameras | with wrist cam present, 3rd-person camera-pose shift: Square .10, Threading .02, ThreePiece .00 | - wrist cam alone for viewpoint robustness | M
[wave3] W3_RoboticManipulationisVisiontoGeometryMap | Q11 cameras | real unseen scene camera (wrist kept): ACT 37->7%, pi0.5 77->52%, VGA 75->58% (20 trials) | + pretrained geometry backbone for viewpoint shift | M
[wave3] W3_GeoPropGroundingRobotStateinVisionforGen | Q11 cameras/fusion | EE-heatmap channel 61.7 vs RC-PE 60.8 vs local feature sampling 64.8 vs no-proprio 59.5 (MetaWorld 15) | + localized state-vision fusion | L
[wave3] W3_RobotUtilityModelsGeneralPoliciesforZero | Q11 cameras | wrist-only iPhone policy: 74.4% zero-shot in 25 unseen homes; ~10% drop moving to xArm/other camera | + wrist camera for env generalization | M
[wave3] W3_BAKUAnEfficientTransformerforMultiTaskPo | Q11 cameras | shared encoder .90 vs separate per-view .92 (+15% params/view) | ~ shared encoder ok | L
[wave3] W3_RoViAugRobotandViewpointAugmentationforC | Q11 cameras | DP, single side cam, 150 demos: same view 100% -> 10cm/20deg shift 0% (10 trials) | - single fixed scene camera without viewpoint aug | H
[wave3] W3_Pix2ActImageSpaceManipulationPolicieswit | Q11 cameras | w/o agent view only -2.8 pts; perturbed agent cam: DP fails both tasks, Pix2Act unaffected (qualitative) | + wrist cams primary; scene cam as context | M
[wave3] W3_PolarNet3DPointCloudsforLanguageGuidedRo | Q11 cameras | single cam 35-48%, L+R 67.0, L+wrist 80.2, all 3 92.1; wrist weakest alone but most complementary | + wrist cam as complement | M
[wave3] W3_SelectivePerceptionforRobotTaskAwareAtte | Q11 cameras | pi0+LoRA 50 demos: router on wrist+prompt 83.3% vs external+prompt 73.3%; static fusion of all streams 10% | + wrist cam as anchor; - naive static multi-stream fusion | L
[wave3] W3_SIDSlidingintoDistributionforRobustFewDe | Q11 cameras | same 50 demos: egocentric wrist RGB-D policy 80.3% vs fixed external cam 26.0% (6 real tasks) | + wrist camera | M
[wave3] W3_BeyondViewpointGeneralizationWhatMultiVi | Q11 cameras | sim DP eval at fixed 0deg: +-10/20/30/60 extra views 29.0/58.0/42.5/19.5 vs 12.5; budget-matched +-20: 33.5; pi0 34.0->42.0 | + multi-viewpoint training data (moderate +-20deg) even for single-cam deployment | M
[wave3] W3_GeoVLAEmpowering3DRepresentationsinVisio | Q11 cameras | camera rotated 15/30/45 deg: GeoVLA 90/80/70 vs CogACT 60/40/0, pi0 50/40/30 | + 3D input for viewpoint robustness | M
[wave3] W3_CRAFTVideoDiffusionforBimanualRobotDataG | Q11 cameras | 4 new camera views: no aug 6/3/2 vs NVS 14/8/6 vs multi-view generated 19/18/18 (/20) | + viewpoint augmentation for camera shift | M
[wave3] W3_PRISMPerformerRSIMLEforSinglepassMultise | Q11 cameras | CALVIN eval dropout: full 65.2, no wrist RGB 41.5, no proprio 15.8, no depth 66.2 | + wrist cam + proprio essential | M
[wave3] W3_ROPASyntheticRobotPoseGenerationforRGBDB | Q11 cameras | ACT CLB 1 cam 41.3 vs 4 tiled cams 72.0 | + multi-view | L
[wave3] W3_mimicvideoVideoActionModelsforGeneraliza | Q11 cameras | real bimanual: DINO ViT-S DiT policy workspace-only 11.0/30.0 vs +wrist cams 42.6/74.1 | + wrist camera | M
[wave3] W3_SeeSelectivelyActAdaptivelyDualLevelStru | Q11 cameras | per-phase wrist-view gating: Hard 22.3->40.7 (alone); real Hard w/ distractors 10-20% -> 40-60% (full model) | + view gating / view dropout vs distractors | M
[wave3] W3_VisualPolicyLearningThroughMultiCameraVi | Q11 cameras | sim cube random-view SR: front-only 2.0, front+wrist 23.3, front+side+wrist 68.7; mug front-only unlearnable (0) vs 2cam 99.3 fixed | + wrist cam and extra views | M
[wave3] W3_VolumeDPModelingVolumetricRepresentation | Q11 cameras | 2D DP collapses 65/60% ID -> 0% under +-5 deg camera rotation | - relying on fixed scene cam with 2D features | M
[wave3] W3_WorldtoWristTaskConditionedFutureWristMo | Q11 cameras | wrist-centric future modeling: real std 70.0 vs 54.4 (VLA-JEPA) vs 41.1 (pi0); OOD 52.2 vs 37.8 (30 trials/task) | + wrist cam as action-proximal signal | L
[wave4] W4_BridgeVLAInputOutputAlignmentforEfficien | Q11 | single static ZED depth cam, real 96.9% | + single scene depth cam enough for keyframe pick-place | L
[wave4] W4_GroundingSimtoRealGeneralizationinRoboti | Q11 cameras | ±1cm camera pose randomization gives +10-20 pts real SR vs clean | + viewpoint randomization | M
[wave4] W4_AdversarialDataCollectionHumanCollaborat | Q11 cameras | masked camera avg: trad 0.0 vs ADC 0.55 | + occlusion-rich data for camera redundancy | L
[wave4] W4_LookWhereItMattersAdaptiveVisualRefineme | Q11 | single third-person RealSense: uncertainty-gated high-res crop 46.5 -> 69.0% real (with registers) | + close-range/high-res detail of interaction region matters | L
[wave4] W4_BehaviorCloningforActivePerceptionwithLo | Q11 cameras | 64x64 wrist RGB only suffices for centering task (5/5) | + low-res wrist cam | L
[wave4] W4_AttentionfromActionforActionEmergentVisu | Q11 cameras | wrist view not cropped; wrist fragile under over-exposure, needs scene view | ~ keep scene+wrist | L
[wave4] W4_BFAHierarchicalBestFeatureAwareTokenPrun | Q11 | wrist occlusion only fatal during manipulation phase; dropping wrist tokens Hammer 0.84→0.73 | + wrist cam | M
[wave4] W4_BreakingtheVisionActionShortcutLatentInt | Q11 cameras | camera-config shift still weakest: real 46.7% (LIT) vs 30.0% base; sim camera 39.4->48.4 (MolmoAct2) | ~ viewpoint shift remains hard | L
[wave4] W4_SEVOSemanticEnhancedVirtualObservationfo | Q11 cameras | adding wrist cam: ACT 90→86, SmolVLA 79→12 (mobile base, oscillation/grasp-release failures) | - wrist cam (mobile-base caveat) | L
[wave4] W4_DoYouNeedProprioceptiveStatesinVisuomoto | Q11 cameras | dual wide wrist w/o overhead 1.0/1.0 vs with overhead 0.983/0.583; overhead-only 0.217/0.133; 20 cm holder shift 0.80 w/o vs 0 with overhead | + wide-FoV wrist cam, - scene cam under placement shift | M
[wave4] W4_ViewpointAgnosticManipulationPolicieswit | Q11 cameras | DP Pick&Place across viewpoints: base 37.0 → Vantage 83.2; VR 8 random views 42.6 (< VR-1 63.8); real ACT reach 44 vs 30-36 | + few targeted extra viewpoints, - many random views | L
[wave4] W4_CLASSContrastiveLearningviaActionSequenc | Q11 cameras | +wrist cam Dyn-Cam Square: BC 21→66%, CLASS 68→90% | + wrist camera | M
[wave4] W4_CoLAFlowPolicyTemporallyCoherentImitatio | Q11 cameras | removing wrist cam: perturbation recovery 90% → 30% | + wrist camera | M
[wave4] W4_CrossViewActionConsistencyforCameraRobus | Q11 cameras | nominal-only VLA camera-track 16.8% vs multi-view 79.8–87.2%; real held-out cam 53.3→74.4% (90 rollouts) | + synchronized multi-view scene cams in training | M
[wave4] W4_WARPEDWristAlignedRenderingforRobotPolic | Q11 | wrist-only DP: WARPED 20/18/17/11/17 vs teleop 16/19/16/15/19 (x/20); novel obj Rotate Obj2 8/10 vs teleop 2/10 | + wrist camera for object-instance generalization | L
[wave4] W4_FromFixedtoFreeCamerasCalibrationFreeVie | Q11 cameras | train-view spacing 15/30/45°: π0 33.2/25.5/16.8, CamVLA 51.4/34.0/21.2 | + dense viewpoint coverage if multi-view training | M
[wave4] W4_GeneralizableRoboticInsertionwithWorldMo | Q11 cameras | sim RL: wrist cam placement with more occlusion of socket lowers success (figure only); blind policy much worse | ~ place wrist cam to avoid object occluding target | L
[wave4] W4_InfiNoVAInfiniteNovelViewAugmentationfor | Q11 cameras | SO-101+SmolVLA (wrist+scene), 70 demos: ref view 65.3% → random views 7.5%; 5 physical views 24% (P&P) | + multi-view training / rigid camera mount | H
[wave4] W4_LearningtoMoveBeforeLearningtoDoTaskAgno | Q11 cameras | single third-person view: viewpoint shift catastrophic, depth ambiguity failures | ~ need viewpoint robustness measures (wrist cam / aug) | L
[wave4] W4_JEPAPolicyDiffusionFreeImitationLearning | Q11 cameras | sim single seed: fixed+wrist beats wrist-only / fixed-only (Tool Hang 65 vs 27.5/35; 3-Piece 60 vs 15/42.5) | + scene+wrist | L
[wave4] W4_RayViTRayConditionedVisualRepresentation | Q11 cameras | 2 static + wrist (D405) cams; wrist view used as anchor | ~ wrist as stable reference view | L
[wave4] W4_MResTMultiResolutionSensingforRealTimeCo | Q11 cameras | real Franka: full 75.0/67.5 (pickup/insert) vs no-wrist 7.5/10.0 vs no-scene 20.0/12.5 | + scene + wrist both | M
[wave4] W4_SensingWhichModalityMattersEvidenceGated | Q11 cameras | single useful camera only: 10/40 -> 29/40 with EGR; policies depend on uninformative wrist/head views | + train each cam to be sufficient when it sees the object | M
[wave4] W4_SynthICLScalableIncontextImitationLearni | Q11 cameras | front+side+wrist 75.0 vs no wrist 60.3 vs no side 64.6 | + keep wrist cam + 2nd view | M
[wave4] W4_TheCurseofPrecisionADataScalingLawforHig | Q11 cameras | removing wrist cam: c 2.35→3.85 mm (DP, sim) | + wrist camera for precision | M
[wave4] W4_RobustBimanualVisionLanguageActionModels | Q11 | mask both wrist views (keep ego) 64.0 vs mask ego 37.0 vs none 23.7 (3 sim tasks) | + wrist cam with structured wrist-dropout, scene cam as anchor | M
[wave4] W4_WhatMattersinLearningfromLargeScaleDatas | Q11 cameras | sim camPose-misaligned: target-only 16.7, low-var cotrain 43.3, camPose-diverse cotrain 90; real aligned camPose +25-50% | + viewpoint diversity/alignment critical | M
[wave4] W4_WhatstheMoveHybridImitationLearningviaSa | Q11 cameras | wrist-only dense policy robust to distraction (1/10 -> 8/10); DP3 w/o wrist < DP with wrist | + wrist cam for precise phase | M
[wave4] W4_NovelDemonstrationGenerationwithGaussian | Q11 cameras | no-aug policy novel view 0-17%, moving cam 0-13% | - relying on fixed scene cam without view aug | M
[wave4] W4_XSimCrossEmbodimentLearningviaRealtoSimt | Q11 cameras | Shoe on Rack: side-only train -> frontal 23.3 / novel 33.3; side+frontal train -> 96.7/80.0/53.5 (10 trials) | + multi-viewpoint training data | L
[wave4] W4_ManiVID3DGeneralizableViewInvariantReinf | Q11 cameras | RGB-D Maniwhere drop 3.9% at ±30° -> 31.5% at ±75° yaw; ManiVID-3D <6.7% | + view-invariant 3D representation for camera shift | L
[wave4] W4_SimulationDrivenImitationLearningforBios | Q11 cameras | wrist-cam-only real-data policy collapses (0%) on new table color | - wrist cam alone not appearance-invariant | L
