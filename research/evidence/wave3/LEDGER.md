W3_AffordDPGeneralizableDiffusionPolicywith | Q04 | real 100 demos/task: DP3 0-40% vs affordance-conditioned DP3 40-80%; DP3 overfits object positions | ~ point cloud alone insufficient; + explicit 3D object prior | L
W3_AffordDPGeneralizableDiffusionPolicywith | Q14 | unseen instance real: Ours 45/50/65% vs DP3 0/0/30% vs DP 0% | + object-centric foundation-model correspondence for novel objects | L
W3_AffordDPGeneralizableDiffusionPolicywith | Q13 | sim 30 demos: all methods ~80% low variance, 13-53% high variance; image DP 0% real w/ 100 demos over 4 objects | + more demos needed as placement variance grows | L
W3_AffordDPGeneralizableDiffusionPolicywith | Q01 | affordance guidance in diffusion sampling: unseen cat 22.2->26.7% (sim) | ~ guided diffusion small gain | L
W3_ActionMapRobotPolicyLearningviaVoxelActi | Q01 action head | real Franka 50 demos: heatmap 14/30 vs L1 4/30; LIBERO 10% data 93.2 vs 67.2; grasp error 15.0 vs 35.5 mm | - L1 regression / + distributional head | M
W3_ActionMapRobotPolicyLearningviaVoxelActi | Q01 action head | vs pi0.5 flow: 98.5 vs 96.9 LIBERO avg | ~ heatmap vs flow | L
W3_ActionMapRobotPolicyLearningviaVoxelActi | Q13 data quantity | Insert 0/10 both heads at 50 demos, 5/10 at 275 | + more demos for multi-stage precision | M
W3_ActionMapRobotPolicyLearningviaVoxelActi | Q10 latency | single-pass heatmap head, no denoising steps (latency not measured) | + single-pass heads | L
W3_ActionQuantizedOfflineReinforcementLearn | Q01 action head | Robomimic PH avg: unimodal BC 22.5, VQ-discrete SAQ-BC 41.7, tuned GMM BC 64.1 (state-based sim) | - unimodal regression; ~ VQ | L
W3_AxisGuideGroundingRobotActionCoordinateS | Q11 cameras | real DP front-only→front+wrist: Flip Pot 36.65→73.33, Grape 83.33→93.39, Close Pot 33.33→36.66 (30 trials) | + wrist cam | M
W3_AxisGuideGroundingRobotActionCoordinateS | Q14 robustness (object position) | rendered EEF-anchored base-axis channels: unseen positions real DP 30.1→50.0, sim SmolVLA 52.4→65.7; robust to 3cm/6deg calib error | + action-frame visual cue | M
W3_AxisGuideGroundingRobotActionCoordinateS | Q02 action space | relative-EEF policies fail to re-target to unseen positions without frame grounding | ~ delta EEF needs grounding | L
W3_AxisGuideGroundingRobotActionCoordinateS | Q12 model size / finetune | full-finetuned SmolVLA used as stronger baseline than frozen-VLM action-expert-only (figure only) | + full finetune of SmolVLA | L
W3_BehaviorRetrievalFewShotImitationLearnin | Q13 | 10 target demos + VAE-retrieved prior data: sim avg 72% vs GC pretrain+FT 36%; real +>20 pts; naive mixing hurts | + filtered co-training with same-embodiment prior data | M
W3_BehaviorRetrievalFewShotImitationLearnin | Q14 | real pickle: new cup color Dt-only 1/10 vs retrieval 6/10; distractors 0/10 vs 4/10 | + data diversity from retrieved prior for appearance shift | L
W3_BehaviorRetrievalFewShotImitationLearnin | Q01 | ResNet18+LSTM+5-mode GMM trained end-to-end; no head ablation | ~ | L
W3_AnchorDreamRepurposingVideoDiffusionforE | Q05 augmentation | real PiPER DP 50 demos: 28% -> 63% (text 60%) with 10x motion-anchored generated demos; RoboCasa 22.5 -> 30.7 (oracle 33.3) | + generative synthetic demos (heavy compute) | M
W3_AnchorDreamRepurposingVideoDiffusionforE | Q13 data diversity | +-10 cm key-state perturbed trajectories give 2x real success at 50 seeds | + spatial coverage over raw count | M
W3_IMLEPolicyFastandSampleEfficientVisuomot | Q01 action head | Push-T 20 demos IMLE 0.10 vs DP 0.03 vs FM-1step 0.01; Robomimic ties within ~0.05; real 17-demo wins figure-only | + single-step IMLE generative head; - 1-step FM | M
W3_IMLEPolicyFastandSampleEfficientVisuomot | Q10 latency | 111 Hz (IMLE) vs 1.8 Hz (DP 100-step DDPM) on RTX3090; select candidate closest to previous chunk tail for consistency | + 1-step head + consistency selection | M
W3_IMLEPolicyFastandSampleEfficientVisuomot | Q13 data | Push-T reward 0.5 at <29% data vs DP ~43% vs FM >80%; real multimodal task from 17 demos | + generative 1-step head in low-data | L
W3_IMLEPolicyFastandSampleEfficientVisuomot | Q06 chunking | Tp=16/Ta=8/To=2 used; no sweep | ~ | L
W3_BridgeDataBoostingGeneralizationofRoboti | Q13 data diversity | 50 target demos + 7.2k multi-domain demos: 66% vs 28% target-only (seen tasks); new tasks 50% vs 22% | + co-train with diverse same-robot data | M
W3_BridgeDataBoostingGeneralizationofRoboti | Q14 robustness | gains only when objects/motions/scenes resemble prior data; camera pose randomized 0-10cm/0-30deg during collection | + collect with camera/scene randomization | L
W3_BridgeDataBoostingGeneralizationofRoboti | Q13 training recipe | joint training >> pretrain+finetune (stated, no numbers); bridge weight 70-90% avoids overfitting 50 demos | + joint co-training | L
W3_TubeDiffusionPolicyReactiveVisualTactile | Q10 latency | real: DP 37 ms/~25 Hz vs TDP 8 ms denoise + 3 ms stream >100 Hz; reorientation 60->96%, jar 84->96% (25 eps) | + per-step feedback correction inside chunk | M
W3_TubeDiffusionPolicyReactiveVisualTactile | Q06 chunking | open-loop DP chunks fail under disturbance; streaming-only (no chunk gen) drops Push-T 96.1->84.3, grasp 88->44% | - pure open-loop chunks; + chunk + step-wise correction | M
W3_TubeDiffusionPolicyReactiveVisualTactile | Q01 action head | DP DDIM-2 5.3% vs DDIM-10 98.4% (dish); image Push-T FM 65.3 vs DDPM 76.0 | - few-step vanilla diffusion | L
W3_CACTIAFrameworkforScalableMultiTaskMulti | Q05 augmentation | SD in-painting aug vs crop+color-jitter only: ~+15-20 abs success on real 10-task Franka (figure only) | + generative in-painting | L
W3_CACTIAFrameworkforScalableMultiTaskMulti | Q13 data diversity | sim held-out layouts: 10→100 training layouts R3M 9.5→33.1, MoCo 18.8→38.4 | + diversity over count | M
W3_CACTIAFrameworkforScalableMultiTaskMulti | Q03 vision encoder | frozen out-of-domain R3M ≈ in-domain MoCo ≈ fine-tuned in real (figure only); sim in-domain MoCo > R3M (75.9 vs 62.0 train) | ~ frozen pretrained | L
W3_CACTIAFrameworkforScalableMultiTaskMulti | Q14 robustness | ≈30% real success with shuffled/novel distractors | ~ | L
W3_CapturingVisualEnvironmentStructureCorre | Q03 | MetaWorld fine-tuned: DINOv2 0.767, CLIP 0.765, ViT-IN 0.683, MAE 0.648; frozen CLIP worst 0.562; best frozen encoder differs by env | + fine-tuned DINOv2/CLIP; - frozen CLIP | M
W3_CapturingVisualEnvironmentStructureCorre | Q09 | aux state-prediction loss joint w/ DP: +2.8..+7.2 pts on 5 backbones (e.g. MAE 0.648->0.712); joint > two-stage | + auxiliary state (pose) prediction | M
W3_CapturingVisualEnvironmentStructureCorre | Q01 | 3-layer MLP policy "somewhat worse" than diffusion, same encoders | + diffusion over MLP regression | L
W3_CoarsetoFineImitationLearningRobotManipu | Q11 cameras | wrist-cam last-inch correction net: 44.4% -> 70.0% avg over 8 real tasks (1 demo) | + wrist camera for fine alignment | L
W3_CoarsetoFineImitationLearningRobotManipu | Q07 history | filtering predictions over frames 35.6% -> 44.4% vs per-frame | + temporal fusion of estimates | L
W3_DABIEvaluationofDataAugmentationMethodsU | Q05 augmentation | symmetric temporal-offset pairing of 100Hz images with 1000Hz robot data (10x) → authors report 100% on 8 objects vs mostly-fail without (numbers not extractable, 5 trials/object) | + temporal-offset aug | L
W3_DABIEvaluationofDataAugmentationMethodsU | Q13 data quantity | 5 demos sufficient with 10x temporal augmentation for 1 Bi-ACT task | ~ | L
W3_VisionBasedManipulatorsNeedtoAlsoSeefrom | Q11 cameras | real BC 360 demos: OOD mean wrist 52% vs third-person 20% (both 85% ID); MW IQM wrist 73.7 / third 56.6 / both 66.3 / both+VIB(third) 87.7 | + wrist cam primary; ~ naive scene+wrist fusion; + bottlenecked scene stream | H
W3_VisionBasedManipulatorsNeedtoAlsoSeefrom | Q14 robustness | real table height +0.05m wrist 65 vs third 0; texture shifts 50/25/10 vs 5/15/5 | + wrist view for OOD | M
W3_VisionBasedManipulatorsNeedtoAlsoSeefrom | Q05 augmentation | DrQ without image aug fails to converge even with wrist cam | + keep image aug | M
W3_VisionBasedManipulatorsNeedtoAlsoSeefrom | Q09 aux objectives | VIB on third-person features +21 IQM OOD; VIB on both views 58.2 (hurts) | + info bottleneck on scene cam only | M
W3_DecomposingtheGeneralizationGapinImitati | Q14 | real RT-1: orig 91.7%, background 88.9, lighting 83.3, distractors 80.6, table texture 52.8, camera pose 45.8; factor pairs don't compound | ~ camera pose & texture hardest, lighting/background easy | M
W3_DecomposingtheGeneralizationGapinImitati | Q05 | random crop improves camera pose AND table texture; photometric helps texture factors (real fig, sim 5 seeds) | + random crop + color jitter | M
W3_DecomposingtheGeneralizationGapinImitati | Q11 | sim: camera range radius 2.5->5->7.5 cm roughly doubles gap each step; real new head pose 45.8% | + keep scene camera rigidly fixed / randomize pose in data | M
W3_DecomposingtheGeneralizationGapinImitati | Q13 | sim gap 0.4 -> <0.1 from 5 to 100 training envs; out-of-domain robot data improves robustness | + environment diversity | M
W3_DecomposingtheGeneralizationGapinImitati | Q03 | frozen R3M/CLIP ResNet50 leave large gap, CLIP ~ scratch CNN except object texture | - frozen pretrained reps for robustness | L
W3_DiffusionVLAGeneralizableandInterpretabl | Q12 model size | DiVLA 2B/7B/72B: sorting 66.2/74.9/82.4, bin-pick 63.7/66.7/75.9 (72B also more pretrain data) | + larger pretrained VLA (not feasible on 8GB) | M
W3_DiffusionVLAGeneralizableandInterpretabl | Q14 robustness | visual changes (lighting/background/distractors, 45 trials): DP 4/45, OpenVLA 12/45, DiVLA-2B 26/45; no aug used | + pretrained VLM backbone; - unaugmented DP | M
W3_DiffusionVLAGeneralizableandInterpretabl | Q11 cameras | OpenVLA 3 views 45.3 vs 1 view 12.7; camera-position shift: DP 0, OpenVLA 0, DiVLA 60% (5 trials) | + multi-view incl wrist | M
W3_DiffusionVLAGeneralizableandInterpretabl | Q10 latency | 8/4-bit quantization significantly degrades VLA (no numbers); DiVLA-2B 82Hz A6000 | - quantization as free speedup | L
W3_DiffusionVLAGeneralizableandInterpretabl | Q08 language | reasoning injection ablation in-dist avg 83.6 vs 50.3 | + richer language conditioning in VLA | L
W3_DiffusionEDFsBiEquivariantDenoisingGener | Q04 3D input | sim: ~80% total success in unseen instances+poses+clutter from 10 demos vs ~0 for non-local baselines without segmentation (keyframe) | + point cloud / equivariance (keyframe) | L
W3_EquivariantDescriptorFieldsSE3Equivarian | Q04 3D input | sim keyframe: 1.00 vs 0.84 (type-0 only) on unseen instances/poses/distractors, 5.1 s inference | + point cloud equivariance (not real-time) | L
W3_EquivariantDescriptorFieldsSE3Equivarian | Q01 action head | SE(3)-TNs fail on multimodal mug demos, EBM handles | + probabilistic head | L
W3_GivingRobotsaHandLearningGeneralizableMa | Q13 data | env-gen avg: robot-only 5.2% / +play (larger) 23.8% / +diverse masked human wrist videos 63.6% | + scene diversity over volume | M
W3_GivingRobotsaHandLearningGeneralizableMa | Q14 robustness | narrow single-env robot demos 0-11% on unseen backgrounds/distractors | - single-scene demo collection | M
W3_GivingRobotsaHandLearningGeneralizableMa | Q11 cameras | wrist-only + top-36% mask allows human video transfer; no mask 24.3 vs 54.3 | + wrist cam | L
W3_GivingRobotsaHandLearningGeneralizableMa | Q07 history/proprio | no grasp-state input 28.6 vs 54.3 (re-grasp loops) | + include gripper state | M
W3_ElicitingCompatibleDemonstrationsforMult | Q13 | adding 5-10 demos from a different-style operator: Hammer 24.7->4.0%, Round Nut 13.3->7.3%; real food plating 60->30% naive vs 85% with compatibility feedback | + single consistent strategy / filter incompatible demos | M
W3_ElicitingCompatibleDemonstrationsforMult | Q01 | MSE-MLP ensembles degrade with heterogeneous operator styles (no multimodal head tested) | ~ multimodality matters for mixed-operator data | L
W3_GeneralizableVLAFinetuningviaRepresentat | Q03 vision encoder | LIBERO-PRO/Plus: frozen VLM 43.1/59.9, BC finetune 61.0/85.1, finetune + frozen-copy feature anchoring 68.1/87.3 (+align 71.9/90.3) | + finetune with anchoring; - frozen | M
W3_GeneralizableVLAFinetuningviaRepresentat | Q14 robustness | lighting 93.2->99.0, background 90.7->99.6, position swap 2.3->22.6; real xArm mean 36.7->60.0 (StarVLA), 28.3->54.2 (VLA-Adapter) | + representation-preserving finetune | M
W3_GeneralizableVLAFinetuningviaRepresentat | Q09 auxiliary objectives | direction-word aux loss alone PRO 61.0->65.9; shuffled labels 61.4 (no gain) | + action-grounded language aux loss | M
W3_GeneralizableVLAFinetuningviaRepresentat | Q08 language | BC picks trained green mug 90% under 'pink mug' instruction; VQA co-training+KI PRO 43.8 < BC 61.0 | - naive co-training | M
W3_DeFMLearningFoundationRepresentationsfro | Q04 depth | depth-pretrained ResNet-18 grasp 0.894 (FT) vs ImageNet 0.795 vs scratch 0.777 (sim RL, depth in all arms) | + depth-specific pretrained encoder if depth used | L
W3_DeFMLearningFoundationRepresentationsfro | Q03 vision encoder | fine-tuned > frozen for all encoders; Kinect-noise shift frozen DeFM 0.486 vs FT 0.876, frozen ImageNet 0.004 | + fine-tune encoder; - frozen | M
W3_DeFMLearningFoundationRepresentationsfro | Q14 robustness | frozen features + head collapse under unseen sensor noise (0.66->0.004 ImageNet) | - frozen encoders under sensor shift | L
W3_EvaVLAEvaluatingVisionLanguageActionMode | Q14 robustness | LIBERO avg failure, random object 3D rotation: OpenVLA 23.5→56.0, OFT 4.7→42.0, pi0.5 4.0→35.0; random illumination pi0.5 4.0→5.0 vs OpenVLA 23.5→38.0 | ~ object-pose shift unsolved by VLAs; pretrained pi0.5 photometrically robust | M
W3_EvaVLAEvaluatingVisionLanguageActionMode | Q05 augmentation | adversarial-perturbation fine-tune pi0.5: patch FR 45.5→24.3, illum 12.3→6.3, 3D 85.8→56.8, clean 4.0→5.0 | + perturbation/scene augmentation | M
W3_EvaVLAEvaluatingVisionLanguageActionMode | Q13 data diversity | object orientation variation is dominant failure → demos must cover pose range | + pose diversity in demos | L
W3_FurnitureVLALearningLongHorizonBimanualF | Q06 | pi0.5 sim avg: no TE 0.65, exp-weighted TE lambda=-0.1 0.80, uniform TE 0.62; exec 5/10/25 of 50: 0.60/0.74/0.67 | + recency-weighted TE, execute ~20% of chunk | M
W3_FurnitureVLALearningLongHorizonBimanualF | Q10 | recency-weighted chunk blending best for smooth bimanual control | + blend overlapping chunks | L
W3_FurnitureVLALearningLongHorizonBimanualF | Q11 | removing rear camera 0.80 -> 0.47; resolution 224/300/448: 0.60/0.72/0.80 | + additional views covering occlusion; + resolution | M
W3_FurnitureVLALearningLongHorizonBimanualF | Q04 | front depth replacing rear RGB: 0.50 vs 0.80 | - depth as extra image channel in VLA (confounded) | L
W3_FurnitureVLALearningLongHorizonBimanualF | Q13 | 125/250/500 demos: 0.50/0.68/0.80 | ~ diminishing returns | L
W3_FurnitureVLALearningLongHorizonBimanualF | Q09 | continuous progress head works; discrete progress 0.00 | + continuous progress aux target | L
W3_HumanintheLoopImitationLearningusingRemo | Q13 data | 30 demos + intervention rounds (IWR, 50/50 balanced) 87.3/87.5% vs equal-budget full demos 76.7/64.9% vs HG-DAgger 75.3/69.6% (sim, low-dim) | + intervention/recovery data upweighted | M
W3_GNFactorMultiTaskRealRobotLearningwithGe | Q09 auxiliary objectives | RLBench 10-task avg: full 36.8 vs w/o neural-rendering aux 24.2 vs w/o RGB render loss 27.2 | + reconstruction/rendering aux | M
W3_GNFactorMultiTaskRealRobotLearningwithGe | Q04 3D | real xArm 5 demos/task: GNFactor 43.3 vs PerAct 22.5 (both voxel 3D, 10 trials/cell) | ~ 3D + foundation features | L
W3_GNFactorMultiTaskRealRobotLearningwithGe | Q11 cameras | PerAct 1→4 input cameras 20.4→22.7 only | ~ more static cams as input low value | L
W3_GNFactorMultiTaskRealRobotLearningwithGe | Q03 vision encoder | distilled SD 36.8 vs CLIP 32.0 vs DINO 30.4 (sim) | ~ | L
W3_GoalRepresentationsforInstructionFollowi | Q08 | LCBC on 7k labeled trajs: 0% on unseen instructions; CLIP transition-aligned GRIF best; goal-image CLIP alignment fails (figure only) | ~ language for few fixed tasks only; novel instructions need big data | L
W3_IdentifyingExpertBehaviorinOfflineTraini | Q13 data | real TriFinger lift/mixed BC 489 -> 917 after filtering to expert episodes; BC on expert beats offline RL | + filter low-quality demos | L
W3_IdentifyingExpertBehaviorinOfflineTraini | Q05 augmentation | Gaussian state noise 635->622 avg (hurt); symmetry-consistent aug +59..95 | ~ physically consistent aug only | L
W3_HermiteCurvesasTrajectoryPriorsforVision | Q10 chunk-boundary smoothness | Hermite aux loss: real seam jump 0.48-0.72x of pi0.5; real SR 63.4 -> 90.0 (4 tasks x 15); zero inference cost (48.6 vs 48.4 ms) | + training-time trajectory smoothness regularizer | M
W3_HermiteCurvesasTrajectoryPriorsforVision | Q09 auxiliary objectives | aux-only Hermite head (98.7 LIBERO, 90.0 real) > as output scaffold (97.7, 81.7); lambda=10, K=2 optimal | + trajectory aux head | M
W3_HermiteCurvesasTrajectoryPriorsforVision | Q06 chunking | T=50/W=20 at 30 Hz; handover jumps 5.5-8.6x interior steps for all methods | ~ seams inherent; execute < half chunk | M
W3_HermiteCurvesasTrajectoryPriorsforVision | Q14 robustness | LIBERO-plus camera 75.8 -> 89.2 from action-side prior; light +2.2, bg +1.7 only | ~ action priors help geometry shifts not appearance | L
W3_ImmersiveDemonstrationsaretheKeytoImitat | Q13 | force-feedback demos: lower force variance and faster execution, mirrored by BC agent (sim, proprio-only, no success rates) | + consistent, feedback-rich teleop | L
W3_HInDexVisualReinforcementLearningwithHan | Q03 vision encoder | frozen encoders, 12 dexterous sim tasks avg success: ImageNet RN50 81.3, VC-1 70.8, MVP 63.1, R3M 42.3, hand-pose RN50+BN-adapt 91.3 | + ImageNet RN50 baseline; - R3M | L
W3_HInDexVisualReinforcementLearningwithHan | Q03 finetune strategy | BN-only (0.18% params) adaptation beats full finetune; full finetune can be worse than frozen (figure only) | ~ partial adaptation | L
W3_HInDexVisualReinforcementLearningwithHan | Q14 robustness | unseen backgrounds: VC-1 16.8%, H-InDex 20.7% success (from near-100 in-dist) | - frozen pretrained encoder alone for bg robustness | L
W3_Instructiondrivenhistoryawarepoliciesfor | Q08 language | CLIP token seq 86.3% vs BERT 40.2% vs GloVe ~1.7% unseen push-buttons; pooled sentence embedding drops; no-instruction multi-task 64.2 vs 83.3 | + token-level CLIP-style text + cross-attn | M
W3_Instructiondrivenhistoryawarepoliciesfor | Q07 history | +history 78.1->81.8 (10 tasks); 74 tasks w/o hist 60.9 vs 65.4; keyframe actions | + history for non-Markovian keyframe tasks; ~ for dense control | L
W3_Instructiondrivenhistoryawarepoliciesfor | Q11 cameras | 3 views 65.4 vs best single view 40.1 (74 RLBench tasks) | + multi-view | M
W3_Instructiondrivenhistoryawarepoliciesfor | Q04 depth | point cloud tokens 73.1->77.1 | + depth/points | L
W3_ImperfectionforPrecisionUpcyclingImperfe | Q13 data quality | naive mixing of low-precision UMI demos: ATX 48.3->33.3, cable 78.3->25.0, sorting 81.7->75.0 (60 trials) | - mixing imprecise demos uniformly | H
W3_ImperfectionforPrecisionUpcyclingImperfe | Q13 data reuse | flow-time routing: +Dpm ATX 73.3, cable 90.0 vs equal extra perfect data 75.0/91.7 (avg -4.2 pts) | + route imperfect data to high-noise flow times | M
W3_ImperfectionforPrecisionUpcyclingImperfe | Q01 action head | flow-matching enables per-source noise-level admission; opposite window 30.0 vs 73.3 | + flow/diffusion head | L
W3_LearningLatentPlansfromPlay | Q13 | sim 18 tasks: Play-LMP on 30 min play 71.8% vs 18 expert BC policies on 90 min 70.3%; 7 h play 85.5%; play-trained more robust to init perturbation | + coverage/varied-start data over narrow clean demos | M
W3_LearningLatentPlansfromPlay | Q01 | CVAE latent plan vs GCBC: pixels 69.4 vs 58.7%, states 85.5 vs 77.9% | + latent-variable (CVAE) head for multimodality | L
W3_LanguageConditionedImitationLearningWith | Q14 robustness | CALVIN ABC->D avg len HULC 0.67 -> SPIL 1.71 (no base skills 1.05); D->D no gain 2.64 vs 2.67; real zero-shot 3% vs 33% | + structured latent skill prior for env shift | L
W3_LanguageConditionedImitationLearningWith | Q06 chunking | latent skill length Nh 4/5/6 -> 1.58/1.71/1.65 | ~ insensitive | L
W3_LearningMultiStepManipulationTasksfromAS | Q14 robustness | modular Grounded-SAM+ICP pipeline: unseen kitchen full task 20-40% (5 trials), pose-estimation 50% of failures | ~ not a learned policy | L
W3_LDA1BScalingLatentDynamicsActionModelvia | Q09 auxiliary objectives | RoboCasa-GR1: future-state target VAE latents 20.0 vs DINO latents 55.4; co-training dynamics+forecast keeps improving with low-quality/actionless data while policy-only degrades (figure) | + future DINO-feature prediction aux | M
W3_LDA1BScalingLatentDynamicsActionModelvia | Q13 data quality | adding ~35% imperfect teleop demos: pi0.5 60→40 / 50→40; LDA 70→80 / 50→60 (10 trials) | - unfiltered imperfect demos for plain BC | L
W3_LDA1BScalingLatentDynamicsActionModelvia | Q12 model size | LDA 0.5B 50.7 vs 1B 55.4; UWM 0.1B 14.2 vs 1B 19.3 (sim) | ~ (outside 8GB regime) | L
W3_LDA1BScalingLatentDynamicsActionModelvia | Q14 robustness | pick&place 10 trials: novel obj 60/40/26.7, unseen bg 60/40/20, OOD pos 40/20/6.7 (LDA/GR00T/pi0.5) | + dynamics-pretrained policy | L
W3_MakingSenseofVisionandTouchLearningMulti | Q09 | sim peg insertion: predictive self-sup rep 78% vs reconstruction 36%, deterministic 24%, no-pairing 22% (RL policy on frozen rep) | + predictive/action-conditional aux over pixel reconstruction | L
W3_MakingSenseofVisionandTouchLearningMulti | Q04 | modality ablation: no-depth worst, no-RGB least harmful (figure, sim insertion) | + depth for geometric/contact tasks | L
W3_LearningVisualRoboticControlEfficientlyw | Q05 augmentation | pixel SAC without random-crop aug fails even on dense FetchReach; with aug+10 demos real xArm 96% avg (figure/RL) | + random crop | L
W3_LearningVisualRoboticControlEfficientlyw | Q13 data quantity | BC with 10 demos only solves reach/switch, fails move/pull/pickup (figure only) | - ~10 demos for plain BC | L
W3_MaskedImitationLearningDiscoveringEnviro | Q07 proprio/inputs | Robomimic Square: all low-dim modalities 12.7% vs masked (drop EEF vel/orientation) 56.7-71.3%; modality dropout 19.3% | + minimal proprio inputs | L
W3_MaskedImitationLearningDiscoveringEnviro | Q11 cameras | real Franka reach: both views 54.2% vs masked spurious top view 95.2% (constructed correlation) | ~ extra views can add spurious cues | L
W3_MaskedImitationLearningDiscoveringEnviro | Q14 robustness | held-out shifted-environment validation selects robust inputs (Can 22.7 -> 56.0) | + shifted-condition validation split | L
W3_MantisAVersatileVisionLanguageActionMode | Q09 aux objectives | LIBERO avg no-foresight 91.3 / foresight w/o residual 94.4 / foresight 95.7 / +video pretrain 96.2 (5.8B VLA) | + separate future-prediction head dropped at inference | L
W3_MantisAVersatileVisionLanguageActionMode | Q10 latency | adaptive temporal ensemble ~50% fewer inference calls, comparable SR (figure) | + ensemble only during fine phases | L
W3_MaskedVisualPretrainingforMotorControl | Q03 vision encoder | frozen MAE(HOI) ViT-S > supervised ImageNet ViT on 7/8 PixMC RL tasks (up to +80 abs, figure only); random frozen fails 6/8 | + pretrained (SSL) > random; ~ vs ImageNet | L
W3_MaskedVisualPretrainingforMotorControl | Q12 model size | ViT-B encoder no better than ViT-S (figure only) | ~ small encoder enough | L
W3_MultiViewMaskedWorldModelsforVisualRobot | Q11 cameras | viewpoint-randomized training + multi-view MAE: real uncalibrated-camera cup pick 74.7% vs 11.3% (MWM) vs 7.1% (MAE+WM) | + train with varied camera poses | M
W3_MultiViewMaskedWorldModelsforVisualRobot | Q09 auxiliary objectives | view-masked multi-view reconstruction: BC +14.35 pts vs single-view MWM; view-masking 57.92->64.48 | + cross-view reconstruction aux | M
W3_MultiViewMaskedWorldModelsforVisualRobot | Q05 augmentation | physically randomized cameras >> rotation/translation/brightness aug for viewpoint robustness (figure only) | - relying on image aug for camera shift | L
W3_MultiViewMaskedWorldModelsforVisualRobot | Q03 vision encoder | frozen CLIP/MAE world models far below in-domain MV-MAE (figure only) | - frozen generic encoders (RL, sim) | L
W3_MimicPlayLongHorizonImitationLearningbyW | Q01 | real, 20 demos: w/o GMM 0.28 (trained)/0.07 (unseen) vs with GMM 0.55/0.47 | + multimodal (GMM) head for human demos | M
W3_MimicPlayLongHorizonImitationLearningbyW | Q13 | Kitchen long-horizon 20->40 demos: 0.47->0.70; +10 min human play: 0.40->0.70 at 40 demos | + more demos / cheap human play for long-horizon | L
W3_MimicPlayLongHorizonImitationLearningbyW | Q03 | R3M-BC (frozen pretrained) long-horizon 0.00/0.17 vs end-to-end ResNet18 hierarchical 0.47/0.70 | - frozen R3M | L
W3_CLIPortWhatandWherePathwaysforRoboticMan | Q03 vision encoder | stack-pyramid seen n=10: CLIP 64.7 / ImageNet-RN50+BERT 35.0 / untrained 12.7; n=1000 98.8/97.5/51.2 | + pretrained VL encoder in low-data | M
W3_CLIPortWhatandWherePathwaysforRoboticMan | Q08 language | multi-task > single in 41/72 evals; unseen-color transfer 45.8->75.7; language fused into spatial stream very poor; real bias exploitation | + multi-task language, keep lang out of low-level spatial features, balance data | M
W3_CLIPortWhatandWherePathwaysforRoboticMan | Q04 depth | CLIP-only RGB ~76% vs two-stream RGB-D >90% (sim avg) | + depth/spatial stream for precision | L
W3_CLIPortWhatandWherePathwaysforRoboticMan | Q13 data | real 2-10 demos/task -> 55-75%; authors estimate 50-100 demos needed for robustness | ~ 50-100 demos | L
W3_OutputFeedbackTubeMPCGuidedDataAugmentat | Q05 | sim quadrotor: 1 demo + tube-sampled synthetic views w/ corrective labels >=94.5% vs baselines needing 40-120 demos | + perturbed-view synthesis with corrective actions (needs model/expert) | L
W3_PolybotTrainingOnePolicyAcrossRobotsWhil | Q11 cameras | wrist-cam multi-robot policy 0.7-1.0 vs exterior-cam naive multi-robot 0.0-0.4 (5 demos, 10 trials; confounded) | + wrist camera for viewpoint/embodiment invariance | L
W3_PolybotTrainingOnePolicyAcrossRobotsWhil | Q13 data | cross-robot data + 5 target demos 0.7-1.0 vs single-robot 0.0-0.3 | + cross-embodiment co-training with aligned spaces | L
W3_PolybotTrainingOnePolicyAcrossRobotsWhil | Q02 action space | per-robot heads on shared EE-delta vs shared blocking controller: shelf 0.9-1.0 vs 0.0 | ~ robot-specific action heads | L
W3_NACNeuralActionCodecforVisionLanguageAct | Q01 action head | small from-scratch policy, success LIBERO-10/RoboMimic/Real(8x10): Bin 4/8/6, DP 25/27/23, FAST 38/28/40, VQ-VLA 11/21/31, OAT 44/32/40, NAC 50/34/50 | + learned RVQ codec tokens; ~ vs diffusion (DP baseline looks under-tuned) | L
W3_NACNeuralActionCodecforVisionLanguageAct | Q01 action head (tokenizer recipe) | no adversarial discriminator → 0%; mel loss → 0%; linear vs ISTFT decoder 42.1 vs 48.3 | - fragile learned tokenizers | M
W3_NACNeuralActionCodecforVisionLanguageAct | Q10 latency | 12 tokens/chunk vs Bin 224 vs FAST 36 | + compressed tokens for AR latency | L
W3_TransporterswithVisualForesightforSolvin | Q01 action head | unseen tasks 10 demos: multimodal proposals+foresight 78.5 vs single-mode GCTN 55.4; real unseen Twin Tower 60 vs 0 | + multimodal action representation | L
W3_TransporterswithVisualForesightforSolvin | Q09 aux objectives | foresight model for planning +16..31 pts unseen (primitive pick-place, sim) | ~ world model for planning, not directly transferable | L
W3_RecoveringAggressivelyPrunedVisionLangua | Q10 latency | 72% width-pruned OpenVLA-OFT: 59.3->51.0 ms H100 (1.16x), 362->162 ms Jetson Thor; CogACT latency floor ~85 ms from 10 DDIM steps; depth pruning 1.31-1.66x | ~ prune depth/denoise steps, not width, for latency | M
W3_RecoveringAggressivelyPrunedVisionLangua | Q12 model size | 72%-pruned 7B student (1.86B) real PiPER 77.5% vs teacher 65.5% (200 eps, with KD); SFT-only 59.5% | + small backbones suffice for task-specific policies (with distillation) | M
W3_RecoveringAggressivelyPrunedVisionLangua | Q14 robustness | hidden-state KD vs SFT at 72% prune under SimplerEnv variants 60.7 vs 37.2 (teacher 66.6) | + representation distillation preserves OOD | M
W3_RealWorldOfflineReinforcementLearningwit | Q02 | real Franka BC: absolute joint targets vs delta: slide 0.681 vs 0.551, lift 0.823 vs 0.721, PnP 0.818 vs 0.678; ORL prefers delta (abs crashes) | + absolute joint position for BC | M
W3_RealWorldOfflineReinforcementLearningwit | Q07 | joint velocity in state: BC PnP 0.632 -> 0.818, slide 0.623 -> 0.681 | + include velocity/short proprio history | L
W3_RealWorldOfflineReinforcementLearningwit | Q13 | BC trained with other-task data drops (lift 0.823 -> 0.58-0.61) while IQL can gain | - naive multi-task mixing for BC | L
W3_PredictionwithActionVisualPolicyLearning | Q09 auxiliary objectives | MetaWorld 50 tasks: PAD 72.5 vs w/o image prediction 43.6 vs w/o video co-train 59.2 | + future-image prediction aux | M
W3_PredictionwithActionVisualPolicyLearning | Q04 depth | real Panda (wrist cam, 50 rollouts/task): PAD 72 → PAD-Depth 78 | + depth as extra input | M
W3_PredictionwithActionVisualPolicyLearning | Q12 model size | B/2 128M 62.4, L/2 449M 68.4, XL/2 661M 72.5; XL/8 (17 tokens) 48.2 | ~ bigger helps in 50-task sim | L
W3_PredictionwithActionVisualPolicyLearning | Q10 latency | joint image+action DiT with 75 DDIM steps → low control rate (stated limitation) | - predicting images at inference | M
W3_RTTrajectoryRoboticTaskGeneralizationvia | Q08 language | unseen skills: language RT-1 16.7%, RT-2 11.1%, goal-image 26%, trajectory sketch 2.5D 67% (73K demos) | - expecting language to generalize to new motions | L
W3_SeFAPolicyFastandAccurateVisuomotorPolic | Q10 latency | 1-step SeFA 16.7 ms vs DP-100 1287 ms vs AdaFlow-20 629 ms; 1-step 62 = 100-step 62 avg; 1-step DDIM fails (Pen 0, Square 0) | + reflow/consistency 1-step sampling | M
W3_SeFAPolicyFastandAccurateVisuomotorPolic | Q01 action head | rectified flow + selective alignment: 66-task avg 62.3 vs DP 38.9; real flower insertion 80 vs 20, knob 40 vs 0 (10-20 trials) | + flow matching over DDPM diffusion | L
W3_RT2VisionLanguageActionModelsTransferWeb | Q12 | 5B from scratch "very poor"; co-FT > FT robot-only; 55B > 5B on unseen (figure-only) | + pretrained init; larger helps OOD but costs latency | M
W3_RT2VisionLanguageActionModelsTransferWeb | Q03 | VLM-pretrained RT-2 ~6x frozen VC-1/R3M, ~2x RT-1 on unseen objects/backgrounds/envs | + web VLM pretrained vision; - frozen VC-1/R3M | M
W3_RT2VisionLanguageActionModelsTransferWeb | Q14 | ~2x RT-1 on unseen objects/backgrounds/environments with same robot data | + VLM pretraining + co-fine-tuning for appearance shift | M
W3_RT2VisionLanguageActionModelsTransferWeb | Q10 | 55B 1-3 Hz, 5B ~5 Hz on multi-TPU cloud | - large VLAs for real-time control | M
W3_RoboMINDBenchmarkonMultiembodimentIntell | Q13 data quality | ACT failures dominated by inaccurate positioning (up to 48%) from non-random placements; gripper failures from too-fast closure (few frames) | + randomize placements, slow gripper actions during teleop | M
W3_RoboMINDBenchmarkonMultiembodimentIntell | Q13 data quantity (sim co-train) | ACT 100 real + up to 500 digital-twin sim traj improves real success; sim-only 10% real (figure) | ~ sim co-training | L
W3_RoboMINDBenchmarkonMultiembodimentIntell | Q01 action head | single-task real: ACT avg 30.7–55.3% by embodiment; DP better on some Franka/humanoid tasks; BAKU worst (10 trials) | ~ ACT ≈ DP | L
W3_ThinkingWhileMovingDeepReinforcementLear | Q10 async execution | concurrent grasping sim: unconditioned 84.1% vs VTG-conditioned 93.5% (blocking 92.7%), 31% faster; real concurrent 68.6% vs blocking 81.4% but 49% faster | + condition next action on in-flight action | L
W3_ThinkingWhileMovingDeepReinforcementLear | Q07 history | frame stacking prior obs/actions nominal gain vs VTG (figure only) | ~ history less useful than explicit committed-action input | L
W3_SeeingAlltheAnglesLearningMultiviewManip | Q11 | 200 demos, randomized camera pose: multiview ~ fixed-view on fixed-view task; fixed-view policy drops sharply with small yaw change (figure only; sim 5 seeds x 50 eps, real 10 eps) | + randomize scene-camera pose during data collection | M
W3_SeeingAlltheAnglesLearningMultiviewManip | Q14 | multiview policy generalizes partly beyond trained view range; learned keypoints view-consistent | + viewpoint diversity for camera-shift robustness | M
W3_SeeingAlltheAnglesLearningMultiviewManip | Q13 | same demo count spread over views: little/no penalty in fixed view | + diversity over repetition | L
W3_VistaBotViewRobustRobotManipulationviaSp | Q11 cameras | single-view-trained ACT: sim 0.83 -> 0.13-0.28 at +-30/45 deg; real 0.79 -> 0.15/0.18 at +-45 deg; VistaBot 0.53/0.61 | - single fixed scene camera without viewpoint diversity | H
W3_VistaBotViewRobustRobotManipulationviaSp | Q04 3D/depth | depth+pose reprojection to training view (GT geometry) VGS 0.79 vs estimated 0.67 vs ACT 0.24 | + geometric canonicalization via depth | M
W3_VistaBotViewRobustRobotManipulationviaSp | Q12 model size | pi0 VGS 0.33 vs ACT 0.24 (sim), 0.27 vs 0.21 (real): large VLA barely more view-robust | - relying on VLA scale for viewpoint robustness | M
W3_VistaBotViewRobustRobotManipulationviaSp | Q10 latency | VGGT+CogVideoX view synthesis pipeline ~3 Hz | - test-time generative view synthesis on 8 GB | M
W3_RVTRoboticViewTransformerfor3DObjectMani | Q04 3D/depth | RLBench avg: RVT re-rendered orthographic virtual views 62.9 vs raw sensor views 22.9; PerAct voxels 49.4; image-BC 1.3; no depth channel 60.3 | + RGB-D → point cloud → virtual views | M
W3_RVTRoboticViewTransformerfor3DObjectMani | Q11 cameras | single virtual front view 35.8 vs 3 views 60.2 vs 5 views 62.9 (all re-rendered from same sensors) | + multi-view (virtual) | L
W3_RVTRoboticViewTransformerfor3DObjectMani | Q05 augmentation | 3D rotation aug on point cloud 60.4 → 62.9 | + 3D aug | L
W3_RVTRoboticViewTransformerfor3DObjectMani | Q13 data quantity | real Franka ~10 demos/task keyframe: 56% overall, 82.5% excl. thin-marker tasks | ~ | L
W3_BeyondAppearanceShiftsTaskSemanticAction | Q08 language | pi0.5 target-object swap still does old task 34%; real PiPER frozen changed-task success 10-24% vs 39-65% calibrated | - relying on language alone for object discrimination | M
W3_BeyondAppearanceShiftsTaskSemanticAction | Q14 robustness | OFT clutter -33, noise -46 pts; pi0.5 illumination -9 pts; masking probe style shift 42->70% | + task-relevant masking / object-centric input | L
W3_BeyondAppearanceShiftsTaskSemanticAction | Q10 latency | SAM2+grounding preserving mode p50 924 ms end-to-end | - runtime segmentation on laptop | M
W3_SPOCImitatingShortestPathsinSimulationEn | Q03 | avg success CLIP-RN50 26.6, DINOv2 ViT-S 44.8, SigLIP ViT-B 49.9 (sim, language-conditioned nav+pick) | + SigLIP/DINOv2 over CLIP-ResNet | M
W3_SPOCImitatingShortestPathsinSimulationEn | Q13 | 100k episodes: 100 houses 43.5 vs 10k houses 57.0; 10k->100k episodes 19.0->57.0 | + environment diversity over repetition | M
W3_SPOCImitatingShortestPathsinSimulationEn | Q07 | context 100 vs shorter: avg 49.9 vs 27.8/39.9; Fetch 14.0 vs 2.3 (partially observable long-horizon) | ~ long history only for partially observable tasks | L
W3_SPOCImitatingShortestPathsinSimulationEn | Q08 | multi-task language IL 49.9 vs single-task 50.0 | + multi-task language conditioning has no penalty at scale | L
W3_BeyondTaskSuccessBehavioralandRepresenta | Q09 auxiliary objectives | WAMs smoother/more target-selective at ~equal LIBERO success (95-98%); aux-only WAMs in between | ~ future prediction aux (associative) | L
W3_BeyondTaskSuccessBehavioralandRepresenta | Q10 latency | p50 per chunk: pi0.5 100 ms, pi0 194, X-VLA 329, Cosmos 956, VLA-JEPA 1588, LingBot-VA 4701 ms (RTX 6000 Ada) | - inference-time world-model imagination | M
W3_BeyondTaskSuccessBehavioralandRepresenta | Q12 model size | GPU mem at inference: pi0 8.6 GB, pi0.5 9.1 GB, X-VLA 7.1 GB, VLA-JEPA 5.5 GB | - pi0-class VLAs on 8 GB GPU | M
W3_Seq2SeqImitationLearningforTactileFeedba | Q07 observation history | tactile POMDP, 50 demos: transformer-history seq2seq 76/84% vs LSTM-seq2seq 56/0% vs BC-LSTM 11/5% (sim/real) | + history only when state truly hidden | L
W3_Seq2SeqImitationLearningforTactileFeedba | Q13 data quantity | real snap-on success converges after ~50 demos (5–200 sweep, figure) | ~ 50 demos saturate narrow task | L
W3_AComparisonofActionSpacesforLearningMani | Q02 action space | RL sim, impedance (task-space) refs learn fastest > ID > PD > torque | ~ task-space targets (RL only, not BC) | L
W3_ActFoveaRuntimeSafeguardingforVLAPolicie | Q10 latency | pi0 LIBERO 2000 eps: 3-frame visual delay 93.0->76.2; fixed action clip/smoothing clean 93.0->82.2 | + minimize obs-action lag, - naive smoothing | M
W3_ActFoveaRuntimeSafeguardingforVLAPolicie | Q06 chunking | fixed shorter executed prefix: drift 83.1->89.9, clean 93.0->91.7, but delay 76.2->70.7 | + shorter execution horizon vs drift | M
W3_ActFoveaRuntimeSafeguardingforVLAPolicie | Q14 robustness | training-free obs repair: localized overlay 49.3->90.3 | ~ runtime monitor layer | L
W3_ActionEffectMemoryPretrainingforRobotMan | Q07 history | Place Shoe DP: 1 frame .40, DINOv2 stack 8f .52, 16f .40, AEM memory .76 | - raw frame stacking, + compact pretrained memory | L
W3_ActionEffectMemoryPretrainingforRobotMan | Q09 aux objectives | masked vision+action pretrain .96/.76 vs obs-only .68/.44 vs joint no-pretrain .60 | + action-conditioned masked pretraining | L
W3_ActionEffectMemoryPretrainingforRobotMan | Q03 vision encoder | memory feats DINOv2 CLS .96/.76 > CLIP CLS .84/.44 > DINOv3 CLS .76/.52 | + DINOv2 | L
W3_ActionEffectMemoryPretrainingforRobotMan | Q14 robustness | real Franka distractors DP 15.0 -> DP+AEM 68.3 (standard 43.3->81.7) | ~ memory helps clutter | L
W3_VisionBasedMultiTaskManipulationforInexp | Q01 | $500 arm, 25 trials x 5 tasks: no autoregressive joint MDN 16/20/52/64/20% vs full 76/80/88/76/88% | + multimodal, joint-coherent action head | M
W3_VisionBasedMultiTaskManipulationforInexp | Q09 | removing VAE-GAN recon aux: 12/72/56/48/16% vs 76/80/88/76/88% (scratch 128px encoder) | + reconstruction aux when encoder trained from scratch | M
W3_VisionBasedMultiTaskManipulationforInexp | Q08 | multi-task one-hot vs single-task: better on T2-T5, worse T1 (36->16%); single-task overfits | + multi-task sharing | L
W3_VisionBasedMultiTaskManipulationforInexp | Q05 | 33 Hz -> 4 Hz downsampling with all phase offsets as augmentation "useful" (no numbers) | + temporal-offset subsampling | L
W3_ADualProcessVLAEfficientRoboticManipulat | Q10 latency | small policy + VLM latent once/episode 0.030 s/step vs OpenVLA ~0.25 s (sim) | + small fast per-step policy | L
W3_ADualProcessVLAEfficientRoboticManipulat | Q12 model size | BC-xfmr from scratch 0.476 vs fine-tuned OpenVLA-7B 0.098 (RoboCasa sim, 3000 demos/task) | + small from-scratch policy | L
W3_ADualProcessVLAEfficientRoboticManipulat | Q08 language | VLM latent task embedding 0.573 vs CLIP text 0.476 (multi-task sim) | + VLM-derived task embedding | L
W3_BayesianDisturbanceInjectionRobustImitat | Q01 action head | real UR3: unimodal GP 7% vs mixture GP 51%; with noise inj 18% vs 91% | - unimodal regression on multimodal demos | M
W3_BayesianDisturbanceInjectionRobustImitat | Q13 data quality | noise-injected demos 51%→91% real (10 demos, low-dim) | + perturbation/recovery demos | M
W3_CageCausalAttentionEnablesDataEfficientG | Q03 vision encoder | frozen DINOv2-L+LoRA w/ spatial tokens: bg-change 0.87 vs ResNet-scratch 0.00; new object 0.80 vs 0.00 (50 demos, real) | + frozen pretrained ViT + LoRA, token-level | M
W3_CageCausalAttentionEnablesDataEfficientG | Q03 vision encoder | mean-pooled DINOv2 tokens: L0 0.40 vs 1.00 with perceiver | - pooled VFM features | M
W3_CageCausalAttentionEnablesDataEfficientG | Q05 augmentation | random perspective+crop: L2 0.40→0.73 | + geometric aug for camera/scene shift | M
W3_CageCausalAttentionEnablesDataEfficientG | Q04 3D vs RGB | RISE single-view point cloud best in-domain but bg 0.13, obj 0.00, L2 0 | - scene point cloud as robustness fix | M
W3_CageCausalAttentionEnablesDataEfficientG | Q14 robustness | pretrained-VFM RGB policy L1 bg/obj/cam 0.87/0.80/0.80 from 50 single-env demos; DP 0.00/0.00/0.27 | + pretrained VFM for OOD | M
W3_CageCausalAttentionEnablesDataEfficientG | Q07 obs history | To=2/4/8 final 0.87/1.00/0.87 (L0, ~15 trials) | ~ short history (4) with causal compression | L
W3_CageCausalAttentionEnablesDataEfficientG | Q01 action head | cross-attn conditioned diffusion UNet vs FiLM: ~+20 pts all settings | + attention conditioning of generative head | L
W3_CageCausalAttentionEnablesDataEfficientG | Q12 model size | DINOv2-L frozen+LoRA fine at 40-50 demos but 280 ms/step on RTX3090 | ~ large frozen encoder OK for data, bad for 8GB latency | L
W3_EVLAEventAugmentedVisionLanguageActionMo | Q14 robustness | SO100 SmolVLA (frozen VLM) trained at 200 lux: 100/65/30/0% at 100/75/40/30 lux | - single-lighting training; SmolVLA lighting-fragile | M
W3_EVLAEventAugmentedVisionLanguageActionMo | Q13 data diversity | multi-illumination training: image-only 40 lux 30%→80%, 75 lux 65%→100% | + collect demos under varied lighting | M
W3_EVLAEventAugmentedVisionLanguageActionMo | Q05 augmentation | Retinex-type enhancement OOD avg 46 vs 39 image-only | - image enhancement preprocessing as lighting fix | L
W3_EVLAEventAugmentedVisionLanguageActionMo | Q11 cameras | wrist-only: stacking fails from occlusion by grasped object; wide FOV lens "critical" (qualitative) | + add scene cam / wide wrist FOV | L
W3_GoalConditionedDualActionImitationLearni | Q06 chunking | open-loop full trajectory in precise phase: GraspNeck 0.000 vs reactive 0.933 (15 trials) | - long open-loop execution near contact | L
W3_GoalConditionedDualActionImitationLearni | Q09 aux objectives | goal-state prediction conditioning: GraspNeck 0.933 vs 0.667 without | + predict goal state as auxiliary/conditioning | L
W3_GoalConditionedDualActionImitationLearni | Q02 action space | reactive delta for local precise phase + trajectory for transport: mean 0.870 vs 0.439 all-trajectory | ~ step-wise delta near contact | L
W3_GoalConditionedDualActionImitationLearni | Q01 action head | default Diffusion Policy GraspNeck 0.111 at 5 Hz data | ~ DP untuned/confounded | L
W3_HumanintheLoopTaskandMotionPlanningforIm | Q13 data | learning only contact segments: Square Broad 80% vs 1.2% from 10 min data (sim) | + shorten learned segment | L
W3_LearningGeneralizableManipulationPolicie | Q04 3D vs RGB | segmented object point clouds in base frame: sim Cam-Hard 61.7 vs BC-RNN 0; Bg-Hard 63.3 vs 0 | + object-centric point cloud | M
W3_LearningGeneralizableManipulationPolicie | Q04 3D vs RGB | naive RGB-D input fails all generalization settings (figure) | - raw RGB-D as robustness fix | M
W3_LearningGeneralizableManipulationPolicie | Q05 augmentation | random point/patch masking needed for large camera shift (figure; MAE-policy Cam-Hard 26.7 vs 0) | + input masking aug | L
W3_LearningGeneralizableManipulationPolicie | Q11 cameras | residual real failures = mm grasp misses without wrist cam (qualitative) | + wrist camera | L
W3_LearningGeneralizableManipulationPolicie | Q14 robustness | segmentation to task objects is main lever for bg/distractor/lighting shift | + object-centric masking | M
W3_LIVLanguageImageRepresentationsandReward | Q08 language | jointly aligned VL encoder > vision encoder + separate LM for multi-task LCBC (figure only) | + aligned VL encoder for multi-object language | L
W3_LIVLanguageImageRepresentationsandReward | Q03 vision encoder | frozen LIV > CLIP/R3M/VIP for frozen-backbone BC (figure only) | ~ control-aware VL pretraining | L
W3_MemoryConsistentNeuralNetworksforImitati | Q01 action head | memory-anchored MLP ≥ diffusion on low-dim sim BC (figure only) | ~ constrained heads in low data | L
W3_OfflinetoonlineReinforcementLearningforI | Q05 augmentation | single-step image BC ~35% at 50/200/500 demos; 500+aug >60% (real, 50 trials) | + random-shift aug | L
W3_OfflinetoonlineReinforcementLearningforI | Q13 data quantity | 50→500 demos no gain without aug (~35%) | ~ more demos alone insufficient | L
W3_OfflinetoonlineReinforcementLearningforI | Q03 vision encoder | E2E > frozen pretrained asymptotically in O2O RL; frozen random fails (figure) | ~ | L
W3_RaCRobotLearningforLongHorizonTasksbySca | Q13 data quality | recover-then-correct interventions: sim 61/100 vs 23/100 full demos vs 22/100 HG-DAgger; real ≥2x data efficiency; shirt 78.3% w/ 5 h vs 75% w/ 89 h (cross-paper) | + human-in-loop recovery data | M
W3_RaCRobotLearningforLongHorizonTasksbySca | Q06 chunking | 1 s flow chunk, execute 0.5 s, replan (not ablated) | ~ | L
W3_RaCRobotLearningforLongHorizonTasksbySca | Q01 action head | 300M flow-matching MM-DiT, 10 Euler steps handles mixed expert+intervention data (not ablated) | + flow matching | L
W3_RobustVisualSimtoRealTransferforRoboticM | Q05 augmentation | real 7-task avg: 2D aug only 0/20 → +textures 11.3 → +light/color 14.0 → +camera 18.6/20 | + texture/background randomization; - photometric only | M
W3_RobustVisualSimtoRealTransferforRoboticM | Q05 augmentation | small camera-pose jitter 14.0→18.6/20; large jitter hurts (proxy) | + small camera-pose aug | M
W3_RobustVisualSimtoRealTransferforRoboticM | Q14 robustness | 150-real-demo scratch policy: tablecloth 1/20, camera 8/20, low light 17/20, color light 14/20, obj color 19/20 | - scratch CNN on background/camera shift | M
W3_RobustVisualSimtoRealTransferforRoboticM | Q13 data diversity | appearance-diverse data avg 17.3 vs real-limited 13.2/20; + real FT 18.2 | + diversity over count | M
W3_RobustVisualSimtoRealTransferforRoboticM | Q11 cameras | second viewpoint 44.97→65.43% avg (+50.4 assembling), sim | + multi-view | M
W3_RobustVisualSimtoRealTransferforRoboticM | Q07 obs history | 3-frame history +28.5 pts, single-step policy, sim | + short frame history | L
W3_SECANTSelfExpertCloningforZeroShotGenera | Q05 augmentation | mixture of strong augs (cutout-color+random conv+mixup+crop) > single ops; weak→strong 2-stage > single-stage strong (figure) | + strong aug mixture via distillation | L
W3_SECANTSelfExpertCloningforZeroShotGenera | Q14 robustness | Robosuite unseen textures: e.g., two-arm lift 610 vs 62 prior best (sim RL) | + strong-aug student | L
W3_SnapFlowOneStepActionGenerationforFlowMa | Q10 latency | SmolVLA E2E 178→50 ms (denoise 79%→24%); pi0.5 274→81 ms; LIBERO 98.75 vs 97.75 | + 1-step flow distillation | M
W3_SnapFlowOneStepActionGenerationforFlowMa | Q01 action head | 1-NFE flow after self-distillation matches 10-step | + flow w/ few steps | M
W3_SnapFlowOneStepActionGenerationforFlowMa | Q06 chunking | n_act of 50: 1→77/72%, 5→90/93%, 20→97/92% (libero_10) | - replanning every step | M
W3_TransporterNetworksRearrangingtheVisualW | Q01 action head | dense spatial heatmap head 100% vs Conv-MLP 11-68% with stochastic demos (sim) | - MLP regression on multimodal demos | M
W3_TransporterNetworksRearrangingtheVisualW | Q04 3D vs RGB | top-down RGB-D heightmap pick-place from 1-10 demos (sim); real kit 98.9% | ~ structured primitive alternative, calibration-sensitive | L
W3_TransporterNetworksRearrangingtheVisualW | Q13 data quantity | 1-10 demos suffice with spatial equivariance (sim) | ~ | L
W3_WhatDoWeLearnfromaLargeScaleStudyofPreTr | Q03 vision encoder | VC-1 Base real avg: frozen ≈71, FT no-aug ≈46.5, FT+aug ≈73 (30-150 demos) | + FT only with aug; frozen safe default | M
W3_WhatDoWeLearnfromaLargeScaleStudyofPreTr | Q12 model size | ViT-B > ViT-L in all 4 configs (best 73 vs 59) at 30-150 demos | + smaller encoder in low data | M
W3_WhatDoWeLearnfromaLargeScaleStudyofPreTr | Q05 augmentation | color jitter + 8px shift turns FT from 46.5 to 73 | + aug when fine-tuning encoder | M
W3_WhatDoWeLearnfromaLargeScaleStudyofPreTr | Q03 vision encoder | frozen real avg R3M 56, CLIP 47, MVP 53, VC-1B 69, VC-1L 63; no PVR best on all tasks | - CLIP for manipulation | L
W3_BridgeDataV2ADatasetforRobotLearningatSc | Q14 robustness | cross-lab (camera/lighting/object shift) zero-shot: GCBC 0.30->0.13, LCBC 0.13->0.03, RT-1 0.47->0.40 (10 trials) | - expecting small policies to survive camera/lighting shift without adaptation | M
W3_BridgeDataV2ADatasetforRobotLearningatSc | Q01 action head | D-GCBC without chunking/history jerky mode oscillation (qualitative); seen avg GCBC 0.49 = D-GCBC 0.49 | ~ diffusion needs chunking | L
W3_BridgeDataV2ADatasetforRobotLearningatSc | Q13 data | 13 skills vs 3 skills at ~27k traj: better unseen pick-place (figure only) | + skill/scene diversity | L
W3_BridgeDataV2ADatasetforRobotLearningatSc | Q12 model size | larger GCBC image encoder strictly better at 60k traj (figure only) | ~ larger encoder at large data | L
W3_AdaptationofGeneralistRobotPolicieswithM | Q03 vision encoder | residual RL on LIBERO: scratch ResNet collapses, frozen DINO slower, pi0.5 feats fastest (figure only) | + pretrained frozen features | L
W3_AdaptationofGeneralistRobotPolicieswithM | Q13 data | 1-demo BC real YAM 40%/27% (15 trials); object swap -> 0%; broader demos restore robustness | + demo coverage over positions | L
W3_AdaptationofGeneralistRobotPolicieswithM | Q14 robustness | color/texture/paraphrase shifts retained by frozen VLM; swap/object change fail | + frozen pretrained backbone for appearance | L
W3_TowardsSynergisticGeneralizedandEfficien | Q10 latency/async | OpenVLA alone 3.9 Hz → jitter/pauses; 20M DiT specialist 0.035 s → 15 Hz; latency-aware training with random obs offset τ∈[0,kg] | + fast small specialist + delay-aware training | M
W3_TowardsSynergisticGeneralizedandEfficien | Q12 model size | 20M-param specialist + VLA prior: 5 demos 73.3% vs DP 20% vs ACT 0% (15 runs) | + small specialist | M
W3_TowardsSynergisticGeneralizedandEfficien | Q14 robustness | real avg over position/distractor/background/novel obj: ACT 21.7, DP 40.0, OpenVLA 41.7, RoboDual 70.0; ACT unseen background 0% | + pretrained prior; - unaugmented ACT | M
W3_TowardsSynergisticGeneralizedandEfficien | Q01 action head | real put-block: 5/10/100 demos ACT 0/6.7/46.7 vs DP 20/20/53.3 | + diffusion over CVAE at low data | M
W3_TowardsSynergisticGeneralizedandEfficien | Q06 chunking | specialist chunk 8 + exponential temporal aggregation m=0.1 + DDIM 5 steps (no ablation) | ~ | L
W3_TowardsSynergisticGeneralizedandEfficien | Q11 cameras | adding gripper camera/depth/tactile to specialist improves CALVIN avg len (figure only) | + wrist cam | L
W3_FlowingWithPurposeLatentActionGuidedFlow | Q01 action head | real 50 demos: LAFM 86.7 / FM 63.3 / ACT 40.0 / pi0 71.7 SR; LIBERO-90 ACT 86.2 > FM 82.6 | + flow w/ structured prior; ~ FM vs ACT | M
W3_FlowingWithPurposeLatentActionGuidedFlow | Q12 model size | 0.11B scratch LAFM 86.7 > pi0 3.3B finetuned 71.7 (real, 15 trials/task) | + small task-specific policy | M
W3_FlowingWithPurposeLatentActionGuidedFlow | Q10 latency | FM/LAFM hold LIBERO-90 SR with 1 vs 10 denoising steps (figure) | + 1-step flow | L
W3_FlowingWithPurposeLatentActionGuidedFlow | Q09 aux objectives | FM 82.6 -> +latent-action aux 85.4 -> LAFM 93.0 (LIBERO-90) | ~ latent action aux small gain | L
W3_FlowingWithPurposeLatentActionGuidedFlow | Q03 vision encoder | ImageNet ResNet18 end-to-end in 0.11B policy beats pi0 real (no ablation) | ~ ResNet18 sufficient | L
W3_WhyDoesActionChunkingImproveBehavioralCl | Q06 | DP success Markov/AC/Delay/AC-RDE: LIBERO-10 19.8/88.7/86.8/88.5; ToolHang 28.0/75.2/51.6/71.8; real 3 tasks x 50 rollouts RDE >= AC (fig) | + chunking (benefit = past-obs prediction + implicit ensemble) | H
W3_WhyDoesActionChunkingImproveBehavioralCl | Q06 | uniform temporal ensemble ToolHang 42.2 vs AC 75.2 vs randomized-delay 71.8 | - uniform TE; + randomized-delay/recency schemes | M
W3_WhyDoesActionChunkingImproveBehavioralCl | Q10 | interleaved inference (1-step delay) on real Franka 15 Hz; RDE gives per-step actions from cached chunks matching AC | + per-step readout from cached chunks to avoid boundary jerks | L
W3_WhyDoesActionChunkingImproveBehavioralCl | Q07 | history-conditioned policies "typically very poor" vs single delayed obs (no table) | - long observation history in low data | M
W3_WhyDoesActionChunkingImproveBehavioralCl | Q12 | explicit ensemble of DPs: Transport 12.6 -> 41.5, ToolHang 75.2 -> 87.6 | + small ensembles if compute allows | M
W3_WhyDoesActionChunkingImproveBehavioralCl | Q02 | at 50-60 Hz delayed policies fail; 5-step sub-chunk actions (10-20 Hz effective) restore performance | ~ keep ~10-20 Hz effective action rate or chunk at high fps | L
W3_Ag2ManipLearningNovelManipulationSkillsw | Q03 vision encoder | real Franka 20 demos, 4 tasks x10: ImageNet R50 8/40, CLIP 10/40, R3M 16/40, VIP 20/40, Ag2Manip 31/40 | - frozen generic ImageNet/CLIP; + manipulation-pretrained | L
W3_CanonicalPolicyLearningCanonical3DRepres | Q04 depth/point cloud | UR5 shoe 50 demos: CP-SO2 4/10 & 6/10 vs ACT/DP/EquiDiff/DP3 0/10; Franka 100 demos CP 7/6/4/3 vs DP 2/1/4/0 | + xyz point cloud (canonicalized) | M
W3_CanonicalPolicyLearningCanonical3DRepres | Q14 robustness | color change: image DP/EquiDiff ~0, CP-SO2 +10-30 pts over 2nd best; black-trained shoes -> white 6/10 | + color-free geometry input | M
W3_CanonicalPolicyLearningCanonical3DRepres | Q11 cameras | camera rotated ~15 deg: image policies 0/10, CP 4-6/10; ~30 deg: CP 3/10 | + 3D canonical input for viewpoint shift | M
W3_CanonicalPolicyLearningCanonical3DRepres | Q01 action head | diffusion vs flow: Stack D1 76 vs 59, Push-T 87 vs 97 (CP-SO2) | ~ task-dependent | M
W3_CanonicalPolicyLearningCanonical3DRepres | Q03 vision encoder | DP3 MLP point encoder >> PointNet++/DGCNN (~0 on MimicGen) | + simple MLP point encoder | M
W3_CanonicalPolicyLearningCanonical3DRepres | Q13 data | at 50 demos only CP non-zero; image policies flat 0-1/10 from 50 to 100 demos on UR5 | ~ 3D equivariance improves low-data | L
W3_FocusVLAFocusedVisualUtilizationforVisio | Q03 vision encoder | LIBERO avg DINOv2+SigLIP 98.4, VLM 98.2, VGGT 96.8; mixed->cascaded attn 93.6->97.0 | ~ fusion matters more than encoder (in-dist) | L
W3_FocusVLAFocusedVisualUtilizationforVisio | Q14 robustness | real bg color+texture change -> substantial drop for FocusVLA and baseline (figure/qualitative) | - architecture alone insufficient | L
W3_FocusVLAFocusedVisualUtilizationforVisio | Q12 model size | 0.5B 98.7 LIBERO > 7B OpenVLA-OFT | + small | L
W3_AhaRobotALowCostOpenSourceBimanualMobile | Q02 action space | base velocity control from spiky teleop -> policy fails to move; position displacement -> smooth (qualitative); absolute joint cmds tolerate noise | + absolute position, - velocity | M
W3_AhaRobotALowCostOpenSourceBimanualMobile | Q10 latency | STS3215 servos: dithering + dual-motor anti-backlash -> 0.72 mm repeatability; pi0 slow inference + chunking -> discontinuities knock tools | + low-level trapezoidal smoothing, + faster inference | M
W3_AhaRobotALowCostOpenSourceBimanualMobile | Q13 data | 50 demos box transfer 10/10 (10 trials); RoboPilot vs VR data 73 vs 70% | + ~50 demos for simple pick-place | L
W3_ChicGraspImitationLearningbasedCustomize | Q01 action head | real UR10e, 50 demos, 3 cams: DP 40.6% (41/101) vs IBC 0% vs LSTM-GMM 0% (GMM never triggers gripper) | + diffusion over IBC/GMM | M
W3_ChicGraspImitationLearningbasedCustomize | Q13 data | 50 demos on variable carcasses: 25-65% per exemplar; failures at grasp height | ~ 50 demos marginal for high-variance objects | L
W3_AnchorDP33DAffordanceGuidedSparseDiffusi | Q13 data | RoboTwin 98.7% headline; 10% DAgger off-trajectory frames claimed helpful, no ablation numbers | ~ recovery data | L
W3_ConstrainedContextConditionalDiffusionMo | Q14 robustness | unseen distractors (sim): C3DM fixation 85-90% vs Diffusion Policy 33-42% | + object-centric crop/fixation | M
W3_ConstrainedContextConditionalDiffusionMo | Q05 augmentation/crop | real Franka 20 demos: small blocks DP 0 / mask 40 / zoom 65%; screw pick+place 0/0/60% | + high-res local crop over masking | L
W3_ConstrainedContextConditionalDiffusionMo | Q11 cameras | single top-down cam occluded by arm prevents recovery (stated) | + wrist cam | L
W3_ConstrainedContextConditionalDiffusionMo | Q04 depth | depth height-map sim-to-real, 5 demos: C3DM 100% kitting/hang-cup; DP 0% (5 demos) | ~ depth helps sim2real keyframe | L
W3_FourierFeaturesLetAgentsLearnHighPrecisi | Q04 3D/depth | real PointPatch+RGB 14.8 -> 40.2 with Fourier xyz; RoboCasa 13 -> 34; ablation no-FF 17.5 vs FF 39.9 | + point cloud only with Fourier pos-encoding; - raw xyz encoders | M
W3_FourierFeaturesLetAgentsLearnHighPrecisi | Q05 augmentation | point jitter: FF+VariableJitter 41.4 vs FF no jitter 39.9 | ~ point jitter minor | M
W3_FourierFeaturesLetAgentsLearnHighPrecisi | Q11 cameras | 2 static + wrist; RGB-only and PC-only failed on real color-goal tasks | ~ fuse RGB+3D | L
W3_RethinkingthePracticalityofVisionlanguag | Q03 vision encoder | real DR (new tabletop+distractors), 200 demos: ACT 18.6->3.0% vs 0.5B VLA 44.2->30.7% | + pretrained VLM features, - scratch/ImageNet ResNet | M
W3_RethinkingthePracticalityofVisionlanguag | Q12 model size | CALVIN AvgLen 0.5B 3.65 vs 7B 3.75 (same arch) | + small (0.5B) VLA | M
W3_RethinkingthePracticalityofVisionlanguag | Q01 action head | CALVIN discrete 256-bin tokens 3.68 vs diffusion head 3.70 | ~ discrete ≈ continuous when chunked | L
W3_RethinkingthePracticalityofVisionlanguag | Q06 chunking | CALVIN chunk 1/5/12/20 -> AvgLen 2.25/3.68/3.35/0.70 | + short chunk for AR token model | L
W3_RethinkingthePracticalityofVisionlanguag | Q11 cameras | CALVIN separate view tokens 1.50 vs merged composite image 3.68 | + wrist+scene, + token-cheap fusion | L
W3_RethinkingthePracticalityofVisionlanguag | Q14 robustness | RoboTwin DR avg: ACT 0.5%, DP 0.6%, LLaVA-VLA 28.6%, RDT 11.4% | - from-scratch small policies under visual shift | M
W3_AnchorVLA4DanAnchorBasedSpatialTemporalV | Q07 history | SimplerEnv: first-frame anchor 55.2 vs past-3 frames 46.9 vs strided 21.9; real xLerobot drawer proprio w/ 50% vs w/o 60% (10 trials) | - frame stacking, - proprio in low data | L
W3_AnchorVLA4DanAnchorBasedSpatialTemporalV | Q03 vision encoder | frozen spatial encoder 64.6 vs unfrozen 59.4 vs removed 58.3 | + freeze pretrained encoders | L
W3_AnchorVLA4DanAnchorBasedSpatialTemporalV | Q04 3D | RGB-only Any4D encoder +4.2 pts (60.4->64.6) no depth sensor | ~ implicit 3D from RGB | L
W3_AnchorVLA4DanAnchorBasedSpatialTemporalV | Q06 chunking | xLerobot: pi0.5 better with executing 50-step chunk than 5 (no numbers); AnchorVLA exec 5 of 50 at 300ms -> 17 Hz | ~ | L
W3_ContinueorReplanBernoulliContinuationPol | Q06 chunking | fixed 50-step horizon, only phase shifted: SR 82.5% worst vs 93.7% best; adaptive replanning real 74->92%, 44->84%; fixed 20/30/40 not better than 50 | + stage-adaptive execution horizon (replan before contact) | M
W3_ContinueorReplanBernoulliContinuationPol | Q10 latency | continuation head +2 ms/query, total runtime 10.43->10.24 s; entropy/uncertainty triggers much slower | + cheap replan trigger vs multi-sample uncertainty | M
W3_ContinueorReplanBernoulliContinuationPol | Q14 robustness | trained Clean, eval Randomized RoboTwin 88.78->92.84%; LIBERO-PRO 30.9->37.7% | ~ adaptive horizon helps under shift | L
W3_OnBringingRobotsHome | Q04 depth | wrist RGB-D (median-pooled depth) > RGB-only on most tasks (figure); blinds-at-night depth 2/10 vs RGB 10/10 | + add depth, beware OOD depth | M
W3_OnBringingRobotsHome | Q03 vision encoder | in-domain MoCo ResNet34 (HPR) >=23% over VC-1/MVP/R3M/IN-1K; VC-1 bimodal | + in-domain pretrain, full fine-tune small CNN | M
W3_OnBringingRobotsHome | Q13 data | 24 demos/task -> 81% over 109 home tasks; novice demos 10%/0% first task -> 70%/90% second | ~ ~24-50 demos enough for short tasks; operator practice matters | M
W3_OnBringingRobotsHome | Q14 robustness | day->night OK; unseen strong arm shadow -> erratic failure, fixed by even lighting | ~ shadows are a key lighting failure mode | M
W3_OnBringingRobotsHome | Q07 history | single-frame policy on aliased shelves 0/10 vs 7/10 with distinguishing cue | + some history/context for aliased states | L
W3_OnBringingRobotsHome | Q01 action head | single-step MSE MLP head, 81% on short unimodal tasks | ~ plain regression OK for short unimodal tasks | L
W3_OneACTPlaySingleDemonstrationBehaviorClo | Q06 chunking/TE | std-adaptive TE: stack 60.8 -> 78.4 (400 demos, sim) vs ACT exponential TE | + disagreement-aware ensembling | L
W3_OneACTPlaySingleDemonstrationBehaviorClo | Q10 smoothness | switch to pure chunk replay when ensemble std large; β-sensitive | ~ training-free chunk-blending fix | L
W3_OneACTPlaySingleDemonstrationBehaviorClo | Q05 synthetic demos | 1 VR demo -> transformed replays; real push 35/70/90% at 50/100/200 | + trajectory-transform augmentation | L
W3_FromPlaytoPolicyConditionalBehaviorGener | Q01 action head | real multimodal C-BeT 24/50 vs unimodal 13/50; BlockPush 0.90 vs 0.35; oven (unimodal data) 9/10 vs 8/10 | - unimodal regression on multimodal human data | M
W3_FromPlaytoPolicyConditionalBehaviorGener | Q03 vision encoder | frozen BYOL ResNet18 embeddings fail on knob state (knob 3/20, NN ~chance) | - frozen global SSL embeddings for fine details | L
W3_FromPlaytoPolicyConditionalBehaviorGener | Q14 robustness | 2 distractors ~67% of perf; >=4 distractors 0 success | - frozen-embedding policy brittle to clutter | L
W3_FromPlaytoPolicyConditionalBehaviorGener | Q13 data | 4.5 h play, no labels; goal-obs conditioning 0.98/0.90/2.80 ~= labels 1.0/0.89/2.75 | ~ play data usable | L
W3_RevisitingEnergyBasedModelsasPoliciesRan | Q01 action head | Push-T sim: I-R-NCE 0.884 vs diffusion 0.864 vs NF 0.866 (3.3M params); IBC objective biased | ~ generative heads equivalent, - IBC | L
W3_ContinuousVisionLanguageActionCoLearning | Q01 action head | ALOHA sim cube transfer human: ACT 50, AWE 71, CCoL 82, DP 4 | ~ CVAE-chunk > (untuned) DP on human sim data | L
W3_ContinuousVisionLanguageActionCoLearning | Q10 smoothness | NeuralODE latent + discontinuity penalty: accel fluctuation -32.7%, insertion scripted 72->87% | + smoothness regularization in chunk decoder | L
W3_ContinuousVisionLanguageActionCoLearning | Q04 depth | RLBench avg: 2D CCoL 68.0 vs CCoL3D (RGB-D 3D tokens) 84.9 | + 3D tokens | L
W3_AStudyonEnhancingtheGeneralizationAbilit | Q05 augmentation | DP 6 tasks x50: matched randomization camera .25->.77, light .56->.76, texture .12->.75, height .50->.73; camera-only aug hurts light .56->.28 | + augment each expected shift explicitly | M
W3_AStudyonEnhancingtheGeneralizationAbilit | Q14 robustness | unaugmented DP: normal ~.77 avg -> texture .12, camera .25; real SO-101 PPO sim2real randomization .28->.44 | + scene randomization; texture/camera most damaging | M
W3_AStudyonEnhancingtheGeneralizationAbilit | Q11 cameras | with wrist cam present, 3rd-person camera-pose shift: Square .10, Threading .02, ThreePiece .00 | - wrist cam alone for viewpoint robustness | M
W3_AStudyonEnhancingtheGeneralizationAbilit | Q13 data | trajectory-only (MimicGen) data fails on visual shifts; diversity-randomized data fixes | + diversity over count | M
W3_GELLOAGeneralLowCostandIntuitiveTeleoper | Q13 data quality | teleop success GELLO .92 vs VR .72 vs SpaceMouse .63 (12 novices) | + joint-space leader teleop | M
W3_RoboticManipulationisVisiontoGeometryMap | Q03 vision encoder | LIBERO VGGT-init+LoRA 98.1 vs VGGT-init full-FT 87.1 vs random init 86.6 | + pretrained, frozen/LoRA; - full fine-tune | M
W3_RoboticManipulationisVisiontoGeometryMap | Q11 cameras | real unseen scene camera (wrist kept): ACT 37->7%, pi0.5 77->52%, VGA 75->58% (20 trials) | + pretrained geometry backbone for viewpoint shift | M
W3_RoboticManipulationisVisiontoGeometryMap | Q04 3D | RGB-only 3D prior (VGGT) beats depth-input GeoVLA 98.1 vs 97.7 LIBERO | ~ implicit 3D from RGB, no depth needed | L
W3_RoboticManipulationisVisiontoGeometryMap | Q09 auxiliary | joint depth+camera prediction 97.2->98.1 LIBERO | ~ small gain | L
W3_RoboticManipulationisVisiontoGeometryMap | Q14 robustness | LIBERO-Plus camera shift: VGA 86.0 vs OFT 59.7 vs pi0 15.8 | + 3D-pretrained features for camera robustness | M
W3_GeoPropGroundingRobotStateinVisionforGen | Q07 obs/proprio | DP-R18 sim vanilla proprio 66.8 vs no-proprio 68.1 vs grounded 75.3; real 38.8 / 28.8 / 50.0 (20 trials x 4 tasks) | + keep proprio, ground spatially; ~ copycat risk | M
W3_GeoPropGroundingRobotStateinVisionforGen | Q14 robustness | projection-grounded proprio holds above baselines only up to 2.5 cm / 1.5 deg extrinsic drift (sim) | - calibration-dependent features under camera moves | M
W3_GeoPropGroundingRobotStateinVisionforGen | Q11 cameras/fusion | EE-heatmap channel 61.7 vs RC-PE 60.8 vs local feature sampling 64.8 vs no-proprio 59.5 (MetaWorld 15) | + localized state-vision fusion | L
W3_CounterfactualBehaviorCloningOfflineImit | Q13 data quality | Counter-BC > BC on noisy human demos incl. Robomimic multi-human and real air hockey (figure only) | + denoising/smoothing noisy teleop actions | L
W3_AsyncVLAAsynchronousFlowMatchingforVisio | Q01 action head | WidowX: SFM 47.9 -> random-mask AFM 62.5 -> rater AFM 70.8; real PiPER 4x50: AsyncVLA 87.0 vs pi0 65.0, OFT 65.5 | + FM with masked partial-chunk conditioning | M
W3_AsyncVLAAsynchronousFlowMatchingforVisio | Q10 latency | SFM 10 steps 47.9 vs 20 steps 51.1; 96 ms total on 4090 for 4B model | + few-step FM sufficient | M
W3_AsyncVLAAsynchronousFlowMatchingforVisio | Q13 data | pause intervals masked out of loss (no ablation) | ~ trim idle teleop frames | L
W3_OrderedActionTokensforVisuomotorPolicyLe | Q01 action head | 5M AR policy real P&P: OAT8 16/20 vs QueST 11/20, FAST 8/20, Bin 4/20; no continuous baseline | - naive binning/FAST; ~ discrete tokens only with learned ordered tokenizer | M
W3_OrderedActionTokensforVisuomotorPolicyLe | Q06 chunking | at fixed token count, success drops as Ha grows 8->64 (LIBERO-Long, figure) | ~ chunk length bounded by representation capacity | L
W3_OrderedActionTokensforVisuomotorPolicyLe | Q12 model size | 5M-param Transformer reaches 16/20 on 2 real tasks (single webcam, 10 Hz) | + tiny policies viable | L
W3_RobotSelfImprovementviaHumanVideoDynamic | Q13 data | real Stretch 5 tasks x15: BC 41.3 -> value-filtered rollout FT (RECAP/AWR) ~61 -> failure-repair DGAC 85.3 | + post-deployment rollout fine-tuning | L
W3_DEFLECTTemporalCounterfactualPreferenceL | Q10 latency/async | Kinetix chunk 8, delay 5-7: naive 1.5%, RTC 2.0%, BID 2.0%, VLASH (future-state input) 67.1%, DEFLECT 73.5%; real conveyor pi0.5 76.7 -> VLASH 86.7 -> DEFLECT 96.7% | + keep delay << chunk; + feed execution-time robot state | M
W3_DEFLECTTemporalCounterfactualPreferenceL | Q06 chunking | RTC/BID need overlap (chunk - delay) > ~3 steps or they collapse | + longer chunk under async | M
W3_AtomicMotionCoordinateforLanguageSteerab | Q08 language | fine-tuned pi0.5: language-only steering separation 39.1/24.0%; OOD fruit progress 60.5 -> 87.8 with FK-grounded coordinate (50 trials) | - relying on language alone to redirect visual motor prior | L
W3_DexterousImitationMadeEasyALearningBased | Q13 data | 30 demos, single-step state BC fails all 3 real tasks; kNN (INN/VINN) solves 2-3 (figure only); pauses <2 cm filtered | ~ single-step BC fails at 30 demos | L
W3_GloVLALetGeometryMoveandLocalVLAInteract | Q14 robustness | real UR10e overall 35.6 -> 90.0 (illumination 0 -> 80, hard 0 -> 70); LIBERO-Challenge 20.9 -> 88.5 | + scripted/geometric transport + local learned policy | M
W3_GloVLALetGeometryMoveandLocalVLAInteract | Q13 data | local-only policy 100% @10 demos clean; 99.9 vs 48.5 perturbed @50 demos (LIBERO task 1) | + train on local interaction clips | L
W3_GloVLALetGeometryMoveandLocalVLAInteract | Q10 latency | episode inference time 60.1 s -> 28.2 s | + fewer policy calls via scripted transport | L
W3_RobotUtilityModelsGeneralPoliciesforZero | Q13 data | equal-size data: 5-6 envs x200 vs ~40 envs x25 -> ~50% drop on reorientation (figure); expert>non-expert, mixing can hurt | + diversity over repeats, + clean expert demos | M
W3_RobotUtilityModelsGeneralPoliciesforZero | Q01 action head | DP better than VQ-BeT on small subsets, VQ-BeT better at 900-1200 demos; ACT/MLP-BC close | + diffusion at small data; ~ algorithm secondary | L
W3_RobotUtilityModelsGeneralPoliciesforZero | Q11 cameras | wrist-only iPhone policy: 74.4% zero-shot in 25 unseen homes; ~10% drop moving to xArm/other camera | + wrist camera for env generalization | M
W3_RobotUtilityModelsGeneralPoliciesforZero | Q14 robustness | 90% in unseen envs with mLLM retry (+15.6 pts, 1.31 tries, 4.8% false positives) | + success detection + retry | M
W3_P3POPrescriptivePointPriorsforVisuoSpati | Q14 robustness | novel objects: pick mug 29/30 vs RGB 6/30, RGB-D 3/30; distractors 5/5 vs <=1/5 | + object-centric keypoint input | M
W3_P3POPrescriptivePointPriorsforVisuoSpati | Q04 3D/depth | naive RGB-D token ~RGB (pick mug 19/40 vs 13/40; novel 3/30 vs 6/30); 3D keypoints 39/40; monocular depth = camera depth (all 5/5) | + depth-lifted keypoints, ~ raw depth channel | M
W3_P3POPrescriptivePointPriorsforVisuoSpati | Q03 vision encoder | frozen DIFT correspondence + CoTracker transfers points across instances | + frozen foundation features for object localization | L
W3_P3POPrescriptivePointPriorsforVisuoSpati | Q13 data | 16-60 demos/task (8-15 per instance) -> 13/20-39/40 in-domain | ~ few demos OK with abstracted input | L
W3_AugInsertLearningRobustVisualForcePolici | Q07 history/proprio | real UR5e 20 rollouts: No-Proprio model better than full on all variations (figure only, 1 seed) | - raw proprio in narrow data | L
W3_AugInsertLearningRobustVisualForcePolici | Q05 augmentation | sim canonical 0.987 -> grasp-pose var 0.087; visual aug/noise did not fix physical shifts (figure) | ~ image aug only for appearance, demos for physical | L
W3_DynamicExecutionHorizonPredictionforChun | Q06 chunking | peg insertion (state DP, H=16): fixed exec 6 71.5% -> DEHP 93.2%; under action noise 0.15 exec 2 > exec 6; one-leg best fixed 70.3 -> 95.2% | + short/adaptive execution horizon near contact, esp. with actuation noise | M
W3_DynamicExecutionHorizonPredictionforChun | Q10 latency | DEHP chooses h~1 in tight-insertion phases (requires per-step replanning) | + fast inference to allow frequent replans | L
W3_RoboTwin20AScalableDataGeneratorandBench | Q14 robustness | 50 clean demos, 50 tasks x100: ACT 29.7->1.7, DP 28.0->0.6, DP3 55.2->5.0, pi0 46.4->16.3 (clean->DR) | - clean-only demos for small policies | H
W3_RoboTwin20AScalableDataGeneratorandBench | Q05 augmentation | real: 10 clean demos 9.0% vs +1k DR sim 42.0% (unseen bg + clutter); sim-only 29.5% | + visually randomized synthetic data | M
W3_RoboTwin20AScalableDataGeneratorandBench | Q13 data | DR pretraining RDT 18.8->24.8, pi0 22.5->29.1; clean pretraining 14.6/24.9 (no gain) | + diversity over clean volume | M
W3_RoboTwin20AScalableDataGeneratorandBench | Q04 3D | DP3 best clean (55.2) but 5.0 under DR despite perfect point clouds | ~ 3D helps in-distribution, not visual-shift robust via clutter | M
W3_RoboTwin20AScalableDataGeneratorandBench | Q03 vision encoder | Hard setting: pretrained RDT 13.7/pi0 16.3 vs scratch ACT 1.7/DP 0.6 | + pretrained backbones | M
W3_PerceiverActorAMultiTaskTransformerforRo | Q04 3D | voxel Perceiver 2.8x over C2FARM-BC, 34x over RGB-D Image-BC (RLBench, 10/100 demos) | + 3D fused input for few-demo multi-task | M
W3_PerceiverActorAMultiTaskTransformerforRo | Q02 action space | keyframe next-best-pose + motion planner; random/fixed-interval keyframes -> 0% | ~ keyframe paradigm viable for quasi-static pick-place only | L
W3_PerceiverActorAMultiTaskTransformerforRo | Q08 language | CLIP-conditioned multi-task agent; no-language ablation -> chance | + language needed only when variations ambiguous | L
W3_PerceiverActorAMultiTaskTransformerforRo | Q12 model size | 8xV100 16 days training; real 53 demos/7 tasks 20-90% | - heavy voxel transformers for 8 GB | M
W3_EvaluatingtheEffectivenessofCorrectiveDe | Q13 data | Adroit relocate (DAPG sim): 10 orig + 20 corrective 66.6/92.7/97.9% vs 10 orig + 20 random 7.0/36.0/75.6% at 200/400/600 iters; no gain when corrective is minority; restrictive-only demos 69% in full space | + targeted corrective demos / wider initial-state coverage | L
W3_pi0EqMEquilibriumMatchingforClosedLoopVi | Q01 action head | EqM decoder vs pi0 flow: RoboTwin 40.4 -> 50.2 at 300 solver steps; LIBERO 94.15 -> 94.35 | ~ alternative generative head, heavy compute | L
W3_pi0EqMEquilibriumMatchingforClosedLoopVi | Q10 latency | half-chunk warm start from previous prediction (not ablated separately); 300 iterations/decode | ~ warm start idea, impractical cost | L
W3_GLUEGlobalLocalUnifiedEncodingforImitati | Q14 robustness | real 50 demos single RealSense: clutter DP/ACT 0 vs GLUE 60; occlusion 0 vs 70; party-light illumination 25 vs 75 (10 trials) | + object-centric key-patch + global fusion | M
W3_GLUEGlobalLocalUnifiedEncodingforImitati | Q03 vision encoder | learnable CLIP global-only (GLUE-S) real 70.0 vs DP-R18 36.2 / ACT 48.8; OOD 30-50 vs 0-25 | + pretrained CLIP-class fine-tuned > ImageNet ResNet18 | M
W3_GLUEGlobalLocalUnifiedEncodingforImitati | Q01 action head | real avg ACT 48.8 vs DP 36.2 (50 demos, 10 Hz); MimicGen ACT 34.8 vs DP 18.8 | ~ ACT >= DP in low data | L
W3_GLUEGlobalLocalUnifiedEncodingforImitati | Q04 3D | MimicGen DP3 34.4 vs RGB GLUE 52.4 vs ACT 34.8 | - plain DP3 | L
W3_BAKUAnEfficientTransformerforMultiTaskPo | Q01 action head | LIBERO-90 MLP .90 GMM .84 BeT .89 VQ-BeT .90 Diff .89 (MW Diff .45); real 30 tasks 150 trials: VQ-BeT .91 vs MLP .86 | + multimodal head on real human data; MLP fine in sim | M
W3_BAKUAnEfficientTransformerforMultiTaskPo | Q06 chunking | LIBERO-90 chunk10 .90 vs no-chunk .76; DMC .70 vs .74 | + chunking + temporal ensembling for manipulation | H
W3_BAKUAnEfficientTransformerforMultiTaskPo | Q07 history | no history .90/.79/.70 vs last-step-loss history .54/.08/.37 vs multi-step-loss .90/.82/.68 | + current frame only | H
W3_BAKUAnEfficientTransformerforMultiTaskPo | Q08 language | FiLM ResNet .90 vs no FiLM .87 (LIBERO-90); text .90 ~ goal image .88 | + FiLM text conditioning | M
W3_BAKUAnEfficientTransformerforMultiTaskPo | Q10 smoothness | real: 10 Hz policy + TE + 100 Hz min-jerk controller (qualitative) | + low-level interpolation | L
W3_BAKUAnEfficientTransformerforMultiTaskPo | Q12 model size | LIBERO-90: 4.4M .85, 10M .90, 31M .87, 114M .19 | + ~10-30M policy for low data | M
W3_BAKUAnEfficientTransformerforMultiTaskPo | Q11 cameras | shared encoder .90 vs separate per-view .92 (+15% params/view) | ~ shared encoder ok | L
W3_RoboVIPMultiViewVideoGenerationwithVisua | Q05 augmentation | real Franka DP 100 demos: cluttered 0/10 -> 9/10 with +100 generatively inpainted episodes; SimplerEnv pi0 17.25 -> 29.0 | + generative background/distractor inpainting (temporally consistent) | M
W3_RoboVIPMultiViewVideoGenerationwithVisua | Q07 history | single-frame inpainting aug collapses Octo at 6-frame history (figure only) | ~ aug must be episode-consistent if using history | L
W3_RoboVIPMultiViewVideoGenerationwithVisua | Q14 robustness | DP 100 clean demos: open 7/10 -> 4 distractors 0/10 | - clean-only demos | M
W3_BCZZeroShotTaskGeneralizationwithRobotic | Q02 action space | 1-step delta targets @10 Hz: 3% vs adaptive multi-step state-diff 45% (same task, multi-task one-hot) | - step-wise small deltas; + look-ahead/absolute targets | M
W3_BCZZeroShotTaskGeneralizationwithRobotic | Q13 data | equal data: manual 27%/23% vs 50% HG-DAgger 53%/47%; sim fixed scene 37 demos 97% vs randomized 40 demos 56% | + intervention/recovery data; variability raises demo need | M
W3_BCZZeroShotTaskGeneralizationwithRobotic | Q08 language | frozen sentence emb + FiLM 40% vs one-hot 42% on train tasks; 32% zero-shot held-out | + frozen text encoder + FiLM | M
W3_RobustPoliciesviaMidLevelVisualRepresent | Q03 vision encoder | RLBench pick+place unseen colors: frozen mid-level features 100% vs scratch pixels+DR 20% | + frozen pretrained encoder | L
W3_RobustPoliciesviaMidLevelVisualRepresent | Q05 augmentation | scratch + domain randomization: train 100->70%, test 4->20% | - relying on randomization with scratch encoder alone | L
W3_RobustPoliciesviaMidLevelVisualRepresent | Q14 robustness | unseen objects: normals features 90% vs state 0%; nav sim2real completion 0.4 -> 0.7 | + pretrained invariant features | L
W3_pimathbfR2ReactiveRealtimeFlowPolicies | Q10 latency/smoothness | real 4 tasks x20: piR2 10/12/16/11 vs Train-time RTC 9/8/10/5 vs naive async+TE 7/7/12/2 vs sync 4/4/11/4 | + train-time in-flight-action inpainting with randomized delay; - naive async / sync | M
W3_pimathbfR2ReactiveRealtimeFlowPolicies | Q06 chunking/TE | naive async + temporal ensembling smoother but loses precision; flow degrades as exec horizon h grows 1->8 (sim) | - TE under async; + short exec horizon for reactive tasks | M
W3_pimathbfR2ReactiveRealtimeFlowPolicies | Q01 action head | 1 NFE/call with staircase per-position noise matches 16-step flow at h=1-2 (sim) | + few-step flow feasible | M
W3_pimathbfR2ReactiveRealtimeFlowPolicies | Q12 model size | GR00T-N1.7: VLM ~60 ms + 4-step DiT ~80 ms per call on A6000; needs 2 GPUs for async | + small policy to avoid latency | M
W3_GroundedActionModel3DGroundingasaFoundat | Q14 robustness | RoboTwin Hard: object-centric filter 42.0 vs none 3.5; GAM 47.6 vs pi0.5 25.9; real YAM OOD 17/20 vs pi0.5 4/20 | + object-centric masking/cropping via prompted grounding | M
W3_GroundedActionModel3DGroundingasaFoundat | Q04 3D/depth | DP3 whole-scene PC 55.2 Easy -> 5.0 Hard; det-only 16.0 / image-only 20.3 / both 46.8 | + RGB + object-cropped 3D; - raw scene point cloud for robustness | M
W3_GroundedActionModel3DGroundingasaFoundat | Q03 vision encoder | frozen 3D-grounding backbone + trained flow head 55.3 avg vs fine-tuned pi0.5 45.0 (RoboTwin single-task) | + frozen strong perception + small head | M
W3_EvoHILSelfEvolvingRewardandFlowMatchedPo | Q14 robustness | SO-101 at 60% lighting shift (60 trials): ACT 0.32 push / 0.45 stow vs EvoHIL (relit-trained) 0.93 / 0.73; HIL-SERL push 0.97 -> 0.37 at 10% shift | + lighting augmentation / relit data; - unaugmented policies | M
W3_EvoHILSelfEvolvingRewardandFlowMatchedPo | Q05 augmentation | relit replay (25% share) + anchors: USB shifted 0.50 -> 1.00, original kept 1.00; no relit (alpha=1) 0.88; relit w/o anchors 0.77/0.67 | + mixed relit/photometric copies at moderate ratio | M
W3_EvoHILSelfEvolvingRewardandFlowMatchedPo | Q01 action head | SO-101 flow-matched chunks (H24/E4) vs Gaussian per-step: action 1st-diff -44.5%, HF power -48 to -58%; push duration 11.45 -> 7.80 s | + flow chunk head for smoothness | M
W3_EvoHILSelfEvolvingRewardandFlowMatchedPo | Q10 smoothness | smoothness loss removal: SR 0.97 unchanged, duration 5.44 -> 6.02 s | ~ smoothness term minor | L
W3_BestofSimandRealDecoupledVisuomotorManip | Q03 vision encoder | frozen DINOv2 multi-layer 91.7/71.7 vs last-layer 78.3/55.0 (K=20); scratch BC worst | + frozen DINOv2 multi-scale | M
W3_BestofSimandRealDecoupledVisuomotorManip | Q13 data | end-to-end BC stack 30% ID -> 0% OOD position; BSR 75/35; K=10 BSR 73.3 vs e2e 20.0 | + demos covering workspace | M
W3_BestofSimandRealDecoupledVisuomotorManip | Q14 robustness | 40x40 vs 20x20 workspace: BSR OOD 35% vs e2e 0% | ~ decouple perception/control | L
W3_BestofSimandRealDecoupledVisuomotorManip | Q07 proprio | w/o proprio 71.7/48.3 vs full 91.7/71.7 | ~ proprio helps with sim-trained relative policy | L
W3_RoViAugRobotandViewpointAugmentationforC | Q11 cameras | DP, single side cam, 150 demos: same view 100% -> 10cm/20deg shift 0% (10 trials) | - single fixed scene camera without viewpoint aug | H
W3_RoViAugRobotandViewpointAugmentationforC | Q05 augmentation | novel-view aug +-25cm: shifted-camera 0->80% (10cm,20deg), 0->50% (25cm,35deg); in-dist 100->90% | + viewpoint augmentation (moderate range) | M
W3_RoViAugRobotandViewpointAugmentationforC | Q05 augmentation | brightness randomization on synthetic robot: place 50->80%, sweep 40->100% | + photometric randomization | M
W3_RoViAugRobotandViewpointAugmentationforC | Q14 robustness | camera shift catastrophic without aug (100->0%) | + train-time viewpoint aug | M
W3_HiWMHumanintheWorldModelforScalableRobot | Q13 data/recovery | real: human corrections in WM avg 94.3 vs self-generated successes 75.4 vs base 56.4 (DP & pi0, 3 tasks) | + failure-targeted corrective demos | M
W3_HiWMHumanintheWorldModelforScalableRobot | Q14 robustness | Push-T appearance/background/distractor gains after corrections under varied scenes (figure only) | + corrections under varied conditions | L
W3_SAFEPrunerSemanticAttentionGuidedFutureA | Q10 latency | real pi0.5 backbone 80.4->43.6 ms (RTX 3090), success 81.3->79.3%; OFT 70->37 ms LIBERO 96.8->96.4 | + token pruning/quantization; our 2 s SmolVLA latency is a pipeline issue | M
W3_FastandAccurateAnAdaptiveVLAInferenceFra | Q12 model size | LIBERO 50 demos/task: BC-ViLT 86.95 vs pi0 94.15; full-workspace randomization 20 vs 56%; real dual-arm ACT 60% vs pi0 100% | ~ small ok in narrow distribution, large better under wide variation | M
W3_FastandAccurateAnAdaptiveVLAInferenceFra | Q10 latency | pi0 called on 15.3% of steps: SR 92.4% at 93.4 Hz vs fixed schedule 90.35%; no action fusion at handoff -1.1 avg / -3 LIBERO-10 | + fast small policy with boundary fusion | M
W3_FastandAccurateAnAdaptiveVLAInferenceFra | Q13 data quality | small policy trained on pi0-distilled rollouts +4.8 pts vs on human teleop | + consistent/clean demos | L
W3_HybridConsistencyPolicyDecouplingMultiMo | Q10 latency | real per-chunk 4080: DDPM80 0.54 s 78.3%; DDIM50 0.34 s 76.7%; HCP25+1 0.17 s 73.3%; 5-step consistency 0.04 s 38.3% | + few-step deterministic sampling; - naive 1-step DDPM distillation | M
W3_HybridConsistencyPolicyDecouplingMultiMo | Q01 action head | DDIM (mode-collapsed, entropy 0) success 87% sim / 76.7% real vs DDPM 79% / 78.3% | ~ inference stochasticity unnecessary for success | M
W3_Pix2ActImageSpaceManipulationPolicieswit | Q02 action space | MimicGen ablation: 3D absolute 41.5 vs 3D EE-relative 55.5 vs image-space 69.3 | + EE-relative over absolute | M
W3_Pix2ActImageSpaceManipulationPolicieswit | Q05 augmentation | removing equivariant obs+action rotation aug: 69.3 -> 51.0 | + equivariant augmentation | M
W3_Pix2ActImageSpaceManipulationPolicieswit | Q11 cameras | w/o agent view only -2.8 pts; perturbed agent cam: DP fails both tasks, Pix2Act unaffected (qualitative) | + wrist cams primary; scene cam as context | M
W3_Pix2ActImageSpaceManipulationPolicieswit | Q13 data | real: 40 demos 55% vs DP 20%; 70 demos 85 vs 60 | ~ representation matters more at low data | L
W3_Pix2ActImageSpaceManipulationPolicieswit | Q14 robustness | agent-view random perturbation: DP fails, Pix2Act unaffected | + wrist-grounded actions for camera shift | L
W3_SAVLASymmetryAwareVisionLanguageActionMo | Q01 action head | real SO-101, 50 demos/task, 20 eps: GR00T flow head 61.7% vs equivariant flow head 71.7%; LIBERO 86.5->91.6 | + flow matching; + equivariant head | L
W3_SAVLASymmetryAwareVisionLanguageActionMo | Q03 vision encoder | frozen GR00T N1.5 VLM + 100M head reaches 55-75% on 3 SO-101 tasks with 50 demos each | + frozen pretrained VLM backbone | M
W3_SAVLASymmetryAwareVisionLanguageActionMo | Q05 augmentation | LIBERO-Goal scene rotation: no aug 41.5, homography-warp aug 69.1, re-rendered aug 74.5 | + geometric (warp) augmentation for pose/viewpoint | M
W3_SAVLASymmetryAwareVisionLanguageActionMo | Q13 data | 10%/25%/100% data: 48.3/66.1/86.5 baseline vs 57.1/71.9/91.6 equivariant | + structural priors matter more at low data | M
W3_SAVLASymmetryAwareVisionLanguageActionMo | Q14 robustness | real SO-101 rotated scene +-30deg: 47.9 -> 57.1 avg | ~ rotation robustness needs priors or aug | L
W3_SeedPolicyHorizonScalingviaSelfEvolvingD | Q07 history | DP frame stacking degrades with longer T_obs (fig); recurrent gated state: long task 33->73%, real ambiguous tasks e.g. 16->54% (100 rollouts) | - naive frame stacking; + recurrent state only for aliased/long tasks | M
W3_SeedPolicyHorizonScalingviaSelfEvolvingD | Q12 model size | RoboTwin 50 demos: 33M SeedPolicy 40.1% clean vs 1.2B RDT 34.5%; Hard 4.3 vs 13.7 | + small for in-distribution; - small scratch for visual shift | M
W3_SeedPolicyHorizonScalingviaSelfEvolvingD | Q14 robustness | all small scratch policies <=4.3% on randomized test (ACT 1.74, DP 0.64-1.44) | - clean-only training | H
W3_SeedPolicyHorizonScalingviaSelfEvolvingD | Q13 data | pauses in demos -> zero-velocity freeze failure (qualitative) | + trim idle pauses from teleop demos | L
W3_KAIAKinematicAwareInterfaceforDataEffici | Q09 aux | sim: no-aux 44.1 -> keypoint+trajectory aux 82.9; future-depth aux only 49.6 | + object-centric structured aux; - generic depth prediction aux | M
W3_KAIAKinematicAwareInterfaceforDataEffici | Q14 robustness | real 15 trials/cell, clean-trained: Ours 66.7/62.2/62.2 (none/bg/obj) vs Seer 37.8/26.7/31.1, DP3 33.3/28.9/24.4 | + aux object localization for bg/distractor shift | L
W3_KAIAKinematicAwareInterfaceforDataEffici | Q04 3D | DP3 point cloud 37.3 sim avg vs ACT 58.5 RGB; fused DINOv2+PC 82.9 | - point-cloud-only; ~ fused RGB+3D | L
W3_KAIAKinematicAwareInterfaceforDataEffici | Q13 data | 100 demos: Ours 42.4 vs DP3 20.1, Seer 20.2; matches baselines with half data | + structured priors raise low-data efficiency | M
W3_KnowingWhentoStopAdaptiveActionChunkingv | Q06 chunking | fixed exec horizon sweep: pi0.5 RoboTwin 61.6(10)->52.2(25); X-VLA 43.5(15)->76.1(30); real pi0.5 41.7-51.7 peak at 30 steps@20Hz; adaptive entropy truncation 62.9/79.0/61.7 | + tune/adapt execution horizon per model (~1-1.5 s) | M
W3_KnowingWhentoStopAdaptiveActionChunkingv | Q10 latency | MS adaptive method with very short chunks -> intermittent pauses, real 18.3% vs 41.7-51.7 fixed; entropy rule adds <7 ms on A100 (0.27 s/chunk) | - very short re-plan horizons without smoothing | L
W3_LaST0LatentSpatioTemporalChainofThoughtf | Q09 auxiliary | RLBench: no future-latent 68% -> 1 token/modality x4 future steps 82% (3.3B VLA) | + compact future-latent aux (img/3D/proprio) | L
W3_LaST0LatentSpatioTemporalChainofThoughtf | Q10 latency | slow:fast 1:1-1:4 75-79%, 1:8 74%, mixed-ratio training 82% (sim) | + train with randomly stale slow conditioning | L
W3_LaST0LatentSpatioTemporalChainofThoughtf | Q04 3D | latent modality alone: image 74%, point cloud 76%, proprio 75%, all 82% | ~ 3D small gain | L
W3_PredVLAPredictiveSensorimotorModelingfor | Q09 aux objectives | LIBERO 3-suite: removing sensory-prediction pathway 63.9->11.6; full 86.1 vs param-matched BC-TF ~20 (frozen RN18+PCA) | + predictive/world-model objective at tiny scale | L
W3_PredVLAPredictiveSensorimotorModelingfor | Q12 model size | 0.68M trainable controller: 75.4% 4-suite LIBERO, 46 ms/step on 5090 | ~ tiny controllers viable on frozen features (sim only) | L
W3_PredVLAPredictiveSensorimotorModelingfor | Q07 history | removing multi-timescale hierarchy -17..-29 pts in predictive model, only -1.2 in plain BC | ~ recurrence helps only with predictive structure | L
W3_PredVLAPredictiveSensorimotorModelingfor | Q14 robustness | exact open-loop (no obs) policy still 77.3% on LIBERO short suites; 50% visual corruption <5 pt | - trust LIBERO success as evidence of visual grounding | M
W3_PolarNet3DPointCloudsforLanguageGuidedRo | Q04 3D/depth | RLBench 10 tasks: XYZ-only 72.1 -> +RGB 91.3 -> all feats 92.1; crop table/background 81.6 -> 92.1; vs 2D Hiveformer 88.4 | + colored cropped point cloud | M
W3_PolarNet3DPointCloudsforLanguageGuidedRo | Q11 cameras | single cam 35-48%, L+R 67.0, L+wrist 80.2, all 3 92.1; wrist weakest alone but most complementary | + wrist cam as complement | M
W3_PolarNet3DPointCloudsforLanguageGuidedRo | Q14 robustness | camera pose perturbation: point cloud drop much smaller than 2D Hiveformer (figure only, sim, calibrated extrinsics) | + 3D for camera shift (needs recalibration) | L
W3_PolarNet3DPointCloudsforLanguageGuidedRo | Q12 model size | single-task de32 92.1 vs de64 91.0; multi-task de32 77.4 vs de64 89.3, L4 86.3 | ~ small for single task | L
W3_ReasoningWithoutInferenceCostLatentSeman | Q09 aux objectives | RoboTwin sim 2B H-RDT: dense phase-local text-alignment aux 90 vs 79 no-aux vs 58 trivial-target aux; zero inference cost | + training-only aux w/ informative targets; - uninformative aux | L
W3_ReasoningWithoutInferenceCostLatentSeman | Q12 model size | frozen 2B backbone at robot finetune -> 0% vs 85 full finetune | - freezing large VLA backbone | L
W3_ItsNotJustMoreDemosCounterfactualActionS | Q14 robustness | ACT clean 0.96/0.90 -> nuisance mean 0.30/0.32 (lighting 0.44/0.57, appearance 0.09/0.71), sim | - clean-only small policy | M
W3_ItsNotJustMoreDemosCounterfactualActionS | Q05 augmentation | action-preserving counterfactual repair K=20: all-nuis 0.30->0.96 (random K=20: 0.56; random K=500: 1.00), sim | + targeted/diverse visual aug paired with original actions | M
W3_ItsNotJustMoreDemosCounterfactualActionS | Q13 data | single-factor targeted repair leaves worst-case 0.0; held-out best with random-500 (0.90) | + diversity/coverage over count | L
W3_PVIPluginVisualInjectionforVisionLanguag | Q03 encoder | GR00T 50 demos sim: 39.8 -> +frozen DINOv2 side-path 56.8 -> +frozen V-JEPA2 69.4 | + frozen dense SSL features injected to action head | M
W3_PVIPluginVisualInjectionforVisionLanguag | Q07 history | V-JEPA2 frames@4fps: 2f 71.6, 4f 71.8, 8f 69.4, 16f 66.6 | + short history (0.5-1 s) via frozen video encoder; - long history | L
W3_PVIPluginVisualInjectionforVisionLanguag | Q12 model size | 3B GR00T fine-tune on 50 demos only 35.7-39.8% sim avg | ~ big VLA not sufficient alone | L
W3_REBOOTFromFailuretoRecoveryADatasetandBe | Q13 data | 60 expert demos/task: install success 16% vs remove 56%; 54% failures at Align/Engage(place); recovery-data effect NOT measured | + collect phase-targeted recovery demos from own rollouts | L
W3_REBOOTFromFailuretoRecoveryADatasetandBe | Q13 data | trailing static segments flagged; IL copies pauses (cited) | + trim idle segments | L
W3_REBOOTFromFailuretoRecoveryADatasetandBe | Q01 action head | ACT ~ DP overall, pi0-FAST best, 15 rollouts/task/policy (figure) | ~ | L
W3_SelfSupervisedCorrespondenceinVisuomotor | Q05 augmentation | noise on proprio input (1mm/1deg) keeping global setpoint label: 30 demos 1.1->73.3%, 200 demos 3.4->97.8% (sim) | + proprio noise injection | M
W3_SelfSupervisedCorrespondenceinVisuomotor | Q03 vision encoder | sim Reach T+R: dense-correspondence keypoints 97.8 vs E2E 32.2 vs AE 61.1; E2E ResNet34 3.3 | + pretrained/correspondence features over scratch E2E | M
W3_SelfSupervisedCorrespondenceinVisuomotor | Q04 3D/depth | 3D keypoints (depth) Push plate 98 vs 2D 87; better outside train convex hull | + depth-lifted features | L
W3_SelfSupervisedCorrespondenceinVisuomotor | Q13 data | real: ~50 demos -> 97-100% single-instance tasks; 146 demos -> 77% novel shoes | ~ 50 demos enough for fixed object; more for category | M
W3_SelfSupervisedCorrespondenceinVisuomotor | Q14 robustness | novel shoe instances 17/22 (77%) vs seen 88% | ~ object-centric features give partial instance generalization | L
W3_SelectivePerceptionforRobotTaskAwareAtte | Q11 cameras | pi0+LoRA 50 demos: router on wrist+prompt 83.3% vs external+prompt 73.3%; static fusion of all streams 10% | + wrist cam as anchor; - naive static multi-stream fusion | L
W3_SelectivePerceptionforRobotTaskAwareAtte | Q07 history/proprio | router with raw state input 30% vs 83% without (acted as noise) | - raw proprio into gating modules | L
W3_SPIRESynergisticPlanningImitationandRein | Q13 data | sim: KL-constrained RL on top of BC reaches >=80% with 10-50 demos vs BC >870 demos over 7 tasks; Tool Hang 10%->94% | ~ (needs sim/RL, not our pipeline) | L
W3_ProgVLAProgressAwareRobotManipulationSki | Q03 vision encoder | LIBERO: fine-tuned DUNE ViT-S 91.1 vs frozen 77.6 (Long 88.6 vs 60.6); DINOv3 88.7 | + fine-tuned pretrained SSL ViT-S; - frozen | M
W3_ProgVLAProgressAwareRobotManipulationSki | Q12 model size | 0.1B no-robot-pretrain 91.1 LIBERO vs SmolVLA-2.25B 88.7; real PiPER 50 demos/task 68% (100 trials) | + ~100M model | M
W3_ProgVLAProgressAwareRobotManipulationSki | Q01 action head | flow matching + progress-weighted loss; w/o weighting 88.8 vs 91.1 | ~ FM fine at 100M | L
W3_ProgVLAProgressAwareRobotManipulationSki | Q09 auxiliary | progress/value heads reweighting: +2.3 avg, +3.5 Long (single seed) | ~ small gain | L
W3_ProgVLAProgressAwareRobotManipulationSki | Q02 action space | delta joint displacement on real leader/follower PiPER, no ablation | ~ delta joints workable | L
W3_SimulationDistillationPretrainingWorldMo | Q09 aux | sim peg/tableleg success: no recon 0.90/0.85 vs +pixel reconstruction 0.32/0.21 | - pixel reconstruction aux | M
W3_SimulationDistillationPretrainingWorldMo | Q13 data | expert-only vs perturbed+suboptimal equal volume: 0.10/0.05 vs 0.90/0.85 (world model) | + recovery/perturbation coverage | L
W3_StartRightArriveRightAsynchronousExecuti | Q10 latency/async | real 6 tasks, d~3: PAINT >= RTC (GR00T toy-drawer 0.85 vs 0.75; pi0 towel 0.80 vs 0.54); B-spline smoothing ~ no prefix fix (sim) | + prefix-conditioned async (RTC/PAINT), - post-hoc smoothing | M
W3_StartRightArriveRightAsynchronousExecuti | Q06 chunking/TE | pi0 H=50: TE SR 0.10-0.20 vs RTC/PAINT 0.50-0.65, completion 58s vs 15s | - temporal ensembling for long-chunk VLAs | M
W3_StartRightArriveRightAsynchronousExecuti | Q01 action head | OT flow matching allows gradient-free prefix anchoring via ODE inversion (86 ms GR00T vs RTC 113 ms) | ~ flow head has deployment advantages | L
W3_StabilizetoActLearningtoCoordinateforBim | Q13 data | acting BC-RNN 20 -> 40 in-distribution demos: Hard OOD objects 28.8->23.1, 53.3->56.7, 26.6->30.0 (no gain) | + diversity over count for novel objects | L
W3_StabilizetoActLearningtoCoordinateforBim | Q14 robustness | vision-only policy: in-dist 76.9 -> OOD objects 52.7 avg (Hard 27-53%) | - expect big drop on different-looking object without diversity/aug | L
W3_SpatialVAMSpatialAwareMultiViewVideoDiff | Q04 3D/depth | real FR3 10 demos: RGB-D point cloud rendered to 3 virtual views; 1 camera 50.0 (orig views)/60.0 (adapted) vs 3 cams 57.1; 20mm/2deg calib error 51.4 | + single RGB-D via virtual-view projection is viable | L
W3_SpatialVAMSpatialAwareMultiViewVideoDiff | Q09 aux objectives | Meta-World: predicting 0->3 extra future RGB views 61.1->89.1; no pretrained video weights 4.6 | + future-frame co-prediction only with big pretrained video model | L
W3_SpatialVAMSpatialAwareMultiViewVideoDiff | Q12 model size | 5B Wan2.2 VAM needs >30 GB and 4.6 s/24-frame chunk on A100 | - video-foundation VAMs on 8 GB laptop | H
W3_SpatialVAMSpatialAwareMultiViewVideoDiff | Q14 robustness | real 10 demos: DP3 0.0, pi0.5 1.4, BridgeVLA 41.4, SpatialVAM 57.1 avg incl. lights-off 3/10, new category 5/10 | ~ 10 demos insufficient for robust OOD for any method | L
W3_TowardsEffectiveUtilizationofMixedQualit | Q13 data | real 50 mixed demos: DP Tissue 10->65%, ACT 0->25%, RISE Pen-3 40->60% after segment select+relabel; discarding low-quality < repairing | + clean/relabel noisy segments, keep mediocre demos | M
W3_TowardsEffectiveUtilizationofMixedQualit | Q13 data | sim: trajectory-smoothing all demos -27.48% vs selected low-quality only +17.07% | - blanket smoothing of demos | M
W3_TowardsEffectiveUtilizationofMixedQualit | Q04 3D | same 50 mixed demos: RISE 3D 90/90/87.5/70/50/40 vs DP 10/35/30/50/30/26.7 | + point cloud (uncontrolled arch) | L
W3_TrainOfflineTestOnlineARealRobotLearning | Q03 vision encoder | frozen+BC real Franka: in-domain MoCo 83.3/72.2%, BYOL 72.2/66.6 vs ImageNet ResNet50 47.2/50.0, MoCo generic 33.3/55.5, R3M 44.4/33.3 (scoop/pour) | - frozen generic (R3M/ImageNet); + in-domain adaptation | M
W3_TrainOfflineTestOnlineARealRobotLearning | Q13 data quality | BC scooping: successes-only 83.3% vs all incl. failures 72.2%; top5% 38.9, 25% 72.2, 50% 77.8 | + filter failed demos; diminishing returns | M
W3_TrainOfflineTestOnlineARealRobotLearning | Q06 chunking | 50-step (1.7 s @30Hz) chunks beat per-step closed-loop and full open-loop (stated, no numbers) | + chunking | L
W3_SIDSlidingintoDistributionforRobustFewDe | Q11 cameras | same 50 demos: egocentric wrist RGB-D policy 80.3% vs fixed external cam 26.0% (6 real tasks) | + wrist camera | M
W3_SIDSlidingintoDistributionforRobustFewDe | Q14 robustness | ACT/DP3/pi0.5 (100 demos) OOD object placement 0-14% vs ID 18-92%; SID 82-92% | - end-to-end BC outside demo coverage; + object-centric segmentation | M
W3_SIDSlidingintoDistributionforRobustFewDe | Q05 augmentation | egocentric point-cloud reprojection aug: 3.7% -> 89.7% avg (2 demos) | + geometric view augmentation | M
W3_SIDSlidingintoDistributionforRobustFewDe | Q13 data | 2/10/50 raw demos after aug: ~19-23/25 all | ~ augmentation substitutes count | L
W3_SIDSlidingintoDistributionforRobustFewDe | Q04 3D | DP3 OOD 0-12% similar to ACT 0%; SID point-cloud egocentric works | ~ 3D alone not enough for spatial OOD | L
W3_TheUnreasonableEffectivenessofDiscreteTi | Q01 action head | RLBench constrained avg: MiDiGaP-5demos 0.95 vs DP-100demos 0.48; multimodal 0.86 vs DP 0.46 (all get GT object pose) | + explicit trajectory mixture/GMM when object pose available | M
W3_TheUnreasonableEffectivenessofDiscreteTi | Q14 robustness | real Franka visual-generalization (tablecloths, distractors, new instances) 1.00 with DINO/FoundationPose task frames | + object-pose/keypoint intermediate | M
W3_TheUnreasonableEffectivenessofDiscreteTi | Q13 data | real 5 demos: DP/LSTM/ARP 0.00, MiDiGaP 1.00 mild / 0.95 constrained | + structured object-frame policies cut demo need | M
W3_VIRALVisualSimtoRealatScaleforHumanoidLo | Q05 augmentation | no visual randomization -> 0.649 normalized success (-35.1%); materials, dome light, camera extrinsics dominant | + lighting/colour/extrinsic randomization | L
W3_VIRALVisualSimtoRealatScaleforHumanoidLo | Q03 encoder | DINOv3 student backbone best (figure only) | + DINO-family | L
W3_VIRALVisualSimtoRealatScaleforHumanoidLo | Q07 history | FF-history and LSTM > single-step (figure only) | + short history | L
W3_VIRALVisualSimtoRealatScaleforHumanoidLo | Q13 data | 10-object vs 1-object training better on all objects (figure); pure BC brittle vs DAgger mix | + object diversity, + on-policy corrections | L
W3_ToolFlowNetRoboticManipulationwithToolsv | Q04 3D/depth | sim tool tasks: RGBD 0.606 vs RGB 0.538 vs point-flow 0.892; flow gives no gain on translation-only variant | ~ 3D helps mainly rotation-heavy tasks | L
W3_ToolFlowNetRoboticManipulationwithToolsv | Q14 robustness | adding GT segmentation mask channel: RGB 0.538->0.693, D 0.311->0.686, RGBD 0.606->0.753 (sim) | + object mask inputs | L
W3_TunetoLearnHowControllerGainsShapeRobotP | Q02 action space | real FR3 BC: compliant-overdamped 71% vs stiff 5-8%; sim 6 tasks significant; holds for abs & rel joints | + low-Kp/high-Kd servo gains under position actions | M
W3_TunetoLearnHowControllerGainsShapeRobotP | Q10 latency/smoothness | compliant gains attenuate action noise (open-loop noisy replay); jitter failures 21.8%@100Hz -> 5.0%@10Hz (RL sim2real) | + compliant/overdamped follower; ~ lower policy rate vs oscillation | M
W3_TunetoLearnHowControllerGainsShapeRobotP | Q13 data | compliant/overdamped gains give steeper BC scaling with #demos (fig); teleop success unchanged with tuned mapping | + tune gains before collecting more demos | L
W3_TunetoLearnHowControllerGainsShapeRobotP | Q12 model size | compliant gains -> higher val MSE but higher success | - select checkpoints by val loss | M
W3_VisionLanguageFoundationModelsasEffectiv | Q03 vision encoder | CALVIN ABCD->D avg len: R3M frozen 0.10, Voltron frozen 0.11, Voltron fine-tuned 2.08, RoboFlamingo 4.09 | - frozen robotics encoders; + fine-tune | M
W3_VisionLanguageFoundationModelsasEffectiv | Q12 model size | 10% data: 3B 0.05-0.13 vs 9B 0.83; full data 3B-IFT 4.09 vs 9B 3.97; full fine-tune 3B 0.50 vs partial 4.09 | ~ pretrained capacity helps, full FT collapses | L
W3_VisionLanguageFoundationModelsasEffectiv | Q07 history | MLP no-history worst; LSTM/GPT history heads best (figure only) | + history via head | L
W3_VisionLanguageFoundationModelsasEffectiv | Q08 language | GPT-4 paraphrases: 1.85 -> 2.12 with frozen embedding layer | + freeze text embeddings | L
W3_TaskAnchorGroundingTaskStateinReactiveVL | Q07 history | RMBench memory tasks: pi0.5 0.14 -> history+stage-coordinate 0.68; history-only 0.18, coordinate-only 0.31 (sim) | ~ structured task-state only for aliased/long tasks | L
W3_VidarEmbodiedVideoDiffusionModelforGener | Q14 robustness | masked IDM (L1-sparse learned pixel mask) vs ResNet: held-out acc 49.0 vs 24.3; real unseen bg 55.6 vs 22.2 (3 trials/task) | + learned sparse spatial mask/attention on image | L
W3_VidarEmbodiedVideoDiffusionModelforGener | Q14 robustness | RoboTwin clean-trained -> randomized: pi0.5 44.8->14.2, Vidar 65.8->17.5 | - relying on pretrained priors without diverse/augmented data | M
W3_VidarEmbodiedVideoDiffusionModelforGener | Q10 latency | 25 s per 7.5 s open-loop plan on 8x A100 | - video-generation planners for our latency | H
W3_VIMAGeneralRobotManipulationwithMultimod | Q08 language | sim primitives: xattn prompt conditioning > GPT concat at small sizes; T5 30M/111M/368M no significant difference (figure only) | + small frozen text encoder w/ cross-attn/FiLM | L
W3_VIMAGeneralRobotManipulationwithMultimod | Q12 model size | object tokens beat pixel tokenizers across 2M-200M, esp. low data (1% data ~ others 10%) (figure only) | + object-centric inputs for small models | L
W3_WaypointBasedImitationLearningforRobotic | Q13 data | AWE relabelling: DP Square 30 demos 44.3->62.3, 50: 57.3->67.0, 200: 95.0->94.7; real ALOHA coffee ACT 36->64 | + waypoint relabelling in low-data regime | M
W3_WaypointBasedImitationLearningforRobotic | Q01 action head | AWE helps GMM but degrades MSE/unimodal BC (figure only) | - plain MSE with multimodal targets; + expressive head | L
W3_WaypointBasedImitationLearningforRobotic | Q06 chunking | ACT sim human insertion 20->30, cube 50->71 with 7-10x shorter horizon; chunk 100->50 steps to keep wall-clock | + shorten decision horizon; size chunks in seconds | M
W3_WaypointBasedImitationLearningforRobotic | Q10 smoothness | authors advise temporal ensembling on ALOHA; slower blocking controller for precision (no numbers) | ~ TE for smoothness | L
W3_UsingBothDemonstrationsandLanguageInstru | Q08 language | sim multi-task: FiLM(demo)+concat(lang) 25.8 / FiLM(both) 22.4 vs concat(both) 7.9; miniLM/DistilBERT ~25-27 vs frozen CLIP ~11 | + FiLM conditioning, small frozen LM | L
W3_vlasimdEfficientCPUInferenceforLanguageC | Q10 latency | actions/s on Ryzen5 CPU: ACT 627, IMPACT 262, SmolVLA 38, DP-100step 3.6; Pi5 query: ACT 0.92s, IMPACT 1.21s, SmolVLA 8.19s | + small ACT-class (34-60M) for real-time | H
W3_vlasimdEfficientCPUInferenceforLanguageC | Q10 latency | time-aligned async needs H/Tq >= ~2x control rate; transport adds 0.5-1.0 s RTT | + measure full obs-to-action path, long chunks | M
W3_vlasimdEfficientCPUInferenceforLanguageC | Q12 model size | SO-101, 44 demos/3 instr: 60M IMPACT 90/85/60% | + small (~60M) model | M
W3_vlasimdEfficientCPUInferenceforLanguageC | Q08 language | SO-101: no-language multi-task ACT 20% vs IMPACT (FiLM+T5 tokens) 60-90%; LIBERO shuffle 91% new goal | + FiLM + cached text tokens | M
W3_vlasimdEfficientCPUInferenceforLanguageC | Q06 chunking | H=50-100 @30Hz covers CPU latency; H=4 (Octo) fails budget | + chunk >= latency x2 | M
W3_vlasimdEfficientCPUInferenceforLanguageC | Q01 action head | CVAE+L1 ACT works on SO-101; DP 100-step 40 s/query on Pi5, 10-step DDIM 5 s | + CVAE/regression for CPU/latency; - many-step diffusion | M
W3_VisualBacktrackingTeleoperationADataColl | Q13 data | 60 min teleop each: in-episode fail->recover->success data BC 73% vs success-only BC 66%; IQL on it 79% (1437 A/B episodes) | + include recovery demos within same episode | M
W3_VisualBacktrackingTeleoperationADataColl | Q13 data | separate failure/play episodes mixed in: OffRL 52-64% vs 67-69% success-only (spurious visual cues) | - mixing visually-dissimilar failure episodes | L
W3_VisualBacktrackingTeleoperationADataColl | Q07 history/copycat | success-only Q function relies on proprio (gripper closed+moving up) not image | ~ proprio shortcut risk in small datasets | L
W3_WhatistheBetterCurriculumControllerShape | Q13 data quality | 30 controller-consistent demos: ACT 95% stable vs 30 best-of-100 manual 15% (contact-screened 30%); pi0.5 95% vs 5% | + demo consistency over count/screening | M
W3_WhatistheBetterCurriculumControllerShape | Q12 model size | ACT 18M 95% = pi0.5 2B 95% ID with 30 demos (fragile cup) | + small model sufficient in-distribution | M
W3_WhatistheBetterCurriculumControllerShape | Q10 latency/reactivity | under disturbance policy-only 55% vs +25Hz reflex arbiter 100% (pi0.5 ~1.7 Hz re-query) | + fast low-level reactive layer / higher re-query rate | M
W3_WhatistheBetterCurriculumControllerShape | Q09 aux objectives | 2nd-order gripper smoothness loss: teacher-near runs ACT 15->18/20, pi0.5 12->16/20 | ~ smoothness loss minor help | L
W3_WhatistheBetterCurriculumControllerShape | Q02 action space | follower-realized state as action label in winning condition (confounded with reflex) | ~ follower vs leader labels unresolved | L
W3_VisualThinkVLAVisualIntermediateReasonin | Q14 robustness | real 50 trials: multi-object pick-place w/ distractors 48.6 -> 75.6 with bbox/edge/motion cues; SmolVLA test split 42.7 -> 54.7 | + explicit object-localization cues | L
W3_VisualThinkVLAVisualIntermediateReasonin | Q09 aux | textual CoT ECoT 8.38 s/step vs visual evidence 0.37 s | + compact visual intermediates; - textual reasoning | L
W3_VisualThinkVLAVisualIntermediateReasonin | Q04 depth | Depth Anything V2 channel screened out as low-utility | ~ monocular depth cue | L
W3_VisuomotorControlinMultiObjectScenesUsin | Q03 vision encoder | sim IBC: MoCo frozen global features did not converge; Slot (object-aware) 57.1 vs RGB 36.9 at 1k eps | - global-pooled contrastive features; + spatial/object-aware | L
W3_VisuomotorControlinMultiObjectScenesUsin | Q14 robustness | RGB+GT segmentation 78.5 vs RGB 36.9 (1k eps); 95.4 vs 95.1 at 10k | + object masks as inputs in low data | L
W3_VisuomotorControlinMultiObjectScenesUsin | Q13 data | representation priors' gain vanishes 1k->10k episodes (all ~95%) | ~ priors matter most in low-data regime | M
W3_ActionControlNetALightweightDelayAwareAd | Q10 latency/async | Kinetix avg d>0: naive async 0.61, RTC 0.72, Training-RTC 0.80, ACNet 0.79 (20% params); SO-ARM101 50 demos: naive 17/20 vs ACNet 20/20, less handoff oscillation | + condition head on executed action prefix; - naive stitching | M
W3_ActionControlNetALightweightDelayAwareAd | Q12 model size | Meta-World latency: Evo-1+ACNet 91 ms/11 Hz vs pi0 RTC 159 ms, Training-RTC 134 ms | + lightweight VLA for real-time | L
W3_ActionControlNetALightweightDelayAwareAd | Q01 action head | residual delay conditioning on final block of flow-matching expert; final-block > early injection (figure) | + flow head supports cheap async conditioning | L
W3_AXISAGrowableCommunityDrivenDataEnginefo | Q14 robustness | LIBERO-Plus pi0.5 + AXIS (camera-randomized): camera 72.5->83.8, noise 82.5->96.2, overall 83.9->88.8 | + viewpoint-randomized training data for camera shift | L
W3_AXISAGrowableCommunityDrivenDataEnginefo | Q05 augmentation | rendered camera(±10cm/±8deg)/light/texture randomization; largest gains on matching axes | + viewpoint/photometric aug | L
W3_AXISAGrowableCommunityDrivenDataEnginefo | Q13 data quality | SG smoothing+resample: jerk -81% but replay success 100->86.2% | ~ smooth/trim idle carefully, verify replay | L
W3_XDiffusionTrainingDiffusionPoliciesonCro | Q13 data quality | real Franka 5 robot+100 human demos: robot-only < naive co-train < manually filtered < noise-gated (fig only; +16% avg over baselines); ~50% human demos infeasible | + filter/down-weight infeasible or low-quality demos | L
W3_XDiffusionTrainingDiffusionPoliciesonCro | Q01 action head | diffusion noise-level gating lets low-quality data help (fig only) | + diffusion/flow if mixing heterogeneous data | L
W3_ZevaEgoEgocentricMidTrainingwithInContex | Q13 data | real: 10 robot demos + 50 task-matched human videos (same cam) -> +55/+40 pts; 10K h ego ~ 2K h robot (75.3 vs 74.7%) | ~ human video helps only with latent-action VLA machinery | L
W3_VisualSpatialAttentionandProprioceptiveD | Q14 robustness | real peg-in-hole, unseen shadow lighting: soft-argmax keypoints 92-95% vs AE latent 19-57% (trained room light only) | + spatial-softmax/keypoint bottleneck | M
W3_VisualSpatialAttentionandProprioceptiveD | Q09 auxiliary | end-to-end next-image prediction via keypoints 93.9 vs pretrained-frozen 92.5 | ~ small gain | L
W3_VisualSpatialAttentionandProprioceptiveD | Q03 vision encoder | autoencoder-reconstruction global latent collapses under lighting (avg 56%) | - reconstruction-pretrained global features | L
W3_ChainVLAChainingVisionLanguageActionQuer | Q10 smoothness | RMBench: full 62.8 vs w/o motion tail 11.2; seam position discontinuity 7.51->3.26 mm; TE and linear blend 0% on Put Back (full 96) | + condition/initialize next chunk on previous unexecuted suffix; - post-hoc blending | M
W3_ChainVLAChainingVisionLanguageActionQuer | Q06 chunking/TE | FIFO history + temporal ensembling 35.6 vs 62.8; TE 0/0% on two tasks | - temporal ensembling as fix | M
W3_ChainVLAChainingVisionLanguageActionQuer | Q07 history | w/o progress context 3.0; event readout removal Put Back 96->25 (memory-dependent sim tasks) | + recurrent/event memory for aliased tasks only | M
W3_WhenShouldWePreferOfflineReinforcementLe | Q13 data | sim image manip: CQL on noisy-expert 86-92% vs BC on expert 15-33% (weak single-step BC) | ~ perturbed/recovery data valuable with reward weighting | L
W3_BlindfoldedExpertsGeneralizeBetterInsigh | Q13 data | real peg insertion, 400 demos/shape: unseen shapes plus/ellipse 20/17% (standard expert) -> 100/96% (SAM2-masked operator view) and 96/79% (moderate pixel noise) | + exploratory/corrective demos over clean shortest-path demos | M
W3_BlindfoldedExpertsGeneralizeBetterInsigh | Q07 history | GRU memory policy used to clone non-Markovian exploratory demos (not ablated) | + history when demos contain search | L
W3_ContrastiveActionImagePretrainingforVisu | Q03 vision encoder | frozen-encoder real avg: CAIP 76.0 vs SigLIP2 43.4, SigLIP 42.4, DINOv2 42.0, MVP 42.0, R3M 17.4 (6 tasks x12) | + action-aligned pretraining; ~ generic frozen encoders task-dependent | M
W3_ContrastiveActionImagePretrainingforVisu | Q14 robustness | trained clean: CAIP 81.3 -> 51.4 shadows / 43.1 dark / 52.8 distractors; MVP 52.1 -> 5.6 / 17.4 / 9.7 | - relying on frozen pretrained features for lighting robustness | M
W3_ContrastiveActionImagePretrainingforVisu | Q12 model size | frozen CAIP encoder ViT-B 47.9 / ViT-L 81.3 / SO400M 87.5 (3 tasks) | ~ bigger frozen encoder helps | L
W3_BenchmarkingActionSpacesinReinforcementL | Q02 action space | real Franka pick (12 trials): joint vel 100, joint pos-inc 100, EE pose-inc 41.7, EE vel 0; push dist 0.405/0.104/0.050/0.000 m | + joint space; - Cartesian IK-based | M
W3_BenchmarkingActionSpacesinReinforcementL | Q02 action space | jerk m/s^3 pick: joint vel 16.0 vs joint pos-inc 52.6 | ~ velocity/integrated commands smoother (RL policy) | L
W3_XDistillCrossArchitectureVisionDistillat | Q03 vision encoder | real xArm 20-25 demos DP: DINOv2-distilled ResNet18 75.6 vs scratch ResNet18 41.9 vs fine-tuned DINOv2 ViT-S 31.4; sim 34 tasks 87.2 vs 64.1 vs 66.2 | + pretrained-prior CNN fine-tuned e2e; - fine-tuned ViT at few demos | M
W3_XDistillCrossArchitectureVisionDistillat | Q12 model size | MW: ResNet18 90.7 vs ViT-S-Half(11M) 57.2 vs ConvNeXt 89M 86.6; real pi0 SFT 26.7 vs 75.6 | + small CNN encoder in low data | M
W3_XDistillCrossArchitectureVisionDistillat | Q14 robustness | unseen cube colours 70 (X-Distill) / 50 scratch / 20 DINOv2 / 0 pi0 (10 trials) | + pretrained-prior CNN for object appearance shift | L
W3_DFMVLAIterativeActionRefinementforRobotM | Q01 action head | real 6 tasks x40: pi0-FAST(AR tokens) 47.5, Dream-VLA(discrete diffusion) 57.1, pi0.5(cont. flow) 70.8, DFM 73.3; CALVIN 10% data AR 1.71 / DD 2.84 / DFM 3.21 | - AR/masked discrete tokens; + continuous flow or refinable decoding | M
W3_DFMVLAIterativeActionRefinementforRobotM | Q14 robustness | LIBERO-Plus camera shift hardest: pi0 13.8, OFT 56.4, pi0.5 70.3, DFM 75.0 vs light 85-97 | - camera viewpoint shift is the weakest axis | M
W3_DecouplingtheDeclarativefromtheProcedura | Q08 language | real SO-101, 16 demos/pair: skill transfer w2VLA 91.7 vs OTTER 30.6 vs pi0.5 38.2 (seen ~94-96 all) | + FiLM with frozen CLIP localization heatmap (where) then skill (what) | M
W3_DecouplingtheDeclarativefromtheProcedura | Q12 model size | SO-101 in-domain: 55M-trainable w2VLA 95.1 vs pi0.5 (693M trainable) 95.8 | + small head over frozen encoders | M
W3_DecouplingtheDeclarativefromtheProcedura | Q05 augmentation | 50% VFM patch masking: skill transfer 58.3 -> 94.4 (seen 100 both) | + token/patch dropout vs spurious correlations | L
W3_DecouplingtheDeclarativefromtheProcedura | Q03 encoder | frozen MetaCLIP2 ViT-L + frozen VFM, 55M trainable works at 16 demos/pair on SO-101 | + frozen pretrained encoders in low data | M
W3_DecouplingtheDeclarativefromtheProcedura | Q14 robustness | +3-5 distractors: -16.6/-13.9 pts; unseen objects -8.3 pts score | + language-grounded localization prior | L
W3_DSWAMADualSystemWorldActionFoundationMod | Q10 latency/async | real folding easy: sync TRT pants 70% -> async TRT+RTC 100%, time 1'50''->1'08''; TensorRT BF16 198->74 ms (5090) | + async+RTC, + TensorRT/compile | M
W3_DSWAMADualSystemWorldActionFoundationMod | Q09 aux objectives | video-co-trained WAM 96.3% vs matched VLA 92.5% real folding (backbone differs, no loss ablation) | ~ world-model co-training | L
W3_DSWAMADualSystemWorldActionFoundationMod | Q08 language | subtask-level instructions: 75.7% -> 100% SR, mistakes 3.53 -> 0.65 per rollout (sorting) | + decompose multi-step language into subtasks | L
W3_DenoisingTellsWhentoReplanDenoisingVaria | Q06 chunking | real 50 demos/task, 30 trials: execute 40 vs 15 steps: 0.53 vs 0.80, 0.43 vs 0.70, 0.23 vs 0.43 | - long fixed open-loop execution | M
W3_DenoisingTellsWhentoReplanDenoisingVaria | Q10 latency | denoising-variance adaptive execution: real SR +6-10 pts over Fix15 with ~50% fewer replans; LIBERO 0.948->0.980, replans 32.6->18.6 | + adaptive execution horizon (flow heads) | M
W3_DenoisingTellsWhentoReplanDenoisingVaria | Q01 action head | flow denoising variance flags contact phases (r<-0.27 with exec length) | + generative head enables uncertainty-aware replanning | L
W3_BeyondViewpointGeneralizationWhatMultiVi | Q05 augmentation | real Franka DP 30 demos: monocular 25/10/5% vs depth-aligned reprojection (EX-4D+DA) 50/40/35 vs RoboNVS +-20deg synthetic views 70/60/55; budget-matched 2D augs (crop/blur/persp.) ~4-10 vs 12.5 baseline vs view-aug 25.5 (sim) | + synthetic novel-view aug from RGB-D; ~ 2D augs (when replacing real data) | M
W3_BeyondViewpointGeneralizationWhatMultiVi | Q11 cameras | sim DP eval at fixed 0deg: +-10/20/30/60 extra views 29.0/58.0/42.5/19.5 vs 12.5; budget-matched +-20: 33.5; pi0 34.0->42.0 | + multi-viewpoint training data (moderate +-20deg) even for single-cam deployment | M
W3_BeyondViewpointGeneralizationWhatMultiVi | Q14 robustness | multi-view gains larger in random-texture mode; Grad-CAM single-view attends to background | + viewpoint diversity reduces background shortcuts | L
W3_BeyondViewpointGeneralizationWhatMultiVi | Q13 data | 10->640 demos: single-view plateaus, multi-view keeps rising (figure only) | + view diversity over more same-view demos | L
W3_FasterVisuomotorPolicyLearningonActionMa | Q01 action head | 1 NFE: DP 0.0 (Tool Hang, Transport) vs flow matching 60/94 vs MeanFlow 64/90+; ceilings equal at 10 NFE | + flow matching / MeanFlow for few-step; - DDPM-eps diffusion at low steps | M
W3_FasterVisuomotorPolicyLearningonActionMa | Q10 latency | MeanFlow 2 NFE Tool Hang 76.0 (best in table) vs DP 74.0 at 10 NFE | + 1-2 step generative heads | M
W3_BeingH05ScalingHumanCentricRobotLearning | Q10 latency/async | RTC-style prefix lock (d>=ceil(t_inf/t_ctrl)+margin) + ring buffer on 5 robots incl SO-101; removing UAC+MPG degrades esp. long-horizon (figure only) | + prefix-conditioned async chunking | M
W3_BeingH05ScalingHumanCentricRobotLearning | Q03 vision encoder | LIBERO 5-shot, frozen Und+ViT: manipulation-pretrained 77.1 vs generic VLM 51.3; full FT 85.1 vs 84.1 | ~ frozen only if robot-pretrained; FT closes gap | M
W3_BeingH05ScalingHumanCentricRobotLearning | Q01 action head | freezing >14 of 28 action-expert layers -> sharp drop, fully frozen <20% | + train action head fully | L
W3_GeometricActionModelforRobotPolicyLearni | Q03 vision encoder | DA3 geometric backbone: LIBERO-Plus camera 83.1 vs best baseline 73.4, OFT 56.4; total 85.5 vs pi0.5 84.6 | + geometric foundation encoder for viewpoint robustness | M
W3_GeometricActionModelforRobotPolicyLearni | Q09 auxiliary | no pretrain: Plus 50.0 -> 73.4 with future depth+feature loss (depth only 80.0); with pretrain ~no effect | + future depth/latent aux loss in low-pretraining regime | M
W3_GeometricActionModelforRobotPolicyLearni | Q07 history | obs history H=1 89.7 vs H=2 84.4, H=4 85.1 (LIBERO-Plus Object) | - multi-frame history | M
W3_GeometricActionModelforRobotPolicyLearni | Q14 robustness | real: external cam moved 85 cm/45 deg, GAM >> pi0.5, Spatial Forcing (figure only); aug crop 90% + rot 5 deg + color jitter | + geometry prior + aug for camera shift | L
W3_GeometricActionModelforRobotPolicyLearni | Q10 latency | 1.4B single-pass L1 head 6.9 ms (17.5 w/o CUDA graphs) vs pi0.5 29.2, OFT 70-78, Cosmos 382 ms | + single-pass heads for latency | M
W3_GeoVLAEmpowering3DRepresentationsinVisio | Q04 3D/depth | real WidowX+D435i: 86.3 vs CogACT 76.3; basket height H1 60 vs 20; EE-frame point token; DP3-MLP encoder 95.8 vs PEN 97.7 LIBERO | + depth branch in robot/EE frame | M
W3_GeoVLAEmpowering3DRepresentationsinVisio | Q11 cameras | camera rotated 15/30/45 deg: GeoVLA 90/80/70 vs CogACT 60/40/0, pi0 50/40/30 | + 3D input for viewpoint robustness | M
W3_GeoVLAEmpowering3DRepresentationsinVisio | Q14 robustness | GeoVLA no-aug: base 93.3 -> background 80.0 -> lighting 73.3 (3 tasks x10) | - depth alone for lighting robustness | L
W3_DeepSE3EquivariantGeometricReasoningforP | Q04 3D/depth | RLBench keyframe placement 10 demos: rot error 0.6-1.2 deg vs TAX-Pose 1.2-5.5 deg (segmented point clouds, planner execution) | ~ equivariant 3D helps precise placement, not closed-loop | L
W3_ImaginingtheSenseofTouchTouchInformedMan | Q09 aux | real 15 trials: vision DP 26.7/20.0/6.7 -> +imagined force field 86.7/60.0/40.0 (bulb/wipe/belt); mismatched TacRGB can hurt (wipe 6.7) | + task-matched structured intermediates | L
W3_GazeRegularizedVisionLanguageActionModel | Q09 auxiliary | KL attention-to-gaze prior: LIBERO-Spatial 85.9->95.5 (pi0), OpenVLA avg 68.5->74.2; real 32->44, 64->72, 30->40% at 40k steps; lambda=10 -> 41.6% | ~ weak attention prior helps, fragile to lambda | L
W3_GazeRegularizedVisionLanguageActionModel | Q14 robustness | sim lighting perturbation Spatial 77.2 -> 89.1; noise 82.1 -> 91.3 | + focus on task-relevant regions | L
W3_CRAFTVideoDiffusionforBimanualRobotDataG | Q05 augmentation | real ACT unseen lighting: none 3/1/0, color jitter 13/9/8, video-diffusion relight 17/14/12 (/20); object color: none 2/0/1, SAM recolor 15/9/11, CRAFT 18/18/17 | + photometric jitter baseline; + generative aug | H
W3_CRAFTVideoDiffusionforBimanualRobotDataG | Q14 robustness | ACT 50-100 clean demos: 0-6/20 under unseen lighting/background/color/camera | - clean-only training | H
W3_CRAFTVideoDiffusionforBimanualRobotDataG | Q11 cameras | 4 new camera views: no aug 6/3/2 vs NVS 14/8/6 vs multi-view generated 19/18/18 (/20) | + viewpoint augmentation for camera shift | M
W3_CRAFTVideoDiffusionforBimanualRobotDataG | Q13 data | pose-only diversity (2x demos) camera-shift 6->13, lighting 3->5 (/20) | ~ spatial diversity helps a bit, not visual robustness | L
W3_FrequencyGuidedActionDiffusionviaSubFreq | Q01 action head | sim DP3 vs FGO avg 52.9->56.6 (Robosuite/MimicGen), 55.9->60.3 (Adroit/DexArt), 3 seeds | ~ frequency-guided diffusion small gain | L
W3_FrequencyGuidedActionDiffusionviaSubFreq | Q10 smoothness | Can approach JerkRMS 50.87->40.79, ATV 14.83->14.76; inference 39.5->44.2 ms | + low-pass/spectral smoothing within chunk (not boundaries) | L
W3_FrequencyGuidedActionDiffusionviaSubFreq | Q13 data quality | human-demo jitter inherited by DP; filtering high freqs improves SR & jerk (sim) | + smooth/filter teleop actions | L
W3_ManiFlowAGeneralRobotManipulationPolicyv | Q01 action head | consistency flow: 1 step 63.7 / 2 steps 64.5 vs DP3 10-step 42.7, 3D flow 10-step 48.1 (RoboTwin); 2D avg 56.5 vs DP 39.4 | + flow+consistency, 1-2 NFE | M
W3_ManiFlowAGeneralRobotManipulationPolicyv | Q04 3D/depth | clutter task @100 demos: xyz-only 57.3 vs +RGB 86.0; real point-cloud ManiFlow 71.0 vs DP3 37.6 | + colored point cloud | M
W3_ManiFlowAGeneralRobotManipulationPolicyv | Q05 augmentation | color jitter on point RGB essential in real (lighting); SE(3) point aug detrimental (stated, no numbers) | + color jitter; - SE3 aug | L
W3_ManiFlowAGeneralRobotManipulationPolicyv | Q12 model size | RoboTwin2 DR 50 demos: scratch ManiFlow 64.7/55.5/55.0/66.7 vs fine-tuned pi0 24.3/18.0/41.0/70.0 | + small scratch flow policy at 50 demos | M
W3_ManiFlowAGeneralRobotManipulationPolicyv | Q13 data | Lift Pot: 50 demos 64.7, 100 ~90, 200 97.7 (pi0 94.0 needs 500) | ~ 100-200 demos saturate single task | M
W3_ManiFlowAGeneralRobotManipulationPolicyv | Q14 robustness | real unseen objects 67.4% vs DP3 31.1% | + expressive head/arch helps novel objects | M
W3_MitigatingtheHumanRobotDomainDiscrepancy | Q03 encoder | frozen R3M Adroit 74.0 -> adapter-aligned 81.3 (full FT 77.7); RLBench D4R 55.3 -> 59.9; real +11-13% (fig) | - frozen human-video encoders as-is; + light last-layer adapter with robot-domain data | L
W3_IsForwardPredictionEnoughPhysicalStateGr | Q09 auxiliary | real 100 demos/task, 50 trials: proprio + multi-horizon dq grounding heads 79.3% vs forward-only JEPA 60.0%; LIBERO-Goal 85.3 vs 77.7 (inverse dynamics aux 82.6) | + state/transition (proprio, dq, IDM) aux heads | M
W3_IsForwardPredictionEnoughPhysicalStateGr | Q03 encoder | frozen DINOv2 probes: EE-yaw r 0.50, gripper vel 0.20 vs grounded 0.98/0.69; fine-tuned DINOv2 80.1 vs 85.3 LIBERO-Goal | - frozen generic encoder w/o state grounding | L
W3_EquiVLAAGeneralFrameworkforRotationallyE | Q02 action space | LIBERO relative vs absolute EE: GR00T 78.1 vs 62.6; EquiVLA 92.6 vs 76.1 | + relative/delta EE | M
W3_EquiVLAAGeneralFrameworkforRotationallyE | Q14 robustness | real ALOHA orientation-varied tasks: House 3->10, Letter 13->19 (/20) with SO(2) equivariance; avg 54->72% | + rotational priors for orientation variation | L
W3_EquiVLAAGeneralFrameworkforRotationallyE | Q10 latency | C8 frame averaging: 64 -> 194 ms/step on H100 | - test-time symmetrization on laptop | M
W3_ImitationLearningPolicybasedonMultiStepC | Q01 action head | RoboTwin 1-NFE multi-step-consistency flow 44.27 vs 3DP 10-NFE 41.39; real (10 trials) 50/40/50 vs DP 40/30/40 vs Shortcut 10/10/20 | + one-step flow head (careful training); - naive Shortcut | L
W3_ImitationLearningPolicybasedonMultiStepC | Q10 latency | same model 1/3/5/10 inference steps: 59.7/59.9/61.4/60.9 avg SR | + few-step sampling costs ~nothing | L
W3_RLDGRoboticGeneralistPolicyDistillationv | Q13 data quality | OpenVLA VGA insertion 100% with 45 RL eps vs 300 human; human plateaus 90% at 900 demos on unseen; relabeling human states with RL actions recovers most gap | + action consistency/quality over quantity; trim hesitation | M
W3_RLDGRoboticGeneralistPolicyDistillationv | Q10 latency | OpenVLA at 4 Hz slower cycle times than 10 Hz RL policy (0.3-2.3 s per task) | ~ control rate matters for speed | L
W3_PRISMPerformerRSIMLEforSinglepassMultise | Q01 action head | MetaWorld Hard: IMLE-1NFE PRISM 58.0 vs DP(10 NFE) 9.0, Flow(1 NFE) 13.4, DP3 38.0; CALVIN10%: 65.2 vs DP 36.4, Flow 44.4 | + single-pass multimodal head (RS-IMLE) | M
W3_PRISMPerformerRSIMLEforSinglepassMultise | Q10 latency/smoothness | A100: 15 ms vs DP 142 ms, Flow 74 ms; jerk 0.052 vs 1.05-3.78; mode switch 0.10 vs 0.28-0.59 | + 1-pass head + pick candidate closest to last action | M
W3_PRISMPerformerRSIMLEforSinglepassMultise | Q11 cameras | CALVIN eval dropout: full 65.2, no wrist RGB 41.5, no proprio 15.8, no depth 66.2 | + wrist cam + proprio essential | M
W3_PRISMPerformerRSIMLEforSinglepassMultise | Q04 depth | dropping depth: 66.2 vs 65.2 full (no loss) | - depth input when wrist RGB present | L
W3_MimicIntentNotJustTrajectories | Q01 action head | multi-scale spectral VQ tokens: LIBERO-Long 93.4 vs time-domain scale-wise 82.8; MINT-30M LIBERO 97.1 vs DP 72.4 | + coarse-to-fine learned action tokens | L
W3_MimicIntentNotJustTrajectories | Q06 chunking | chunk 8/16/32/64 -> LIBERO-Long 80.6/93.2/86.6/87.4; ensemble none 85.8, TE 89.2, intent-weighted 93.2 | + mid chunk (~16 steps) + similarity-weighted ensembling | M
W3_MimicIntentNotJustTrajectories | Q12 model size | 30M scratch policy (frozen SigLIP+DINOv2): LIBERO 97.1 vs SmolVLA 88.8; LIBERO-Plus 69.5 vs pi0.5 65.0 | + small policy on frozen strong encoders | M
W3_MimicIntentNotJustTrajectories | Q03 vision encoder | frozen SigLIP+DINOv2 concat: LIBERO-Plus light 92.2, background 77.1, camera 61.4 | + frozen foundation features for photometric robustness | L
W3_MimicIntentNotJustTrajectories | Q13 data | learning curve: MINT-30M 0.95 vs ACT 0.65 at 10k iters | ~ sample-efficient head | L
W3_HiFlowTokenizationFreeScaleWiseAutoregre | Q01 action head | real HSR 50 demos @10Hz, 12 trials: Orange->Plate ACT 8.3 / DP 16.7 / VQ-AR 25.0 / flow-AR 41.7; Mustard 33.3/58.3/58.3/83.3 | + continuous flow head; - ACT, - VQ tokens | M
W3_HiFlowTokenizationFreeScaleWiseAutoregre | Q13 data | 50 demos placement tasks best method 42-58% real | ~ 50 demos marginal for precise placement | L
W3_PALMProgressAwarePolicyLearningviaAfford | Q09 auxiliary | CALVIN avg len 4.48; w/o affordance foresight 3.58, w/o IDM 3.92, w/o progress 4.02 (finetune stage) | + affordance/IDM/progress aux heads | L
W3_PALMProgressAwarePolicyLearningviaAfford | Q14 robustness | real 200 demos, 6-step task: avg len PALM 3.05/3.80 vs OpenVLA 0.95/1.60 (random pose / distractors) | ~ (weak baselines) | L
W3_MMACTLearnfromMultimodalParallelGenerati | Q09 aux objectives | RoboTwin unseen 8 tasks: action-only 43.13, +text 46.5, +future image 48.75, +both 52.38 | + future-image/plan co-training (big model) | L
W3_MMACTLearnfromMultimodalParallelGenerati | Q10 latency | cs=8 one-step 43.13 @0.22s vs 6-step re-mask 42.38 @1.06s; cs=16 43.75 vs 56.75 | ~ iterative decoding only pays for long chunks | L
W3_SoftVTBenchADeformationAwareVisuoTactile | Q14 robustness | sim pooled OOD (illum/mass/stiffness) vision-only TSR drop: DP -8.2/-4.6, pi0.5 -5.8/-1.6; DP degrades strongly at illumination extremes (fig) | ~ lighting shift hurts DP; large pretrained slightly more robust | L
W3_ROPASyntheticRobotPoseGenerationforRGBDB | Q05 augmentation | ACT RGB 5 sim tasks: ROPA pose-aug 68.0/30.7/62.7/24.3/30.7 vs ACT 41.3/10.7/43.3/21.3/17.3 vs VISTA novel-view 52.7/1.6/54.3/10.3/15.7; real 30 demos Lift Drawer 4->10/20 | + action-labelled corrective state aug; - novel-view-only aug | M
W3_ROPASyntheticRobotPoseGenerationforRGBDB | Q04 depth | ACT RGB->RGB-D single D415: CLB 41.3->56.7, CPB 43.3->49.7, BSR 21.3->26.7; real 13->15, 4->5, 14->17 /20 | + depth channel on scene cam | M
W3_ROPASyntheticRobotPoseGenerationforRGBDB | Q13 data | +100 extra demos did not reliably help ACT (RGB-D CLB 56.7->33.3; RGB CPID 17.3->10.3) | - more nominal demos; + recovery states | L
W3_ROPASyntheticRobotPoseGenerationforRGBDB | Q11 cameras | ACT CLB 1 cam 41.3 vs 4 tiled cams 72.0 | + multi-view | L
W3_RoboticTableTennisACaseStudyintoaHighSpe | Q10 latency | sim latency = measured -> 1.83/2.0 real; 50% -> 1.33; 0/20/150% very poor; real perf flat until ~150 ms added latency / 50 FPS then collapses | + measure & match deploy latency; interpolate obs | M
W3_RoboticTableTennisACaseStudyintoaHighSpe | Q14 robustness | 4 cm systematic obs bias -> -36% reward vs +-8 cm zero-mean noise minor | + guard against systematic (camera/extrinsic) shift | L
W3_RoboticTableTennisACaseStudyintoaHighSpe | Q02 action space | task-space position actions train faster, survive frozen joints, morphology fix by residual; joint-velocity cannot | ~ (RL, industrial arm) | L
W3_RealtimeVLAFLASHSpeculativeInferenceFram | Q10 latency | pi0 4090D 58 ms/round (enc 11, prefill 27, denoise 20); Triton 39.7 ms same SR; FLASH 19.1 ms SR 93.8 vs 94.1; conveyor 13 m/min: 0% (JAX) vs 50% (FLASH) | + optimize inference latency; ~2 s SmolVLA latency is anomalous | M
W3_RealtimeVLAFLASHSpeculativeInferenceFram | Q06 chunking | draft-only (stale context) LIBERO-10 58.4 vs 85.2 full; periodic refresh PF=2 restores 80.6 | - long open-loop/stale execution; + frequent refresh | L
W3_RealtimeVLAFLASHSpeculativeInferenceFram | Q12 model size | 110M regression draft w/ stale KV 58.4% vs 2.7B pi0 85.2% (LIBERO-10) | ~ tiny regression head weaker on long horizon | L
W3_mimicvideoVideoActionModelsforGeneraliza | Q11 cameras | real bimanual: DINO ViT-S DiT policy workspace-only 11.0/30.0 vs +wrist cams 42.6/74.1 | + wrist camera | M
W3_mimicvideoVideoActionModelsforGeneraliza | Q09 auxiliary | video-model features vs VLM features, same decoder/data: LIBERO 93.9 vs 85.9; SIMPLER 46.9 vs 35.4; intermediate-noise video latents best | + dynamics-aware features; ~ full reconstruction unnecessary | M
W3_mimicvideoVideoActionModelsforGeneraliza | Q03 vision encoder | video-pretrained (Cosmos 2B) > PaliGemma 3B VLM features, 10x sample efficiency (LIBERO) | + video/dynamics pretraining (large scale) | M
W3_RoboGSimAReal2Sim2RealRoboticGaussianSpl | Q05 augmentation | UR5 ring toss 10 trials, place TV/NV/NS: real 90/0/20, real+2D aug 80/0/60, GS-synthetic 90/0/90; Isaac-sim data -> real place 0 | + 3D-consistent scene synthesis over 2D aug; - raw sim textures | L
W3_RoboGSimAReal2Sim2RealRoboticGaussianSpl | Q14 robustness | novel camera view: place 0% for real, 2D-aug and GS-synthetic data | - none solved camera shift here | L
W3_TacSushiTactileGroundedWorldActionModeli | Q09 auxiliary | training-only future RGB/progress/contact decoder (removed at deploy): ID 36.7->68.3, OOD ingredients 10.0->37.5 (gated); 15.0->25.0 / 5.0->17.5 (concat); 20 trials/cell | + training-only future-consequence aux loss | M
W3_TacSushiTactileGroundedWorldActionModeli | Q13 data quality | 50 failed trials used for consequence targets with imitation masked (not isolated) | + reuse failures for aux targets, mask their actions | L
W3_TacSushiTactileGroundedWorldActionModeli | Q14 robustness | held-out ingredients OOD 37.5% full vs 10.0% without aux; GR00T+tactile 15.0 | + aux supervision aids novel-object transfer | L
W3_SutureBotAPrecisionFrameworkBenchmarkFor | Q12 model size | real dVRK, 10 trials: multitask ACT pickup/throw/knot 9/8/9, E2E 3/10 vs pi0 7/7/4, 0/10; GR00T 1/2/1; OpenVLA-OFT 0/0/0 | + small from-scratch ACT in out-of-domain low-data | M
W3_SutureBotAPrecisionFrameworkBenchmarkFor | Q14 robustness | new lighting: ACT pickup 9->3/10, pi0 7->0/10; swapped tools ACT 9->1/10 | - relying on VLA pretraining for lighting robustness; + diverse data/aug | M
W3_SutureBotAPrecisionFrameworkBenchmarkFor | Q08 conditioning | point-label goal overlay: ACT insertion error 1.3 mm vs 3.2 no goal; pi0 1.0 vs 3.9 | + image-space goal marks for placement precision | L
W3_ReconcilingRealitythroughSimulationAReal | Q13 data | real book-on-shelf: BC 15 demos 10/0/0%, BC 50 demos 40/30/20%, RialTo(15 demos+sim RL) 90/70/60% (pose/distractor/disturbance) | + diversity & recovery coverage over count | M
W3_ReconcilingRealitythroughSimulationAReal | Q14 robustness | BC avg 25% pose -> 11% distractors -> 5% disturbances; distractor training mug 30->70% | + train with distractors | M
W3_ReconcilingRealitythroughSimulationAReal | Q05 augmentation | digital-twin sim RL data + real co-training: avg 91/77/75% vs BC 25/11/5% | + synthetic sim demos (heavy engineering) | M
W3_ReconcilingRealitythroughSimulationAReal | Q04 3D | single depth-cam point-cloud BC still 11% with distractors | ~ 3D alone not robust to distractors | L
W3_VLACacheEfficientVisionLanguageActionMan | Q10 latency | 7B VLA KV token reuse: 1.63-1.7x latency, -27% FLOPs, -0.3 pt LIBERO; naive reuse 84.4->74.2% | - relying on VLA inference tricks (too small a gain) | L
W3_SeeSelectivelyActAdaptivelyDualLevelStru | Q14 robustness | RoboTwin 50 demos Easy->Hard: ACT 35.3->0.2, DP 24.3->0.0, pi0.5 61.5->22.3, +view router/MoE 81.2->58.0 | - small scratch policy w/o visual diversity; + pretrained backbone | M
W3_SeeSelectivelyActAdaptivelyDualLevelStru | Q11 cameras | per-phase wrist-view gating: Hard 22.3->40.7 (alone); real Hard w/ distractors 10-20% -> 40-60% (full model) | + view gating / view dropout vs distractors | M
W3_SeeSelectivelyActAdaptivelyDualLevelStru | Q12 model size | LoRA 2x capacity 41.3 vs 41.9 baseline (no gain) | ~ capacity not bottleneck | L
W3_VisualPolicyLearningThroughMultiCameraVi | Q11 cameras | sim cube random-view SR: front-only 2.0, front+wrist 23.3, front+side+wrist 68.7; mug front-only unlearnable (0) vs 2cam 99.3 fixed | + wrist cam and extra views | M
W3_VisualPolicyLearningThroughMultiCameraVi | Q14 robustness | fixed-view policy 96.5 -> 2.0 under random camera pose; distilled single-cam student w/ view randomization 96.0 sim, real 50-80% (20 trials/view) vs 20-60% | + viewpoint randomization with multi-view supervision | M
W3_VisualPolicyLearningThroughMultiCameraVi | Q05 augmentation | camera randomization without KD teacher -> 0% success (RL) | ~ extreme view randomization needs a stabilizing signal | L
W3_VideoGeneratorsareRobotPolicies | Q09 aux | RoboCasa: video horizon 32 steps 0.67 vs 16 0.55 vs 0 (reconstruction) 0.30; no in-domain video FT 0.09 | + future prediction; - current-frame reconstruction | M
W3_VideoGeneratorsareRobotPolicies | Q10 latency | ~9 s per chunk on A100 (SVD, 30 steps) | - video-generation policies for real-time | H
W3_VideoGeneratorsareRobotPolicies | Q14 robustness | real unseen background: M&Ms-to-cup 0.8 -> 0.2 (10 rollouts); pick-place 1.0 -> 0.8 | - relying on priors for precise tasks under bg change | L
W3_VolumeDPModelingVolumetricRepresentation | Q14 robustness | real 100 demos: camera rotated +-5 deg DP 0% vs VolumeDP 40%; env/background 20->45; layout 35->65; LIBERO-Plus camera 1.6->23.1, light 25.0->56.5 | + 3D lifting; - plain 2D DP under camera shift | M
W3_VolumeDPModelingVolumetricRepresentation | Q04 3D/depth | RGB-only volume 90.7 vs 2D tokens 78.2 vs GT-depth occupancy selection 75.8 (LIBERO-Spatial) | + calibrated 3D lifting even without depth | M
W3_VolumeDPModelingVolumetricRepresentation | Q09 auxiliary | proprio-derived EE/gripper-change attention supervision 82.2 -> 90.7 | + cheap attention supervision | L
W3_VolumeDPModelingVolumetricRepresentation | Q11 cameras | 2D DP collapses 65/60% ID -> 0% under +-5 deg camera rotation | - relying on fixed scene cam with 2D features | M
W3_SharedExecutionClockDriftingPolicyforDyn | Q01 action head | real, Thor: DP 16-NFE 252 ms cup place 98%; distilled OneDP 1-NFE 71%; native 1-step drifting+clock 95% at 25 ms | + natively-trained few/one-step head; - post-hoc distillation | M
W3_SharedExecutionClockDriftingPolicyforDyn | Q10 latency | conveyor 16 m/min: DP (252 ms) 0% vs 1-NFE policies 31-91% | + minimize inference latency / async | M
W3_SharedExecutionClockDriftingPolicyforDyn | Q06 chunking | H=16 execute 8 @20Hz (0.4 s) across 4 real tasks, 300 trials | ~ half-chunk execution works | L
W3_TowardsAccessiblePhysicalAILoRABasedFine | Q13 data | SO-101 button press VLA LoRA: 20 eps 18%, 50 eps 45-52%, 100 eps 68-72%, 200 eps 74-76% (no trial counts; dubious model description) | + plan 100+ demos for VLA fine-tune | L
W3_TowardsAccessiblePhysicalAILoRABasedFine | Q10 latency | 4-bit LoRA VLA on RTX 4060 8GB: 45 ms total, 20 Hz, 6.8 GB peak | + 2 s latency on 5060 likely config issue | L
W3_TowardsAccessiblePhysicalAILoRABasedFine | Q03 vision encoder | frozen 74% vs LoRA-unfrozen 76% (200 eps); vision-influence 4.5 vs 6.2 | ~ freezing costs little at 200 demos | L
W3_TowardsAccessiblePhysicalAILoRABasedFine | Q07 copycat | 20 eps: zeroing images barely changes actions (0.8) -> proprio shortcut, oscillation near target | + test image-ablation sensitivity | L
W3_TSMaskVLA2DTemporalSpatialMaskingforVisi | Q01 action head | masked discrete diffusion 0.5B: LIBERO 95.7, CALVIN 4.19; 2D vs 1D mask Long 91.6 vs 85.0 | ~ discrete masked diffusion viable (sim) | L
W3_TSMaskVLA2DTemporalSpatialMaskingforVisi | Q12 model size | 0.5B beats 7B OpenVLA-OFT on CALVIN (4.19 vs 4.10) | + small backbone | L
W3_WorldtoWristTaskConditionedFutureWristMo | Q09 aux objectives | future wrist-latent prediction: LIBERO 97.5->98.5 (Long 93.6->95.2); wrist target 98.5 > main-view 97.7 > both 98.0 | + predict future wrist features as aux loss | L
W3_WorldtoWristTaskConditionedFutureWristMo | Q11 cameras | wrist-centric future modeling: real std 70.0 vs 54.4 (VLA-JEPA) vs 41.1 (pi0); OOD 52.2 vs 37.8 (30 trials/task) | + wrist cam as action-proximal signal | L
W3_WorldtoWristTaskConditionedFutureWristMo | Q10 latency | explicit CoT decoding 1550-1615 ms/chunk vs latent tokens 111 ms, same SR | - reasoning decoding at inference | M
W3_WorldtoWristTaskConditionedFutureWristMo | Q14 robustness | real OOD clutter/light/background: 70.0 -> 52.2 (best model, 100 demos/task) | ~ OOD still costly even for 5B VLA | L
W3_ZETAAControlledStudyofZeroShotCrossEmbod | Q02 action space | real (Franka, 50 demos/task): EEF-Delta state+EEF-Delta action 89.9 avg vs AbsEEF/World-Delta 56.0; on source robot 100 vs 87.5 | + gripper-frame relative actions and state | M
W3_ZETAAControlledStudyofZeroShotCrossEmbod | Q07 history/proprio | sim: AbsEEF state -> EEF-Delta state avg 64.6 -> 75.7 (ARM shift 39.9 -> 74.3) | ~ de-emphasize absolute proprio | L
W3_ZETAAControlledStudyofZeroShotCrossEmbod | Q09 auxiliary | sim co-training bbox 82.3 / subgoal 81.8 / EEF language-action 81.3 vs none 75.7 (gains under embodiment shift) | ~ small gains | L
