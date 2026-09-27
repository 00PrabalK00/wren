# Q01_action_head — 135 ledger lines
[fulltext] ACT | action_head | plain L1 chunk regression collapses on human demos (35.3%→2%, sim) | - regression, + generative/latent | M
[fulltext] DiffusionPolicy | action_head | diffusion beats GMM/IBC/BET, +46.9% | + generative | H
[fulltext] BAKU | action_head | sim: MLP>=multimodal; real: VQ-BeT 91% vs MLP 86% | ~ multimodal for real human data | M
[fulltext] OFT | action_head | L1≈diffusion only with 7B VLM on filtered LIBERO; authors credit capacity | ~ L1 only with big pretrained backbone | M/H
[fulltext] RTC | action_head | RTC requires flow/diffusion head | + flow | H
[fulltext] BeT | Q01 action_head | Kitchen (566 human demos) ≥2 tasks: MLP-MSE 0 vs BeT .93; CARLA MSE collapses to 1 mode (0/0.98 L/R) | - MSE regression on multimodal data | M
[fulltext] BeT | Q01 action_head | GPT-MDN (GMM head) rel. perf 0.30/0.83/0.86; no-offset 0.78 in 9-D Kitchen | - GMM head, - pure discretization, + bin+offset | L/M
[fulltext] robomimic | Q01 action head | no-GMM (deterministic) −58% rel on MH Transport low-dim; smaller gap for BC-RNN | + multimodal head for multi-operator data | M
[fulltext] VQ-BeT | Q01 action_head | real Stretch single-phase VQ-BeT 47/50 ≈ DP-T 45/50 >> MLP-BC 29/50; two-phase 19/30 vs 11/30 vs 7/30 | + VQ tokens / generative, - MLP regression | L/M
[fulltext] ImplicitBC | Q01 action_head | real xArm (95-502 human demos, 60 trials): EBM 85/88/83/48% vs MSE 35/55/7/20%; 1mm insertion 83 vs 7 | - single-step MSE regression | M/H
[fulltext] ImplicitBC | Q01 action_head | DFO inference fails beyond ~5-D actions; Langevin needs grad penalty; others (BeT, DP) find IBC unstable | - EBM head for 6-DoF chunks | M
[fulltext] ImplicitBC | Q01 action_head | sim pixels pushing: MDN 10% vs MSE 87% vs EBM 100% | - GMM/MDN head | L/M
[fulltext] RT-1 | Q01 action head | Gaussian continuous vs 256-bin discrete: seen 97→68, unseen 76→43 | + multimodal/discrete head | M/H
[fulltext] ConsistencyPolicy | Q01 action_head | real Franka 180 demos: CP-1 0.8/0.7/0.4 vs DDIM-15 0.8/0.6/0.5 (10-20 trials); sim ToolHang CP-3 .77 vs DDPM .79 | + few-step generative head | M
[fulltext] ConsistencyPolicy | Q01 action_head | CP/EDM lose multimodality (Push-T one side); CT w/o teacher Square .55 vs .92 | - distillation complexity; ~ multimodality | L/M
[fulltext] FlowPolicy | Q01 action_head | 37 sim tasks, 10 scripted demos: 1-step consistency-FM 70.0 vs DP3 10-step 68.7 vs SimpleDP3 67.4 | + 1-step flow (no distillation) | L/M
[fulltext] StreamingFlowPolicy | Q01 action_head | same velocity field trained w/o noise (regression) vs flow-matching: Can 12.4 vs 95.6, Push-T 72.1 vs 91.7 | - regression, + flow matching | M
[fulltext] StreamingFlowPolicy | Q01 action_head | SFP ≈ DP-100: Square 78.0 vs 77.2, Can 98.4 vs 94.0, Push-T img 83.9 vs 87.0; stabilization k=0 → Square 53.2 | + flow w/ stabilizing target | M
[fulltext] DiffusionTransformerPolicy | Q01 action_head | real Franka 50 demos/task, same backbone: discretized 256-bin 19.3% vs MLP diffusion head 34.8% vs DiT denoiser 46.9%; ManiSkill2 30.2/58.6/65.8 | - per-dim discrete tokens, + continuous diffusion w/ strong denoiser | M
[fulltext] SmolVLA | action_head | LIBERO flow 80.25 vs L1 75.25 (long 53 vs 38), frozen VLM | + flow | M
[fulltext] ReactVLA | action_head | mean flow + Pseudo-Huber; MSE unstable with JVP; AttnRes 88.0 vs 28.7 | + iMF head | L/M
[fulltext] TinyVLA | action_head | inside VLA: diffusion 94 vs ACT head ~13 vs MLP 0 | + diffusion (baseline integration suspect) | L/M
[fulltext] VLA-Adapter | action_head | L1 one-pass 95.0 vs DiT 91.6 (LIBERO-Long) | + L1 when conditioning rich (conflicts SmolVLA/FLOWER/ACT) | M
[fulltext] FLOWER | action_head | CALVIN-ABC len: flow 4.44 vs L1 3.33 vs discrete 1.12 | + flow | M
[fulltext] DataScalingLaws | evaluation | val action MSE unreliable (LoRA lower MSE but 0.72 vs 0.90 score) | - MSE for model selection | M
[fulltext] MobileALOHA | action head | ACT 95 vs DP 65 (co-trained, Wipe Wine, 50 demos) | + CVAE/light head in low data | L/M
[fulltext] ALOHA-Unleashed | action head | diffusion 70 vs L1 25 (ShirtMessy, 150M); authors: ACT easier in low data | + generative head; data-dependent | M
[fulltext] 3DDiffuserActor | Q01 action_head | Act3D (regression/classification, similar tokens) 65.3 vs diffusion 78.4 single-view | + diffusion | M
[fulltext] Hyper-DP3 | Q01 action_head | 2 DDIM steps ≈ 10 steps (58.2 vs 58.0); 1 step 53.0; DP3 also 59.3@2 vs 59.9@10 | + diffusion with 2 steps | M/H
[fulltext] RoboVLMs-WhatMatters | Q01 action_head | continuous 4.09 vs discrete bins 0.55 (KosMos); flow 3.68 ≈ MSE+BCE 3.57 (ABC→D) | + continuous; FM≈MSE | H
[fulltext] Dita | Q01 action_head | CALVIN scratch: in-context DiT 2.38 vs UNet1D head 1.80 vs MLP head 1.68 vs single-token chunk 0.84; ManiSkill2 discrete 30.2 vs diffusion 58.6/65.8 | + continuous diffusion, - discrete bins | M
[fulltext] Octo | Q01 action head | Octo-Small WidowX 40 trials: diffusion 83 vs MSE 35 (hedging, slow) vs discrete-256 18 (misses grasps) | + diffusion over MSE/discrete at small scale | M
[fulltext] OpenVLA | Q01 action head | 7B discrete-token works (Bridge 70.6) but DP from scratch smoother/more precise and competitive on narrow single-instruction fine-tunes | - discrete tokens for small single-task policy | M
[fulltext] RDT-1B | Q01 action head | diffusion vs regression (1.2B pretrained): unseen object 50 vs 12.5, instruction 100 vs 12.5 (8 trials) | + diffusion over regression | M
[fulltext] CogACT | Q01 action head | SIMPLER avg: DiT-B 89M 62.5 vs MLP-7L 89M 52.5; DiT-S 13M 58.5 > MLP 89M | + transformer diffusion head over MLP head | M
[fulltext] pi0 | Q01 action_head | 3.3B VLM + 300M flow expert (bidirectional over H=50, block-causal from obs, 10 Euler steps) beats OpenVLA/Octo/ACT/DP (figure only) | + flow with separate small action transformer | M
[fulltext] pi0.5 | Q01 action_head | FAST-token pretrain + flow post-train > pi0 flow-only even at 300k steps (figure) | ~ large-backbone only | L
[fulltext] FAST | Q01 action_head | naive per-step binning makes no progress at 20/50 Hz; FAST ≈ diffusion pi0 on small data (<50 h) | - naive discrete tokens; ~ FAST vs flow | H
[fulltext] KnowledgeInsulation | Q01 action_head | flow-only pi0 needs 7.5x steps; KI DROID 0.55 vs pi0 0.49 vs FAST 0.45; LIBERO-Long 85.8 < OFT 94.5 | + flow at inference + aux discrete objective | M (L at 10-50M)
[fulltext] GR00T-N1 | Q01 action_head | cross-attn flow DiT (H=16, K=4) vs DP @100 demos sim avg 45.0 vs 33.4; real full 76.8 vs 46.4 | + flow DiT, cross-attn to vision tokens | M
[wave3] W3_AffordDPGeneralizableDiffusionPolicywith | Q01 | affordance guidance in diffusion sampling: unseen cat 22.2->26.7% (sim) | ~ guided diffusion small gain | L
[wave3] W3_ActionMapRobotPolicyLearningviaVoxelActi | Q01 action head | real Franka 50 demos: heatmap 14/30 vs L1 4/30; LIBERO 10% data 93.2 vs 67.2; grasp error 15.0 vs 35.5 mm | - L1 regression / + distributional head | M
[wave3] W3_ActionMapRobotPolicyLearningviaVoxelActi | Q01 action head | vs pi0.5 flow: 98.5 vs 96.9 LIBERO avg | ~ heatmap vs flow | L
[wave3] W3_ActionQuantizedOfflineReinforcementLearn | Q01 action head | Robomimic PH avg: unimodal BC 22.5, VQ-discrete SAQ-BC 41.7, tuned GMM BC 64.1 (state-based sim) | - unimodal regression; ~ VQ | L
[wave3] W3_BehaviorRetrievalFewShotImitationLearnin | Q01 | ResNet18+LSTM+5-mode GMM trained end-to-end; no head ablation | ~ | L
[wave3] W3_IMLEPolicyFastandSampleEfficientVisuomot | Q01 action head | Push-T 20 demos IMLE 0.10 vs DP 0.03 vs FM-1step 0.01; Robomimic ties within ~0.05; real 17-demo wins figure-only | + single-step IMLE generative head; - 1-step FM | M
[wave3] W3_TubeDiffusionPolicyReactiveVisualTactile | Q01 action head | DP DDIM-2 5.3% vs DDIM-10 98.4% (dish); image Push-T FM 65.3 vs DDPM 76.0 | - few-step vanilla diffusion | L
[wave3] W3_CapturingVisualEnvironmentStructureCorre | Q01 | 3-layer MLP policy "somewhat worse" than diffusion, same encoders | + diffusion over MLP regression | L
[wave3] W3_EquivariantDescriptorFieldsSE3Equivarian | Q01 action head | SE(3)-TNs fail on multimodal mug demos, EBM handles | + probabilistic head | L
[wave3] W3_ElicitingCompatibleDemonstrationsforMult | Q01 | MSE-MLP ensembles degrade with heterogeneous operator styles (no multimodal head tested) | ~ multimodality matters for mixed-operator data | L
[wave3] W3_ImperfectionforPrecisionUpcyclingImperfe | Q01 action head | flow-matching enables per-source noise-level admission; opposite window 30.0 vs 73.3 | + flow/diffusion head | L
[wave3] W3_LearningLatentPlansfromPlay | Q01 | CVAE latent plan vs GCBC: pixels 69.4 vs 58.7%, states 85.5 vs 77.9% | + latent-variable (CVAE) head for multimodality | L
[wave3] W3_MimicPlayLongHorizonImitationLearningbyW | Q01 | real, 20 demos: w/o GMM 0.28 (trained)/0.07 (unseen) vs with GMM 0.55/0.47 | + multimodal (GMM) head for human demos | M
[wave3] W3_NACNeuralActionCodecforVisionLanguageAct | Q01 action head | small from-scratch policy, success LIBERO-10/RoboMimic/Real(8x10): Bin 4/8/6, DP 25/27/23, FAST 38/28/40, VQ-VLA 11/21/31, OAT 44/32/40, NAC 50/34/50 | + learned RVQ codec tokens; ~ vs diffusion (DP baseline looks under-tuned) | L
[wave3] W3_NACNeuralActionCodecforVisionLanguageAct | Q01 action head (tokenizer recipe) | no adversarial discriminator → 0%; mel loss → 0%; linear vs ISTFT decoder 42.1 vs 48.3 | - fragile learned tokenizers | M
[wave3] W3_TransporterswithVisualForesightforSolvin | Q01 action head | unseen tasks 10 demos: multimodal proposals+foresight 78.5 vs single-mode GCTN 55.4; real unseen Twin Tower 60 vs 0 | + multimodal action representation | L
[wave3] W3_SeFAPolicyFastandAccurateVisuomotorPolic | Q01 action head | rectified flow + selective alignment: 66-task avg 62.3 vs DP 38.9; real flower insertion 80 vs 20, knob 40 vs 0 (10-20 trials) | + flow matching over DDPM diffusion | L
[wave3] W3_RoboMINDBenchmarkonMultiembodimentIntell | Q01 action head | single-task real: ACT avg 30.7–55.3% by embodiment; DP better on some Franka/humanoid tasks; BAKU worst (10 trials) | ~ ACT ≈ DP | L
[wave3] W3_VisionBasedMultiTaskManipulationforInexp | Q01 | $500 arm, 25 trials x 5 tasks: no autoregressive joint MDN 16/20/52/64/20% vs full 76/80/88/76/88% | + multimodal, joint-coherent action head | M
[wave3] W3_BayesianDisturbanceInjectionRobustImitat | Q01 action head | real UR3: unimodal GP 7% vs mixture GP 51%; with noise inj 18% vs 91% | - unimodal regression on multimodal demos | M
[wave3] W3_CageCausalAttentionEnablesDataEfficientG | Q01 action head | cross-attn conditioned diffusion UNet vs FiLM: ~+20 pts all settings | + attention conditioning of generative head | L
[wave3] W3_GoalConditionedDualActionImitationLearni | Q01 action head | default Diffusion Policy GraspNeck 0.111 at 5 Hz data | ~ DP untuned/confounded | L
[wave3] W3_MemoryConsistentNeuralNetworksforImitati | Q01 action head | memory-anchored MLP ≥ diffusion on low-dim sim BC (figure only) | ~ constrained heads in low data | L
[wave3] W3_RaCRobotLearningforLongHorizonTasksbySca | Q01 action head | 300M flow-matching MM-DiT, 10 Euler steps handles mixed expert+intervention data (not ablated) | + flow matching | L
[wave3] W3_SnapFlowOneStepActionGenerationforFlowMa | Q01 action head | 1-NFE flow after self-distillation matches 10-step | + flow w/ few steps | M
[wave3] W3_TransporterNetworksRearrangingtheVisualW | Q01 action head | dense spatial heatmap head 100% vs Conv-MLP 11-68% with stochastic demos (sim) | - MLP regression on multimodal demos | M
[wave3] W3_BridgeDataV2ADatasetforRobotLearningatSc | Q01 action head | D-GCBC without chunking/history jerky mode oscillation (qualitative); seen avg GCBC 0.49 = D-GCBC 0.49 | ~ diffusion needs chunking | L
[wave3] W3_TowardsSynergisticGeneralizedandEfficien | Q01 action head | real put-block: 5/10/100 demos ACT 0/6.7/46.7 vs DP 20/20/53.3 | + diffusion over CVAE at low data | M
[wave3] W3_FlowingWithPurposeLatentActionGuidedFlow | Q01 action head | real 50 demos: LAFM 86.7 / FM 63.3 / ACT 40.0 / pi0 71.7 SR; LIBERO-90 ACT 86.2 > FM 82.6 | + flow w/ structured prior; ~ FM vs ACT | M
[wave3] W3_CanonicalPolicyLearningCanonical3DRepres | Q01 action head | diffusion vs flow: Stack D1 76 vs 59, Push-T 87 vs 97 (CP-SO2) | ~ task-dependent | M
[wave3] W3_ChicGraspImitationLearningbasedCustomize | Q01 action head | real UR10e, 50 demos, 3 cams: DP 40.6% (41/101) vs IBC 0% vs LSTM-GMM 0% (GMM never triggers gripper) | + diffusion over IBC/GMM | M
[wave3] W3_RethinkingthePracticalityofVisionlanguag | Q01 action head | CALVIN discrete 256-bin tokens 3.68 vs diffusion head 3.70 | ~ discrete ≈ continuous when chunked | L
[wave3] W3_OnBringingRobotsHome | Q01 action head | single-step MSE MLP head, 81% on short unimodal tasks | ~ plain regression OK for short unimodal tasks | L
[wave3] W3_FromPlaytoPolicyConditionalBehaviorGener | Q01 action head | real multimodal C-BeT 24/50 vs unimodal 13/50; BlockPush 0.90 vs 0.35; oven (unimodal data) 9/10 vs 8/10 | - unimodal regression on multimodal human data | M
[wave3] W3_RevisitingEnergyBasedModelsasPoliciesRan | Q01 action head | Push-T sim: I-R-NCE 0.884 vs diffusion 0.864 vs NF 0.866 (3.3M params); IBC objective biased | ~ generative heads equivalent, - IBC | L
[wave3] W3_ContinuousVisionLanguageActionCoLearning | Q01 action head | ALOHA sim cube transfer human: ACT 50, AWE 71, CCoL 82, DP 4 | ~ CVAE-chunk > (untuned) DP on human sim data | L
[wave3] W3_AsyncVLAAsynchronousFlowMatchingforVisio | Q01 action head | WidowX: SFM 47.9 -> random-mask AFM 62.5 -> rater AFM 70.8; real PiPER 4x50: AsyncVLA 87.0 vs pi0 65.0, OFT 65.5 | + FM with masked partial-chunk conditioning | M
[wave3] W3_OrderedActionTokensforVisuomotorPolicyLe | Q01 action head | 5M AR policy real P&P: OAT8 16/20 vs QueST 11/20, FAST 8/20, Bin 4/20; no continuous baseline | - naive binning/FAST; ~ discrete tokens only with learned ordered tokenizer | M
[wave3] W3_RobotUtilityModelsGeneralPoliciesforZero | Q01 action head | DP better than VQ-BeT on small subsets, VQ-BeT better at 900-1200 demos; ACT/MLP-BC close | + diffusion at small data; ~ algorithm secondary | L
[wave3] W3_pi0EqMEquilibriumMatchingforClosedLoopVi | Q01 action head | EqM decoder vs pi0 flow: RoboTwin 40.4 -> 50.2 at 300 solver steps; LIBERO 94.15 -> 94.35 | ~ alternative generative head, heavy compute | L
[wave3] W3_GLUEGlobalLocalUnifiedEncodingforImitati | Q01 action head | real avg ACT 48.8 vs DP 36.2 (50 demos, 10 Hz); MimicGen ACT 34.8 vs DP 18.8 | ~ ACT >= DP in low data | L
[wave3] W3_BAKUAnEfficientTransformerforMultiTaskPo | Q01 action head | LIBERO-90 MLP .90 GMM .84 BeT .89 VQ-BeT .90 Diff .89 (MW Diff .45); real 30 tasks 150 trials: VQ-BeT .91 vs MLP .86 | + multimodal head on real human data; MLP fine in sim | M
[wave3] W3_pimathbfR2ReactiveRealtimeFlowPolicies | Q01 action head | 1 NFE/call with staircase per-position noise matches 16-step flow at h=1-2 (sim) | + few-step flow feasible | M
[wave3] W3_EvoHILSelfEvolvingRewardandFlowMatchedPo | Q01 action head | SO-101 flow-matched chunks (H24/E4) vs Gaussian per-step: action 1st-diff -44.5%, HF power -48 to -58%; push duration 11.45 -> 7.80 s | + flow chunk head for smoothness | M
[wave3] W3_HybridConsistencyPolicyDecouplingMultiMo | Q01 action head | DDIM (mode-collapsed, entropy 0) success 87% sim / 76.7% real vs DDPM 79% / 78.3% | ~ inference stochasticity unnecessary for success | M
[wave3] W3_SAVLASymmetryAwareVisionLanguageActionMo | Q01 action head | real SO-101, 50 demos/task, 20 eps: GR00T flow head 61.7% vs equivariant flow head 71.7%; LIBERO 86.5->91.6 | + flow matching; + equivariant head | L
[wave3] W3_REBOOTFromFailuretoRecoveryADatasetandBe | Q01 action head | ACT ~ DP overall, pi0-FAST best, 15 rollouts/task/policy (figure) | ~ | L
[wave3] W3_ProgVLAProgressAwareRobotManipulationSki | Q01 action head | flow matching + progress-weighted loss; w/o weighting 88.8 vs 91.1 | ~ FM fine at 100M | L
[wave3] W3_StartRightArriveRightAsynchronousExecuti | Q01 action head | OT flow matching allows gradient-free prefix anchoring via ODE inversion (86 ms GR00T vs RTC 113 ms) | ~ flow head has deployment advantages | L
[wave3] W3_TheUnreasonableEffectivenessofDiscreteTi | Q01 action head | RLBench constrained avg: MiDiGaP-5demos 0.95 vs DP-100demos 0.48; multimodal 0.86 vs DP 0.46 (all get GT object pose) | + explicit trajectory mixture/GMM when object pose available | M
[wave3] W3_WaypointBasedImitationLearningforRobotic | Q01 action head | AWE helps GMM but degrades MSE/unimodal BC (figure only) | - plain MSE with multimodal targets; + expressive head | L
[wave3] W3_vlasimdEfficientCPUInferenceforLanguageC | Q01 action head | CVAE+L1 ACT works on SO-101; DP 100-step 40 s/query on Pi5, 10-step DDIM 5 s | + CVAE/regression for CPU/latency; - many-step diffusion | M
[wave3] W3_ActionControlNetALightweightDelayAwareAd | Q01 action head | residual delay conditioning on final block of flow-matching expert; final-block > early injection (figure) | + flow head supports cheap async conditioning | L
[wave3] W3_XDiffusionTrainingDiffusionPoliciesonCro | Q01 action head | diffusion noise-level gating lets low-quality data help (fig only) | + diffusion/flow if mixing heterogeneous data | L
[wave3] W3_DFMVLAIterativeActionRefinementforRobotM | Q01 action head | real 6 tasks x40: pi0-FAST(AR tokens) 47.5, Dream-VLA(discrete diffusion) 57.1, pi0.5(cont. flow) 70.8, DFM 73.3; CALVIN 10% data AR 1.71 / DD 2.84 / DFM 3.21 | - AR/masked discrete tokens; + continuous flow or refinable decoding | M
[wave3] W3_DenoisingTellsWhentoReplanDenoisingVaria | Q01 action head | flow denoising variance flags contact phases (r<-0.27 with exec length) | + generative head enables uncertainty-aware replanning | L
[wave3] W3_FasterVisuomotorPolicyLearningonActionMa | Q01 action head | 1 NFE: DP 0.0 (Tool Hang, Transport) vs flow matching 60/94 vs MeanFlow 64/90+; ceilings equal at 10 NFE | + flow matching / MeanFlow for few-step; - DDPM-eps diffusion at low steps | M
[wave3] W3_BeingH05ScalingHumanCentricRobotLearning | Q01 action head | freezing >14 of 28 action-expert layers -> sharp drop, fully frozen <20% | + train action head fully | L
[wave3] W3_FrequencyGuidedActionDiffusionviaSubFreq | Q01 action head | sim DP3 vs FGO avg 52.9->56.6 (Robosuite/MimicGen), 55.9->60.3 (Adroit/DexArt), 3 seeds | ~ frequency-guided diffusion small gain | L
[wave3] W3_ManiFlowAGeneralRobotManipulationPolicyv | Q01 action head | consistency flow: 1 step 63.7 / 2 steps 64.5 vs DP3 10-step 42.7, 3D flow 10-step 48.1 (RoboTwin); 2D avg 56.5 vs DP 39.4 | + flow+consistency, 1-2 NFE | M
[wave3] W3_ImitationLearningPolicybasedonMultiStepC | Q01 action head | RoboTwin 1-NFE multi-step-consistency flow 44.27 vs 3DP 10-NFE 41.39; real (10 trials) 50/40/50 vs DP 40/30/40 vs Shortcut 10/10/20 | + one-step flow head (careful training); - naive Shortcut | L
[wave3] W3_PRISMPerformerRSIMLEforSinglepassMultise | Q01 action head | MetaWorld Hard: IMLE-1NFE PRISM 58.0 vs DP(10 NFE) 9.0, Flow(1 NFE) 13.4, DP3 38.0; CALVIN10%: 65.2 vs DP 36.4, Flow 44.4 | + single-pass multimodal head (RS-IMLE) | M
[wave3] W3_MimicIntentNotJustTrajectories | Q01 action head | multi-scale spectral VQ tokens: LIBERO-Long 93.4 vs time-domain scale-wise 82.8; MINT-30M LIBERO 97.1 vs DP 72.4 | + coarse-to-fine learned action tokens | L
[wave3] W3_HiFlowTokenizationFreeScaleWiseAutoregre | Q01 action head | real HSR 50 demos @10Hz, 12 trials: Orange->Plate ACT 8.3 / DP 16.7 / VQ-AR 25.0 / flow-AR 41.7; Mustard 33.3/58.3/58.3/83.3 | + continuous flow head; - ACT, - VQ tokens | M
[wave3] W3_SharedExecutionClockDriftingPolicyforDyn | Q01 action head | real, Thor: DP 16-NFE 252 ms cup place 98%; distilled OneDP 1-NFE 71%; native 1-step drifting+clock 95% at 25 ms | + natively-trained few/one-step head; - post-hoc distillation | M
[wave3] W3_TSMaskVLA2DTemporalSpatialMaskingforVisi | Q01 action head | masked discrete diffusion 0.5B: LIBERO 95.7, CALVIN 4.19; 2D vs 1D mask Long 91.6 vs 85.0 | ~ discrete masked diffusion viable (sim) | L
[wave4] W4_ArmnetBenchv01ParallelRealWorldEvaluatio | Q01 action head | DP 26.7 vs ACT 19.2 pooled; ACT>DP on eye_drops_to_basket 63 vs 43; ACT 2.5% bimanual | ~ task-dependent | L
[wave4] W4_BridgeVLAInputOutputAlignmentforEfficien | Q01 | heatmap output 88.2 vs direct MSE position regression 31.4 (RLBench) | + spatial heatmap/classification head for keyframe pose | M
[wave4] W4_FACTRForceAttendingCurriculumTrainingfor | Q01 action head | MSE regression on absolute joint chunk k=100, ACT arch w/o CVAE works at 50 demos | ~ regression | L
[wave4] W4_ImprovingGenerativeBehaviorCloningviaSel | Q01 | Push-T: CFG 0.070, vanilla 0.496, AutoGuidance 0.735, self-guidance 0.873 | ~ diffusion head + past-obs guidance; avoid CFG | M
[wave4] W4_MINERVAHowSmallCanaManipulationPolicyBea | Q01 action head | flow→L1 regression +0.34 (95.63±1.08 → 95.97±0.80, 3 seeds), L1 3.8x faster | + L1 regression (small model) | M
[wave4] W4_ASystematicStudyofDataModalitiesandStrat | Q01 | FAST/VQ/latent-action token co-training no significant gain, FAST hurts unseen tasks | + continuous flow head, - discrete token aux | M
[wave4] W4_BitVLA1bitVisionLanguageActionModelsforR | Q01 action head | L1 chunk regression (OFT parallel decoding) 96% LIBERO with pretrained 3B backbone | ~ L1 regression ok with big pretrained backbone | L
[wave4] W4_MolmoAct2ActionReasoningModelsforRealwor | Q01 | per-layer KV-conditioned flow expert 95.9 vs hidden-state 94.0; flow samples K=8 95.9 vs K=1 94.15 (LIBERO) | + flow expert with multiple flow-time samples | M
[wave4] W4_ControlVLAFewshotObjectcentricAdaptation | Q01 action head | 11-20 demos: DP 20.8% vs ACT 5.0% vs Octo 1.6% | + diffusion over CVAE/regression in tiny data | L
[wave4] W4_BimanualManipulationWithinan8GBBudgetZer | Q01 action head | SO-101 bimanual, 100 demos: ACT 19/20 @100k steps vs Diffusion Policy 0/10 @200k (LeRobot defaults) | + ACT/CVAE under compute budget, - DP w/o tuning | M
[wave4] W4_CoLAFlowPolicyTemporallyCoherentImitatio | Q01 action head | long-horizon real: raw 1-step Flow 20%, VQ-latent flow 70%, continuous GRU-VAE latent flow 80%; real avg 77.5 vs RDP 70.0 vs DP3 57.9 | + generative head in continuous latent action space | M
[wave4] W4_DecouplingVisionLanguageandActionforEffi | Q01 action head | params-matched heads on DINOv3+NeoBERT: DP 53.8, FM 54.7, ACT 52.4, MeanFlow 55.6 (18 RoboCasa tasks x100) | ~ head choice minor; + one-step MeanFlow for speed | M
[wave4] W4_CronusVLATowardsEfficientandRobustManipu | Q01 action head | DiT diffusion 70.9 vs SiT flow 67.6 vs MLP 51.8 (large data) | ~ generative > MLP at scale | L
[wave4] W4_ChronosAPhysicsInformedFullHistoryFramew | Q01 action head | ALOHA insertion 50 demos, same encoder: diffusion 66 / flow 72 / regression 76 / IMLE 86 / IMLE+2nd-order bridge 90% | ~ regression >= flow/diffusion in low data | L
[wave4] W4_DCODADiffusionforCoordinatedDualArmDataA | Q01 | pi0-FAST produced sudden large actions on augmented OOD states | - discrete action tokens | L
[wave4] W4_E0EnhancingGeneralizationandFineGrainedC | Q01 action head | discrete Tweedie diffusion vs π0 flow: LIBERO-Long 92.2 vs 85.2; real 8 tasks avg 45.6 vs 43.1 (mixed per task); π0-FAST AR 10.0 real | ~ discrete diffusion ≈ flow; - AR tokens | L
[wave4] W4_HybridFlowA2NFEGenerativePolicyforRealTi | Q01 action head | real Franka ~300 demos: MeanFlow-1NFE 0%, DDIM-2 ≈0%, ReFlow-2 5.0%, DDIM-16 42.1%, HybridFlow-2NFE 70.1% (M-avg) | + generative head with enough/structured steps; - naive 1-2 step flow/diffusion | M
[wave4] W4_GuidedActionFlowQGuidedInferenceforFlowM | Q01 action head | flow head allows Q-gradient guidance at sampling, beta=2 | ~ generative head enables test-time steering | L
[wave4] W4_FLASHEfficientVisuomotorPolicyviaSparseS | Q01 | history-anchored 1-step flow 96.8% vs Gaussian-start flow 79.2% (5 sim tasks) | + informative-prior 1-step flow | M
[wave4] W4_JEPAPolicyDiffusionFreeImitationLearning | Q01 action head | real ARX-5 100 demos: DP-100 18.7%, DP-16 31.8%, MIP (deterministic 2-pass) 54.7%, JEPA 66.9%; sim 9-task MIP 77.4 vs DP 75.1 | + deterministic few-pass regression w/ training noise; - "generative head required" | M
[wave4] W4_MaxQSelectiveImitationforHumanintheLoopO | Q01 action head | ACT 99% vs flow 96% actors in HIL RL | ~ | L
[wave4] W4_PocketDP3EfficientPocketScale3DVisuomoto | Q01 action head | NFE 1/2/5/10: 53.0/58.2/57.7/58.0 (Adroit, 5000 eps); plain MLP decoder fails (0%) | + diffusion x0-pred with 2 steps; need mixer/residual structure | M
[wave4] W4_PatchPolicyEfficientEmbodiedControlviaDe | Q01 action head | VQ-BeT vs DP on same patch features similar (BlockPush 1.68 vs 1.65) | ~ | L
[wave4] W4_TimeFrequencyGeometricCrossAttentionforC | Q01 action head | wavelet+geometric chunk attention on pi0.5: LIBERO-Plus 66.7->73.0; real AgiBot 50.0->61.7% (60 trials) | ~ structured chunk decoder helps big VLA | L
[wave4] W4_UniVLALearningtoActAnywherewithTaskcentr | Q01 action head | visual-query chunk decoder vs autoregressive discrete: +42.1 LIBERO-Long; w/o visual query 92.5 vs 95.2 | - discrete AR tokens, + chunked continuous | M
[wave4] W4_TeachingTinyVLAModelsWheretoLookandHowto | Q01 | SmolVLA-0.25B + CVAE-latent flow (z=0 at test): LIBERO 82.8→87.4; full XS-VLA real multi-operator 21.7→65.0 (60 trials) | + CVAE latent on flow head for multi-style demos | M
[wave4] W4_TaskPrototypeGuidedFlowMatchingforFewSho | Q01 action head | SO-101 SR@6: ACT 49.3, DP 55.6, FlowPolicy 59.8, TP-Flow 82.1 (trials/protocol unreported) | ~ flow >= diffusion > CVAE (weak evidence) | L
[wave4] W4_GlobalPriorMeetsLocalConsistencyDualMemo | Q01 action head | flow matching from retrieved prior instead of N(0,I) | ~ | L
[wave4] W4_SimulationDrivenImitationLearningforBios | Q01 action head | unseen-room SR: ACT 57.4, VTM-VAE 55.8, diffusion 49.0 (unseen obj 42.2/44.9/33.2) | ~ CVAE >= diffusion in small low-dim setting | L
