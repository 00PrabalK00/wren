# Q10_latency_async — 141 ledger lines
[fulltext] ACT | control_rate | 5 Hz vs 50 Hz teleop: 62% slower | + higher rate | M
[fulltext] RTC | execution | TE fails (invalid averages; protective stops at +100ms); RTC robust to +200ms | + inpainting async, - blending/TE | H
[fulltext] Legato | execution | training-time continuation ~10% smoother/faster than RTC; stops mode switching | + flow + Legato | M
[fulltext] SO101-Benchmark | evaluation | ACT 33.75 ≈ SmolVLA 32.5 < Wall-X 51 < π0.5 56; execution failures dominate; recovery ACT 6.5%, SmolVLA 3.2% | + recovery demos, + grasp robustness | M
[fulltext] BeT | Q10 latency | 2.8 ms/action BeT vs 52 ms IBC vs 0.5 ms MLP | + single-pass heads | M
[fulltext] VQ-BeT | Q10 latency | single pass 18 ms vs DP-T 573 ms GPU closed-loop (15 vs 100 ms sim @10 DDIM steps) | + single-pass head | M/H
[fulltext] ImplicitBC | Q10 latency | EBM 7.2 ms vs MSE 3.5 ms (2-D action, 2080Ti) | ~ | L
[fulltext] RT-1 | Q10 latency | TokenLearner 2.4× speed-up, token caching 1.7×; AR actions 36 vs 15 ms no gain | + token reduction, - AR action decoding | M
[fulltext] ConsistencyPolicy | Q10 latency | laptop 3070Ti 8GB: CP 21 ms (enc 6 + net 13.5) vs DDIM-15 192 ms vs DDPM-100 ~1.5 s | + 1-3 step head on 8GB laptop | H
[fulltext] ConsistencyPolicy | Q10 steps_vs_quality | DDIM-15 ToolHang .14 vs DDPM-100 .79 vs CP-3 .77; low-var init +.04 | - naive step reduction on precise tasks | M
[fulltext] FlowPolicy | Q10 latency | 19.9 ms vs DP3 145.7 ms vs SimpleDP3 63.0 ms (2080Ti) | + 1-step head | M
[fulltext] StreamingFlowPolicy | Q10 latency | per-action 3.5-8.8 ms vs DP-100 40-127 ms, DDIM-10 4.4-10.4 ms; chunk starts at last action (no boundary jump), smoother real motion (video only) | + streaming/continuity-aware flow | M
[fulltext] DiffusionTransformerPolicy | Q10 latency | DDPM 100 steps on 334M model, no latency reported | - (unknown; likely too slow for 8GB) | L
[fulltext] SmolVLA | execution | async 9.7s vs sync 13.75s/task, 19 vs 9 cubes/min; success 78.3->73.3 (sorting 70->50), no continuity handling | + async queue, - async without boundary fix | M
[fulltext] ReactVLA | latency | real: 38.6 ms (5-step iMF) vs SmolVLA 82.2 ms; stack 90 vs 75%; LIBERO 88.0 @18.3 ms vs SmolVLA 87.3 @74.1 ms | + few-step mean flow; our 2 s SmolVLA latency is a deployment bug | M
[fulltext] BidirectionalDecoding | execution | EMA/TE under noise 1.5: 18.4 vs vanilla 29.5; BID 31.7; BID +32% rel sim, +46% with EMA; 2x latency (13->26 ms) | + coherence-based sample selection, - naive TE | M
[fulltext] VLA-Adapter | latency | 36.5 ms / 219 Hz (8-step chunk) vs OFT 112 ms; train VRAM 24.7 GB @batch 8 (not 8 GB) | + single-pass head; - full FT on 8 GB | M
[fulltext] FLOWER | latency | RTX 4090: 52 ms/chunk, 1.85 GB (pi0 104 ms/6.7 GB, DP 341 ms/0.5 GB) | + 4-step flow VLA fits laptop inference | M/H
[fulltext] MobileALOHA | compute | ACT collection+inference on 8 GB RTX 3070 Ti laptop, 50 Hz | + small ACT-class model fits our GPU | H
[fulltext] UMI | latency | latency matching 105/120 vs 69/120 without; jitter removed; 0.5× exec speed smoother | + measure & compensate latency | M/H
[fulltext] 3DDiffuserActor | Q10 latency | 600 ms per 6-pose trajectory on 2080 Ti (DP3 581 ms) | - many-step diffusion on laptop | M
[fulltext] Hyper-DP3 | Q10 latency | 4.5 ms (2 steps, 2.5M) vs DP3 51.4 ms vs DP 460 ms | + few-step small 3D policy | H
[fulltext] RoboVLMs-WhatMatters | Q06 execution | unseen scenes: execute full chunk 3.68 > ensemble 3.14 > first action 2.45 | + full-chunk execution | M/H
[fulltext] Dita | Q10 steps_vs_quality | DDIM steps 100/50/20/10/5/2 → Pick-Coke var 76.4/79.1/85.5/85.3/82.7/70.4; Move-Near var 52.1/66.0/73.0/69.5/63.5/51.6 | + ~10 steps; - 2 steps w/o distillation | M
[fulltext] Dita | Q10 latency | 334M VLA run at 3 Hz on A100 server | - mid-size VLA on 8GB laptop | L/M
[fulltext] VideoPredictionPolicy | Q10 latency | TVP 1-step ≈140 ms on 4090 (7–10 Hz w/ chunk 10); no Video Former ≈450 ms | ~ heavy encoders cost latency | M
[fulltext] HPT | Q10 latency | HPT-Base 47 Hz, HPT-XL 19 Hz on RTX 3070 | + small trunk real-time on laptop GPU | H
[fulltext] OpenVLA | Q10 latency | int8 at 1.2 Hz on 5 Hz task: 58.1 vs bf16 71.3 (same token accuracy) | + keep inference rate >= control rate | M
[fulltext] CogACT | Q10 latency/smoothness | 2-step chunk exec 50.7 vs temporal ensemble 58.9 vs adaptive (cos-sim weighted) ensemble 62.5 | + overlapping-chunk similarity-weighted ensembling | M
[fulltext] pi0 | Q10 latency | RTX 4090: img enc 14 + prefix 32 + 10x expert 27 = 73 ms; KV-cache prefix | + cache obs prefix, small expert makes K steps cheap | H
[fulltext] FAST | Q10 latency | pi0-FAST ~750 ms vs diffusion pi0 <100 ms per 1 s chunk (4090) | + continuous flow head over autoregressive tokens | H
[fulltext] KnowledgeInsulation | Q10 latency | expert ~10 Hz vs AR 1.3 Hz; pi0-FAST 2x wall-clock per task | + small continuous expert | M/H
[fulltext] GR00T-N1 | Q10 latency | 2.2B, 16-action chunk 63.9 ms on L40 bf16 with K=4 | + reduce flow steps to ~4 | M
[wave3] W3_ActionMapRobotPolicyLearningviaVoxelActi | Q10 latency | single-pass heatmap head, no denoising steps (latency not measured) | + single-pass heads | L
[wave3] W3_IMLEPolicyFastandSampleEfficientVisuomot | Q10 latency | 111 Hz (IMLE) vs 1.8 Hz (DP 100-step DDPM) on RTX3090; select candidate closest to previous chunk tail for consistency | + 1-step head + consistency selection | M
[wave3] W3_TubeDiffusionPolicyReactiveVisualTactile | Q10 latency | real: DP 37 ms/~25 Hz vs TDP 8 ms denoise + 3 ms stream >100 Hz; reorientation 60->96%, jar 84->96% (25 eps) | + per-step feedback correction inside chunk | M
[wave3] W3_DiffusionVLAGeneralizableandInterpretabl | Q10 latency | 8/4-bit quantization significantly degrades VLA (no numbers); DiVLA-2B 82Hz A6000 | - quantization as free speedup | L
[wave3] W3_FurnitureVLALearningLongHorizonBimanualF | Q10 | recency-weighted chunk blending best for smooth bimanual control | + blend overlapping chunks | L
[wave3] W3_HermiteCurvesasTrajectoryPriorsforVision | Q10 chunk-boundary smoothness | Hermite aux loss: real seam jump 0.48-0.72x of pi0.5; real SR 63.4 -> 90.0 (4 tasks x 15); zero inference cost (48.6 vs 48.4 ms) | + training-time trajectory smoothness regularizer | M
[wave3] W3_MantisAVersatileVisionLanguageActionMode | Q10 latency | adaptive temporal ensemble ~50% fewer inference calls, comparable SR (figure) | + ensemble only during fine phases | L
[wave3] W3_NACNeuralActionCodecforVisionLanguageAct | Q10 latency | 12 tokens/chunk vs Bin 224 vs FAST 36 | + compressed tokens for AR latency | L
[wave3] W3_RecoveringAggressivelyPrunedVisionLangua | Q10 latency | 72% width-pruned OpenVLA-OFT: 59.3->51.0 ms H100 (1.16x), 362->162 ms Jetson Thor; CogACT latency floor ~85 ms from 10 DDIM steps; depth pruning 1.31-1.66x | ~ prune depth/denoise steps, not width, for latency | M
[wave3] W3_PredictionwithActionVisualPolicyLearning | Q10 latency | joint image+action DiT with 75 DDIM steps → low control rate (stated limitation) | - predicting images at inference | M
[wave3] W3_SeFAPolicyFastandAccurateVisuomotorPolic | Q10 latency | 1-step SeFA 16.7 ms vs DP-100 1287 ms vs AdaFlow-20 629 ms; 1-step 62 = 100-step 62 avg; 1-step DDIM fails (Pen 0, Square 0) | + reflow/consistency 1-step sampling | M
[wave3] W3_RT2VisionLanguageActionModelsTransferWeb | Q10 | 55B 1-3 Hz, 5B ~5 Hz on multi-TPU cloud | - large VLAs for real-time control | M
[wave3] W3_ThinkingWhileMovingDeepReinforcementLear | Q10 async execution | concurrent grasping sim: unconditioned 84.1% vs VTG-conditioned 93.5% (blocking 92.7%), 31% faster; real concurrent 68.6% vs blocking 81.4% but 49% faster | + condition next action on in-flight action | L
[wave3] W3_VistaBotViewRobustRobotManipulationviaSp | Q10 latency | VGGT+CogVideoX view synthesis pipeline ~3 Hz | - test-time generative view synthesis on 8 GB | M
[wave3] W3_BeyondAppearanceShiftsTaskSemanticAction | Q10 latency | SAM2+grounding preserving mode p50 924 ms end-to-end | - runtime segmentation on laptop | M
[wave3] W3_BeyondTaskSuccessBehavioralandRepresenta | Q10 latency | p50 per chunk: pi0.5 100 ms, pi0 194, X-VLA 329, Cosmos 956, VLA-JEPA 1588, LingBot-VA 4701 ms (RTX 6000 Ada) | - inference-time world-model imagination | M
[wave3] W3_ActFoveaRuntimeSafeguardingforVLAPolicie | Q10 latency | pi0 LIBERO 2000 eps: 3-frame visual delay 93.0->76.2; fixed action clip/smoothing clean 93.0->82.2 | + minimize obs-action lag, - naive smoothing | M
[wave3] W3_ADualProcessVLAEfficientRoboticManipulat | Q10 latency | small policy + VLM latent once/episode 0.030 s/step vs OpenVLA ~0.25 s (sim) | + small fast per-step policy | L
[wave3] W3_SnapFlowOneStepActionGenerationforFlowMa | Q10 latency | SmolVLA E2E 178→50 ms (denoise 79%→24%); pi0.5 274→81 ms; LIBERO 98.75 vs 97.75 | + 1-step flow distillation | M
[wave3] W3_TowardsSynergisticGeneralizedandEfficien | Q10 latency/async | OpenVLA alone 3.9 Hz → jitter/pauses; 20M DiT specialist 0.035 s → 15 Hz; latency-aware training with random obs offset τ∈[0,kg] | + fast small specialist + delay-aware training | M
[wave3] W3_FlowingWithPurposeLatentActionGuidedFlow | Q10 latency | FM/LAFM hold LIBERO-90 SR with 1 vs 10 denoising steps (figure) | + 1-step flow | L
[wave3] W3_WhyDoesActionChunkingImproveBehavioralCl | Q10 | interleaved inference (1-step delay) on real Franka 15 Hz; RDE gives per-step actions from cached chunks matching AC | + per-step readout from cached chunks to avoid boundary jerks | L
[wave3] W3_AhaRobotALowCostOpenSourceBimanualMobile | Q10 latency | STS3215 servos: dithering + dual-motor anti-backlash -> 0.72 mm repeatability; pi0 slow inference + chunking -> discontinuities knock tools | + low-level trapezoidal smoothing, + faster inference | M
[wave3] W3_ContinueorReplanBernoulliContinuationPol | Q10 latency | continuation head +2 ms/query, total runtime 10.43->10.24 s; entropy/uncertainty triggers much slower | + cheap replan trigger vs multi-sample uncertainty | M
[wave3] W3_OneACTPlaySingleDemonstrationBehaviorClo | Q10 smoothness | switch to pure chunk replay when ensemble std large; β-sensitive | ~ training-free chunk-blending fix | L
[wave3] W3_ContinuousVisionLanguageActionCoLearning | Q10 smoothness | NeuralODE latent + discontinuity penalty: accel fluctuation -32.7%, insertion scripted 72->87% | + smoothness regularization in chunk decoder | L
[wave3] W3_AsyncVLAAsynchronousFlowMatchingforVisio | Q10 latency | SFM 10 steps 47.9 vs 20 steps 51.1; 96 ms total on 4090 for 4B model | + few-step FM sufficient | M
[wave3] W3_DEFLECTTemporalCounterfactualPreferenceL | Q10 latency/async | Kinetix chunk 8, delay 5-7: naive 1.5%, RTC 2.0%, BID 2.0%, VLASH (future-state input) 67.1%, DEFLECT 73.5%; real conveyor pi0.5 76.7 -> VLASH 86.7 -> DEFLECT 96.7% | + keep delay << chunk; + feed execution-time robot state | M
[wave3] W3_GloVLALetGeometryMoveandLocalVLAInteract | Q10 latency | episode inference time 60.1 s -> 28.2 s | + fewer policy calls via scripted transport | L
[wave3] W3_DynamicExecutionHorizonPredictionforChun | Q10 latency | DEHP chooses h~1 in tight-insertion phases (requires per-step replanning) | + fast inference to allow frequent replans | L
[wave3] W3_pi0EqMEquilibriumMatchingforClosedLoopVi | Q10 latency | half-chunk warm start from previous prediction (not ablated separately); 300 iterations/decode | ~ warm start idea, impractical cost | L
[wave3] W3_BAKUAnEfficientTransformerforMultiTaskPo | Q10 smoothness | real: 10 Hz policy + TE + 100 Hz min-jerk controller (qualitative) | + low-level interpolation | L
[wave3] W3_pimathbfR2ReactiveRealtimeFlowPolicies | Q10 latency/smoothness | real 4 tasks x20: piR2 10/12/16/11 vs Train-time RTC 9/8/10/5 vs naive async+TE 7/7/12/2 vs sync 4/4/11/4 | + train-time in-flight-action inpainting with randomized delay; - naive async / sync | M
[wave3] W3_EvoHILSelfEvolvingRewardandFlowMatchedPo | Q10 smoothness | smoothness loss removal: SR 0.97 unchanged, duration 5.44 -> 6.02 s | ~ smoothness term minor | L
[wave3] W3_SAFEPrunerSemanticAttentionGuidedFutureA | Q10 latency | real pi0.5 backbone 80.4->43.6 ms (RTX 3090), success 81.3->79.3%; OFT 70->37 ms LIBERO 96.8->96.4 | + token pruning/quantization; our 2 s SmolVLA latency is a pipeline issue | M
[wave3] W3_FastandAccurateAnAdaptiveVLAInferenceFra | Q10 latency | pi0 called on 15.3% of steps: SR 92.4% at 93.4 Hz vs fixed schedule 90.35%; no action fusion at handoff -1.1 avg / -3 LIBERO-10 | + fast small policy with boundary fusion | M
[wave3] W3_HybridConsistencyPolicyDecouplingMultiMo | Q10 latency | real per-chunk 4080: DDPM80 0.54 s 78.3%; DDIM50 0.34 s 76.7%; HCP25+1 0.17 s 73.3%; 5-step consistency 0.04 s 38.3% | + few-step deterministic sampling; - naive 1-step DDPM distillation | M
[wave3] W3_KnowingWhentoStopAdaptiveActionChunkingv | Q10 latency | MS adaptive method with very short chunks -> intermittent pauses, real 18.3% vs 41.7-51.7 fixed; entropy rule adds <7 ms on A100 (0.27 s/chunk) | - very short re-plan horizons without smoothing | L
[wave3] W3_LaST0LatentSpatioTemporalChainofThoughtf | Q10 latency | slow:fast 1:1-1:4 75-79%, 1:8 74%, mixed-ratio training 82% (sim) | + train with randomly stale slow conditioning | L
[wave3] W3_StartRightArriveRightAsynchronousExecuti | Q10 latency/async | real 6 tasks, d~3: PAINT >= RTC (GR00T toy-drawer 0.85 vs 0.75; pi0 towel 0.80 vs 0.54); B-spline smoothing ~ no prefix fix (sim) | + prefix-conditioned async (RTC/PAINT), - post-hoc smoothing | M
[wave3] W3_TunetoLearnHowControllerGainsShapeRobotP | Q10 latency/smoothness | compliant gains attenuate action noise (open-loop noisy replay); jitter failures 21.8%@100Hz -> 5.0%@10Hz (RL sim2real) | + compliant/overdamped follower; ~ lower policy rate vs oscillation | M
[wave3] W3_VidarEmbodiedVideoDiffusionModelforGener | Q10 latency | 25 s per 7.5 s open-loop plan on 8x A100 | - video-generation planners for our latency | H
[wave3] W3_WaypointBasedImitationLearningforRobotic | Q10 smoothness | authors advise temporal ensembling on ALOHA; slower blocking controller for precision (no numbers) | ~ TE for smoothness | L
[wave3] W3_vlasimdEfficientCPUInferenceforLanguageC | Q10 latency | actions/s on Ryzen5 CPU: ACT 627, IMPACT 262, SmolVLA 38, DP-100step 3.6; Pi5 query: ACT 0.92s, IMPACT 1.21s, SmolVLA 8.19s | + small ACT-class (34-60M) for real-time | H
[wave3] W3_vlasimdEfficientCPUInferenceforLanguageC | Q10 latency | time-aligned async needs H/Tq >= ~2x control rate; transport adds 0.5-1.0 s RTT | + measure full obs-to-action path, long chunks | M
[wave3] W3_WhatistheBetterCurriculumControllerShape | Q10 latency/reactivity | under disturbance policy-only 55% vs +25Hz reflex arbiter 100% (pi0.5 ~1.7 Hz re-query) | + fast low-level reactive layer / higher re-query rate | M
[wave3] W3_ActionControlNetALightweightDelayAwareAd | Q10 latency/async | Kinetix avg d>0: naive async 0.61, RTC 0.72, Training-RTC 0.80, ACNet 0.79 (20% params); SO-ARM101 50 demos: naive 17/20 vs ACNet 20/20, less handoff oscillation | + condition head on executed action prefix; - naive stitching | M
[wave3] W3_ChainVLAChainingVisionLanguageActionQuer | Q10 smoothness | RMBench: full 62.8 vs w/o motion tail 11.2; seam position discontinuity 7.51->3.26 mm; TE and linear blend 0% on Put Back (full 96) | + condition/initialize next chunk on previous unexecuted suffix; - post-hoc blending | M
[wave3] W3_DSWAMADualSystemWorldActionFoundationMod | Q10 latency/async | real folding easy: sync TRT pants 70% -> async TRT+RTC 100%, time 1'50''->1'08''; TensorRT BF16 198->74 ms (5090) | + async+RTC, + TensorRT/compile | M
[wave3] W3_DenoisingTellsWhentoReplanDenoisingVaria | Q10 latency | denoising-variance adaptive execution: real SR +6-10 pts over Fix15 with ~50% fewer replans; LIBERO 0.948->0.980, replans 32.6->18.6 | + adaptive execution horizon (flow heads) | M
[wave3] W3_FasterVisuomotorPolicyLearningonActionMa | Q10 latency | MeanFlow 2 NFE Tool Hang 76.0 (best in table) vs DP 74.0 at 10 NFE | + 1-2 step generative heads | M
[wave3] W3_BeingH05ScalingHumanCentricRobotLearning | Q10 latency/async | RTC-style prefix lock (d>=ceil(t_inf/t_ctrl)+margin) + ring buffer on 5 robots incl SO-101; removing UAC+MPG degrades esp. long-horizon (figure only) | + prefix-conditioned async chunking | M
[wave3] W3_GeometricActionModelforRobotPolicyLearni | Q10 latency | 1.4B single-pass L1 head 6.9 ms (17.5 w/o CUDA graphs) vs pi0.5 29.2, OFT 70-78, Cosmos 382 ms | + single-pass heads for latency | M
[wave3] W3_FrequencyGuidedActionDiffusionviaSubFreq | Q10 smoothness | Can approach JerkRMS 50.87->40.79, ATV 14.83->14.76; inference 39.5->44.2 ms | + low-pass/spectral smoothing within chunk (not boundaries) | L
[wave3] W3_EquiVLAAGeneralFrameworkforRotationallyE | Q10 latency | C8 frame averaging: 64 -> 194 ms/step on H100 | - test-time symmetrization on laptop | M
[wave3] W3_ImitationLearningPolicybasedonMultiStepC | Q10 latency | same model 1/3/5/10 inference steps: 59.7/59.9/61.4/60.9 avg SR | + few-step sampling costs ~nothing | L
[wave3] W3_RLDGRoboticGeneralistPolicyDistillationv | Q10 latency | OpenVLA at 4 Hz slower cycle times than 10 Hz RL policy (0.3-2.3 s per task) | ~ control rate matters for speed | L
[wave3] W3_PRISMPerformerRSIMLEforSinglepassMultise | Q10 latency/smoothness | A100: 15 ms vs DP 142 ms, Flow 74 ms; jerk 0.052 vs 1.05-3.78; mode switch 0.10 vs 0.28-0.59 | + 1-pass head + pick candidate closest to last action | M
[wave3] W3_MMACTLearnfromMultimodalParallelGenerati | Q10 latency | cs=8 one-step 43.13 @0.22s vs 6-step re-mask 42.38 @1.06s; cs=16 43.75 vs 56.75 | ~ iterative decoding only pays for long chunks | L
[wave3] W3_RoboticTableTennisACaseStudyintoaHighSpe | Q10 latency | sim latency = measured -> 1.83/2.0 real; 50% -> 1.33; 0/20/150% very poor; real perf flat until ~150 ms added latency / 50 FPS then collapses | + measure & match deploy latency; interpolate obs | M
[wave3] W3_RealtimeVLAFLASHSpeculativeInferenceFram | Q10 latency | pi0 4090D 58 ms/round (enc 11, prefill 27, denoise 20); Triton 39.7 ms same SR; FLASH 19.1 ms SR 93.8 vs 94.1; conveyor 13 m/min: 0% (JAX) vs 50% (FLASH) | + optimize inference latency; ~2 s SmolVLA latency is anomalous | M
[wave3] W3_VLACacheEfficientVisionLanguageActionMan | Q10 latency | 7B VLA KV token reuse: 1.63-1.7x latency, -27% FLOPs, -0.3 pt LIBERO; naive reuse 84.4->74.2% | - relying on VLA inference tricks (too small a gain) | L
[wave3] W3_VideoGeneratorsareRobotPolicies | Q10 latency | ~9 s per chunk on A100 (SVD, 30 steps) | - video-generation policies for real-time | H
[wave3] W3_SharedExecutionClockDriftingPolicyforDyn | Q10 latency | conveyor 16 m/min: DP (252 ms) 0% vs 1-NFE policies 31-91% | + minimize inference latency / async | M
[wave3] W3_TowardsAccessiblePhysicalAILoRABasedFine | Q10 latency | 4-bit LoRA VLA on RTX 4060 8GB: 45 ms total, 20 Hz, 6.8 GB peak | + 2 s latency on 5060 likely config issue | L
[wave3] W3_WorldtoWristTaskConditionedFutureWristMo | Q10 latency | explicit CoT decoding 1550-1615 ms/chunk vs latent tokens 111 ms, same SR | - reasoning decoding at inference | M
[wave4] W4_0ResourceAwareRobustManipulationviaTamin | Q10 latency/smoothness | chunk-wise smoothing (drop stale + linear cross-fade) > sync/async/TE/RTC in most settings; +RTC best (figure only, π0.5, 3 garment tasks) | + async+crossfade | M
[wave4] W4_ImprovingGenerativeBehaviorCloningviaSel | Q10 | SG+adaptive chunking: +23.25% avg over DP, +12.27% over BID (6 sim tasks, 3 seeds); real SO-100 moving-cup 70%; BID 16 Hz halting vs ours 29 Hz smooth | + similarity-gated chunk switching / self-guidance | M
[wave4] W4_ImprovingtheperformanceofAIpoweredAfford | Q10 smoothness | TE removes jitter of small models but slows motion | ~ TE | L
[wave4] W4_LatentActionasIntentionEnablesEfficientF | Q10 | latency/chunk A800: 196.5 (Fast-WAM), 338.5 (LAWA), 593.1 ms (Joint-WAM) | - video-DiT WAMs for laptop | M
[wave4] W4_MINERVAHowSmallCanaManipulationPolicyBea | Q10 latency/smoothness | TE 96.3 > BID 95.0 > plain 94.1 > RTC 91.8; 0.54M L1: 2.2 ms GPU / 5.1 ms CPU vs SmolVLA 118/1010 ms | + tiny model + replan-every-step + TE | M
[wave4] W4_LookWhereItMattersAdaptiveVisualRefineme | Q10 | crop triggered ~30% of replans, ~1.4-1.6x compute | ~ uncertainty-gated extra compute | L
[wave4] W4_ASystematicStudyofDataModalitiesandStrat | Q10 | real jerky chunk boundaries fixed by uniform avg of last 4 overlapping chunks, 0.146 s latency (qualitative) | + temporal ensembling | M
[wave4] W4_BFAHierarchicalBestFeatureAwareTokenPrun | Q10 | pi0 real 5.8→9.4 Hz with 768→241 visual tokens, SR 0.27→0.48 (5 tasks x20) | + supervised token pruning for speed | M
[wave4] W4_ARWAMAVisualConditionedAgentReadyWorldAc | Q10 latency | 14.09 ms/chunk (4090) vs pi0.5 62 ms via KV-cache reuse | + compact flow w/ KV reuse | M
[wave4] W4_SEVOSemanticEnhancedVirtualObservationfo | Q10 latency | SmolVLA ~2 min/grasp on Orin NX, ACT real-time | - SmolVLA on edge | M
[wave4] W4_BitVLA1bitVisionLanguageActionModelsforR | Q10 latency | A100 latency: BitVLA 73ms, π0 86ms, DP 90ms, RDT 297ms, OFT+ 321ms | + low-bit inference for VLAs | M
[wave4] W4_MolmoAct2ActionReasoningModelsforRealwor | Q10 | CUDA Graphs + cache: flow VLA 23.0 -> 55.8 Hz on H100; discrete token path 3.94x slower | + CUDA-graph/caching of flow loop; continuous head for speed | H
[wave4] W4_BimanualManipulationWithinan8GBBudgetZer | Q10 latency | Orin Nano: FP32 114 ms -> TRT FP16 17.9 ms -> INT8 12.7 ms; success 19/18/19 of 20 | + TensorRT FP16 | M
[wave4] W4_CoLAFlowPolicyTemporallyCoherentImitatio | Q10 latency/smoothness | latency 8.6ms (latent flow) vs 6.5 raw flow vs ~30ms DP3/RDP (4080); smoothness −93.7% vs raw flow | + latent-space 1-step flow for smooth real-time; - raw 1-step flow | M
[wave4] W4_AugmentedRealityforRObotsARROPointingVis | Q10 latency | GroundingDINO+GPT-4o init + SAM2 tracking per frame; no latency reported | - extra perception in loop | L
[wave4] W4_DecouplingVisionLanguageandActionforEffi | Q10 latency | forward pass DEM 6.1 ms vs SmolVLA 99.3, pi0.5 103.3, GR00T 51.8 ms (RTX PRO 6000) | + decoupled small policy + 1-step head | H
[wave4] W4_ClutterRobustVisionLanguageActionModelst | Q10 | perception adds seg 0.04+VLM 0.41+depth 0.18 s; pi0 0.15 s; cycle 0.62-0.78 s | ~ cost of modular grounding | M
[wave4] W4_CronusVLATowardsEfficientandRobustManipu | Q10 latency | cached features 8.73 Hz vs naive multi-frame 3.09 Hz (7B) | + feature caching | M
[wave4] W4_SLIM05BLearningActionGroundedPredictiveL | Q10 | H100 latency 60.6 ms/4.26 GiB vs pi0.5 193 ms/7.94 GiB vs Fast-WAM 361 ms/13.6 GiB | + compact non-VLM flow policy for latency | M
[wave4] W4_DissectingMotionPriorRegularizationforDa | Q10 smoothness | 15 demos insertion: min-jerk loss 70/80 vs none 66/80 vs generic smooth 67/80 (CIs overlap); intra-chunk only | ~ jerk penalty small/non-sig, no boundary fix | L
[wave4] W4_DepthCacheDepthGuidedTrainingFreeVisualT | Q10 latency | π0.5 191→143 ms (1.33×), real 55/60→52/60; perturbation recovery 17.4→13.7 s | ~ token compression small gain; small model better for 2 s gap | L
[wave4] W4_ChronosAPhysicsInformedFullHistoryFramew | Q10 smoothness | pi0.5 stop-and-go jitter vs acceleration-field chunks smooth (qualitative); 1-step 84 vs 3-5 steps 90% | + second-order/smooth action parameterization | L
[wave4] W4_CTVAMACerebelloThalamicInspiredVisionAct | Q10 latency/async | FCI async: RTX 4080 56.8 ms fully hidden (20 Hz eff.), exec 8.33->6.41 s, success 100 vs 95% (20 trials); Jetson 200 ms, exec 10.24->7.23 s | + async + flow-consistent overlap inpainting | M
[wave4] W4_HoloBrain0TechnicalReport | Q10 latency/smoothness | SimpleRTC async (prefix inpaint first d steps + blend) beats sync on cloth folding; teacher-forcing 5% hurts, 25% default | + async + prefix-inpainting + TF training | M
[wave4] W4_HybridFlowA2NFEGenerativePolicyforRealTi | Q10 latency | Jetson Thor action-gen 19ms vs 152ms (DDIM-16); static PP 86.3 vs 63.8 under async execution | + minimize action-generation latency even for static tasks | M
[wave4] W4_FastinSlowADualSystemFoundationModelUnif | Q10 latency | slow:fast 1:1 0.60 / 1:2 0.63 / 1:4 0.69 / 1:8 0.61; 21.9 Hz vs pi0 13.8 Hz | + dual-rate (slow features reused over steps) | L
[wave4] W4_LiMABridgingLongtermImaginationtoRealtim | Q10 latency | H100 chunk latency: Cosmos-Policy 600 ms vs LiMA 325 ms; w/o async 450 ms same SR 80% | - video WAMs for laptop; + async slow/fast split | M
[wave4] W4_FLASHEfficientVisuomotorPolicyviaSparseS | Q10 | C1-continuous Legendre chunks: tracking err 4.7x lower than FM-DiT (spikes at chunk boundaries); 31.4 ms per episode inference | + continuity-constrained chunk param. | M
[wave4] W4_JEPAPolicyDiffusionFreeImitationLearning | Q10 latency | 13.2 ms (2 pass) vs 439.5 ms DP-100; real median 20 ms vs 316 ms | + few-pass heads | M
[wave4] W4_FoundationandSmallModelsCoordinationforV | Q10 latency | SAM3 15 ms/prompt, DA3 52 ms/frame on RTX 4060 Ti | ~ acceptable perception overhead | L
[wave4] W4_MResTMultiResolutionSensingforRealTimeCo | Q10 latency | real insert: 5Hz 45.0, 20Hz 62.5, multi-rate 67.5; sim dynamic 4.2/12.2/73.6 | + multi-rate cached slow encoder + fast head | M
[wave4] W4_PocketDP3EfficientPocketScale3DVisuomoto | Q10 latency | 2-NFE PocketDP3 4.2-4.8 ms vs DP3 51.4 ms vs DP 460 ms; real inference on RTX 4060 | + tiny 3D policy with 2-step sampling | H
[wave4] W4_PatchPolicyEfficientEmbodiedControlviaDe | Q10 latency | VQ-BeT DINOv2 11 ms, ACT 8.6 ms, OFT 62 ms, DP ~420–450 ms (H200) | + single-pass/few-step heads | M
[wave4] W4_SemanticVLASemanticAlignedSparsification | Q10 latency | visual tokens 256→32: LIBERO 97.7 (vs OFT 97.1), 8.45→2.37 TFLOPs, 0.134→0.089 s; 32× pruning → 92.0 | + prune visual tokens ~8× | L
[wave4] W4_TheGateNottheCacheGateProvenanceBoundsth | Q10 latency | token skipping: -18-22% latency; self-harvested gate at 0.9 skip -> success 0.68/0.31 vs dense 1.00; refresh -> 0.98 | - token skipping as main latency fix; + compute next chunk during execution | M
[wave4] W4_TheGateNottheCacheGateProvenanceBoundsth | Q10 async | one-step observation delay (dense) -0.08 success on LIBERO-Spatial | ~ stale obs in async costs success | L
[wave4] W4_ReflexEnablingFastandPredictiveVisionLan | Q10 latency/async | SmolVLA: async < sync at low inference Hz, > sync near 20-30 Hz (fig); batched enc + CUDA Graph 125 -> 65 ms, SR 71.7 -> 73.8 | + cut latency first, async only when fast | M
[wave4] W4_UniVLALearningtoActAnywherewithTaskcentr | Q10 latency | OpenVLA 0.18 s/step (0.68 s/4-chunk) stutter -> 38.3% real avg | ~ latency hurts real performance | L
[wave4] W4_TaskPrototypeGuidedFlowMatchingforFewSho | Q10 latency | SO-101 ResNet-18 flow policy, H=16, 8 ODE steps: 54.3 ms, 3.9 GB, 10 Hz | + small flow policy fits 8 GB budget | L
[wave4] W4_TraceGenWorldModelingin3DTraceSpaceEnabl | Q10 latency | 3D-trace planning 3.8x faster than trace baselines, >50x than video-gen models | ~ trace space cheaper than pixel world models | L
[wave4] W4_GaussianDreamEfficient3DGaussianWorldMod | Q10 latency | pi0.5 286 ms vs 330 ms per chunk with 20 extra tokens (training heads removed) | ~ | L
[wave4] W4_GlobalPriorMeetsLocalConsistencyDualMemo | Q10 latency/smoothness | flow init from retrieved trajectory prior: NFE 10 -> 3.2 (LIBERO 98.6 vs 96.9); real 85.0 vs 75.0 with 2.9x speedup | + informed prior / fewer NFE | L
