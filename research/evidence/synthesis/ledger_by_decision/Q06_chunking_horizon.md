# Q06_chunking_horizon — 65 ledger lines
[fulltext] ACT | chunking | k=1→1%, k=100 (2 s @50Hz)→44%; TE +3.3% | + chunk ~1-2 s + TE | H
[fulltext] DiffusionPolicy | chunking | execute 8 of 16 @10Hz optimal; latency tolerant ≤4 steps | + | H
[fulltext] BAKU | chunking | LIBERO -14% without | + | H
[fulltext] RTC | chunking | shorter execution horizon better when continuity handled | + frequent re-query | M/H
[fulltext] ActionSpaceStudy | chunking | absolute likes long exec horizon; delta shorter | ~ | M
[fulltext] VQ-BeT | Q06 chunking | receding-horizon open-loop "fails completely" on low-cost robot (OOD within 3 steps); chunking hurt VQ-BeT | - long open-loop chunks on cheap arms | M
[fulltext] StreamingFlowPolicy | Q06 chunking | exec chunk peak 8 (3/4 envs) or 6 of Tpred 16 | + exec ~half of predicted | M
[fulltext] DiffusionTransformerPolicy | Q06 chunking | pred length 2→32: 40.8→65.8; exec 1 vs 16 steps: 61.6 vs 58.0 | + long prediction, short execution | M
[fulltext] SmolVLA | chunking | re-query every 1/10/30/50 steps: 80.3/82.8/70.8/51.8; chunk 10 best (84.0) | + short exec horizon, chunk 10-50 | M/H
[fulltext] BidirectionalDecoding | chunking | open-loop chunk collapses with noise (64->13) vs closed-loop (49->30); longer context hurts, longer horizon helps | + long pred horizon, frequent re-query | M
[fulltext] RoboAgent-MT-ACT | chunking | chunk 20 (4 s @5 Hz) best; 10 −5%; 40 >−20% | + moderate chunk | M
[fulltext] RoboVLMs-WhatMatters | Q06 execution | unseen scenes: execute full chunk 3.68 > ensemble 3.14 > first action 2.45 | + full-chunk execution | M/H
[fulltext] Octo | Q06 chunking | chunking helps coherence; ALOHA best = chunk 64 exec 12 receding horizon; temporal ensemble no benefit | + chunk + receding horizon, ~ temporal ensemble | L/M
[fulltext] RDT-1B | Q06 chunking | Ta=64 with DPM-Solver++ 5 steps: 6 chunks/s, 381 actions/s on RTX 4090 (not ablated) | ~ long chunk + fast solver | L
[fulltext] CogACT | Q06 chunking | future steps 0/3/15/31 → avg 42.8/55.5/62.5/51.2 | + chunk ~16 (1–3 s), - very long chunks | M
[fulltext] pi0 | Q06 chunking | H=50, execute 16 @20Hz / 25 @50Hz open-loop; temporal ensembling "hurt" (no number) | + ~1-2.5 s chunk, execute ~half, no TE | M
[fulltext] FAST | Q06 chunking | 1 s chunks all rates; DROID 15 @15 Hz, execute 8–15 (not ablated) | ~ | L
[fulltext] GR00T-N1 | Q06 chunking | H=16 @20 Hz with K=4 Euler steps across all embodiments (not ablated) | + ~0.8 s chunk, few flow steps | L/M
[wave3] W3_IMLEPolicyFastandSampleEfficientVisuomot | Q06 chunking | Tp=16/Ta=8/To=2 used; no sweep | ~ | L
[wave3] W3_TubeDiffusionPolicyReactiveVisualTactile | Q06 chunking | open-loop DP chunks fail under disturbance; streaming-only (no chunk gen) drops Push-T 96.1->84.3, grasp 88->44% | - pure open-loop chunks; + chunk + step-wise correction | M
[wave3] W3_FurnitureVLALearningLongHorizonBimanualF | Q06 | pi0.5 sim avg: no TE 0.65, exp-weighted TE lambda=-0.1 0.80, uniform TE 0.62; exec 5/10/25 of 50: 0.60/0.74/0.67 | + recency-weighted TE, execute ~20% of chunk | M
[wave3] W3_HermiteCurvesasTrajectoryPriorsforVision | Q10 chunk-boundary smoothness | Hermite aux loss: real seam jump 0.48-0.72x of pi0.5; real SR 63.4 -> 90.0 (4 tasks x 15); zero inference cost (48.6 vs 48.4 ms) | + training-time trajectory smoothness regularizer | M
[wave3] W3_HermiteCurvesasTrajectoryPriorsforVision | Q06 chunking | T=50/W=20 at 30 Hz; handover jumps 5.5-8.6x interior steps for all methods | ~ seams inherent; execute < half chunk | M
[wave3] W3_LanguageConditionedImitationLearningWith | Q06 chunking | latent skill length Nh 4/5/6 -> 1.58/1.71/1.65 | ~ insensitive | L
[wave3] W3_ActFoveaRuntimeSafeguardingforVLAPolicie | Q06 chunking | fixed shorter executed prefix: drift 83.1->89.9, clean 93.0->91.7, but delay 76.2->70.7 | + shorter execution horizon vs drift | M
[wave3] W3_GoalConditionedDualActionImitationLearni | Q06 chunking | open-loop full trajectory in precise phase: GraspNeck 0.000 vs reactive 0.933 (15 trials) | - long open-loop execution near contact | L
[wave3] W3_RaCRobotLearningforLongHorizonTasksbySca | Q06 chunking | 1 s flow chunk, execute 0.5 s, replan (not ablated) | ~ | L
[wave3] W3_SnapFlowOneStepActionGenerationforFlowMa | Q06 chunking | n_act of 50: 1→77/72%, 5→90/93%, 20→97/92% (libero_10) | - replanning every step | M
[wave3] W3_TowardsSynergisticGeneralizedandEfficien | Q06 chunking | specialist chunk 8 + exponential temporal aggregation m=0.1 + DDIM 5 steps (no ablation) | ~ | L
[wave3] W3_WhyDoesActionChunkingImproveBehavioralCl | Q06 | DP success Markov/AC/Delay/AC-RDE: LIBERO-10 19.8/88.7/86.8/88.5; ToolHang 28.0/75.2/51.6/71.8; real 3 tasks x 50 rollouts RDE >= AC (fig) | + chunking (benefit = past-obs prediction + implicit ensemble) | H
[wave3] W3_WhyDoesActionChunkingImproveBehavioralCl | Q06 | uniform temporal ensemble ToolHang 42.2 vs AC 75.2 vs randomized-delay 71.8 | - uniform TE; + randomized-delay/recency schemes | M
[wave3] W3_RethinkingthePracticalityofVisionlanguag | Q06 chunking | CALVIN chunk 1/5/12/20 -> AvgLen 2.25/3.68/3.35/0.70 | + short chunk for AR token model | L
[wave3] W3_AnchorVLA4DanAnchorBasedSpatialTemporalV | Q06 chunking | xLerobot: pi0.5 better with executing 50-step chunk than 5 (no numbers); AnchorVLA exec 5 of 50 at 300ms -> 17 Hz | ~ | L
[wave3] W3_ContinueorReplanBernoulliContinuationPol | Q06 chunking | fixed 50-step horizon, only phase shifted: SR 82.5% worst vs 93.7% best; adaptive replanning real 74->92%, 44->84%; fixed 20/30/40 not better than 50 | + stage-adaptive execution horizon (replan before contact) | M
[wave3] W3_OneACTPlaySingleDemonstrationBehaviorClo | Q06 chunking/TE | std-adaptive TE: stack 60.8 -> 78.4 (400 demos, sim) vs ACT exponential TE | + disagreement-aware ensembling | L
[wave3] W3_OrderedActionTokensforVisuomotorPolicyLe | Q06 chunking | at fixed token count, success drops as Ha grows 8->64 (LIBERO-Long, figure) | ~ chunk length bounded by representation capacity | L
[wave3] W3_DEFLECTTemporalCounterfactualPreferenceL | Q06 chunking | RTC/BID need overlap (chunk - delay) > ~3 steps or they collapse | + longer chunk under async | M
[wave3] W3_DynamicExecutionHorizonPredictionforChun | Q06 chunking | peg insertion (state DP, H=16): fixed exec 6 71.5% -> DEHP 93.2%; under action noise 0.15 exec 2 > exec 6; one-leg best fixed 70.3 -> 95.2% | + short/adaptive execution horizon near contact, esp. with actuation noise | M
[wave3] W3_BAKUAnEfficientTransformerforMultiTaskPo | Q06 chunking | LIBERO-90 chunk10 .90 vs no-chunk .76; DMC .70 vs .74 | + chunking + temporal ensembling for manipulation | H
[wave3] W3_pimathbfR2ReactiveRealtimeFlowPolicies | Q06 chunking/TE | naive async + temporal ensembling smoother but loses precision; flow degrades as exec horizon h grows 1->8 (sim) | - TE under async; + short exec horizon for reactive tasks | M
[wave3] W3_KnowingWhentoStopAdaptiveActionChunkingv | Q06 chunking | fixed exec horizon sweep: pi0.5 RoboTwin 61.6(10)->52.2(25); X-VLA 43.5(15)->76.1(30); real pi0.5 41.7-51.7 peak at 30 steps@20Hz; adaptive entropy truncation 62.9/79.0/61.7 | + tune/adapt execution horizon per model (~1-1.5 s) | M
[wave3] W3_StartRightArriveRightAsynchronousExecuti | Q06 chunking/TE | pi0 H=50: TE SR 0.10-0.20 vs RTC/PAINT 0.50-0.65, completion 58s vs 15s | - temporal ensembling for long-chunk VLAs | M
[wave3] W3_TrainOfflineTestOnlineARealRobotLearning | Q06 chunking | 50-step (1.7 s @30Hz) chunks beat per-step closed-loop and full open-loop (stated, no numbers) | + chunking | L
[wave3] W3_WaypointBasedImitationLearningforRobotic | Q06 chunking | ACT sim human insertion 20->30, cube 50->71 with 7-10x shorter horizon; chunk 100->50 steps to keep wall-clock | + shorten decision horizon; size chunks in seconds | M
[wave3] W3_vlasimdEfficientCPUInferenceforLanguageC | Q06 chunking | H=50-100 @30Hz covers CPU latency; H=4 (Octo) fails budget | + chunk >= latency x2 | M
[wave3] W3_ChainVLAChainingVisionLanguageActionQuer | Q06 chunking/TE | FIFO history + temporal ensembling 35.6 vs 62.8; TE 0/0% on two tasks | - temporal ensembling as fix | M
[wave3] W3_DenoisingTellsWhentoReplanDenoisingVaria | Q06 chunking | real 50 demos/task, 30 trials: execute 40 vs 15 steps: 0.53 vs 0.80, 0.43 vs 0.70, 0.23 vs 0.43 | - long fixed open-loop execution | M
[wave3] W3_MimicIntentNotJustTrajectories | Q06 chunking | chunk 8/16/32/64 -> LIBERO-Long 80.6/93.2/86.6/87.4; ensemble none 85.8, TE 89.2, intent-weighted 93.2 | + mid chunk (~16 steps) + similarity-weighted ensembling | M
[wave3] W3_RealtimeVLAFLASHSpeculativeInferenceFram | Q06 chunking | draft-only (stale context) LIBERO-10 58.4 vs 85.2 full; periodic refresh PF=2 restores 80.6 | - long open-loop/stale execution; + frequent refresh | L
[wave3] W3_SharedExecutionClockDriftingPolicyforDyn | Q06 chunking | H=16 execute 8 @20Hz (0.4 s) across 4 real tasks, 300 trials | ~ half-chunk execution works | L
[wave4] W4_FP3A3DFoundationPolicyforRoboticManipula | Q06 | chunk 16 / execute 8 at 15 Hz; no ablation | ~ | L
[wave4] W4_ImprovingGenerativeBehaviorCloningviaSel | Q06 | EMA temporal ensembling 0.456 vs vanilla 0.496 Push-T; EMA below vanilla on real SO-100; EMA lambda task-sensitive | - temporal ensembling with diffusion heads | M
[wave4] W4_MINERVAHowSmallCanaManipulationPolicyBea | Q06 chunking | chunk 16 best; 8: -3.16, 32: -2.20; exec 1-2 steps > 4 > 8 | + chunk ~0.8s, execute 1-2 + TE | M
[wave4] W4_BimanualManipulationWithinan8GBBudgetZer | Q06 chunking | chunk 100 fully executed (10 s open loop @10Hz) -> 95% on quasi-static task | ~ long exec horizon ok for static pick-place | L
[wave4] W4_RefinementofAcceleratedDemonstrationsvia | Q06 | erasing ~65% vs better direct playback; temporal ensembling suspected to damp corrections (no ablation) | - temporal ensembling for fast reactive motion | L
[wave4] W4_DecouplingVisionLanguageandActionforEffi | Q06 chunking | H16/replan8 55.6, H8/4 55.9, H4/2 52.7, H1 50.6 | + chunk 8-16 replan half; per-step only -5 | M
[wave4] W4_ClutterRobustVisionLanguageActionModelst | Q06 | 10 Hz exec horizon H=5/10/15/20 → pick-place 81/85/76/56 | + ~1 s execution horizon | M
[wave4] W4_E0EnhancingGeneralizationandFineGrainedC | Q06 chunking | action horizon 10–20 steps best on LIBERO (fig) | ~ moderate horizon | L
[wave4] W4_CTVAMACerebelloThalamicInspiredVisionAct | Q06 chunking | H=8, overlap 4 @20 Hz with 30 demos real; not ablated | ~ short chunk + overlap | L
[wave4] W4_FastinSlowADualSystemFoundationModelUnif | Q06 chunking | H=1/2/4/8: 0.69/0.68/0.66/0.69 on keyframe RLBench | ~ chunk size irrelevant for keyframe actions | L
[wave4] W4_FLASHEfficientVisuomotorPolicyviaSparseS | Q06 | sparse stride k=1 24% → k=4 96%, k≥13 collapse (Stack Cube) | + long bounded horizon | M
[wave4] W4_LatentPolicySteeringAnEfficientandFlexib | Q06 chunking | horizon 4–16 OK, 24 degrades LPS (Can) | ~ | L
[wave4] W4_SynthICLScalableIncontextImitationLearni | Q06 chunking | real precision task: temporal ensembling 15/20 vs direct exec H=1/2/4/8 12/13/13/11 of 20 | + temporal ensembling | L
[wave4] W4_ReflexEnablingFastandPredictiveVisionLan | Q06 chunking | at 30 Hz async: bigger chunk (8-16) with short executed horizon (1-4) best (fig only); default chunk 8 exec 2 | + predict long, execute short | L
[wave4] W4_StageACTStageConditionedImitationforRobu | Q06 chunking | ACT chunk 100 steps (~3 s) + TE at 30 Hz used on real humanoid, no ablation | ~ | L
