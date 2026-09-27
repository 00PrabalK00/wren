# Final synthesis: a small, robust, real-time SO-101 manipulation policy

Evidence base: 480 full-text notes (fulltext/notes 65, wave3/notes 252, wave4/notes 120, realtime/notes 43), 1,458 ledger findings (synthesis/ledger_by_decision), 3,133 abstract-level cards (synthesis/cards_by_decision), and the two real-time reports (realtime/TRACK_A_REPORT.md, realtime/TRACK_B_REPORT.md). Every number below is quoted from a note, ledger line or report and the source file is given in brackets. "Figure only" means the paper gave no table. Confidence: H/M/L. Weighting: real robot > sim; controlled ablations; low-cost arms (SO-100/101, Koch, Piper, AgileX); 20–150 demos; 8 GB-class compute.

Notation used throughout: N = note path relative to the litreview directory. Shorthand F=fulltext/notes, W3=wave3/notes, W4=wave4/notes, RT=realtime/notes.

---

## 1. Executive summary

### 1.1 The recommended policy in one paragraph

Build a ~55M-parameter, LeRobot-native policy: a pretrained DINO-family ViT-S image encoder (shared across the RealSense scene camera and the wrist camera, fine-tuned end-to-end at 10× lower LR than the rest, spatial patch tokens kept, never pooled to a CLS), a ~20M transformer trunk over [scene tokens, wrist tokens, one proprio token], and a ~10M flow-matching action expert (DiT-style, cross-attention to the observation tokens, per-token flow time so it can be trained with prefix conditioning) that predicts a chunk of ~1.6 s of absolute leader-joint targets and is executed asynchronously with a 0.5–0.8 s execution horizon. Training uses strong but hue-preserving photometric augmentation, random crop/shift plus small perspective warps on the scene camera, background replacement (green screen or offline segmentation masks), scene-camera token dropout, proprio noise/dropout, VLASH-style state-offset augmentation and training-time prefix conditioning (TT-RTC) so that chunk boundaries are continuous without any blending. Data: 100–150 demos recorded at 30 fps, spread deliberately over 4–6 pumpkins, 3–4 lighting conditions, 3–4 backgrounds, small camera re-positions between sessions, distractors, and 15–25% in-episode recovery demos, with one operator using one consistent strategy. A depth/object-centric branch and a language path are staged add-ons, not v1. The execution stack is a timestamped 100 Hz servo executor, an async policy loop at ≥10 Hz re-query, a TIDE-style inter-chunk discrepancy monitor with conformal threshold, and rewind-to-checkpoint recovery.

### 1.2 Why (the ten findings that drive the design)

1. **Your 1.9 s SmolVLA latency is a deployment problem, not a model property.** Independent measurements: 101 ms on a laptop RTX 5080 [RT/A2C2.md], 74/82 ms sim/real [F/ReactVLA.md], 19.7 ms optimised [RT/FlashVLA.md], 45 ms on an RTX 4060 8 GB with 4-bit LoRA [W3_TowardsAccessiblePhysicalAILoRABasedFine.md, low credibility]. Power mode alone is a 1.6× effect on the same chip [RT/JetsonPI.md]; CUDA graphs ~3× [RT/JetsonPI.md]; TensorRT FP16 6.4× for ACT [RT/QuantACT8GB.md]. Your eval_real.py loads the model in fp32 without compile and only requests the next chunk after the executed prefix is exhausted, so the arm starves during inference. Confidence H.
2. **The three real-arm failures (night lighting, different pumpkin, moved camera) are the three shifts that every small policy trained on one-scene clean demos fails, regardless of architecture.** RoboTwin 2.0: 50 clean demos, clean→randomised ACT 29.7→1.7, DP 28.0→0.6, DP3 55.2→5.0 [W3_RoboTwin20AScalableDataGeneratorandBench.md]; CRAFT real ACT 0–6/20 under unseen lighting/background/colour/camera [W3_CRAFTVideoDiffusionforBimanualRobotDataG.md]; on SO-101 specifically, SmolVLA 70→0% under a coloured spotlight with no augmentation [W4_LightsCameraMalfunctionWhenIlluminationR.md], SmolVLA 65.3→7.5% under camera viewpoint change even with a wrist camera [W4_InfiNoVAInfiniteNovelViewAugmentationfor.md], ACT/SmolVLA 75/70→30/35% in a novel-similar room and 0% in an extreme one [W4_SEVOSemanticEnhancedVirtualObservationfo.md]. Pretraining does not fix it (7B OFT 0% on a colour change [W4_ReShootGenerativeVisualDomainRandomizati.md]; π0 63→16% at 15° camera rotation [W4_FromFixedtoFreeCamerasCalibrationFreeVie.md]). Confidence H.
3. **Data diversity and targeted augmentation, not model tricks, are the primary robustness lever**, and each shift axis must be covered explicitly because factors transfer poorly across axes [W3_AStudyonEnhancingtheGeneralizationAbilit.md: camera-only randomisation hurt lighting .56→.28]. Diversity beats count: 50% vs 100% of demos per environment overlap once environments are many [F/DataScalingLaws.md]; on SO-101 varied backgrounds/lighting/distractors in the demos gave +9 to +23 pts and novel-room 30→85% [W4_SEVO...md]; multi-illumination demos 30→80% at 40 lux [W3_EVLAEventAugmentedVisionLanguageActionMo.md]. Confidence H.
4. **A pretrained, fine-tuned encoder with spatial tokens beats both frozen features and scratch CNNs for our shifts**, but only when fine-tuning is paired with augmentation and a small encoder. Frozen 0.00 / LoRA 0.72 / full FT 0.90 [F/DataScalingLaws.md]; frozen 32.6 vs FT 55.6 [W4_DecouplingVisionLanguageandActionforEffi.md]; FT without aug 46.5 vs FT+aug 73 [W3_WhatDoWeLearnfromaLargeScaleStudyofPreTr.md]; spatial tokens 78.9 vs CLS 50.0 [F/Theia.md]; mean-pooled DINOv2 0.40 vs tokens 1.00 [W3_CageCausalAttentionEnablesDataEfficientG.md]; scratch CNN lighting robustness 1–7% [W4_MINERVAHowSmallCanaManipulationPolicyBea.md]. Confidence M/H.
5. **Small models are enough for this task; ~100M+ from scratch overfits at 50 demos.** BAKU 4.4M/10M/31M ≈ same, 114M collapses (LIBERO-90 .19) [W3_BAKUAnEfficientTransformerforMultiTaskPo.md]; on SO-101 with 50 demos ACT 63% vs π0 70% vs π0.5 67% vs SmolVLA 23% on the pick-place task [W4_ArmnetBenchv01ParallelRealWorldEvaluatio.md]; ACT 52.6M reached 19/20 on bimanual SO-101 with 100 demos [RT/QuantACT8GB.md]. Confidence M/H.
6. **Use a generative (flow-matching) head, not plain L1, but the head choice is secondary to everything above.** Plain L1 chunk regression collapsed on human demos 35.3→2% [F/ACT.md]; diffusion 83 vs MSE 35 [F/Octo.md]; flow > L1 80.25 vs 75.25 [F/SmolVLA.md]; but heads are within 3.2 pts at large data [W4_DecouplingVisionLanguage...md] and L1 ≈ flow at 1M params on LIBERO [W4_MINERVA...md]. Flow is chosen because it also unlocks the async continuity fixes (RTC/TT-RTC/PAINT need a flow head [F/RTC.md, RT/TrainingTimeRTC.md]). Confidence M.
7. **Absolute leader-joint targets, not step-wise deltas, on this leader/follower rig.** Switching targets from leader positions to follower states cost 60→15, 50→25, 30→0 on contact tasks [W4_BeyondImplicitForceEvaluatingExplicitFor.md]; 1-step deltas at 10 Hz gave 3% vs 45% [W3_BCZZeroShotTaskGeneralizationwithRobotic.md]; the only pro-delta evidence at scale is chunk-wise delta with "marginal" gains [F/ActionSpaceStudy.md]. Confidence M/H.
8. **Do not blend or temporally ensemble chunks from a stochastic head; make the head continue the committed prefix instead.** TE/EMA hurt under stochasticity 18.4 vs 29.5 [F/BidirectionalDecoding.md], triggered protective stops at +100/+200 ms [F/RTC.md], EMA below vanilla on a real SO-100 [W4_ImprovingGenerativeBehaviorCloningviaSel.md]; on SO-101 with 50 demos naive async 17/20 → prefix-conditioned 20/20 with visibly less oscillation [RT/ActionControlNet.md]; training-time prefix conditioning equals RTC at zero inference cost [RT/TrainingTimeRTC.md]. Confidence M/H.
9. **Execution horizon matters as much as the continuity method: predict ~1–2 s, execute ~0.5–1 s, never 1 step, never the whole chunk.** SmolVLA executed 1/10/30/50 of 50 → 80.3/82.8/70.8/51.8 [F/SmolVLA.md]; real Fix15 0.800 vs Fix40 0.533 with 50 demos [RT/DenoisingVarianceChunking.md]; H=5/10/15/20 at 10 Hz → 81/85/76/56 [W4_ClutterRobustVisionLanguageActionModelst.md]. Confidence M.
10. **Wrist + scene cameras are both essential, and the wrist view is the robust anchor.** Real pickup 75.0 vs 7.5 (no wrist) vs 20.0 (no scene) [W4_MResTMultiResolutionSensingforRealTimeCo.md]; real Can 73.3 vs 43.3 without wrist [F/robomimic.md]; naive fusion can hurt OOD unless the scene stream is regularised (73.7 wrist-only vs 66.3 both vs 87.7 both + bottleneck) [W3_VisionBasedManipulatorsNeedtoAlsoSeefrom.md]. Confidence H for "keep both", M for the regularisation.

### 1.3 What changed versus the first naive plan (frozen DINOv2 + L1 + ~100M + blending)

| Naive plan | Recommendation | Why |
|---|---|---|
| Frozen DINOv2 | Pretrained DINO-family ViT-S, fine-tuned at low LR with augmentation, spatial tokens | Frozen 0.00 vs FT 0.90 [F/DataScalingLaws.md]; frozen DINOv2 is mid-pack even in frozen benchmarks [F/SPA.md, F/WhatMakesPVRsRobust.md]; frozen DINOv2-L got worse when fine-tuned only in Theia's one odd case [F/Theia.md] — a small ViT-S avoids the VC-1 collapse regime [F/VC-1.md] |
| L1 regression | Flow matching (5–10 Euler steps), optional CVAE latent | ACT CVAE ablation 35.3→2% on human data [F/ACT.md]; enables RTC/TT-RTC continuity [F/RTC.md] |
| ~100M params | ~55M total, ~35M trainable-from-scratch, small trunk (~20M) | BAKU 114M overfits at 50 demos [W3_BAKU...md]; "shrink the head, not the eyes" [W4_MINERVA...md] |
| Linear fade between chunks | Training-time prefix conditioning (TT-RTC) + VLASH state roll-forward; no blending | Averaging modes gives invalid actions [F/RTC.md]; naive async 17/20→20/20 on SO-101 with prefix conditioning [RT/ActionControlNet.md] |
| (implicit) clean single-scene data | Diversity-first protocol, 30 fps, recovery demos, background replacement | Finding 2–3 above |

### 1.4 Versus SmolVLA

SmolVLA's own gains come from in-embodiment pretraining plus multi-task training (single-task no-PT 40.0 < ACT 48.3; +PT and multi-task 78.3) [F/SmolVLA.md]; on harder SO-101 benchmarks it ties ACT (33.75 vs 32.5) [F/SO101-Benchmark.md] or loses to it (15.0 vs 19.2 pooled; 23 vs 63 on pick-place) [W4_ArmnetBench...md]. Its VLM is frozen, so the vision tower cannot adapt to a new camera rig (vision tower needs the highest adapter rank; LoRA r=8 gives 0–27% vs full FT 87–100% [W4_AdaptiveCapacityAllocationforVisionLangu.md]). It is lighting-fragile at one training illumination (100/65/30/0% at 100/75/40/30 lux) [W3_EVLA...md] and viewpoint-fragile (−88.5% relative) [W4_InfiNoVA...md]. Its async stack has no continuity mechanism and lost 20 pts on sorting when run async [F/SmolVLA.md]. A 0.2B LLM-free policy matched it at 31 ms/0.9 GB [RT/TurboVLA.md] and a 0.1B model with a fine-tuned ViT-S beat the 2.25B variant on LIBERO [W3_ProgVLAProgressAwareRobotManipulationSki.md]. Keep SmolVLA only as a fixed-latency baseline (Section 8, Stage 0).

---

## 2. Per-decision verdicts Q01–Q14

Weights: H = real robot, controlled, ≥20 trials/cell or large sim N; M = real but small n or sim controlled; L = figure-only, anecdotal, confounded, or far from our regime.

### Q01 Action head

**Verdict:** Flow-matching head over a ~1.6 s chunk, DiT-style (cross-attention to observation tokens, self-attention over action tokens, AdaLN flow-time), trained with per-token flow time. 10 Euler steps in training, 5–10 at inference. Optional ACT-style CVAE latent (z=0 at test) if we ever mix operators. Never per-dimension binning. Confidence M.

| Paper | Setting | Key number | Direction | Weight |
|---|---|---|---|---|
| ACT [F/ACT.md] | sim, 2 tasks, human demos, from scratch | CVAE→plain L1: 35.3→2% | − plain L1 on human data | M |
| DiffusionPolicy [F/DiffusionPolicy.md] | 15 tasks + real | +46.9% over LSTM-GMM/IBC/BeT; real Push-T 95 vs LSTM-GMM 20 | + generative | H |
| Octo [F/Octo.md] | WidowX, 40 trials | diffusion 83 vs MSE 35 vs 256-bin 18 | + diffusion, − MSE/bins | M |
| SmolVLA [F/SmolVLA.md] | LIBERO, frozen VLM | flow 80.25 vs L1 75.25 (long 53 vs 38) | + flow | M |
| FLOWER [F/FLOWER.md] | CALVIN | flow 4.44 vs L1 3.33 vs discrete 1.12 | + flow | M |
| RDT-1B [F/RDT-1B.md] | real, 8 trials | diffusion 50 vs regression 12.5 (unseen object) | + diffusion | L/M |
| StreamingFlowPolicy [F/StreamingFlowPolicy.md] | sim | same velocity field regression vs flow: Can 12.4 vs 95.6 | + noise-trained head | M |
| BAKU [W3_BAKU...md] | real xArm, 150 trials | VQ-BeT .91 vs MLP .86; sim MLP ≥ all | ~ multimodal head small real gain | M |
| HiFlow [W3_HiFlowTokenizationFreeScaleWiseAutoregre.md] | real HSR, 50 demos @10 Hz, 12 trials | flow 41.7–83.3 > DP 16.7–66.7 > ACT 8.3–50 | + flow at 10 Hz/50 demos | M (ACT possibly untuned) |
| EvoHIL [W3_EvoHILSelfEvolvingRewardandFlowMatchedPo.md] | real SO-101 | flow chunks vs per-step Gaussian: −44.5% action first-diff, −48–58% HF power | + flow chunk for smoothness | M |
| OpenVLA-OFT [F/OpenVLA-OFT.md] | 7B VLM, filtered LIBERO | L1 ≈ diffusion (authors credit capacity) | ~ L1 only with big backbone | M/H |
| VLA-Adapter [F/VLA-Adapter.md] | 0.5B VLM, LIBERO-Long | L1 95.0 vs DiT 91.6 | + L1 with rich conditioning | M (sim) |
| MINERVA [W4_MINERVA...md] | LIBERO sim, 3 seeds | flow→L1 +0.34 (within band), 3.8× faster | ~ head irrelevant at 1M | M (sim) |
| DEM [W4_DecouplingVisionLanguage...md] | RoboCasa, 500 demos/task | DP 53.8 / FM 54.7 / ACT 52.4 / MeanFlow 55.6 | ~ heads within 3.2 pts | M (sim, large data) |
| JEPA-Policy/MIP [W4_JEPAPolicyDiffusionFreeImitationLearning.md] | real ARX-5, 100 demos, sync loop | deterministic 2-pass MIP 54.7 vs DP-16 31.8 vs DP-100 18.7 | + deterministic iterative head | M (DP latency-confounded) |
| Chronos [W4_ChronosAPhysicsInformedFullHistoryFramew.md] | ALOHA sim insertion, 50 demos | regression 76 ≥ flow 72 > diffusion 66; IMLE 86 | ~ regression fine at 50 demos | L |
| QuantACT8GB [RT/QuantACT8GB.md] | real bimanual SO-101, 100 demos | ACT 19/20 vs LeRobot-default DP 0/10 | + CVAE/L1 converges on our budget | M (DP untuned) |
| MobileALOHA [F/MobileALOHA.md] | real, 50 demos | ACT 95 vs DP 65 (Wipe Wine) | + light head in low data | L/M |
| ArmnetBench [W4_ArmnetBench...md] | real SO-101, 50 demos | DP 26.7 vs ACT 19.2 pooled; ACT 63 vs DP 43 on pick-place | ~ task dependent | L |
| HybridFlow [RT/HybridFlow.md] | real Franka, 80 trials | 1-step MeanFlow 0/80, DDIM-2 0/80, DDIM-16 47–64, 2-NFE jump+refine 60–86 | − naive 1–2 step | M/H |
| Hyper-DP3/PocketDP3 [F/Hyper-DP3.md, W4_PocketDP3...md] | sim 5000 eps + real Piper | 2 DDIM steps 58.2 ≈ 10 steps 58.0; 1 step 53.0 | + 2–10 steps enough | M/H |
| Dita [F/Dita.md] | SimplerEnv | DDIM 100/50/20/10/5/2 → 76.4/79.1/85.5/85.3/82.7/70.4 | + ~10 steps; − 2 | M |
| XS-VLA [W4_TeachingTinyVLAModelsWheretoLookandHowto.md] | SmolVLA-0.25B, multi-operator real | flow + CVAE latent +4.6 LIBERO; real 21.7→65.0 (combined) | + CVAE latent on flow | M |
| DiffusionTransformerPolicy [F/DiffusionTransformerPolicy.md] | real Franka, 50 demos | 256-bin 19.3 vs MLP-diffusion 34.8 vs DiT 46.9 | − per-dim bins, + transformer denoiser | M |
| FAST [F/FAST.md] | π0 backbone | naive binning "no progress" at 20/50 Hz; AR decoding 750 ms vs flow <100 ms | − naive bins, − AR for latency | H |

**Adjudication of the generative-vs-regression conflict.** The results split cleanly by regime. Regression heads win or tie when (a) conditioning is very rich from a large pretrained backbone (OFT 7B, VLA-Adapter 0.5B with all-layer bridging, TurboVLA 0.2B with grounding-pretrained cross-attention [RT/TurboVLA.md]), (b) demos are unimodal/scripted (LIBERO, MINERVA), or (c) the regression head is iterative with training noise (MIP/JEPA-Policy). Generative heads win when demos are human, multimodal, multi-operator and the model is small and from scratch (ACT's own ablation, Octo, RDT, HiFlow at 10 Hz, C-BeT 24/50 vs 13/50 [W3_FromPlaytoPolicyConditionalBehaviorGener.md], ALOHA-Unleashed 70 vs 25 at scale [F/ALOHA-Unleashed.md]). Two further reasons tip us to flow: (1) on SO-101 the same head produced measurably smoother commanded motion than per-step Gaussian [W3_EvoHIL...md], and (2) every zero-cost async continuity fix (TT-RTC, PAINT, Legato, REMAC, StreamingDP) requires a flow/diffusion head with per-token time [RT/TrainingTimeRTC.md, RT/InitialNoiseSelection.md, F/Legato.md]. The ACT/CVAE-L1 family remains the safest-to-converge baseline on SO-101 (19/20 [RT/QuantACT8GB.md]; ACT 18M matched π0.5 on a 30-demo task [W3_WhatistheBetterCurriculumControllerShape.md]) and must be run as the baseline, but it is unimodal at z=0 and its chunk boundaries can only be smoothed by TE, which conflicts with Q06/Q10.

**Step count.** Do not cut to 1–2 steps without distillation/refinement: real collapses at DDIM-2/ReFlow-2/1-step MeanFlow [RT/HybridFlow.md], 5-step consistency student 38.3% vs 78.3% [W3_HybridConsistencyPolicyDecouplingMultiMo.md], DDIM-15 ToolHang .14 vs .79 [F/ConsistencyPolicy.md]. 5–10 Euler steps of a ~10M expert are ~free (10 steps of a 300M expert = 27 ms on a 4090 [F/pi0.md]); VLAPerf models 10→1 steps as only −26% end-to-end for a VLM-heavy model [RT/VLAPerf.md].

**Residual doubt / cheap ablation:** train the identical trunk with (a) flow head, (b) L1 head, (c) flow + CVAE latent on the same 100 demos; 20 in-distribution trials each plus 20 with a moved pumpkin. If L1 ties in-distribution and is smoother, keep flow anyway for async (Q10) unless TE-based ACT execution is chosen.

### Q02 Action space

**Verdict:** Absolute leader-joint targets (what LeRobot records), per-dimension quantile-normalised (1–99% → [−1,1]); gripper as a continuous absolute value. First ablation: chunk-wise delta (relative to follower state at chunk start). Never step-wise deltas or velocities. Follower gains: keep P low and D high (compliant, over-damped) at both collection and deployment. Confidence M/H.

| Paper | Setting | Key number | Direction | Weight |
|---|---|---|---|---|
| ACT [F/ACT.md] | ALOHA leader/follower | delta joint targets degraded (no number); actions = leader positions | + absolute leader | M |
| BeyondImplicitForce [W4_BeyondImplicitForceEvaluatingExplicitFor.md] | ALOHA real, 10–20 trials | leader→follower-state targets: Wipe 60→15, Bottle 50→25, Plug 30→0 | + absolute LEADER targets | M |
| Real-ORL [W3_RealWorldOfflineReinforcementLearningwit.md] | real Franka BC | abs joint 0.681/0.823/0.818 vs delta 0.551/0.721/0.678 | + absolute joint | M |
| AhaRobot [W3_AhaRobotALowCostOpenSourceBimanualMobile.md] | same STS3215 servos | velocity actions from spiky teleop fail; position smooth | + absolute position | M (qualitative) |
| χ0 [W4_0ResourceAwareRobustManipulationviaTamin.md] | real π0.5 garments | delta joint < absolute joint on Task B (figure) | + absolute joint | M |
| BC-Z [W3_BCZZeroShotTaskGeneralizationwithRobotic.md] | real, 10 Hz | 1-step delta 3% vs look-ahead state-diff 45% | − step-wise delta | M |
| DiffusionPolicy [F/DiffusionPolicy.md] | sim + real | position > velocity for DP; latency-tolerant | − velocity | M/H |
| ActionSpaceStudy [F/ActionSpaceStudy.md] | PiPER, 13k rollouts, 250 demos/task | chunk-wise delta > step-wise ~10%; chunk-wise delta ≥ absolute "marginal" | + chunk-wise delta (small) | M/H |
| UMI [F/UMI.md] | UR5e, 20 trials | relative-to-chunk-start 20/20 vs step delta 16/20 vs absolute 5/20 (calibration bias) | + chunk-relative (when abs frame noisy) | M |
| DoYouNeedProprio [W4_DoYouNeedProprioceptiveStatesinVisuomoto.md] | real, state-free | rel EEF 0.984/0.584 vs abs EEF, rel joint, abs joint all 0/0 (height/horizontal shift) | + relative EEF (needs IK) | M |
| ZETA [W3_ZETAAControlledStudyofZeroShotCrossEmbod.md] | Franka cross-embodiment | EEF-delta state+action 89.9 vs 56.0 | + gripper-frame deltas (transfer) | M |
| EquivariantDP [F/EquivariantDP.md] | MimicGen | absolute EE 42.0 vs relative 33.3 | + absolute pose | M |
| TuneToLearn [W3_TunetoLearnHowControllerGainsShapeRobotP.md] | real FR3 + sim grid | compliant-overdamped 71% vs stiff 5–8%; holds for abs & rel | + low-Kp/high-Kd gains | M |
| ArmnetBench, MolmoAct2, REBOOT, QuantACT8GB | SO-100/101 | all use absolute joint targets (not ablated) | ~ common practice | L |

**Adjudication.** ACT's and DP's "delta is worse" results compare against step-wise deltas/velocities; ActionSpaceStudy's positive result is for chunk-wise deltas [F/ActionSpaceStudy.md, RESOLVED line in synthesis/ledger_by_decision/Q02_action_space.md]. UMI's absolute failure is a SLAM-to-robot calibration artefact that does not exist on a leader/follower rig where absolute joint targets are exact [F/UMI.md]. The state-free/relative-EEF results (DoYouNeedProprio, ZETA) are about spatial generalisation when training data has zero spatial variation and require an EE frame; on a 5-DoF backlash-prone SO-101, EE-frame actions need IK/FK that adds error, and our demos will cover placements. The leader-target evidence (60→15 when switching to follower states) is on the identical leader/follower paradigm and is the strongest real datum. So: absolute leader targets by default; chunk-wise delta relative to the follower state is a one-line ablation (it also makes VLASH state roll-forward trivial).

**Residual doubt / ablation:** same model, absolute vs chunk-wise delta, 20 trials each at in-distribution and shifted placements; expect ≤10 pt difference either way per [F/ActionSpaceStudy.md].

### Q03 Vision encoder

**Verdict:** Pretrained DINO-family ViT-S (DINOv2-S/14 or DINOv3-S/16; ImageNet-SSL) fine-tuned end-to-end at 10× lower LR than the policy, with augmentation always on; use spatial patch tokens per camera (224² → 256 tokens, optionally 2×2-pooled to 64 tokens per camera); one shared encoder for both cameras with a per-camera learned embedding. Fallback/second arm of the encoder ablation: ImageNet ResNet-18 (LeRobot ACT default) or a DINOv2-distilled ResNet-18. Do not freeze; do not train a ViT from scratch; do not use CLS/mean pooling; do not fine-tune a ViT-L. Confidence M/H.

| Paper | Setting | Key number | Direction | Weight |
|---|---|---|---|---|
| DiffusionPolicy [F/DiffusionPolicy.md] | robomimic + real | frozen R18/R34/CLIP 0.58/0.40/0.70 vs fine-tuned 0.92/0.94/0.98; scratch R18 0.94 | + fine-tune low LR | H (in-dist) |
| DataScalingLaws [F/DataScalingLaws.md] | UMI, blind real eval | frozen DINOv2 0.00, LoRA 0.72, full FT 0.90, scratch 0.03; ViT-S/B/L 0.66/0.81/0.90 | + full FT pretrained | H |
| DEM [W4_DecouplingVisionLanguage...md] | RoboCasa 1800 rollouts/config | DINOv3 ConvNeXt-B frozen 32.6 vs FT 55.6; ViT-B 54.1; SigLIP 53.9 | + FT; DINO ≥ SigLIP | H (sim) |
| ProgVLA [W3_ProgVLA...md] | LIBERO + real PiPER | frozen ViT-S 77.6 vs FT 91.1 (Long 60.6 vs 88.6) | + FT small SSL ViT | M |
| WhatDoWeLearn [W3_WhatDoWeLearnfromaLargeScaleStudyofPreTr.md] | real Franka, 30–150 demos | frozen ≈71; FT no-aug ≈46.5; FT+aug ≈73.3; ViT-B > ViT-L everywhere | + FT only with aug; small ViT | M |
| VC-1 [F/VC-1.md] | CortexBench + real | E2E FT of ViT-L: MW 88.8→22.7; real LR 1e-5 frozen 70 vs E2E 67.5 vs MAE-adapt 85 | − FT large ViT with MLP-on-CLS | H |
| UnbiasedLookPVR [F/UnbiasedLookPVR.md] | real Franka, 50 demos | ImageNet 41 / Kinetics 44 vs Ego4D 28 / VC-1 33; scratch ViT-B 0% | + curated-image init; − robot PVRs | M/H |
| WhatMakesPVRsRobust [F/WhatMakesPVRsRobust.md] | 9k sim evals + real | manipulation PVRs rank 7/15 OOD; DINO/MoCo-v3 ViT best; DINOv2-S < DINO v1 frozen | + ImageNet-SSL ViT for OOD | M |
| SPA [F/SPA.md] | 268 tasks frozen + Koch real | DINOv2 < MoCoV3/MAE frozen; CLIP-style poor | − frozen DINOv2/SigLIP | M |
| Theia [F/Theia.md] | frozen bench + real WidowX | spatial tokens 78.9 vs CLS 50.0; drawer FT: Theia 85→100, DINOv2-L 35→20 | + spatial tokens, + small distilled ViT | H/M |
| CAGE [W3_CageCausalAttentionEnablesDataEfficientG.md] | real, 50 mono-env demos | frozen DINOv2-L+LoRA tokens: bg 0.87 / obj 0.80 / cam 0.80 vs scratch ResNet 0/0/0.27; mean-pooled 0.40 | + pretrained ViT tokens for OOD; − pooling | M/H |
| PatchPolicy [W4_PatchPolicyEfficientEmbodiedControlviaDe.md] | sim 3 seeds + real | DINOv2 0.69/0.96 vs SigLIP2 0.51/0.83; 256→1 patches 0.69→0.48; real patch 0.70 vs ACT-scratch 0.35 | + DINOv2 patches; − SigLIP; − pooling | M/H |
| X-Distill [W3_XDistillCrossArchitectureVisionDistillat.md] | real xArm, 20–25 demos | distilled R18 75.6 vs scratch R18 41.9 vs FT DINOv2-S 31.4 | + CNN prior at ≤25 demos; − FT ViT at tiny data | M |
| Octo [F/Octo.md] | ~100 demos scratch | ResNet beats ViT from scratch; ViT wins only with 800k-traj pretraining | + CNN if from scratch | M |
| GLUE [W3_GLUEGlobalLocalUnifiedEncodingforImitati.md] | real, 50 demos, 10 Hz | learnable CLIP global 70.0 vs DP-R18 36.2 / ACT 48.8; OOD 30–50 vs 0–25 | + pretrained ViT over ImageNet R18 | M (confounded) |
| MResT [W4_MResT...md] | real Franka, novel objects | frozen VLM scene 72.3 vs FT 45.6 heldout (train equal) | + frozen language-grounded scene encoder for novel objects | M |
| SynthICL [W4_SynthICLScalableIncontextImitationLearni.md] | sim→real | frozen DINOv3 75.0 vs LoRA 20.7 (shared across views, synthetic data) | + frozen in sim2real | M |
| KnowledgeInsulation [F/KnowledgeInsulation.md] | π0 scale | frozen backbone + new expert = 0%; fresh-head gradients degrade backbone | + FT with protected gradients | M |
| MINERVA [W4_MINERVA...md] | sim | scratch CNN: light 1.1–6.5%, background 4.7–9.3%, camera 11.5–34.6% | − scratch for robustness | M |
| Spotlighting [W4_SpotlightingTaskRelevantFeaturesObjectCe.md] | real, frozen only | frozen dense DINOv2 real OOD 0.07; slots 0.28–0.41 | − frozen dense alone OOD | M |
| SEVO [W4_SEVO...md] | SO-101 | trainable R18 ACT 95 vs frozen-SigLIP SmolVLA 83 | + trainable encoder | M |

**Adjudication (frozen vs fine-tuned vs scratch).** The RESOLVED line in synthesis/ledger_by_decision/Q03_vision_encoder.md holds up on the notes: fine-tuning wins in-distribution when the encoder is small, the LR is ~10× lower, and augmentation is on (DP, DataScalingLaws, DEM, ProgVLA, WhatDoWeLearn); fine-tuning collapses only for ViT-L + MLP-on-CLS + tiny data (VC-1) or when fine-tuning on synthetic data then testing on real (SynthICL). OOD robustness depends on the pretraining recipe (DINO/MoCo/ImageNet-SSL ViT > R3M/MVP/VC-1), not on frozen-vs-FT per se (WhatMakesPVRsRobust, UnbiasedLook). The strongest pro-frozen OOD results (CAGE 0.87 bg with frozen DINOv2-L+LoRA; MResT 72.3 novel objects) are with a large frozen ViT plus a trainable adapter and token-level readout — i.e. they preserve pretrained invariances while still adapting; the anti-frozen results (DataScalingLaws 0.00, DEM 32.6, KI 0%) are for fully frozen features feeding a small head. Our compromise is the DataScalingLaws/LBM recipe: full fine-tune at LR ×0.1 with augmentation, plus a feature-anchoring regulariser toward a frozen copy if OOD tests show the encoder drifts (Anchor-Align: frozen 43.1 < BC-FT 61.0 < FT+anchoring 68.1 on LIBERO-PRO [W3_GeneralizableVLAFinetuningviaRepresentat.md]).

**Which pretraining.** DINO-family beats SigLIP/CLIP for control features (PatchPolicy, DEM, SPA "CLIP-style poor", WhatDoWeLearn CLIP weakest). Robot-specific PVRs (R3M/MVP/VC-1) are worse OOD and on real robots (UnbiasedLook, Burns). SPA/MAE are strong frozen but were not tested fine-tuned at our scale; DINOv3-S is the most commonly successful small choice in 2026 notes (ProgVLA DUNE≈DINOv3, RayViT, CT-VAM, TurboVLA). At ≤25 demos a distilled ResNet-18 beat a fine-tuned DINOv2-S (X-Distill), so ResNet-18 (ImageNet or X-Distill weights) is the required second ablation arm and the LeRobot ACT baseline already uses it.

**Tokens vs pooled.** Unambiguous: Theia 78.9 vs 50.0, CAGE 1.00 vs 0.40, PatchPolicy 0.69 vs 0.48 — keep patch tokens; compress with a small attention pooler/perceiver to ~64 tokens per camera if latency requires (GR00T uses 64 tokens/frame [F/GR00T-N1.md]; CAGE's causal perceiver to 4 tokens still worked).

**Residual doubt / ablation:** DINOv3-S fine-tuned vs ImageNet ResNet-18 fine-tuned on the same data and head; evaluate in-dist + lighting + new pumpkin + camera nudge, 20 trials each. Also test LR ×0.1 vs frozen-first-5k-steps warm-up.

### Q04 3D / depth

**Verdict:** Not in v1. In v2 add an object-centric branch from the RealSense depth: segment pumpkin + tray (+ gripper) once per episode and track (SAM2-small or a colour/detector mask), back-project to ~256–512 points each in the camera frame, encode with a tiny MLP+max-pool (DP3-style), inject into the action expert through a zero-initialised additive projection (PointVLA pattern). Also cheap and zero-latency: a training-only depth-prediction auxiliary head on the scene tokens. Never feed a raw full-scene point cloud or a naive 4-channel RGB-D image as the robustness fix. Confidence M for "object-centric 3D helps OOD", L for "we need it at all after the Q05/Q13 protocol".

| Paper | Setting | Key number | Direction | Weight |
|---|---|---|---|---|
| DP3 [F/DP3.md] | real, 40 demos, 10 trials | DP3 85 vs image DP 35 vs depth-image DP 20; OOD claims 1 trial/cond | + colour-free cloud (in-dist) | M/H (OOD anecdotal) |
| iDP3 [F/iDP3.md] | humanoid, 10 trials/cell | new object/view/scene: image DP 0–3/10 vs iDP3 9/10; in-dist finetuned R3M DP ≥ iDP3 | + camera-frame cloud for OOD | M/H |
| Hyper-DP3 / PocketDP3 [F/Hyper-DP3.md, W4_PocketDP3...md] | Piper + single D455, 50 demos, 15 trials | HDP3 73/47/20 vs DP3 53/33/7; 4.5 ms | + stereo-depth cloud works on low-cost arm | M |
| CAGE (RISE baseline) [W3_CageCausal...md] | real, 50 mono-env demos | RISE full-scene cloud: bg 0.13, obj 0.00, L2 0 (best in-domain) | − scene cloud for robustness | M |
| GAM [W3_GroundedActionModel3DGroundingasaFoundat.md] | RoboTwin Hard + real | DP3 55.2→5.0 under randomisation; whole-scene points 12.8 vs object-cropped 46.8 | − raw scene cloud; + object-cropped | M/H |
| RoboTwin 2.0 [W3_RoboTwin20...md] | sim, perfect clouds | DP3 55.2 Easy → 5.0 Hard | − cloud alone for visual shift | M |
| RayViT [W4_RayViTRayConditionedVisualRepresentation.md] | RoboCasa camera shift | point-map input drop 21.3 vs RGB 18.5 | − 3D input as viewpoint fix (uncalibrated) | M |
| GROOT [W3_LearningGeneralizableManipulationPolicie.md] | sim 3 seeds + real | segmented object clouds: Cam-Hard 61.7 vs 0; Bg-Hard 63.3 vs 0; naive RGB-D fails all | + object-centric cloud | M |
| Lan-o3dp [W4_LanguageGuidedObjectCentricDiffusionPoli.md] | RLBench 40 demos | object-only cloud 68.7 vs DP3 43.6 vs RGB 39.3; MLP+res 68.8 vs PointNet 14.9 | + segmented object cloud, simple MLP | M |
| SKIL [W4_SKILSemanticKeypointImitationLearningfor.md] | real, 20–30 demos | unseen objects 72.8 vs DP3 25.0; bg+distractors 8/10 vs 0/10 | + sparse 3D keypoints | M |
| P3-PO [W3_P3POPrescriptivePointPriorsforVisuoSpati.md] | real xArm | 3D keypoints 39/40 vs RGB 13/40, RGB-D token 19/40; monocular depth = camera depth | + depth-lifted keypoints; ~ raw depth token | M |
| OBEYED [W4_ClutterRobustVisionLanguageActionModelst.md] | UR10e, 100 trials/config | masked depth over masked RGB: unseen objects 57→69, 70→78 | + masked depth for novel appearance | M |
| RoboMP [F/RoboMP-DINOv2.md] | sim | hard object-centric 3D filter: obstacle 3–7% vs full-scene 80–83% | − hard filtering when context matters | M |
| PointVLA [F/PointVLA.md] | real, tiny n | zero-init side injection; table height 3→52 mm 0/5→5/5; DP3+RGB < DP3 in 12/13 tasks | + side-branch fusion; − naive RGB+points concat | M/L |
| VO-DP [W4_VODPSemanticGeometricAdaptiveDiffusionPo.md] | real, 60 trials | RGB+VGGT 87.9 vs DP3 67.5 (depth noise hurts DP3 in real) | ~ geometry-aware RGB features | M |
| VolumeDP [W3_VolumeDPModelingVolumetricRepresentation.md] | real 20 trials | ±5° camera: DP 0% vs 40%; learned lifting > GT-depth occupancy | ~ 3D lifting from RGB | M |
| GeoVLA [W3_GeoVLAEmpowering3DRepresentationsinVisio.md] | WidowX + D435i | 45° view shift 70 vs 0; lighting still −20 | + EE-frame cloud for viewpoint | M (confounded) |
| ROPA [W3_ROPASyntheticRobotPoseGenerationforRGBDB.md] | ACT sim + real | RGB→RGB-D: CLB 41.3→56.7; real 13→15, 4→5, 14→17 | + depth channel modest | M |
| GaussianDream++ / GeoPredict / GAM [W4_GaussianDreamEfficient3DGaussianWorldMod.md, W4_GeoPredictLeveragingPredictiveKinematics.md, W3_GeometricActionModelforRobotPolicyLearni.md] | VLA scale | depth as training-only target: camera 76.5→80.1; real 22.5→42.5; no-pretrain Plus 50→80 with depth aux | + depth as aux supervision | M |
| Chronos [W4_Chronos...md], iDP3 | real | D435 clouds too noisy for small objects | ~ depth quality caveat | L |

**Adjudication (full-scene cloud robust vs collapses).** The DP3/iDP3 robustness claims rest on 1–10 trials per OOD cell in scenes where the background change did not add clutter; every controlled study with randomised clutter/textures (RoboTwin 2.0, GAM, RISE-in-CAGE) shows full-scene clouds collapse, and the same studies show object-cropped points restore most of it (GAM 12.8 → 46.8). RayViT shows uncalibrated point maps are no better than RGB under camera shift; the viewpoint gains (GeoVLA, FP3, SPHINX) all depend on calibrated robot/EE-frame clouds. Conclusion: 3D helps for (i) height/scale/geometry shifts and (ii) novel appearance when the object is segmented and colour is removed; it does not help lighting (GeoVLA −20) and it needs calibration to help camera shift. Because our pumpkin is large and matte, D4xx stereo depth is adequate for it (Hyper-DP3 used a single D455 on a Piper), but thin gripper parts will be noisy [W4_Chronos...md, F/iDP3.md].

**When to add it.** Only after the v1 data+augmentation protocol is evaluated: if "new pumpkin" or "moved camera (recalibrated)" cells remain <50% while in-distribution is >80%. Cheaper first: masked-region colour randomisation in the RGB branch (Q05) and the depth-prediction aux loss (Q09).

**Residual doubt / ablation:** v1 RGB vs v1 + object-point branch vs v1 + masked-depth channel on the new-pumpkin and moved-camera cells, 20 trials each.

### Q05 Augmentation

**Verdict:** Always on: random crop/shift (≈95% crop, up to 8–10 px shift), small rotation (±5°) and a small random perspective warp on the scene camera; photometric jitter with hue FIXED (brightness/contrast/saturation/sharpness/gamma, plus grayscale on the wrist camera only); background replacement of the scene camera (green screen chroma key or offline SAM2 masks) with high-entropy random textures/ImageNet images on ~50% of samples; masked-region colour/texture randomisation of the pumpkin on a subset; copy-paste distractors; scene-camera token dropout (p≈0.3–0.5) and occasional whole-scene-view drop (p≈0.1); proprio Gaussian noise + dropout. Generative relighting/NVS only if a remote GPU is available. Confidence H for photometric+crop, M/H for background replacement, M for the rest.

| Paper | Setting | Key number | Direction | Weight |
|---|---|---|---|---|
| robomimic [F/robomimic.md] | real Can | 73.3 with pixel-shift vs 26.7 without | + random shift | H |
| HULC [F/WhatMattersLanguageIL.md] | CALVIN | no random shift 2.64→1.99 | + random shift | M/H |
| GreenScreenAug [F/GreenScreenAug.md] | real ACT, 8.2k evals, 50 demos | +65% vs none, +29% vs CV aug, +21% vs generative; textures 87% vs solid 65% | + chroma-key random textures | H |
| RoboEngine [F/RoboEngine.md] | real DP, 50 demos, 6 new scenes | +210% vs no gen-aug; textures/ImageNet strong & fast | + segmentation-based bg replacement | M/H |
| ChromaGuard [W4_LightsCameraMalfunctionWhenIlluminationR.md] | real SO-101 SmolVLA | no-aug 70→0 under spotlight; full-HSV 80/70 but colour task 77.5→47.5; hue-fixed 80/70 and 97.5/92.5 | + jitter with hue fixed; − hue jitter | H |
| CRAFT [W3_CRAFTVideoDiffusionforBimanualRobotDataG.md] | real ACT, 20 trials | lighting: none 3/1/0 → jitter 13/9/8 → generative 17/14/12; object colour: SAM recolour 15/9/11 | + photometric baseline; + object recolour | H |
| RoLight [W4_PhysicallybasedLightingGenerationforRobo.md] | 1000 real trials | relit > crop+jitter by +33 pts under side/coloured light | ~ jitter insufficient for strong directional light | M |
| RoboMP [F/RoboMP-DINOv2.md] | sim | masked-region colour rand 72.5 vs full-image 19.1; global jitter erased decision colour 88→25 | + object-region randomisation | M |
| AStudyOnEnhancing [W3_AStudyonEnhancingtheGeneralizationAbilit.md] | sim DP + SO-101 sim2real | camera .25→.77, light .56→.76, texture .12→.75 with matched randomisation; camera-only hurt light .56→.28 | + augment each axis explicitly | M |
| CAGE [W3_CageCausal...md] | real | perspective+crop: L2 0.40→0.73 | + geometric aug | M |
| E0 [W4_E0EnhancingGeneralizationandFineGrainedC.md] | LIBERO camera perturbation | spherical warp aug: π0 19.7→50.8 | + camera-rotation warp | M |
| RoVi-Aug [W3_RoViAugRobotandViewpointAugmentationforC.md] | real DP, 10 trials | 10 cm/20° shift 0→80% with NVS; −10 pts in-dist | + viewpoint aug (moderate) | M |
| GroundingSim2Real [W4_GroundingSimtoRealGeneralizationinRoboti.md] | >10k real trials | camera-pose DR largest gain; per-frame > per-episode | + geometric aug, per-frame | M |
| M3 [W4_RobustBimanualVisionLanguageActionModels.md] | 0.5B VLA, 50 demos | visual aug 22.3 vs structured view masking 64.0 (base 23.7); real distractors 12.5→61.1 | + structured view/token masking | M |
| w2VLA [W3_DecouplingtheDeclarativefromtheProcedura.md] | real SO-101 | 50% VFM patch masking: transfer 58.3→94.4 | + token masking | L/M |
| EGR [W4_SensingWhichModalityMattersEvidenceGated.md] | real bimanual | uniform ModDrop hurts (12.5→7.5 sim); evidence-gated 12/40→34/40 | − naive random camera dropout | M |
| MResT [W4_MResT...md] | real | asymmetric aug (jitter+grayscale wrist, crop scene) ≈ +15% heldout | + asymmetric per-camera aug | L/M |
| WhatMattersWhenDiagnosing [W4_WhatMattersWhenDiagnosingandImprovingCon.md] | sim 600 rollouts/cell + UR3e | copy-paste distractors 39.5→100 / 14→64; real 0/20→13/20 (combined) | + copy-paste distractor aug | M |
| Seeker [W4_AttentionfromActionforActionEmergentVisu.md] | real, 20 trials | mask-guided overlay OOD 60.0 vs uniform overlay 11.7 | + foreground-preserving overlay | M |
| SelfSupCorrespondence [W3_SelfSupervisedCorrespondenceinVisuomotor.md] | sim | proprio noise 1 mm/1°: 30 demos 1.1→73.3% | + proprio noise | M |
| RDT-1B, π0.5 [F/RDT-1B.md, F/pi0.5.md] | VLA practice | colour jitter + corruption + proprio noise 40 dB; crop 95% + rot ±5° + jitter(0.3,0.4,0.5) | ~ defaults (not ablated) | L/M |
| EvoHIL [W3_EvoHIL...md] | real SO-101 | relit copies at 25% share: shifted 0.50→1.00; no relit 0.88 | + moderate share of relit data | M |
| InfiNoVA / RoboSplat [W4_InfiNoVA...md, W4_NovelDemonstrationGenerationwithGaussian.md] | SO-101 / Franka | 3DGS NVS 40.5 vs 7.5; camera avg 6.1→80.6; single-image generative NVS (VISTA) no gain | + 3D-consistent NVS only | M (heavy) |
| ReShoot / EMMA [W4_ReShoot...md, W4_EMMAGeneralizing...md] | real | novel colours 0→19/40; keep ≤50% synthetic; lighting −2.2 (no gain) | + generative appearance aug offline; − for lighting | M |
| iDP3 [F/iDP3.md] | real | colour jitter alone did not rescue new scene | ~ jitter insufficient alone | M |

**The hue caveat.** ChromaGuard's real SO-101 result is decisive: full hue jitter makes the policy colour-blind (colour task 77.5→47.5) while giving the same lighting robustness as hue-fixed jitter. Since the pumpkin is orange and a future "green box" instruction is colour-grounded, keep hue at 0 (or ≤0.02) and get appearance robustness from (a) object-region colour randomisation on a subset (RoboMP 72.5 vs 19.1) and (b) several physical pumpkins (Q13), not from global hue jitter.

**Adjudication (augmentation alone vs data diversity).** Photometric jitter recovers a large fraction of lighting robustness for mild shifts (CRAFT 3→13/20) but fails on strong directional/coloured light (RoLight, iDP3), which is why the protocol collects under several real lighting conditions and can add relit copies. Background replacement is the best-evidenced cheap fix for scene/background shift (GreenScreenAug H) and helps less for object appearance (GenAug pick 45% vs env 85% [F/GenAug.md]). Camera shift needs geometric augmentation plus multi-pose data (Q11). Structured view/token masking outperforms generic photometric aug for multi-view fusion robustness (M3), but uniform whole-camera dropout can hurt (EGR) — hence token dropout on the scene view plus rare whole-view drops, never dropping the wrist view.

**Residual doubt / ablation:** the offline "action drift" audit of [W3_ItsNotJustMoreDemosCounterfactualActionS.md]: apply each augmentation family to held-out frames and measure how much the trained policy's predicted chunk moves; the families with largest drift are under-covered.

### Q06 Chunking and execution horizon

**Verdict:** Predict 1.6 s (16 steps at 10 fps; 48 at 30 fps), execute 0.5–0.8 s (5–8 at 10 fps; 15–24 at 30 fps) and re-query, with the execution horizon adaptively shortened near grasp/place (rule-based first: shorten when the gripper command changes or the wrist view shows the target close; DVAC denoising-variance later). Never execute 1 step per query (stop-go) and never the whole chunk. No temporal ensembling with the flow head (see Q10). Confidence M.

| Paper | Setting | Key number | Direction | Weight |
|---|---|---|---|---|
| ACT [F/ACT.md] | sim, 50 Hz | k=1 1% → k=100 (2 s) 44% | + chunk ~1–2 s | H |
| DiffusionPolicy [F/DiffusionPolicy.md] | 10 Hz | predict 16, execute 8 optimal; ≤4 steps latency tolerated | + execute half | H |
| WhyChunking [W3_WhyDoesActionChunkingImproveBehavioralCl.md] | LIBERO/robomimic + real | Markov 19.8 vs AC 88.7 (LIBERO-10); uniform TE 42.2 vs AC 75.2 (Tool Hang) | + chunking; − uniform TE | H |
| SmolVLA [F/SmolVLA.md] | LIBERO | chunk 10 best (84.0); execute 1/10/30/50 → 80.3/82.8/70.8/51.8 | + short exec, chunk 10–50 | M/H |
| DVAC [RT/DenoisingVarianceChunking.md] | real, 50 demos, 30 trials | Fix15 0.800 vs Fix40 0.533; adaptive 0.867, −40% replans | + short/adaptive exec | M |
| OBEYED [W4_ClutterRobust...md] | UR10e 10 Hz | H=5/10/15/20 → 81/85/76/56 | + ~1 s exec at 10 Hz | M |
| KnowingWhenToStop [W3_KnowingWhentoStopAdaptiveActionChunkingv.md] | real π0.5 20 Hz | fixed 10/20/30/40/50 → 45/46.7/51.7/46.7/41.7; multi-sample short chunks 18.3 (stop-go) | ~ sweep in seconds; − stop-go | M |
| BCP [W3_ContinueorReplanBernoulliContinuationPol.md] | RoboTwin + real | phase of boundary alone 82.5–93.7; fixed 20/30/40 no better than 50; replan-before-contact 74→92 | + stage-adaptive replanning | M/H |
| DEHP [W3_DynamicExecutionHorizonPredictionforChun.md] | sim under action noise | exec 2 > 6 of 16 under noise; adaptive +23 pts | + short exec under actuation noise (SO-101 backlash) | M |
| CogACT [F/CogACT.md] | SIMPLER | predict 16 best; 32 → 51.2 | + ~1–3 s prediction | M |
| MINERVA [W4_MINERVA...md] | sim | chunk 16 best; 8 −3.16; 32 −2.20 | + chunk ~0.8 s @20 Hz | M |
| DEM [W4_DecouplingVisionLanguage...md] | sim | H16/8 55.6, H8/4 55.9, H1 50.6 | + H 8–16, per-step −5 | M |
| SnapFlow [W3_SnapFlowOneStepActionGenerationforFlowMa.md] | libero_10 | n_act 1→77/72, 5→90/93, 20→97/92 | − replan every step | M |
| VQ-BeT [F/VQ-BeT.md] | low-cost Stretch | receding-horizon open-loop "fails completely" (OOD within 3 steps) | − long open-loop on cheap arms | M |
| QuantACT8GB [RT/QuantACT8GB.md] | SO-101 | 100 steps (10 s) open-loop still 19/20 on quasi-static task | ~ long exec OK for static task | L |
| A2C2 [RT/A2C2.md] | SmolVLA LIBERO | e=50 0.71 vs e=10 0.85 at d=0 | − full-chunk exec | M |
| RevisitingOpenLoop [RT/RevisitingOpenLoop.md] | real 500+ demos | T_o=2 best at T_exec=8; T_o=8 best at 2 | ~ optimum depends on context | M |
| RoboAgent [F/RoboAgent-MT-ACT.md] | 5 Hz real | chunk 20 (4 s) best; 40 (8 s) >−20% | + moderate chunk | M |
| DEFLECT [W3_DEFLECT...md] | Kinetix | overlap (chunk − delay) must be >~3 steps or RTC/BID collapse | + chunk ≫ delay when async | M |
| FurnitureVLA [W3_FurnitureVLALearningLongHorizonBimanualF.md] | sim π0.5 | exec 5/10/25 of 50 → 0.60/0.74/0.67; recency TE 0.80 vs uniform 0.62 vs none 0.65 | + ~20% of chunk; recency-weighted TE (big model, sync) | M |

**Adjudication (short vs full chunk).** Shorter is better for SmolVLA, π0.5, DP under noise and every real 50-demo study (DVAC, OBEYED, A2C2, SmolVLA); full chunk is better only for X-VLA (KnowingWhenToStop) and for BCP's fixed-horizon sweep, where the authors show that boundary *timing* relative to contact moves success by 11 pts and that replanning right before contact is what matters. QuantACT8GB's 10 s open loop works only because the task is quasi-static and the beanbag forgiving. On SO-101, backlash and tracking error act like DEHP's "action noise", which pushes toward shorter execution near contact. Express horizons in seconds, not steps: at 30 fps our 1.6 s chunk is 48 steps.

**Residual doubt / ablation:** execution horizon sweep {0.3, 0.5, 0.8, 1.2 s} with the same checkpoint, 20 trials each; then the gripper-event rule vs fixed best.

### Q07 History and proprioception

**Verdict:** Current frame only (To=1; To=2 as ablation), no past actions, no joint velocities; the current 6-D joint state enters as one token but is regularised (state dropout p≈0.3, Gaussian noise ≈1° / 40 dB, and VLASH offset augmentation). Add explicit low-dim phase/progress signals only if aliasing failures (loops, stalls) appear. Confidence M.

| Paper | Setting | Key number | Direction | Weight |
|---|---|---|---|---|
| BAKU [W3_BAKU...md] | LIBERO-90 | no history .90 vs last-step-loss history .54; multi-step-loss .90 → no gain | − history | H |
| CopycatAgents [F/CopycatAgents.md] | MuJoCo state | history lowers test loss but can lower reward; past-action copying | − past actions; − loss-based selection | M |
| DoYouNeedProprio [W4_DoYouNeedProprio...md] | real, 30–60 trials, ACT/DP/π0 | with state 0/30 at new height vs without 30/30; ACT 0/0.084 vs 0.933/0.517 | − raw proprio (spatial shift) | M/H |
| HPT [F/HPT.md] | real, ~100 demos | no-proprio 26.7 vs with 43.3 (scratch) | + current proprio | M |
| GeoProp [W3_GeoPropGroundingRobotStateinVisionforGen.md] | real DP-R18, 50 demos | no-proprio 28.8 vs vanilla 38.8 vs grounded 50.0 | + keep proprio (real) | M |
| robomimic [F/robomimic.md] | sim/real | +EEF vel/joint vel: −49–88% low-dim, −2–29% image | − extra proprio | M |
| HULC [F/WhatMattersLanguageIL.md] | CALVIN | adding proprio 2.64→2.20 (task-cue shortcut) | − proprio as task cue | M |
| Octo / RDT [F/Octo.md, F/RDT-1B.md] | pretraining | proprio "generally worse"; no proprio history to avoid shortcuts | ~ caution | L/M |
| FACTR [W4_FACTRForceAttendingCurriculumTrainingfor.md] | real ACT 50 demos | excluding current joints "greatly improves generalisation" (no numbers) | − proprio | L |
| AnchorVLA4D [W3_AnchorVLA4DanAnchorBasedSpatialTemporalV.md] | xLerobot SO-101-class, 30 demos | past 3 frames 46.9 vs anchor 55.2; proprio w/ 50 vs w/o 60 (10 trials) | − frame stacking; ~ proprio | L/M |
| GAM [W3_GeometricActionModel...md] | LIBERO-Plus | H=1 89.7 vs H=2 84.4 vs H=4 85.1 | − multi-frame history for robustness | M |
| SeedPolicy [W3_SeedPolicyHorizonScalingviaSelfEvolvingD.md] | RoboTwin + real | naive stacking degrades; recurrent state 33→73 on long/aliased tasks | − stacking; + memory only for aliased tasks | M |
| CronusVLA [W4_CronusVLA...md] | 7B | naive 7-frame stack +1.4; cached-feature history + current-frame emphasis 70.9 | + compressed history only with current-frame weighting | M |
| DiffusionTransformerPolicy [F/DiffusionTransformerPolicy.md] | ManiSkill2 | 2 obs 65.8 vs 1 obs 61.6; 3 obs 35.4 | ~ 1–2 frames | L/M |
| MINERVA [W4_MINERVA...md] | sim, 1 run | 1→2 obs steps +4–6 | ~ 2 frames (sim) | L |
| StageACT [W4_StageACTStageConditionedImitationforRobu.md] | humanoid, 10–20 trials | ACT 20 vs +5-frame history 10 vs stage-token 55 | − raw history; + explicit stage | L |
| RT-1 [F/RT-1.md] | 130k demos, no chunking | w/o history seen 97→82, distractors 83→50 | + history only for non-chunked big-data | M (not our regime) |
| robomimic BC-RNN [F/robomimic.md] | no chunking | BC-RNN ≫ BC on human data | + history only when NOT chunking | M |
| Blindfolded [W3_BlindfoldedExpertsGeneralizeBetterInsigh.md] | 400 demos/shape | exploratory demos need GRU policy | ~ | L |

**Adjudication (proprio helps vs hurts).** "Hurts" results share one structure: the training data has no spatial variation along the tested axis, so state becomes a perfect shortcut (DoYouNeedProprio trained at one table height; HULC's neutral reset pose; Octo's heterogeneous delta-EEF mix). "Helps" results are single-embodiment real tasks with varied placements and current-state-only input (HPT, GeoProp real). Our demos vary pumpkin/tray placement and start pose, so the copycat pressure is moderate; the wrist camera cannot see the tray from far away, so some state is useful. The robust middle is what several papers converge on: keep current joint state, add noise/dropout (SelfSupCorrespondence 1.1→73.3 with 1° noise; RDT 40 dB; DreamGen zero-state), never velocities or past actions, and run the "zero the images" sensitivity test [W3_TowardsAccessiblePhysicalAI...md] to detect a proprio shortcut. VLASH's offset augmentation (Q10) additionally forces the model to *use* state correctly rather than as a memorised trajectory index.

**History.** With chunking, history gives nothing on Markovian pick-place (BAKU H, GAM, VO-DP T=1 ≥ T=3 [W4_VODP...md]) and hurts robustness; it helps only for aliased/memory tasks (SeedPolicy, Chronos, ChainVLA) or transient occlusion (CronusVLA). Pumpkin→tray is Markovian given gripper state; keep To=1.

**Residual doubt / ablation:** To=1 vs 2; state dropout 0 vs 0.3; image-zeroing action-sensitivity diagnostic.

### Q08 Language (second object)

**Verdict:** v1: no language; a task-ID embedding if we ever train two tasks jointly. v2 (pumpkin vs green box): frozen small sentence/text encoder (MiniLM-L3 SBERT or T5-small/BERT-base tokens, cached) + zero-initialised FiLM on the encoder/trunk features, trained on paired data where the same scene contains both objects and the instruction decides the target; optionally a decoupled grounding cue (detector mask of the named object fused at feature level) because end-to-end fine-tuned VLAs ignore the instruction. Do not rely on SmolVLA's language head for this. Confidence M.

| Paper | Setting | Key number | Direction | Weight |
|---|---|---|---|---|
| OFT [F/OpenVLA-OFT.md] | ALOHA real | no FiLM → language following at chance (33%) with wrist cams | + FiLM essential | H |
| RoboAgent [F/RoboAgent-MT-ACT.md] | real | FiLM vs concat −5–10% | + FiLM | M |
| BAKU [W3_BAKU...md] | LIBERO-90 | FiLM .90 vs no FiLM .87 | + FiLM | M |
| MoE-ACT [W4_MoEACTScalingMultiTaskBimanualManipulati.md] | sim 16 tasks | decoder FiLM 53.1→62.0 | + FiLM | M |
| RT-1 / BC-Z [F/RT-1.md, W3_BCZ...md] | large real | frozen sentence emb + FiLM ≈ one-hot on train tasks (40 vs 42) | + frozen text + FiLM | M |
| HULC [F/WhatMattersLanguageIL.md] | CALVIN | MiniLM-L3 2.64 > CLIP 2.42 > BERT 2.03; alignment aux 2.29→2.64 | + small SBERT; + contrastive aux | M |
| DEM [W4_DecouplingVisionLanguage...md] | paraphrase eval | none 11.3, one-hot 37.4, T5 44.5, BERT 47.8, NeoBERT frozen 55.6 | + frozen modern text encoder | M |
| vla.simd/IMPACT [W3_vlasimdEfficientCPUInferenceforLanguageC.md] | real SO-101, ~15 demos/instr | no-language multi-task ACT 20% vs FiLM+T5 60–90% | + FiLM + cached tokens on SO-101 | M |
| w2VLA [W3_DecouplingtheDeclarative...md] | real SO-101, 16 demos/pair | skill transfer 91.7 vs OTTER 30.6 vs π0.5 38.2 with CLIP heatmap "where" FiLM | + decoupled localisation cue | M |
| SVP-IL [W4_DecouplingSemanticsandGeometricGrounding.md] | real Aloha 100 demos | segmenter-mask feature fusion 60.0 vs π0 31.7 | + mask grounding over e2e language | M |
| OBEYED [W4_ClutterRobust...md] | real π0/π0.5 | fine-tuned VLAs grasp any object >75% under mismatched instruction | − e2e VLA language grounding | H |
| BAS-VLA / Anchor-Align [W3_BeyondAppearanceShifts...md, W3_GeneralizableVLAFinetuning...md] | real | π0.5 still does old task 34%; BC picks trained green mug 90% under "pink mug" | − language alone | M |
| ChromaGuard [W4_LightsCamera...md] | SO-101 colour task | SmolVLA+hue-fixed aug 97.5 vs π0.5 55.0 | + colour-preserving aug for colour grounding | M |
| MINERVA / CT-VAM [W4_MINERVA...md, W4_CTVAMA...md] | closed task set | task-ID matches language VLAs | + task ID for closed sets | M |
| Hiveformer [W3_Instructiondrivenhistory...md] | RLBench | CLIP token sequence 86.3 vs BERT 40.2 unseen; pooled embedding drops | + token-level text + cross-attn (for unseen instructions) | M |
| KI / TRI co-training [F/KnowledgeInsulation.md, W4_ASystematicStudy...md] | VLA | robot-only fine-tune erodes language; stop-grad/co-training restores | ~ only if using a VLM | M |
| InterleaveVLA / WhatMattersWhenDiagnosing [W4_InterleaveVLA...md, W4_WhatMattersWhen...md] | real | image-of-target conditioning 36.1→69.4 Lift; target-crop prompt redirects selection | + visual target prompt | L/M |

**Adjudication.** For two fixed instructions the evidence is consistent: a frozen small text encoder with FiLM is sufficient (RT-1, BC-Z, BAKU, IMPACT on SO-101) and cheap; the failure mode is not the encoder but grounding — small-data fine-tunes bind the instruction to scene statistics unless the data contains the other object in the same scene (OBEYED, Anchor-Align, BAS-VLA). So the language phase is mostly a data-protocol question (both objects present in every scene, instruction balanced, hue-preserving augmentation) plus FiLM; a detector-mask cue (SVP-IL/w2VLA on SO-101) is the fallback if the FiLM policy picks the wrong object.

**Residual doubt / ablation:** FiLM-only vs FiLM + mask cue on the two-object set; measure wrong-object rate separately from grasp failure.

### Q09 Auxiliary objectives

**Verdict:** v1 ships with two zero-inference-cost auxiliaries, both switchable: (a) a trajectory-smoothness/Hermite auxiliary head on the chunk (λ small), (b) latent future prediction: cosine-align a few future tokens in the action expert with the frozen/EMA encoder embedding of the frame at t+H (FLARE-style, λ≈0.2), in the shared stack. Candidates for v2: state/Δq grounding heads from proprio, depth-prediction head from RealSense depth, cross-view action-consistency if a second scene camera is used. Avoid pixel/VAE reconstruction of future frames and CFG-style guidance. Confidence M (evidence is mostly sim or big-model; expected gain at 100 demos is a few points).

| Paper | Setting | Key number | Direction | Weight |
|---|---|---|---|---|
| Hermite [W3_HermiteCurvesasTrajectoryPriorsforVision.md] | π0.5 real 4 tasks×15 | reg 63.4→90.0; seam jump 0.48–0.72×; +0.2 ms latency | + trajectory aux head | M (big model/data) |
| FLARE [F/FLARE.md] | RoboCasa/GR1 sim, 32 H100 | 61.9→70.1; generic frozen SigLIP2 target +6–7; UWM pixel-latent 60.8 | + latent future alignment; − pixel/VAE | M |
| MDT [F/MDT.md] | CALVIN/LIBERO | MGF masked future recon: MT-ACT 2.80→4.03; ≤20 demos from scratch ≈+1 pt | + masked foresight (small at 20 demos) | M |
| JEPA-Policy [W4_JEPAPolicy...md] | real + sim | future-latent loss in shared stack +5.6; separate branch 0 gain | + only if in shared stack | M |
| Reflex [W4_ReflexEnablingFastandPredictiveVisionLan.md] | dynamic sim | frozen DINOv3 target 36.8→62.8; trainable target 4.9 (collapse) | + frozen target | M |
| PSG-JEPA [W3_IsForwardPredictionEnoughPhysicalStateGr.md] | real, 100 demos, 50 trials | proprio + Δq grounding heads 60.0→79.3 | + state/transition heads | M |
| CapturingVisualEnvStructure [W3_CapturingVisualEnvironmentStructureCorre.md] | sim 5 backbones | state-prediction aux +2.8..+7.2 | + state aux | M |
| GeoPredict / GaussianDream / GAM | VLA scale | future depth/track aux: +2–2.5 each; camera 76.5→80.1; no-pretrain 50→80 with depth aux | + depth aux (training only) | M |
| Seer [F/Seer-PIDM.md] | CALVIN scratch | +future image 3.31→3.41; +inverse dynamics on foresight 3.64 | + predictive/IDM coupling | M |
| SLIM [W4_SLIM05B...md] | 0.5B | IDM+FDM latent pre-stage with EMA 77.45 vs 66.82 (no EMA) | + latent IDM/FDM pre-stage | M |
| CLASS [W4_CLASSContrastiveLearningviaActionSequenc.md] | real, 200 demos | action-similarity contrastive: random-camera 0.10→0.60 | + action-contrastive for view invariance | M |
| CrossView [W4_CrossViewActionConsistencyforCameraRobus.md] | real, 90 rollouts | held-out cams 53.3→74.4 with consistency loss (needs 2 synced cams) | + cross-view consistency | M |
| VIB scene stream [W3_VisionBasedManipulatorsNeed...md] | Meta-World RL | VIB on third-person +21 IQM; on both views hurts | + bottleneck scene stream only | M |
| Anchor-Align [W3_GeneralizableVLAFinetuning...md] | LIBERO-PRO + real | anchoring +7.1, direction-word aux +4.9 | + feature anchoring | M |
| AFP [W4_ArtificialFoveatedPerceptionforMitigatin.md] | real π0.5 | attention-mask aux: OOD 0.30→0.67 | + attention grounding (needs masks) | M |
| WhatsTheMove [W4_WhatstheMoveHybridImitationLearningviaSa.md] | sim 50 demos | salient-point aux Square 13→65.5 | + target-point aux | M |
| ImprovingGenBC [W4_ImprovingGenerativeBehaviorCloningviaSel.md] | Push-T | CFG 0.070 vs vanilla 0.496 | − CFG guidance | M |
| SimulationDistillation [W3_SimulationDistillationPretrainingWorldMo.md] | sim | +pixel recon 0.90→0.32 | − pixel reconstruction aux | M |
| VisionBasedMultiTask [W3_VisionBasedMultiTaskManipulationforInexp.md] | $500 arm, scratch encoder | VAE-GAN recon 41→81.6 | + recon only for scratch low-res encoder | M (not our case) |
| KnowledgeInsulation [F/KnowledgeInsulation.md] | π0 | aux discrete objective converges 7.5× faster; heads mutually masked | ~ aux action objective (untested small) | M/L |

**Adjudication.** Future-prediction auxiliaries consistently help when the target is a compact latent from a frozen/EMA encoder and the loss enters the action stack (FLARE, Reflex, JEPA-Policy, SLIM); raw-pixel or raw-patch targets help less or hurt (FLARE vs UWM, AR-WAM raw patches −10.8 [W4_ARWAMA...md], SimulationDistillation). Gains at ≤100 demos from scratch are small (MDT ≈+1 at 20 demos) — treat as cheap insurance, ablate off. The Hermite regulariser is the only aux with a large real smoothness+success effect and it costs nothing; its evidence is on a 3B model with ~800 demos, so its transfer to us is unverified.

**Residual doubt / ablation:** three runs on identical data: no aux; +Hermite; +Hermite+future-latent. Compare success and commanded-action D2/boundary-jump.

### Q10 Latency, asynchrony, and continuity

**Verdict:** (1) First make inference fast (bf16, torch.compile/CUDA graphs, performance power mode, static buffers, resize before transfer); target <40 ms per query for our model. (2) Measure camera and servo latency and put both into the delay estimate. (3) Async with a timestamped executor: request the next chunk while executing, index into the new chunk at (now + measured delay), discard stale actions, hold last pose if starved. (4) Continuity: train the flow head with TT-RTC prefix conditioning (random d ∈ [0, d_max], clean ground-truth prefix, loss on postfix) plus VLASH state-offset augmentation and feed the last queued target as state; no linear fade, no temporal ensembling. (5) Interpolate 10/30 Hz targets to the 100 Hz servo loop with a C1 profile. Confidence H for (1)–(3), M/H for (4), M for (5).

| Paper | Setting | Key number | Direction | Weight |
|---|---|---|---|---|
| A2C2 [RT/A2C2.md] | laptop RTX 5080 | SmolVLA 101 ms/inference; residual head 4.7 ms | ~ 2 s is deployment | H |
| ReactVLA [F/ReactVLA.md] | real | SmolVLA 82.2 ms; iMF 38.6 ms | ~ | M |
| FlashVLA [RT/FlashVLA.md] | desktop | SmolVLA 19.7→10.1 ms optimised | ~ | M/H |
| JetsonPI [RT/JetsonPI.md] | Orin | 30 W vs 50 W 1.6×; CUDA graphs reaction 1420→165 ms with scheduling | + power mode, CUDA graphs | M/H |
| QuantACT8GB [RT/QuantACT8GB.md] | SO-101 Orin Nano | ACT FP32 114 → TRT FP16 17.9 → INT8 12.7 ms; 19/18/19 of 20 | + TensorRT FP16 | M |
| MolmoAct2 [W4_MolmoAct2...md] | H100 | CUDA Graph + caching 23→55.8 Hz | + graph capture of flow loop | H |
| VLAPerf [RT/VLAPerf.md] | analytic, validated | 10→1 steps −26% E2E; chunk 5→50 nearly free | ~ prefill dominates VLM policies | M/H |
| AsyncInferenceStudy [RT/AsyncInferenceStudy.md] | SmolVLA LIBERO | vision prefill 89.8% of FLOPs; naive async collapses with d; A2C2 best at high d; TT-RTC robust on short chunks | + never naive async at d≫1 | M |
| UMI [F/UMI.md] | real tossing | latency matching 105/120 vs 69/120; jitter removed | + measure & compensate latency | M/H |
| LatencyAwareIndustrial [RT/LatencyAwareIndustrial.md] | ABB, 20×3 | camera 82 ms, actuator 225 ms; timestamped buffer keeps jerk within 9% of demo at 100–500 ms | + timestamped executor | M |
| RealtimeVLAV2 [RT/RealtimeVLAV2.md] | engineering | readout 33 + camera 55 + proprio 50 + motion lag 150 ms | + measure non-model delays | M |
| RTC [F/RTC.md] | π0.5 real, 480 episodes | TE protective stop at +100/+200 ms; RTC robust to +200 ms | + inpainting async; − TE | H |
| TrainingTimeRTC [RT/TrainingTimeRTC.md] | Kinetix + π0.6 real | ≥ RTC at d≥2; 108 vs 135 ms E2E | + train-time prefix conditioning | M/H |
| ActionControlNet [RT/ActionControlNet.md] | real SO-101, 50 demos | naive async 17/20 → prefix-conditioned 20/20, less oscillation | + prefix conditioning on our arm | M |
| Soft RTC [RT/ActionPriorDenoising.md] | real single arm, 10 trials | base 6/10, hard TT-RTC 9/10, soft 8/10; boundary jump 0.052→0.0285→0.0118 | + hard prefix first; log D1–D3 | M |
| VLASH [RT/VLASH.md] | Kinetix, LIBERO SmolVLA, real SO-101 | d=4 81.7 vs naive 51.2; SmolVLA LIBERO d=3 79.1 vs sync 79.0; ping-pong 11/20 vs 0/20 | + state roll-forward + offset FT (any head) | M/H |
| DEFLECT [W3_DEFLECT...md] | Kinetix + real conveyor | overlap ≤3 → RTC/BID ≤5%; VLASH 67.1 | + keep d ≪ chunk; + state forwarding | M/H |
| REMAC [RT/MaskedActionChunking.md] | Kinetix + real π0 | LoRA prefix masking 0.61→0.78 avg d>0; robust to mis-estimated delay | + LoRA-able; delay jitter tolerated | M |
| PAINT [RT/InitialNoiseSelection.md] | real GR00T/π0, 20 trials | ≈ RTC success, no VJP; TE/B-spline ≈ naive | + training-free fallback; − smoothing | M |
| Legato [F/Legato.md] | dual-arm real | ~10% smoother/faster than RTC; stops mode switching | + training-time continuation | M |
| BID [F/BidirectionalDecoding.md] | sim + real | EMA under noise 18.4 vs 29.5; 2× latency | − TE/EMA; ~ coherence selection | M |
| ImprovingGenBC [W4_ImprovingGenerativeBehaviorCloningviaSel.md] | real SO-100 DP, 30 Hz | EMA below vanilla; similarity-gated switching 70% moving-cup; BID 16 Hz halting | − TE; + gated switching | M |
| ChainVLA [W3_ChainVLAChainingVisionLanguageActionQuer.md] | sim | TE and linear blend 0% on memory tasks; suffix-init −57% seam | − post-hoc blending; + suffix init | M |
| χ0 [W4_0ResourceAware...md] | real π0.5 | drop-stale + linear cross-fade > sync/naive/TE/RTC "in most cases" (figure) | ~ cross-fade OK for big unimodal-ish VLA | M (figure only) |
| CogACT [F/CogACT.md] | SIMPLER | similarity-weighted ensemble 62.5 > TE 58.9 > 2-step chunk 50.7 | ~ ensembling helps in sync sim | M |
| MINERVA [W4_MINERVA...md] | sim, ~5 ms model | TE 96.3 > BID 95.0 > plain 94.1 > RTC 91.8 with replan every step | ~ TE fine when latency ≈0 | M (sim) |
| FurnitureVLA / TRI [W3_FurnitureVLA...md, W4_ASystematicStudy...md] | sync big VLA | recency-weighted TE 0.80 vs uniform 0.62; avg of last 4 chunks removes jerk | ~ recency TE at low latency | M |
| StreamingFlowPolicy / StreamingDP [F/StreamingFlowPolicy.md, RT/StreamingDP.md] | sim + real Push-T | chunk starts at last action; SDP 0.85 vs DP 0.50 | + start next chunk from current state | M |
| HybridFlow [RT/HybridFlow.md] | real 80 trials | naive 1–2 step 0%; 19 ms vs 152 ms | − naive step cutting | M/H |
| AhaRobot [W3_AhaRobot...md] | STS3215 | trapezoidal/C1 profiling + dithering → 0.72 mm; π0 chunk discontinuities knocked tools | + servo-level profiling | M |
| TuneToLearn [W3_TunetoLearn...md] | real + RL sim2real | jitter failures 21.8% @100 Hz → 5.0% @10 Hz; compliant gains attenuate action noise | + compliant follower gains | M |
| vla.simd [W3_vlasimd...md] | SO-101 CPU | need H/T_q ≥ 2× control rate for time-aligned async | + chunk ≥ 2× delay | M |
| OpenVLA [F/OpenVLA.md] | real | inference 1.2 Hz on a 5 Hz task: 71→58 | − inference slower than control rate | M |
| Reflex [W4_Reflex...md] | dynamic sim | async < sync at low inference Hz; > sync near 20–30 Hz; CUDA graph 125→65 ms | + cut latency before async | M |
| CT-VAM [W4_CTVAMA...md] | real 68M policy | 56 ms on RTX 4080; FCI async hides latency at 20 Hz | + small policy + overlap inpainting | M |

**Adjudication (temporal ensembling helps vs hurts).** TE helps when (a) the head is near-deterministic (ACT with z=0: +3.3% [F/ACT.md]; MINERVA L1/flow at 1M params in sim), (b) inference is synchronous or latency ≈0 so the averaged chunks share the same observation (MINERVA, CogACT, FurnitureVLA), and (c) weighting is recency-biased rather than uniform (FurnitureVLA 0.80 vs 0.62; WhyChunking 71.8 vs 42.2). TE hurts when the head is stochastic and chunks come from different modes (RTC, BID, ImprovingGenBC on a real SO-100, PAINT, ChainVLA) and when latency is significant (RTC's protective stop). Our situation is (stochastic flow head, ~50–100 ms latency after fixes, backlash arm) — the "hurts" regime. χ0's cross-fade result is figure-only and on a 3B model with 20 h/task of data. Your current linear fade is a TE-class average and was observed to be jumpy; replace it with prefix conditioning.

**Adjudication (which async method).** Rankings flip by benchmark (Track A §5.1), but at our post-fix delay (d≈1–2 at 10 Hz, ≈3–6 at 30 Hz) every continuity method works and the zero-inference-cost ones (TT-RTC, VLASH, REMAC) are preferred; RTC's guidance adds ~27 ms and doubles expert latency [RT/TrainingTimeRTC.md, RT/VLASH.md]. VLASH's state forwarding assumes the servo tracks the last command, which backlash violates; SAIL's rule of gating continuity on tracking error [RT/SAIL.md] and measuring the commanded-vs-reached gap on our arm is the mitigation. The intermediate step, if retraining is not yet possible, is PAINT (N extra small-expert forward passes, no backward).

**Residual doubt / ablation:** same checkpoint, four executors: (i) sync, (ii) naive async, (iii) async + TT-RTC prefix, (iv) async + TT-RTC + VLASH state; 20 trials each; log D1/D2/D3, boundary jump, completion time.

### Q11 Cameras

**Verdict:** Keep both cameras; wrist camera is the anchor stream (no dropout, no crop), scene camera is regularised (token dropout, rare whole-view drop, stronger geometric aug). Mount the scene RealSense rigidly with a fiducial so its pose can be re-registered; re-position it by small amounts between recording sessions; if convenient, add a second cheap scene camera during data collection only. Prefer a wider-FoV wrist lens. Confidence H for keeping both, M for the regularisation, M for the camera-pose protocol.

| Paper | Setting | Key number | Direction | Weight |
|---|---|---|---|---|
| robomimic [F/robomimic.md] | real Can | 73.3 vs 43.3 without wrist | + wrist | H |
| MResT [W4_MResT...md] | real Franka | 75.0 / no-wrist 7.5 / no-scene 20.0 | + both | M/H |
| Hsu et al. [W3_VisionBasedManipulatorsNeed...md] | sim + real 360 demos | OOD wrist 52 vs third 20 (both 85 ID); both+VIB 87.7 vs naive both 66.3 | + wrist primary; regularise scene | H/M |
| JEPA-Policy [W4_JEPAPolicy...md] | sim single seed | fixed+wrist > either alone (Tool Hang 65 vs 27.5/35) | + both | L/M |
| Dita / VPP [F/Dita.md, F/VideoPredictionPolicy.md] | LIBERO/CALVIN | +wrist 82.4→92.3; 3.58→4.33 | + wrist | M |
| CoLA-Flow [W4_CoLAFlowPolicyTemporallyCoherentImitatio.md] | real | recovery 90→30 without wrist | + wrist for recovery | M |
| SEVO [W4_SEVO...md] | SO-101 on MOBILE base | +wrist: ACT 90→86, SmolVLA 79→12 | − wrist (mobile base, saturated LED) | L for fixed arm |
| DoYouNeedProprio [W4_DoYouNeedProprio...md] | real | overhead cam hurts under placement shift (holder moved 20 cm: 0 vs 0.80 without); dual wide wrist best | ~ scene cam is the shift-fragile stream | M |
| UMI [F/UMI.md] | real | 69° FoV crop 11/20 vs fisheye 20/20 | + wide wrist FoV | M |
| InfiNoVA [W4_InfiNoVA...md] | SO-101 SmolVLA | ref view 65.3 → random views 7.5 (wrist present); 5 physical views 24; dense NVS 40.5 | ~ wrist alone does not fix camera shift | H |
| RoVi-Aug / VistaBot / FromFixedToFree [W3_RoViAug...md, W3_VistaBot...md, W4_FromFixedtoFree...md] | real | 10 cm/20° → 0%; ±45° ACT 0.79→0.15; π0 63→16 at 15° | − fixed single view without aug | H |
| VolumeDP [W3_VolumeDP...md] | real | ±5° rotation DP 0% | − 2D fixed view | M |
| SeeingAllAngles / GroundingSim2Real / WhatMattersLargeScale [W3_SeeingAlltheAngles...md, W4_GroundingSimtoReal...md, W4_WhatMattersinLearningfromLarge...md] | real/sim | demos from randomised poses: little fixed-view penalty; ±1 cm pose DR +10–20 pts; camera pose is the most harmful misaligned DV | + small camera-pose diversity in data | M |
| BeyondViewpoint [W3_BeyondViewpointGeneralizationWhatMultiVi.md] | sim + real 30 demos | extra ±20° views help even at fixed test view (12.5→58.0) | + moderate multi-view data | M |
| CrossView [W4_CrossView...md] | real | nominal-only 16.8 vs multi-view 74.7; +consistency 87.2 | + synced multi-view + consistency | M |
| M3 [W4_RobustBimanual...md] | 0.5B VLA | mask both wrists jointly 64.0 vs mask ego 37.0 | ~ anchor view choice is setup-specific | M |
| EGR [W4_SensingWhichModality...md] | real | policies depend on uninformative views; EGR 21/40→36/40 | + train each view to be sufficient | M |
| X-VLA [F/X-VLA.md] | pretraining | wrist view outside VLM: +16.7 | ~ separate wrist path | M |
| DecomposingGap [W3_DecomposingtheGeneralization...md] | real RT-1 | camera pose 45.8 < texture 52.8 < distractors 80.6 < lighting 83.3 < background 88.9 | ~ camera shift hardest | M/H |

**Adjudication (wrist essential vs hurts).** SEVO's negative result is on a mobile base with a body-fixed camera pair, a red LED that saturates the close wrist view, and a 400k-step/batch-24 ACT run; every fixed-base study with a decent wrist view finds the opposite (robomimic H, MResT, Hsu H, JEPA-Policy, Dita). Hsu's finding that naive fusion can be worse OOD than wrist-only, fixed by bottlenecking the third-person stream, plus DoYouNeedProprio's overhead-camera harm under placement shift and InfiNoVA's collapse under view change, all point the same way: the scene camera is the stream that overfits to scene statistics and camera pose. So keep it, but regularise it and diversify its pose in the data. Which stream to anchor is setup-specific (M3 anchors the ego view for a bimanual head-cam rig); for a single fixed arm the wrist view is the anchor.

**Residual doubt / ablation:** wrist-only vs scene-only vs both vs both + scene token dropout, on in-dist and camera-nudge cells.

### Q12 Model size

**Verdict:** ~55M total (22M ViT-S encoder + ~20M trunk + ~10M flow expert), all trainable; do not exceed ~100M trainable from scratch; inference budget <40 ms/query on the RTX 5060; training fits 8 GB at batch 32 with bf16. Confidence M/H.

| Paper | Setting | Key number | Direction | Weight |
|---|---|---|---|---|
| BAKU [W3_BAKU...md] | LIBERO-90 50 demos/task | 4.4M .85, 10M .90, 31M .87, 114M .19 | + 10–30M trainable | M/H |
| MINERVA [W4_MINERVA...md] | sim | 0.54M 95.05 … 9.66M 97.45 vs π0.5 97.5; 5M new objects 62→96 | + small; capacity helps generalisation | M |
| QuantACT8GB / ArmnetBench / SO101-Benchmark [RT/QuantACT8GB.md, W4_Armnet...md, F/SO101-Benchmark.md] | SO-101 real | ACT 52.6M 19/20; ACT 63 vs SmolVLA 23 on pick-place; ACT 33.75 ≈ SmolVLA 32.5 | + ACT-size sufficient | M |
| WhatIsTheBetterCurriculum [W3_WhatistheBetterCurriculum...md] | Piper + SO-101 leader, 30 demos | ACT 18M 95% = π0.5 95% | + small in-dist | M |
| MobileALOHA [F/MobileALOHA.md] | 8 GB laptop | ACT trains + runs real-time on RTX 3070 Ti | + fits 8 GB | H |
| HPT [F/HPT.md] | RTX 3070 | 12.6M trunk 47 Hz | + small trunk real-time | H |
| DataScalingLaws [F/DataScalingLaws.md] | UMI | U-Net small/base/large 0.88/0.90/0.83 | + small head | M |
| Hyper-DP3 / PocketDP3 | sim + real | 2.5M ≈ 255M | + tiny decoder | M/H |
| PatchPolicy [W4_PatchPolicy...md] | real | 22.8M→40.4M trunk 0.07→0.83 Push-T; ~50M beats 7.6B OFT | ~ trunk must not be too small | M |
| WhatDoWeLearn [W3_WhatDoWeLearn...md] | real 30–150 demos | ViT-B > ViT-L in all configs | + smaller encoder | M |
| XR-1 / MoE-ACT [W4_XR1...md, W4_MoEACT...md] | downstream-only | 230M 42.5 > full large 28.3; dense ACT 84M→0.9B 44.6→48.5 | − dense scaling in low data | M |
| TinyVLA [F/TinyVLA.md] | real | 0.4B VLA 23.3 < DP 35.3; ≥0.74B better | − small VLA from own VLM | M |
| TurboVLA / DEM / ProgVLA / CT-VAM | sim + real | 0.2B LLM-free 31 ms 0.9 GB; 0.1B beats SmolVLA 2.25B; 68M ≈ π0 | + 0.1–0.2B LLM-free sufficient | M |
| ImprovingAffordable [W4_ImprovingtheperformanceofAIpoweredAfford.md] | Moss arm | ACT dim ≤64 unstable without TE | ~ don't shrink below d≈128 | L |
| LPS / EMS [W4_LatentPolicySteering...md, W3_FastandAccurate...md] | 50 demos | sim DP 550K ≈ π0.5 (57 vs 61) but real π0.5 69 vs DP 46; small policy 20 vs 56 under full randomisation | ~ pretrained large helps under wide variation | M |
| RoboDual [W3_TowardsSynergistic...md] | real | 20M specialist does the motor work at 15 Hz | + small fast specialist | M |

**Adjudication.** Larger pretrained VLAs win when the distribution is wide or multi-task (ArmnetBench eye_drops_to_shelf ACT 0 vs π0 76; EMS full-workspace 20 vs 56) and lose or tie on simple single-arm pick-place at 50 demos. Their advantage is pretraining, not parameter count (LPS sim vs real; GR00T 10% data ≈ DP full [F/GR00T-N1.md]) and none fits the 8 GB/latency budget. For a single task with 100–150 diverse demos, the ~50M class is the evidence-backed choice; the compensating lever for the width of the distribution is data diversity and augmentation (Q05, Q13), and, later, co-training with community SO-100/101 data (Q13).

### Q13 Data

**Verdict:** 100–150 demos for the single pumpkin task, collected under a written protocol: 30 fps, 4–6 pumpkins, 3–4 lighting conditions, 3–4 backgrounds/table covers, distractors in ~30%, small scene-camera re-positioning between sessions, placements on a grid covering slightly more than the evaluation region, randomised start pose, one operator with one consistent strategy and decisive (non-hesitant) motions, slow gripper closure, 15–25% of episodes containing an in-episode failed grasp→recovery, idle prefix/suffix trimmed, a replay-ability spot check, and later an intervention (HG-DAgger/RaC-style) round with the leader arm. Co-train 30–50% with retrieved same-embodiment public SO-100/101 episodes only if their camera layout is compatible. Confidence H for diversity-over-count and recovery data, M for the counts.

| Paper | Setting | Key number | Direction | Weight |
|---|---|---|---|---|
| DataScalingLaws [F/DataScalingLaws.md] | >15k blind rollouts | 8 objects → >0.8 unseen; 50% vs 100% demos/env overlap; ≤100 total "unstable" | + diversity; ~100–150 partial OOD | H |
| DemoGen [F/DemoGen.md] | sim + real | success region = union of demonstrated placements; 100→150 demos +37, 150→200 +6; ADR 40.4→92.3 | + placement grid; + recovery data | H/M |
| UMI [F/UMI.md] | real | 1400 demos/30 envs 71.7% unseen; narrow data 0% | + scene diversity | H |
| SEVO [W4_SEVO...md] | SO-101, 100 trials/cond | varied bg/light/distractors +9–23 pts; novel room 30→85 | + diversify collection | H/M |
| E-VLA [W3_EVLA...md] | SO100 | multi-illumination: 40 lux 30→80 | + varied lighting | M |
| π0.5 [F/pi0.5.md] | 104 locations | monotone gain with #locations | + diversity | M |
| RT-1 [F/RT-1.md] | 130k | 75% tasks ≈ 51% data; ≤50 ep/task unseen 14% | + diversity | M/H |
| MobileALOHA [F/MobileALOHA.md] | real 8 GB laptop | co-train 50/50 same-embodiment: +0 to +95; 35 co-trained > 50 plain; ratio 30–70 insensitive | + co-train with same-embodiment data | M/H |
| WhatMattersLargeScale [W4_WhatMattersinLearningfromLarge...md] | real | all-DROID co-train 0%; retrieved aligned subsets up to 85 | + retrieve aligned data only | M |
| MolmoAct2 [W4_MolmoAct2...md] | SO-100 | filtered community SO-100 data enables 56.7% zero-shot vs SmolVLA 2.3 | ~ community data usable if filtered | M |
| LBM [F/LBM-CarefulExamination.md] | 1800 blind rollouts | 15% task data + pretraining beats 100% single-task; idle-start trimming (5 cm/15°); ≥50 trials to separate policies | + trim idle; + evaluation power | H |
| FAST / SeedPolicy / REBOOT [F/FAST.md, W3_SeedPolicy...md, W3_REBOOT...md] | various | idle frames → hovering/freezes | + trim pauses | M |
| robomimic [F/robomimic.md] | sim/real | MH 300 < PH 200; +100 worse demos hurt BC | + quality/consistency | M/H |
| ElicitingCompatible [W3_ElicitingCompatibleDemonstrationsforMult.md] | sim + real | 5 incompatible demos halve success (24.7→4.0; real 60→30) | + one strategy | M |
| WhatIsTheBetterCurriculum [W3_WhatistheBetter...md] | SO-101 leader, 30 demos | consistent demos 95% vs best-of-100 manual 15–30% | + consistency | M/H |
| CurseOfPrecision [W4_TheCurseofPrecision...md] | sim | decisive expert 1.27 mm vs cautious 2.35 mm | + decisive motions | M |
| RoboMIND [W3_RoboMIND...md] | large real | positioning errors from non-random placement (up to 48%); gripper failures from fast closure | + randomise placements; slow gripper | M |
| VBT [W3_VisualBacktrackingTeleoperationADataColl.md] | real 1437 eps | in-episode fail→recover: BC 66→73 | + in-episode recovery demos | M |
| ADC [W4_AdversarialDataCollectionHumanCollaborat.md] | real π0 | 20% ADC ≈ 0.65 vs 100% traditional 0.24; dynamic 0→0.88 | + perturbation demos (moderate for small models) | M |
| RaC / IWR / BC-Z / HiWM [W3_RaC...md, W3_HumanintheLoop...md, W3_BCZ...md, W3_HiWM...md] | real/sim | recovery+correction 61/100 vs 23/100; IWR 87.3 vs 76.7; HG-DAgger 27→53; corrections +37.9 | + intervention rounds | M/H |
| ALOHA-Unleashed [F/ALOHA-Unleashed.md] | 26k demos | shortest-50% filter 55 vs all 30; over-filter 40; retries emerge only if in data | ~ mild filtering; + recovery | L/M |
| S2I [W3_TowardsEffectiveUtilizationofMixedQualit.md] | real 50 mixed demos | repair segments > discard; smoothing good demos −27% | + segment-level cleanup only | M |
| MOVE [W4_MOVEASimpleMotionBasedDataCollectionPara.md] | Piper orange→tray | static 3.3 vs MOVE 23.3 at 35k steps | + spatial coverage per demo | M |
| ArmnetBench / SO101-Benchmark / HiFlow | SO-101 / 10 Hz | 50 demos → 60–70% simple pick-place; recovery rates ACT 6.5%, SmolVLA 3.2% | ~ 50 is a floor; recovery is the gap | M |
| RoboTwin 2.0 / SeedPolicy | sim | clean-only → ~1% under randomisation | − clean-only | H |
| TuneToLearn [W3_TunetoLearn...md] | real | compliant gains → steeper data scaling | + tune gains before collecting | L/M |
| GELLO [W3_GELLOAGeneralLowCostandIntuitiveTeleoper.md] | novices | joint-space leader .92 vs VR .72 | + leader-arm teleop | M |
| OnBringingRobotsHome [W3_OnBringingRobotsHome.md] | 109 tasks | novice 10%→70% by second task | + practice episodes | M |
| RoboAgent [F/RoboAgent-MT-ACT.md] | real | new task: 50 demos ×4 aug + 10% replay, no forgetting | + adding a task later | L |

**Adjudication (quality/consistency vs diversity/exploration).** These are orthogonal axes: vary environment, object, lighting, placement (helps everywhere), keep *strategy* consistent within a state (Eliciting, WhatIsTheBetterCurriculum, robomimic), and add recovery from realistic failure states with a consistent correcting action (VBT, RaC, DemoGen ADR). Blindfolded's exploratory-demo result needs a memory policy and 400 demos/shape; not for us. ADC's small-model caveat (ACT oscillated on very diverse data) argues for moderate perturbations.

**Residual doubt / ablation:** hold out one lighting condition and one pumpkin entirely; compare a 100-demo diverse set vs a 100-demo single-condition set trained identically (this is also the go/no-go gate in Section 8).

### Q14 Robustness

**Verdict:** Expected difficulty ordering for our policy: camera pose ≈ new object appearance > distractors > lighting > background, where lighting and background are the axes most fixable by data+augmentation and camera pose the least. Robustness is engineered through Q05+Q11+Q13; architecture (Q03 pretrained tokens) shifts the floor; object-centric inputs (Q04) are the escalation for appearance/clutter. Confidence M/H.

| Paper | Setting | Key number | Direction | Weight |
|---|---|---|---|---|
| DecomposingGap [W3_Decomposing...md] | real RT-1 | camera 45.8 < texture 52.8 < distractors 80.6 < lighting 83.3 < background 88.9; factors don't compound | ~ ordering | M/H |
| GroundingSim2Real [W4_GroundingSimtoReal...md] | >10k real trials | distractors largest drop, lighting smallest (big VLA) | ~ | M |
| CRAFT / RoboTwin / SeedPolicy / TFGCA / PriorVLA | ACT/DP/DP3 clean-trained | 0–6/20 real; ~0–6% randomised sim | − clean-only small policies | H |
| ChromaGuard / E-VLA / SutureBot [W4_LightsCamera...md, W3_EVLA...md, W3_SutureBot...md] | SO-101/SO100/dVRK | SmolVLA 70→0 spotlight; 100→0 at 30 lux; ACT 9→3, π0 7→0 under new lighting | − pretraining for lighting | M/H |
| GreenScreenAug / RoboEngine / SEVO | real | bg replacement +65%; +210%; diversified collection 30→85 | + data/aug for bg/lighting | H/M |
| GenAug / GR00T / ReShoot / VO-DP | real | object appearance hardest (pick 45 vs env 85; 92→72; 0/40 on colour; blue 50/green 40 vs 85) | − appearance is the hard axis | M/H |
| OBEYED / FoundationSmall / ARRO / SKIL / GAM / ControlVLA | real | masking/canonical inputs: 5→85 distractors; SmolVLA 4→78 tabletop colour; unseen objects 72.8 vs 25 | + object-centric escalation | M/H |
| InfiNoVA / FromFixedToFree / VistaBot / RoViAug / VolumeDP | real | camera shift catastrophic for all (SmolVLA −88.5%; π0 63→16; DP 0 at ±5°) | − camera shift hardest; physical fix first | H |
| CAGE / GLUE / TinyVLA / DiVLA [W3_Cage...md, W3_GLUE...md, F/TinyVLA.md, W3_DiffusionVLA...md] | real | pretrained ViT/VLM policies keep 30–87% under bg/obj/cam vs 0 scratch | + pretrained tokens raise floor | M |
| Seer / LBM / RoboDual [F/Seer-PIDM.md, F/LBM...md, W3_TowardsSynergistic...md] | real | pretraining advantage grows under shift (3/16→10/16 sim); scratch bg 6.7 | + pretraining/co-training as regulariser | H/M |
| Rewind-IL / RUM [RT/RewindIL.md, W3_RobotUtility...md] | real low-cost arms | detect+rewind: perturbed 18.3→76.7; retry +15.6 | + runtime monitor + retry | M/H |
| UnbiasedLook [F/UnbiasedLookPVR.md] | real | policy dropout 0.2: perturbed 10→24% | + dropout | M |
| ItsNotJustMoreDemos [W3_ItsNotJustMoreDemos...md] | sim ACT | nuisance mean 0.30; targeted counterfactual repair 0.96 | + action-drift audit | M |

**Adjudication (SmolVLA vs ACT on SO-101).** SmolVLA's paper (78.3 vs ACT 48.3) compares a multi-task, community-pretrained SmolVLA to single-task ACT with partial credit and unstated trial counts; its own single-task no-pretrain SmolVLA is 40.0 < ACT 48.3 [F/SmolVLA.md]. Independent SO-101 benchmarks with per-task fine-tuning find ACT ≈ SmolVLA (33.75 vs 32.5, recovery 6.5 vs 3.2% [F/SO101-Benchmark.md]) or ACT > SmolVLA (63 vs 23 on pick-place; SmolVLA worst of 7 [W4_ArmnetBench...md]; ACT 95 vs 83 [W4_SEVO...md]), and every robustness study finds SmolVLA as fragile as any small policy to lighting/view/distractors (ChromaGuard, InfiNoVA, E-VLA, Guided Action Flow 0/11 with one distractor [W4_GuidedActionFlowQGuidedInferenceforFlowM.md]). Its zero-shot value on a new SO-100 rig is ~2% [W4_MolmoAct2...md]. Conclusion: SmolVLA's advantage is multi-task pretraining, which we do not exploit in a single-task fine-tune; the frozen vision tower and the missing continuity mechanism make it a poor base for our robustness and latency goals.

---

## 3. Architecture specification ("SO-101 flow policy v1")

Buildable as a LeRobot policy class (config + `select_action`/`predict_action_chunk`) on LeRobotDataset v3 with the existing `observation.images.camera1` (scene), `observation.images.camera2` (wrist), `observation.state` (6-D) and `action` (6-D absolute leader targets) keys. Where a number below is an estimate rather than a paper measurement it is marked (est.).

### 3.1 Inputs and preprocessing
- Two RGB streams at 224×224 (resize from 640×480 with aspect-preserving crop; scene camera: random-resized crop of 90–95% then resize; wrist: crop 95% + resize). Resolution 224 is the standard in every small-policy note that reports it (DP, LBM, DEM, SLIM); FurnitureVLA's 224→448 gain [W3_FurnitureVLA...md] is on a 3B model and costs latency we do not have. 112–128 px suffices for pick-place in several notes (ProgVLA 112², JEPA-Policy 128², RoboSplat 128²) and is the fallback if latency is tight.
- Proprio: 6-D joint state (degrees, gripper 0–100) → quantile-normalised (1–99%) → one token. No velocities, no history (Q07).
- Actions: chunk of H absolute leader-joint targets (6-D), per-dimension quantile-normalised to [−1, 1] using 1st/99th percentiles (π0.5/FAST practice [F/pi0.5.md, F/FAST.md]; LBM uses 2–98% → [−1.5, 1.5] [F/LBM-CarefulExamination.md]).

### 3.2 Vision encoder (≈22M params, trainable at LR ×0.1)
- DINOv2 ViT-S/14 (or DINOv3 ViT-S/16), pretrained, shared across both cameras with a learned per-camera embedding added to the patch tokens. Shared vs separate: BAKU shared .90 vs separate .92 [W3_BAKU...md]; separate wrist path helped X-VLA (+16.7) only because their alternative was pushing the wrist view through a VLM [F/X-VLA.md]; sharing halves memory and latency. Ablation arm: separate encoders.
- Output: 256 patch tokens per camera at 224/14=16×16 (DINOv2) → 2×2 average-pooled to 64 tokens per camera (GR00T's budget [F/GR00T-N1.md]; PatchPolicy shows 256→64 costs little vs 256→1 [W4_PatchPolicy...md]). Never CLS/mean-pool to a single vector (Q03).
- Fallback encoder for the ablation and the ACT baseline: ImageNet ResNet-18 (11M) with spatial-softmax/flattened 7×7 features, or X-Distill's DINOv2-distilled ResNet-18 weights [W3_XDistill...md].
- Regularisation on the scene stream only: token dropout p=0.3–0.5 (w2VLA 50% masking [W3_DecouplingtheDeclarative...md]; M3 structured masking [W4_RobustBimanual...md]), whole-scene-view drop p≈0.1 (tokens replaced by a learned "missing" token). Wrist stream never dropped.
- Optional (v1.1): feature-anchoring loss to a frozen copy of the encoder on 10% of tokens (Anchor-Align [W3_GeneralizableVLAFinetuning...md]) if OOD tests show drift.

### 3.3 Trunk (≈20M params, from scratch)
- Transformer encoder, 6 layers, d=512, 8 heads, MLP 2048, pre-LN, over the sequence [64 scene tokens, 64 wrist tokens, 1 state token, 1 task/ID token] = 130 tokens. Size rationale: BAKU 10–31M ≈ optimal [W3_BAKU...md]; PatchPolicy trunk 22.8M→40.4M mattered [W4_PatchPolicy...md]; MINERVA "shrink the head, not the eyes" [W4_MINERVA...md].
- Proprio token receives dropout p=0.3 and Gaussian noise σ≈1° (Q07); VLASH offset augmentation feeds the state at t+δ with the action targets shifted accordingly (Q10).
- Task/ID token: learned embedding (v1: constant); v2: FiLM from a frozen MiniLM/T5-small text embedding (Q08), zero-initialised.

### 3.4 Action expert / head (≈10M params)
- Flow-matching DiT: 6 blocks, d=384, 6 heads; action tokens (H×6-D projected) with self-attention among action tokens and cross-attention to the 130 trunk tokens; flow time τ injected by AdaLN in every block (π0/GR00T pattern [F/pi0.md, F/GR00T-N1.md]; TRI found per-layer τ injection matters [W4_ASystematicStudy...md]); per-token τ so that TT-RTC prefix conditioning works [RT/TrainingTimeRTC.md].
- Training: conditional flow matching with linear (OT) path, τ ~ Beta-shifted toward high noise as in π0 [F/pi0.md], MSE on velocity; 10 steps sampled per chunk in the loss as in MolmoAct2 K=8 > K=1 [W4_MolmoAct2...md] (cheap: one encoder pass, several expert passes).
- Inference: 5–10 Euler steps (Q01); prefix overwrite each step with the committed actions (TT-RTC inference rule).
- Optional CVAE latent (ACT-style, KL β=10, z=0 at test) conditioning the expert — enable if multiple operators contribute data (XS-VLA +4.6 [W4_TeachingTiny...md]).
- Auxiliary heads (training only, dropped at inference): Hermite/trajectory-smoothness head (K=2 cubic Hermite boundary states, λ≈1–10 [W3_Hermite...md]); 4 future tokens cosine-aligned to the EMA encoder's pooled embedding at t+H (FLARE λ=0.2, ρ=0.995 [F/FLARE.md]); optional depth-prediction head on scene tokens (v2).

### 3.5 Chunk length and execution
- At 10 fps: H=16 (1.6 s), execute 5–8 (0.5–0.8 s). At 30 fps: H=48 (1.6 s), execute 15–24. Rationale: Q06 (ACT k≈1–2 s; DP 16/8; SmolVLA 10 of 50; DVAC Fix15 > Fix40; OBEYED H=10 at 10 Hz).
- Async continuity: TT-RTC prefix conditioning, d sampled from [0, d_max] with d_max = measured delay + 1 step margin (at 10 Hz d_max≈2; at 30 Hz d_max≈5); VLASH state roll-forward (state token = last queued target, or measured state if tracking error is large [RT/SAIL.md]).
- Temporal ensembling: OFF (Q10). Linear fade: OFF.

### 3.6 Depth / object-centric branch (v2, off by default)
- Segment pumpkin + tray (+ gripper) in the scene view (first-frame prompt + SAM2-small tracking, or a colour/YOLO-seg detector), back-project with RealSense intrinsics to ≤512 points per object in the camera frame (iDP3 camera-frame, no extrinsics [F/iDP3.md]), MLP(64)+max-pool per object → 2 tokens; zero-initialised linear into the expert's cross-attention memory (PointVLA injection [F/PointVLA.md]). Adds ≈0.3M params, ≈1–5 ms (est., PocketDP3 encoder+decoder 4.5 ms total [W4_PocketDP3...md]) plus segmentation cost (SAM3 ≈15 ms/prompt on a 4060 Ti [W4_FoundationandSmall...md]; SAM2-small similar order, est.).
- Alternative cheaper depth use: masked depth of the pumpkin as an extra image channel injected at a mid-level feature map, not at the pixel stem (SVP-IL early-concat 43.4 vs mid-feature addition 67.8 [W4_DecouplingSemantics...md]; BridgeVLA 88.2→56.2 when altering the input stem [W4_BridgeVLA...md]).

### 3.7 Language path (v2, off by default)
- Frozen sentence encoder (paraphrase-MiniLM-L3, 384-d; HULC ranking [F/WhatMattersLanguageIL.md]) or T5-small tokens cached per instruction (IMPACT on SO-101 [W3_vlasimd...md]); zero-init FiLM on the encoder's last block and on the trunk (RT-1 identity-init FiLM [F/RT-1.md]); optional detector-mask token of the named object (SVP-IL). Cost: negligible at inference (cached).

### 3.8 Parameter and latency budget

| Component | Params | Per-query cost on RTX 5060 8 GB (bf16, compiled) |
|---|---|---|
| ViT-S/14 ×2 images at 224² | 22M | ≈8–15 ms (est.) |
| Trunk 6×512 over 130 tokens | ≈19M | ≈2–4 ms (est.) |
| Flow expert 6×384, 8 steps, 16 action tokens + cross-attn | ≈9M | ≈4–8 ms (est.) |
| Total | ≈50–55M | ≈15–30 ms (est.); ≤50 ms conservative |

Derivation of the estimate (all reference points are measured in notes; the RTX 5060 laptop is not benchmarked in any note): ConsistencyPolicy on a laptop RTX 3070 Ti 8 GB: two-camera image encoding 6 ms + 1-step UNet 13.5 ms = 21 ms [F/ConsistencyPolicy.md]; MINERVA 9.66M flow policy 11.1 ms on a laptop RTX 5080 [W4_MINERVA...md]; HPT-Base (frozen ResNet-18 + 12.6M trunk) 47 Hz on an RTX 3070 [F/HPT.md]; TaskPrototype ResNet-18 + 6-block flow head with 8 ODE steps 54 ms on SO-101 with an unstated GPU [W4_TaskPrototype...md]; CT-VAM 68M with DINOv3-S+ dual view 56 ms on an RTX 4080 [W4_CTVAMA...md]; DEM 195M active 6.1 ms on an RTX PRO 6000 [W4_DecouplingVisionLanguage...md]; SmolVLA 101 ms on a laptop RTX 5080 [RT/A2C2.md]. An RTX 5060 laptop is slower than a 5080 laptop and than a 4080 desktop; a 55M policy with two ViT-S passes should land between MINERVA's 11 ms and CT-VAM's 56 ms. Camera-path latency is separate: ≈55–82 ms camera + readout in two systems [RT/RealtimeVLAV2.md, RT/LatencyAwareIndustrial.md]; at 10 fps the camera bounds observation age at ~100 ms [RT/QuantACT8GB.md], which is one reason to record and run at 30 fps.

Training memory: JEPA-Policy trained a 44M scratch policy in <6 GiB at 128² [W4_JEPAPolicy...md]; MINERVA trained 10M policies on a laptop RTX 5080 [W4_MINERVA...md]; MobileALOHA trained ACT on an RTX 3070 Ti 8 GB [F/MobileALOHA.md]. At 224² with two views, batch 32, bf16 autocast and activation checkpointing in the ViT, 55M params fits 8 GB (est.); if not, drop to 160² or batch 16 with gradient accumulation.

### 3.9 Why not the alternatives
- SmolVLA fine-tune: frozen vision tower, no continuity mechanism, 15–23% on SO-101 benchmarks (Section 1.4).
- ACT (LeRobot): kept as the baseline (converges reliably on SO-101, 19/20 [RT/QuantACT8GB.md]); its deterministic head cannot use TT-RTC/PAINT and needs TE for smoothness, and it has no pretrained-encoder/token structure by default. If v1 does not beat ACT on the robustness cells, ACT + the same data protocol + DINO encoder is the fallback.
- Diffusion Policy (LeRobot default): 0/10 at 200k steps on SO-101 with defaults [RT/QuantACT8GB.md]; 100-step DDPM latency (DP 460 ms [F/Hyper-DP3.md]); flow with few steps is the same family with the latency problem removed.
- π0/π0.5/GR00T: strongest on SO-101 (π0.5 47.6 pooled [W4_ArmnetBench...md]) but 8–9 GB inference memory [W3_BeyondTaskSuccess...md] and 100–200 ms class latency; not deployable on this laptop.
- Point-cloud-only policy (DP3/iDP3/PocketDP3): loses the wrist view and appearance semantics; collapses under clutter/texture randomisation (Q04).

## 4. Training recipe

### 4.1 Augmentation (applied online, per frame, both cameras unless stated)
| Augmentation | Setting | Evidence |
|---|---|---|
| Random resized crop / pixel shift | scene: crop 90–95% + up to ±8–10 px shift; wrist: crop 95%; per-frame not per-episode | robomimic 73.3 vs 26.7 [F/robomimic.md]; HULC 2.64 vs 1.99 [F/WhatMattersLanguageIL.md]; per-frame > per-episode [W4_GroundingSimtoReal...md] |
| Small rotation ±5° | both | π0.5/UMI defaults [F/pi0.5.md, F/UMI.md] |
| Random perspective / spherical warp | scene only, small (≈ equivalent to ±5–10° camera rotation, ±5 cm) | CAGE L2 0.40→0.73 [W3_Cage...md]; E0 19.7→50.8 [W4_E0...md]; RoVi-Aug: moderate range, wide range costs −10 in-dist [W3_RoViAug...md] |
| Photometric jitter, HUE FIXED | brightness 0.3–0.4, contrast 0.4, saturation 0.5, gamma, sharpness; hue 0 (≤0.02); grayscale p=0.2 on wrist only; per-frame | ChromaGuard hue-fixed 80/70 vs full-HSV colour task 77.5→47.5 [W4_LightsCamera...md]; CRAFT jitter 3→13/20 [W3_CRAFT...md]; MResT asymmetric wrist jitter+grayscale [W4_MResT...md] |
| Background replacement (scene cam) | p=0.5; chroma-key if green screen used, else offline SAM2 masks of robot+pumpkin+tray; random high-entropy textures + ImageNet images | GreenScreenAug +65%/+29% vs CV aug; textures 87% vs solid 65% [F/GreenScreenAug.md]; RoboEngine +210% [F/RoboEngine.md] |
| Object-region colour/texture randomisation | p=0.2–0.3 inside the pumpkin mask (offline masks), per-episode consistent | RoboMP 72.5 vs 19.1 [F/RoboMP-DINOv2.md]; CRAFT SAM recolour 2→15/20 [W3_CRAFT...md] |
| Copy-paste distractors | p=0.3, pasted away from the pumpkin/tray masks | 39.5→100 / 14→64 sim; UR3e 0/20→13/20 [W4_WhatMattersWhenDiagnosing...md] |
| Scene-token dropout / view drop | p=0.3–0.5 tokens; p≈0.1 whole scene view; wrist never | M3 64.0 vs 23.7 [W4_RobustBimanual...md]; w2VLA 58.3→94.4 [W3_DecouplingtheDeclarative...md]; but uniform ModDrop hurt [W4_SensingWhichModality...md] |
| Proprio noise + dropout | σ≈1° (≈40 dB), p=0.3 zero-state | SelfSupCorrespondence 1.1→73.3 [W3_SelfSupervisedCorrespondence...md]; RDT [F/RDT-1B.md]; DreamGen zero-state [W4_DreamGen...md] |
| VLASH state/action offset | δ ∈ {0..d_max}, same image, shifted state & targets | [RT/VLASH.md] |
| TT-RTC prefix | d ∈ [0, d_max] exponentially weighted toward small d; clean GT prefix; loss on postfix | [RT/TrainingTimeRTC.md] |
| Relit copies (optional, offline) | ≤25–50% share, keep originals | EvoHIL α=0.75 [W3_EvoHIL...md]; EMMA ≤50% synthetic [W4_EMMA...md] |
| Not recommended | full hue jitter; uniform random camera dropout; heavy blur/noise curricula; generative single-image NVS | ChromaGuard; EGR; FACTR aug 65 vs 77.7 [W4_FACTR...md]; InfiNoVA VISTA 7.5 [W4_InfiNoVA...md] |

Do NOT augment the action labels except through VLASH/TT-RTC; smoothing all demos hurt −27% [W3_TowardsEffectiveUtilization...md].

### 4.2 Normalisation
- Images: ImageNet mean/std expected by the DINO weights.
- State and actions: per-dimension 1–99% quantile scaling to [−1, 1] computed from OUR data only (MobileALOHA normalises with in-domain stats when co-training [F/MobileALOHA.md]); LBM notes normalisation "often dominates architectural changes" [F/LBM-CarefulExamination.md].

### 4.3 Optimiser and schedule
- AdamW, betas (0.9, 0.95), weight decay 1e-4 (0 on norms/bias). Encoder LR 1e-5 (×0.1), everything else 1e-4 (DP "10× lower LR" [F/DiffusionPolicy.md]; DataScalingLaws encoder 3e-5 / head 3e-4 [F/DataScalingLaws.md]; SLIM DINOv2 lr 1e-5 [W4_SLIM05B...md]; robomimic: 1e-3 vs 1e-4 costs −35–63% for image agents [F/robomimic.md]).
- Warm-up 1k steps with the encoder frozen, then unfreeze (KI: fresh-head gradients damage a pretrained backbone early [F/KnowledgeInsulation.md]); cosine decay; grad-clip 1.0; EMA of weights 0.999 for evaluation (FAST/DP practice [F/FAST.md, F/DiffusionPolicy.md]); GroupNorm/LayerNorm only (DP: BatchNorm interacts badly with EMA).
- Batch 32–64 (accumulate if needed), bf16 autocast, 60–120k steps for ~100 demos at 30 fps (QuantACT8GB ACT 100k steps [RT/QuantACT8GB.md]; MINERVA 90–120k [W4_MINERVA...md]); save checkpoints every 10k.
- Loss = flow-matching MSE + λ_H Hermite + λ_F future-latent (0.2) + λ_KL if CVAE (β=10) — all aux terms must be ablatable flags.
- Dropout 0.1–0.2 in trunk/expert MLPs (UnbiasedLook: policy dropout 0.2 improved real success and smoothness [F/UnbiasedLookPVR.md]).

### 4.4 Checkpoint selection (not by validation loss)
- Validation action loss is unreliable: lowest-val-loss or last checkpoint 10–100% worse than best [F/robomimic.md]; LoRA lower MSE but 0.72 vs 0.90 [F/DataScalingLaws.md]; compliant gains raise val MSE and raise success [W3_TunetoLearn...md]; MDT authors used last epoch for ACT-style [F/MDT.md].
- Practical rule: train a fixed schedule, keep the EMA checkpoints at 60/80/100% of training, run a 10-trial smoke test on each in the in-distribution condition, then the full protocol on the best one. Add two cheap offline proxies: (i) closed-loop-ish "action drift" under augmentation on held-out frames [W3_ItsNotJustMoreDemos...md]; (ii) held-out shifted-condition split (one lighting/pumpkin held out) for modality/aug selection [W3_MaskedImitation...md].

### 4.5 Co-training (optional)
- 30–50% of each batch from retrieved same-embodiment SO-100/101 LeRobot community episodes whose camera layout resembles ours (scene + wrist), zero-padding nothing (same 6-D space), normalised with OUR statistics; co-train, do not pretrain-then-finetune (MobileALOHA co-train 95 vs pretrain-then-FT no gain [F/MobileALOHA.md]; RoboVLMs same-robot other-task data > OXE [F/RoboVLMs-WhatMatters.md]; all-DROID 0% vs retrieved subsets 85 [W4_WhatMattersinLearningfromLarge...md]). Community data quality varies; MolmoAct2 needed a reward filter [W4_MolmoAct2...md].

## 5. Data-collection protocol (SO-101 v2 dataset)

1. **Before recording.** Set follower gains compliant and well-damped (LeRobot already lowers P to 16; consider raising D) and keep them identical at deployment [W3_TunetoLearn...md]. Calibrate so the follower wrist_flex range matches what the task needs (current cap ~85° vs leader ~100°). Mount the RealSense rigidly with an AprilTag/fiducial in view for re-registration. Do 5–10 practice episodes (novice→expert in a few trials [W3_OnBringingRobotsHome.md]; ALOHA-Unleashed protocol dry run [F/ALOHA-Unleashed.md]).
2. **Rate.** Record at 30 fps (ACT 5 vs 50 Hz teleop 62% slower [F/ACT.md]; camera bounds observation age at 10 fps [RT/QuantACT8GB.md]; WhyChunking: 10–20 Hz effective action rate is the sweet spot, so train on 30 fps with H=48 or subsample to 15 Hz [W3_WhyDoesActionChunking...md]).
3. **Count and split.** 120–150 demos for v1 (DemoGen 100→150 +37 pts on a 40×40 cm space [F/DemoGen.md]; ArmnetBench 50 demos → 60–70% simple pick-place [W4_Armnet...md]). Spread as: 4–6 physical pumpkins (DataScalingLaws 8 objects → >0.8 [F/DataScalingLaws.md]) × 3–4 lighting conditions (daylight, evening/room light, lamp from the side, one coloured/dim) × 3–4 backgrounds/table covers, with 5–15 demos per condition cell (50% vs 100% per env overlap [F/DataScalingLaws.md]). Include the night condition that failed.
4. **Placements.** Pumpkin and tray positions on a grid covering the intended eval region plus a margin; randomise the arm's start pose slightly each demo [F/DataScalingLaws.md App. B, F/DemoGen.md]; never repeat an identical placement [W3_RoboMIND...md].
5. **Camera pose.** Between sessions, move the scene camera by a few cm / few degrees and re-register with the fiducial (SeeingAllAngles, GroundingSim2Real ±1 cm +10–20 pts, WhatMattersLargeScale). If possible add a second scene camera during collection only (BeyondViewpoint ±20° views 12.5→58.0 at the fixed test view [W3_BeyondViewpoint...md]).
6. **Distractors / clutter.** ~30% of demos with 1–3 other objects present (Decomposing gap; WhatMattersWhenDiagnosing).
7. **Operator behaviour.** One operator, one strategy (same approach direction, grasp, lift height, place), decisive motions, no wiggling [W3_ElicitingCompatible...md, W4_TheCurseofPrecision...md]; close the gripper slowly over ≥0.5 s [W3_RoboMIND...md]; if two people collect, show reference demos first.
8. **Recovery.** 15–25% of episodes include a deliberate missed/slipped grasp followed by a re-grasp in the same episode (VBT 66→73 [W3_VisualBacktracking...md]; DemoGen ADR 40.4→92.3 [F/DemoGen.md]; RaC/REBOOT). A helper may nudge the pumpkin/tray mid-episode in ~10% (ADC; keep moderate for a small model [W4_AdversarialDataCollection...md]).
9. **Trimming and QA.** Trim idle prefixes until the arm has moved >5 cm/15° and trim trailing static segments (LBM 89/200 idle rollouts [F/LBM...md]; FAST, SeedPolicy, REBOOT); keep episodes with corrected mistakes, drop uncorrected failures (ALOHA-Unleashed 30→55 with mild filtering, 40 with aggressive [F/ALOHA-Unleashed.md]; TOTO successes-only 83.3 vs 72.2 [W3_TrainOfflineTestOnline...md]); spot-check replay-ability by replaying a demo open-loop from its start pose [W4_0ResourceAware...md].
10. **Green screen.** Optional but cheap and best-evidenced for background robustness (GreenScreenAug H). If not used, run SAM2 offline once on the scene stream to get robot/pumpkin/tray masks for background replacement and object-region augmentation (RoboEngine); do not attempt mask-based replacement on the wrist view (GreenScreenAug: wrist masks unreliable).
11. **Intervention round (after v1 is trained).** Run the policy ~20 times, note failing phases, then record 20–30 leader-arm interventions: rewind to a familiar pre-grasp pose, then complete (RaC 61/100 vs 23/100 [W3_RaC...md]; IWR 50/50 balanced sampling 87.3 vs 76.7 [W3_HumanintheLoop...md]; HG-DAgger 27→53 [W3_BCZ...md]). Log only the human segment; upweight 50/50.
12. **Language phase later.** Every scene contains both objects; instructions balanced; hue-preserving augmentation (Q08).

## 6. Real-time execution and decision architecture (merged Track A + B)

### 6.1 Latency budget (targets)
| Stage | Target | Reference |
|---|---|---|
| Camera capture → tensor (30 fps stream, JPEG decode, resize) | ≤40 ms | camera+readout 55–82 ms measured elsewhere [RT/RealtimeVLAV2.md, RT/LatencyAwareIndustrial.md]; zero-copy path 99→101 ms max on Orin [RT/QuantACT8GB.md] |
| Policy forward (bf16, compiled) | ≤30 ms (est.) | Section 3.8 |
| Servo command → motion lag | measure (150–225 ms on other arms [RT/RealtimeVLAV2.md, RT/LatencyAwareIndustrial.md]) | sinusoid cross-correlation test |
| d (delay in control steps) | ≤2 at 10 Hz, ≤5 at 30 Hz | keep d ≪ chunk (DEFLECT overlap >3 [W3_DEFLECT...md]) |

### 6.2 Layers
- **L0 servo executor (existing 100 Hz process).** Holds a timestamped trajectory (each action stamped observation_time + i·Δt + measured motion lag); every tick sends the interpolated target for now (linear or C1/trapezoidal profile [W3_AhaRobot...md]); when a new chunk arrives, drop actions whose timestamps have passed and switch at index d (LatencyAwareIndustrial, SAIL, UMI latency matching [F/UMI.md]); if the buffer runs dry, hold the last target. Safety reflex: joint/velocity/workspace limits; on violation or monitor alarm, time-scale (slow/pause along the path) rather than modify the path (PACS +37% vs CBF [RT/PathSafetyFilter.md]; ActFovea clipping costs ~11 pts [W3_ActFovea...md]).
- **L1 policy loop.** Request the next chunk as soon as the previous request returns (not after the executed prefix is exhausted, as eval_real.py does now); delay estimate = max over the last ~10 measured delays (RTC/REMAC practice); execution horizon 0.5–0.8 s with a rule to shorten near gripper events; TT-RTC prefix overwrite + VLASH state token. Fallback if the head was trained without prefix conditioning: PAINT inversion [RT/InitialNoiseSelection.md].
- **L2 monitors (every policy step, calibrated on 10–30 successful rollouts with conformal thresholds).** (a) TIDE inter-chunk discrepancy on the overlap of successive chunks (0.22 ms; balanced accuracy 0.95 on a low-cost arm with ACT/50 demos [RT/RewindIL.md]); (b) RND/nearest-neighbour novelty on the policy's pooled encoder embedding, windowed and ANDed with (a) or with action entropy (FIPER AND-logic TNR [RT/FIPER.md]; FAIL-Detect per-step TNR 0.08 [RT/FAILDetect.md]); (c) optional entropy from N≤8 batched flow samples to shorten the horizon with a minimum-length floor (AAC +15 real [RT/AAC.md]; beware stop-go [W3_KnowingWhentoStop...md]); (d) checkpoint tracker: embeddings of pre-grasp / lifted / above-tray demo frames, cosine similarity (Rewind-IL, StreamVLA gating); (e) grasp check from servo gripper position + Present_Load (our proposal; untested in any note — L).
- **L3 response table.** Alarm → flush queue, re-query; persistent alarm or failed-grasp signal → rewind to the last checkpoint pose, clear memory, retry (Rewind-IL perturbed 18.3→76.7 [RT/RewindIL.md]; RC-NF homing [RT/RCNF.md]); K=2 retries → safe hold and ask; log every alarm episode as a recovery-demo candidate (REBOOT).
- **L4 slow layer.** None for the single task (H). For the language phase: cached text embedding; a small VLM success checker only at ~1 Hz or on events (Hi Robot 1 s clock [RT/HiRobot.md]); never a cloud VLM in the loop (14 s [RT/Sentinel.md]).

### 6.3 Profiling and diagnosis steps (Stage 0 of the build plan)
1. Confirm CUDA build uses sm_120, performance power mode on AC, bf16, `torch.compile`/CUDA graphs, warm-up; profile SmolVLA per stage (preprocess, vision/VLM prefill, denoise loop). Expected ≤100–150 ms for SmolVLA on this laptop (A2C2 101 ms on a 5080 laptop; Jetson-PI 1.6× power effect).
2. Measure camera latency (film a screen clock), proprio read time, and servo motion lag (command a sinusoid; fit the phase shift) [RT/RealtimeVLAV2.md, RT/LatencyAwareIndustrial.md]; enter them into d.
3. Log commanded-action D1/D2/D3 and the chunk-boundary jump on every run (Soft RTC metrics [RT/ActionPriorDenoising.md]); target a boundary jump within the interior-step distribution (Hermite: handovers were 5.5–8.6× interior steps for all methods [W3_Hermite...md]).

## 7. Evaluation protocol

- **Conditions (one factor at a time, then a combined cell):** (1) in-distribution; (2) lighting: night/room light, lamp-from-side, coloured spotlight; (3) new pumpkin: one held-out pumpkin never in training; (4) camera shift: scene camera moved ~3–5 cm / 5–10° without re-registration, and with re-registration; (5) distractors: 2–4 look-alike/other objects; (6) placements: grid corners outside the demonstrated hull by ~5 cm; (7) perturbation: pumpkin nudged after the approach begins.
- **Trials.** ≥20 per cell for screening (SO101-Benchmark; most notes), 50 for the decisions that matter (LBM: 50 blind randomised rollouts needed to separate policies; 20 detects only huge effects [F/LBM-CarefulExamination.md]). Interleave methods A/B in randomised order with image-overlay initial conditions (LBM); pre-register the cell layout.
- **Failure taxonomy** (SO101-Benchmark): grasp instability, repetition loop, state mismatch (continues after failed grasp), precision misalignment, timeout/hesitation; plus recovery rate (retry after a failed grasp) — ACT 6.5%, SmolVLA 3.2% today [F/SO101-Benchmark.md]; report stage-wise success (reach / grasp / lift / place).
- **Statistics.** Wilson 95% intervals per cell; two-sided Fisher/Barnard tests for pairwise comparisons; report seeds if more than one training run. Smoothness: commanded D1/D2/D3, boundary jump, completion time, starved ticks.
- **Diagnostics.** Image-zeroing action sensitivity (proprio shortcut) [W3_TowardsAccessiblePhysicalAI...md]; augmentation action-drift audit [W3_ItsNotJustMoreDemos...md].

## 8. Build plan (ordered for information gain)

**Stage 0 — Fix and baseline the current system (1–2 days).**
- Make eval_real.py fast: bf16, compile, performance mode, overlapped requests (request next chunk immediately), timestamped buffer, no blend. Measure SmolVLA latency; if >150 ms, profile stages.
- Re-run SmolVLA in-distribution with n_action_steps ≈10 of 50 at 10 fps (SmolVLA's own best [F/SmolVLA.md]) for a 20-trial baseline.
- Go/no-go: latency ≤150 ms and in-dist success >50% → SmolVLA remains the "fixed" baseline; otherwise it is dropped after Stage 2.

**Stage 1 — ACT baseline on existing data (1 day).** LeRobot ACT, ResNet-18, chunk 100 at 10 fps executed with n_action_steps 10–20 and TE on; 20 trials in-dist (expect 60–90% [W4_Armnet...md, RT/QuantACT8GB.md]) and 20 under night lighting. This calibrates the rig and the eval protocol before new data.

**Stage 2 — Collect dataset v2 (2–4 sessions).** Protocol of Section 5; 120–150 demos; 30 fps. Keep v1 data for a "single-condition vs diverse" control.
- Go/no-go gate (the single most informative experiment): ACT trained on v2 vs ACT trained on 100 single-condition demos, evaluated on lighting + new pumpkin cells. If diversity alone lifts those cells from ~0–30% to >60%, the data protocol is doing most of the work and architecture changes are incremental.

**Stage 3 — Policy v1 (1 week).** Implement Section 3 as a LeRobot policy; train on v2 with the Section 4 recipe; ablations in this order: (a) DINO-ViT-S vs ResNet-18 encoder; (b) flow vs L1 head; (c) execution horizon sweep; (d) scene-token dropout on/off; (e) aux losses on/off. 20 trials per cell, 50 for the final v1-vs-ACT comparison.
- Go/no-go: v1 ≥ ACT in-dist and ≥ +15 pts on the lighting/pumpkin/camera cells → continue; otherwise adopt ACT + DINO encoder + v2 data as the deployed policy.

**Stage 4 — Async continuity (2–3 days).** Retrain with TT-RTC + VLASH; executor of Section 6; compare sync / naive async / TT-RTC / TT-RTC+VLASH on success, boundary jump, completion time.

**Stage 5 — Monitors and recovery (2–3 days).** TIDE + RND, checkpoint rewind; intervention round (Section 5 item 11); retrain with the intervention data.

**Stage 6 — Escalations only if cells remain weak.** Object-centric depth branch (new pumpkin/camera cells); feature anchoring (drift); relit copies (lighting); second collection-time camera + cross-view consistency (camera shift).

**Stage 7 — Language / second object.** Data with both objects; FiLM text path; wrong-object rate as the primary metric; mask cue fallback.

## 9. Risks, unknowns, and where the literature is thin or contradictory for our exact setting

1. **No paper tests our exact recipe end-to-end.** The pieces are individually evidenced on SO-100/101 (ACT/QuantACT, SEVO, ChromaGuard, InfiNoVA, EvoHIL, vla.simd, w2VLA, SAVLA, ACNet, VLASH, E-VLA) but the combination (DINO-ViT-S + flow + TT-RTC on SO-101 with 100–150 diverse demos) is an extrapolation; expected in-distribution success 60–90% (ArmnetBench/QuantACT range), robustness cells unknown.
2. **Camera shift without re-registration is the least solved axis in the whole corpus**: even 5-view training collapses at 15° [W4_FromFixedtoFree...md]; the physical fix (rigid mount + fiducial re-registration) plus small-pose data diversity and perspective augmentation is the plan, with calibrated 3D as the escalation. Expect partial robustness only.
3. **New pumpkin appearance** is the second-hardest axis (GenAug, GR00T −20, ReShoot 0/40); several physical pumpkins plus masked-region randomisation should help, but only object-centric inputs have shown large gains (SKIL 72.8 vs 25) and those add a segmentation stack.
4. **Small-trial evidence.** Many real results are 10–20 trials per cell (±10–15 pts); LBM shows 50 are needed. Several key papers are 2026 preprints without replication (Hermite, TT-RTC parity figure-only, VLASH real figure-only, TaskPrototype low credibility, TowardsAccessiblePhysicalAI low credibility).
5. **Backlash vs state roll-forward.** VLASH assumes the last command ≈ current state; STS3215 backlash (observed wrist sag ~6°) violates it. Mitigation: measure tracking error, gate the prefix/state trick on it (SAIL), keep compliant gains; consider recording follower-realised positions alongside leader targets (WhatIsTheBetterCurriculum used follower states, but confounded).
6. **Flow head at 100 demos vs ACT.** Real evidence is split (HiFlow, RoboDual, ControlVLA favour generative; MobileALOHA, QuantACT8GB, Chronos favour ACT/L1 at low data); the ablation in Stage 3 decides. The flow head is worth carrying mainly for the async continuity machinery.
7. **Auxiliary losses** have mostly big-model/sim evidence; at ≤100 demos the expected gain is small (MDT ≈+1 pt at 20 demos); they are cheap but should be the first things removed if training is unstable.
8. **Monitors** are untested on SO-100/101 class arms except Rewind-IL on a Piper; thresholds must be recalibrated per checkpoint; the gripper-load grasp check is our own idea.
9. **30 fps vs 10 fps.** No controlled study on this arm; ACT's 5 vs 50 Hz teleop and WhyChunking's sub-chunk result support 30 fps recording, but copycat/action-redundancy risk rises (FAST). Chunk sizes must be re-expressed in seconds.
10. **Green screen / masks on the wrist camera** are unreliable (GreenScreenAug); wrist-view robustness relies on photometric aug and physical variety only.
11. **Co-training with community SO-100 data** is promising (MolmoAct2) but camera layouts and quality vary; MobileALOHA's gains came from data with identical hardware and camera placement.
12. **8 GB training feasibility at 224² with a ViT-S** is inferred from 44M/128² and ACT/224² examples, not measured.

## 10. Appendix: key references (short name → path; why it matters)

| Short name | Title / venue | Why it matters here |
|---|---|---|
| ACT [F/ACT.md] | Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware (2023) | chunking curve; CVAE vs L1 on human data; leader targets |
| DiffusionPolicy [F/DiffusionPolicy.md] | Visuomotor Policy Learning via Action Diffusion (2023/24) | frozen vs fine-tuned encoders; predict 16/execute 8; position control |
| BAKU [F/BAKU.md, W3_BAKU...md] | BAKU: Efficient Transformer for Multi-Task Policy Learning (2024) | model-size sweep; no history; FiLM |
| SmolVLA [F/SmolVLA.md] | SmolVLA (2025) | our current model; exec-horizon ablation; async without continuity |
| SO101-Benchmark [F/SO101-Benchmark.md] | Benchmarking VLAs on SO-101 (2026) | ACT ≈ SmolVLA; failure taxonomy; recovery rates |
| ArmnetBench [W4_ArmnetBenchv01ParallelRealWorldEvaluatio.md] | ArmnetBench v0.1 (2026) | 7 policies on SO-101 with 50 demos |
| QuantACT8GB [RT/QuantACT8GB.md, W4_BimanualManipulationWithinan8GBBudgetZer.md] | Bimanual Manipulation Within an 8 GB Budget (2026) | ACT 19/20 on SO-101; TensorRT 114→18 ms |
| SEVO [W4_SEVOSemanticEnhancedVirtualObservationfo.md] | SEVO (2026) | SO-101 data diversity +9–23; ACT > SmolVLA |
| ChromaGuard [W4_LightsCameraMalfunctionWhenIlluminationR.md] | Lights, Camera, Malfunction (2026) | SO-101 lighting; hue-fixed jitter |
| InfiNoVA [W4_InfiNoVAInfiniteNovelViewAugmentationfor.md] | InfiNoVA (2026) | SO-101 SmolVLA −88.5% under view change |
| E-VLA [W3_EVLAEventAugmentedVisionLanguageActionMo.md] | E-VLA (2026) | SO100 SmolVLA lighting curve; multi-illumination demos |
| EvoHIL [W3_EvoHILSelfEvolvingRewardandFlowMatchedPo.md] | EvoHIL (2026) | SO-101 lighting shift; flow chunks smoother |
| ACNet [RT/ActionControlNet.md] | Action ControlNet (2026) | SO-101 naive async 17/20 → 20/20 |
| VLASH [RT/VLASH.md] | VLASH (2025) | state roll-forward + offset FT; SO-101 & SmolVLA |
| TT-RTC [RT/TrainingTimeRTC.md] | Training-Time Action Conditioning for RTC (2025) | zero-cost prefix conditioning |
| RTC [F/RTC.md] | Real-Time Execution of Action Chunking Flow Policies (NeurIPS 2025) | TE fails under latency; inpainting works |
| AsyncInferenceStudy [RT/AsyncInferenceStudy.md] | Understanding Async Inference for VLAs (2026) | controlled comparison; SmolVLA prefill 89.8% |
| A2C2 [RT/A2C2.md] | Leave No Observation Behind (2025) | SmolVLA 101 ms on laptop 5080; residual head |
| DVAC [RT/DenoisingVarianceChunking.md] | Denoising Tells When to Replan (2026) | Fix15 vs Fix40 real; adaptive horizon |
| KnowingWhenToStop / BCP / DEHP [W3_...] | adaptive horizon papers (2026) | horizon in seconds; replan before contact |
| Rewind-IL [RT/RewindIL.md] | Rewind-IL (2026) | TIDE monitor; rewind recovery on a low-cost arm |
| FIPER / FAIL-Detect / Sentinel [RT/...] | runtime failure detection | windowed AND monitors; conformal thresholds |
| DataScalingLaws [F/DataScalingLaws.md] | Data Scaling Laws in IL (ICLR 2025) | diversity over count; encoder FT; 8 objects |
| DemoGen [F/DemoGen.md] | DemoGen (2025) | placement hull; 100–150 demos; ADR |
| MobileALOHA [F/MobileALOHA.md] | Mobile ALOHA (2024) | co-training on 8 GB laptop |
| LBM [F/LBM-CarefulExamination.md] | Careful Examination of LBMs (2025) | 50-trial statistics; idle trimming |
| GreenScreenAug [F/GreenScreenAug.md] | Green Screen Augmentation (2024) | background replacement, 8.2k evals |
| RoboEngine [F/RoboEngine.md] | RoboEngine (2025) | segmentation-based background replacement |
| RoboMP [F/RoboMP-DINOv2.md] | RoboMP-DINOv2 (2026) | masked-region colour randomisation |
| CRAFT / RoLight / ReShoot / EMMA [W3_/W4_...] | generative augmentation (2025–26) | jitter baseline; lighting needs data; ≤50% synthetic |
| Theia / SPA / UnbiasedLook / WhatMakesPVRsRobust / VC-1 [F/...] | PVR studies (2023–24) | spatial tokens; DINO-family; small ViT; no scratch ViT |
| CAGE [W3_CageCausalAttentionEnablesDataEfficientG.md] | CAGE (2024) | pretrained ViT tokens robust from 50 mono-env demos; RISE collapse |
| DEM [W4_DecouplingVisionLanguageandActionforEffi.md] | Decoupling Vision, Language and Action (2026) | frozen 32.6 vs FT 55.6; heads within 3 pts; 6 ms |
| MINERVA [W4_MINERVAHowSmallCanaManipulationPolicyBea.md] | MINERVA (2026) | tiny policies; scratch CNN robustness ≈0 |
| PatchPolicy [W4_PatchPolicyEfficientEmbodiedControlviaDe.md] | Patch Policy (2026) | DINOv2 patches > SigLIP; pooling hurts |
| X-Distill [W3_XDistillCrossArchitectureVisionDistillat.md] | X-Distill (2026) | distilled ResNet-18 at ≤25 demos |
| Hsu et al. [W3_VisionBasedManipulatorsNeedtoAlsoSeefrom.md] | Vision-Based Manipulators Need to Also See from Their Hands (ICLR 2022) | wrist anchor; bottleneck the scene stream |
| MResT [W4_MResTMultiResolutionSensingforRealTimeCo.md] | MResT (2024) | both cameras essential; asymmetric aug |
| M3 / EGR / w2VLA [W4_/W3_...] | structured masking (2026) | token/view masking > photometric aug for fusion |
| DoYouNeedProprio [W4_DoYouNeedProprioceptiveStatesinVisuomoto.md] | Do You Need Proprioceptive States? (2025) | state shortcut; overhead cam harm |
| HPT / GeoProp [F/HPT.md, W3_GeoProp...md] | proprio helps (real) | keep current state |
| WhyChunking [W3_WhyDoesActionChunkingImproveBehavioralCl.md] | Why Does Action Chunking Improve BC? (2026) | mechanism; uniform TE hurts; 10–20 Hz effective |
| ActionSpaceStudy / BeyondImplicitForce / Real-ORL / AhaRobot / BC-Z [F/, W4_, W3_] | action space | absolute leader targets; chunk-wise delta ablation |
| DP3 / iDP3 / GAM / GROOT / Lan-o3dp / SKIL / OBEYED / PointVLA / RayViT [F/, W3_, W4_] | 3D | object-centric vs full-scene; injection pattern |
| Hermite / FLARE / JEPA-Policy / PSG-JEPA / SLIM [W3_, F/, W4_] | auxiliary losses | smoothness reg; latent future prediction |
| HybridFlow / ConsistencyPolicy / SnapFlow / Hyper-DP3 [RT/, F/, W3_] | step counts | naive 1–2 steps fail; 5–10 fine |
| TurboVLA / ReactVLA / FlashVLA / JetsonPI / VLAPerf [RT/, F/] | latency systems | SmolVLA true cost; compile/graphs; power mode |
| UMI / LatencyAwareIndustrial / RealtimeVLAV2 / SAIL [F/, RT/] | latency matching | timestamped execution; measure delays |
| TuneToLearn [W3_TunetoLearnHowControllerGainsShapeRobotP.md] | Tune to Learn (2026) | compliant/over-damped follower gains |
| vla.simd / IMPACT [W3_vlasimdEfficientCPUInferenceforLanguageC.md] | vla.simd (2026) | SO-101 FiLM language; CPU-feasible ACT |
| w2VLA / SVP-IL / OBEYED [W3_, W4_] | language grounding | decoupled mask cues; VLA grounding failures |
| RaC / IWR / VBT / ADC / HiWM / REBOOT [W3_, W4_] | recovery data | interventions and in-episode recovery |
| ElicitingCompatible / WhatIsTheBetterCurriculum / CurseOfPrecision / RoboMIND [W3_, W4_] | demo consistency | one strategy; decisive; slow gripper; random placements |
