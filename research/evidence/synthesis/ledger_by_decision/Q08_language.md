# Q08_language — 48 ledger lines
[fulltext] BAKU | language | FiLM vision >= unconditioned | + FiLM | M
[fulltext] OFT | language | no FiLM → language following at chance (33%) with wrist cams | + FiLM essential | H
[fulltext] WhatMattersLanguageIL | Q08 language | frozen MiniLM-L3 SBERT 2.64 avg len > Distilroberta-SBERT 2.50 > CLIP 2.42 > MPNet-SBERT 2.24 > BERT 2.03 > MPNet 1.92 (CALVIN D) | + small sentence-embedding encoder | M
[fulltext] WhatMattersLanguageIL | Q08 language | CLIP-style contrastive video-language loss 2.64 vs none 2.29 vs regression 2.45 | + contrastive alignment aux loss | L/M
[fulltext] RT-1 | Q08 language | USE embedding → identity-init FiLM in ImageNet EfficientNet; RT-1 97/76 seen/unseen vs Gato late-fusion 65/52 (same data) | + frozen sentence enc + zero-init FiLM early fusion | M
[fulltext] MDT | Q08 language | frozen CLIP text token + CLA: LIBERO (2% labels) avg 68.5→73.1 | + frozen text token; + contrastive alignment for sparse labels | M
[fulltext] RoboAgent-MT-ACT | language | FiLM vs concat: −5–10% without FiLM | + FiLM | M
[fulltext] LBM-CarefulExamination | Q08 language | non-finetuned LBM with small CLIP text encoder executes wrong task in ambiguous scenes | - small frozen text encoder w/o finetune | M
[fulltext] OpenVLA | Q08 language | OXE pretraining helps mainly multi-object language-grounded fine-tunes; DP wins narrow tasks | ~ language/VLA only needed for multi-object tasks | M
[fulltext] KnowledgeInsulation | Q08 language | gradients from fresh expert erode language following; stop-grad or VLM co-training restores | ~ only if multi-task language | M
[wave3] W3_DiffusionVLAGeneralizableandInterpretabl | Q08 language | reasoning injection ablation in-dist avg 83.6 vs 50.3 | + richer language conditioning in VLA | L
[wave3] W3_GeneralizableVLAFinetuningviaRepresentat | Q08 language | BC picks trained green mug 90% under 'pink mug' instruction; VQA co-training+KI PRO 43.8 < BC 61.0 | - naive co-training | M
[wave3] W3_GoalRepresentationsforInstructionFollowi | Q08 | LCBC on 7k labeled trajs: 0% on unseen instructions; CLIP transition-aligned GRIF best; goal-image CLIP alignment fails (figure only) | ~ language for few fixed tasks only; novel instructions need big data | L
[wave3] W3_Instructiondrivenhistoryawarepoliciesfor | Q08 language | CLIP token seq 86.3% vs BERT 40.2% vs GloVe ~1.7% unseen push-buttons; pooled sentence embedding drops; no-instruction multi-task 64.2 vs 83.3 | + token-level CLIP-style text + cross-attn | M
[wave3] W3_CLIPortWhatandWherePathwaysforRoboticMan | Q08 language | multi-task > single in 41/72 evals; unseen-color transfer 45.8->75.7; language fused into spatial stream very poor; real bias exploitation | + multi-task language, keep lang out of low-level spatial features, balance data | M
[wave3] W3_RTTrajectoryRoboticTaskGeneralizationvia | Q08 language | unseen skills: language RT-1 16.7%, RT-2 11.1%, goal-image 26%, trajectory sketch 2.5D 67% (73K demos) | - expecting language to generalize to new motions | L
[wave3] W3_BeyondAppearanceShiftsTaskSemanticAction | Q08 language | pi0.5 target-object swap still does old task 34%; real PiPER frozen changed-task success 10-24% vs 39-65% calibrated | - relying on language alone for object discrimination | M
[wave3] W3_SPOCImitatingShortestPathsinSimulationEn | Q08 | multi-task language IL 49.9 vs single-task 50.0 | + multi-task language conditioning has no penalty at scale | L
[wave3] W3_VisionBasedMultiTaskManipulationforInexp | Q08 | multi-task one-hot vs single-task: better on T2-T5, worse T1 (36->16%); single-task overfits | + multi-task sharing | L
[wave3] W3_ADualProcessVLAEfficientRoboticManipulat | Q08 language | VLM latent task embedding 0.573 vs CLIP text 0.476 (multi-task sim) | + VLM-derived task embedding | L
[wave3] W3_LIVLanguageImageRepresentationsandReward | Q08 language | jointly aligned VL encoder > vision encoder + separate LM for multi-task LCBC (figure only) | + aligned VL encoder for multi-object language | L
[wave3] W3_AtomicMotionCoordinateforLanguageSteerab | Q08 language | fine-tuned pi0.5: language-only steering separation 39.1/24.0%; OOD fruit progress 60.5 -> 87.8 with FK-grounded coordinate (50 trials) | - relying on language alone to redirect visual motor prior | L
[wave3] W3_PerceiverActorAMultiTaskTransformerforRo | Q08 language | CLIP-conditioned multi-task agent; no-language ablation -> chance | + language needed only when variations ambiguous | L
[wave3] W3_BAKUAnEfficientTransformerforMultiTaskPo | Q08 language | FiLM ResNet .90 vs no FiLM .87 (LIBERO-90); text .90 ~ goal image .88 | + FiLM text conditioning | M
[wave3] W3_BCZZeroShotTaskGeneralizationwithRobotic | Q08 language | frozen sentence emb + FiLM 40% vs one-hot 42% on train tasks; 32% zero-shot held-out | + frozen text encoder + FiLM | M
[wave3] W3_VisionLanguageFoundationModelsasEffectiv | Q08 language | GPT-4 paraphrases: 1.85 -> 2.12 with frozen embedding layer | + freeze text embeddings | L
[wave3] W3_VIMAGeneralRobotManipulationwithMultimod | Q08 language | sim primitives: xattn prompt conditioning > GPT concat at small sizes; T5 30M/111M/368M no significant difference (figure only) | + small frozen text encoder w/ cross-attn/FiLM | L
[wave3] W3_UsingBothDemonstrationsandLanguageInstru | Q08 language | sim multi-task: FiLM(demo)+concat(lang) 25.8 / FiLM(both) 22.4 vs concat(both) 7.9; miniLM/DistilBERT ~25-27 vs frozen CLIP ~11 | + FiLM conditioning, small frozen LM | L
[wave3] W3_vlasimdEfficientCPUInferenceforLanguageC | Q08 language | SO-101: no-language multi-task ACT 20% vs IMPACT (FiLM+T5 tokens) 60-90%; LIBERO shuffle 91% new goal | + FiLM + cached text tokens | M
[wave3] W3_DecouplingtheDeclarativefromtheProcedura | Q08 language | real SO-101, 16 demos/pair: skill transfer w2VLA 91.7 vs OTTER 30.6 vs pi0.5 38.2 (seen ~94-96 all) | + FiLM with frozen CLIP localization heatmap (where) then skill (what) | M
[wave3] W3_DSWAMADualSystemWorldActionFoundationMod | Q08 language | subtask-level instructions: 75.7% -> 100% SR, mistakes 3.53 -> 0.65 per rollout (sorting) | + decompose multi-step language into subtasks | L
[wave3] W3_SutureBotAPrecisionFrameworkBenchmarkFor | Q08 conditioning | point-label goal overlay: ACT insertion error 1.3 mm vs 3.2 no goal; pi0 1.0 vs 3.9 | + image-space goal marks for placement precision | L
[wave4] W4_3DCAVLALeveragingDepthand3DContexttoGene | Q08 | w/o CoT-expanded instruction 42.4 vs 45.2 unseen LIBERO | + LLM step decomposition in instruction | L
[wave4] W4_MINERVAHowSmallCanaManipulationPolicyBea | Q08 language | task-ID embedding matches language VLAs; permutation → 6.5% | + task ID for closed task set | M
[wave4] W4_ASystematicStudyofDataModalitiesandStrat | Q08 | robot-only VLA training loses all language generation / VLM benchmark ability; VL co-train (9:1) restores | - robot-only finetune of VLM when language needed | M
[wave4] W4_ARWAMAVisualConditionedAgentReadyWorldAc | Q08 language | RoboTwin avg SR: bbox+skill token 87.2 vs text 74.2 vs box+text 84.6; AdaLN 87.2 vs cross-attn 73.4 | + spatial prompt / AdaLN, - raw text | M
[wave4] W4_DecouplingVisionLanguageandActionforEffi | Q08 language | none 11.3, one-hot 37.4, T5 44.5, BERT 47.8, NeoBERT frozen 55.6, Gemma2 55.0 (held-out paraphrases) | + frozen modern text encoder, cached tokens | M
[wave4] W4_ClutterRobustVisionLanguageActionModelst | Q08 | fine-tuned pi0/pi0-FAST/pi0.5 grasp absent-target >75% (ignore instruction); OBEYED ~95% rejection | - relying on VLA FT for language grounding | H
[wave4] W4_DecouplingSemanticsandGeometricGrounding | Q08 language | real Aloha 100 demos: SVP-IL (SAM3 mask feature-fusion into DP) 60.0 vs π0 FT 31.7 vs DP 28.3; sim custom lang tasks 39.5 vs π0 24.0 vs ACT 2.8 | + decoupled segmenter-mask grounding over end-to-end language | M
[wave4] W4_EasyMimicALowCostFrameworkforRobotImitat | Q08 language | LC 4-combo task 0.40 (20 robot) -> 0.90 (co-train) | ~ language ok w/ pretrained VLA | L
[wave4] W4_InContextVLAEndowingVisionLanguageAction | Q08 language | LIBERO: generate CoT 81.5 (359 ms) vs inject evidence action-only loss 97.4 (73 ms) | - generative CoT; + injected grounded text | M
[wave4] W4_CTVAMACerebelloThalamicInspiredVisionAct | Q08 language | one-hot task token instead of LM, LIBERO 82.1 | + compact task token for few tasks | L
[wave4] W4_LightsCameraMalfunctionWhenIlluminationR | Q08 language | color-dependent 240 demos: SmolVLA+CG 97.5%, π0.5+CG 55.0% (66.7% failures wrong color) | ~ color grounding needs color-preserving aug; SmolVLA fine | M
[wave4] W4_InterleaveVLAEnhancingRobotManipulationw | Q08 language | SimplerEnv OOD avg text pi0 40.9 vs image+text 60.7; real Lift 36.1 vs 69.4% (12 trials/object) | + image-of-target conditioning for novel objects | L
[wave4] W4_MoEACTScalingMultiTaskBimanualManipulati | Q08 | decoder FiLM task conditioning: 53.1→62.0 avg over 16 sim tasks (50 trials each) | + FiLM task conditioning for multi-task | M
[wave4] W4_WhatMattersWhenDiagnosingandImprovingCon | Q08 language | target-crop prompt swap redirects selection 0-1%→35-91%; π0.5 routing 5/10→10/10 with cue | + visual target prompts for disambiguation | L
[wave4] W4_SSIPolicyLearningStructuredSceneInterfac | Q08 language | GroundingDINO layout from instruction + tracks; motion+layout Goal 81.5 vs motion-only 58.7-77.8 | + language-grounded layout maps | L
[wave4] W4_StageACTStageConditionedImitationforRobu | Q08 conditioning | stage GT 60% vs constant/random stage 0% (human gives stage at test time) | + one-hot subtask conditioning | L
