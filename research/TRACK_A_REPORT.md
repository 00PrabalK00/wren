# Track A — Real-time execution of learned (imitation / VLA) chunking policies

Scope: fast, smooth execution of chunked policies under inference delay, for our SO-101 setup. The setup is one arm, scene RealSense plus wrist cam, 50–150 demos, an RTX 5060 8 GB laptop and 10 fps data. Current state: a SmolVLA fine-tune with naive async, which jerks at chunk boundaries at ~2 s latency.

Sources:
- 24 new full-text notes in `realtime/notes/`. These are VLASH, TrainingTimeRTC, AsyncInferenceStudy, FutureRTC, A2C2, SAIL, MaskedActionChunking (REMAC), ActionControlNet, InitialNoiseSelection (PAINT), ActionPriorDenoising (Soft RTC), JetsonPI, LatencyAwareIndustrial, RealtimeVLAV2, StreamingDP, FlashVLA, MP1, OneStepFlowPolicy, HybridFlow, TurboVLA, QuantACT8GB, VLAPerf, VLACache, DenoisingVarianceChunking (DVAC) and RevisitingOpenLoop.
- Earlier notes in `fulltext/notes/`: RTC, Legato, BidirectionalDecoding, StreamingFlowPolicy, ConsistencyPolicy, ReactVLA and SmolVLA.
- Earlier notes in `wave3/notes/`: DEFLECT, πR2, SnapFlow, SeFA, IMLE, HybridConsistencyPolicy, DEHP, KnowingWhenToStop, BCP (ContinueOrReplan), WhyDoesActionChunking, EMS, ThinkingWhileMoving, AsyncVLA and π0-EqM.

Every number below is quoted from those notes. "Figure only" means the paper gave no table.

---

## 1. The problem, decomposed

Notation: d = ⌊latency / control period⌋. The papers separate three failure modes of naive asynchronous chunk execution (AsyncInferenceStudy, REMAC, VLASH):

1. **Chunk-boundary discontinuity.** The new chunk was sampled independently. It may come from a different mode than the chunk being executed, or start somewhere else. This is the jerk/oscillation we see.
   - Real-robot manifestations reported: back-and-forth oscillation and stalls near contact (ActionPriorDenoising, ACNet on SO-101). Other papers report force spikes of 5.1–5.5× the demonstration peak force (LatencyAwareIndustrial), and RTC saw TE hit a protective stop.
2. **Stale conditioning.** The chunk was computed from an observation and state that are d steps old. The robot state, and in dynamic scenes the world, has moved on (VLASH, FutureRTC, DEFLECT).
3. **Open-loop degradation.** Committed actions cannot react while they are executed. This gets worse with long execution horizons (A2C2, DVAC, SmolVLA ablation).

Separately, delay has sources other than the model:
- Camera ≈55–82 ms, proprio read ≈50 ms, actuator/PD tracking lag ≈150–225 ms (RealtimeVLAV2, LatencyAwareIndustrial).
- With 10 fps cameras the camera alone bounds observation age at ~100 ms (QuantACT8GB on SO-101).

---

## 2. Taxonomy of methods

**A. Execution-side bookkeeping (no model change)**
- Timestamped action buffer: index the chunk by wall clock plus the measured actuator latency, discard stale actions, hold the last pose if the buffer runs dry (LatencyAwareIndustrial, SAIL scheduling).
- Delay estimate = max delay over a recent window (RTC practice, used by REMAC).
- Retime chunks with a QP and pre-amplify commands for PD lag, without changing the path shape (RealtimeVLAV2).
- Naive async queue with aggregation (SmolVLA/LeRobot). This is the baseline that fails.

**B. Averaging / selection (inference-time, no retraining)**
- Temporal ensembling / EMA / linear blending (ACT). Randomized-delay readout of cached chunks, RDE (WhyDoesActionChunking).
- Sample-and-select for coherence: BID, and IMLE consistency selection.

**C. Inference-time continuity for flow/diffusion heads**
- RTC: freeze the committed prefix and inpaint the rest with ΠGDM guidance plus a soft mask.
- PAINT: invert the committed prefix to noise, then run the unmodified ODE.
- Warm start from the previous chunk (π0-EqM, OFP).

**D. Training-time continuity (the policy learns to continue a committed prefix)**
- TT-RTC: per-token flow time, clean ground-truth prefix, loss on the postfix only, random delay.
- Legato: per-step guidance schedule with ω-conditioning.
- Soft RTC: action-prior denoising over a short soft window.
- REMAC: LoRA, prefix masking and self-conditioned curriculum.
- ACNet: ControlNet-style adapter on the executed suffix.
- πR2: staircase noise schedule with fast/slow conditioning.

**E. Latency compensation of the conditioning (predict the execution-time context)**
- VLASH: roll the proprio state forward through the committed actions, and fine-tune with random state/action offsets on a fixed image.
- DEFLECT: preference post-training on top of VLASH-style inputs.
- FutureRTC: state correction plus predicted future vision latents, base frozen.
- Jetson-PI: future VLM latent predicted from committed actions.
- ThinkingWhileMoving: condition on the vector-to-go / in-flight action (RL).

**F. Per-step closed-loop correction over a chunk**
- A2C2: residual head run every control step.
- EMS-style fast/slow two-tier policies; πR2 fast proprio path.

**G. Streaming / rolling generation (continuity and speed from one mechanism)**
- Streaming Diffusion Policy, FlashVLA (multi-chunk buffer at staggered noise levels) and Streaming Flow Policy (flow time = execution time).

**H. Fast generators (cut per-call latency)**
- Distillation: Consistency Policy, SnapFlow (self-distillation, 1 NFE), SeFA (reflow + alignment).
- From scratch: MeanFlow / MP1, iMF / ReactVLA, OFP (self-distilled 1-step), HybridFlow (2 NFE jump + refine), IMLE (1-step).

**I. Inference acceleration of the network**
- Systems work: CUDA Graphs, compile, static buffers, unrolled denoise loop (Jetson-PI, FlashVLA), TensorRT FP16/INT8 (QuantACT8GB).
- Model-level: token caching (VLA-Cache), LLM-free VLA (TurboVLA), caching VLM features and re-running only the action expert (Jetson-PI).
- Environment: GPU power mode (Jetson-PI).

**J. Execution-horizon selection**
- Fixed sweeps: SmolVLA, A2C2, DVAC, KnowingWhenToStop, RevisitingOpenLoop.
- Training-free adaptive: DVAC (denoising variance), KnowingWhenToStop (cross-attention entropy).
- Learned: BCP (RL continue/replan head), DEHP (RL horizon head).
- Human-taught speed: SAIL adaptive speed, RealtimeVLAV2 throttle model.

---

## 3. Comparison table

"Retrain?" means the base policy must be retrained or fine-tuned. Latency tolerance is what was actually tested. Costs are inference-time unless noted.

| Method | Retrain? | Head type required | Latency / delay tested | Real-robot evidence | Smoothness metric reported | Cost |
|---|---|---|---|---|---|---|
| Naive async (SmolVLA/LeRobot) | no | any | ~SO-100 real | SO-100: success 78.3 sync → 73.3 async (sorting 70→50), 13.75→9.70 s. FlashVLA Franka: 80.0 sync vs 75.6 naive | none | 0 |
| Temporal ensembling / blending (ACT) | no | any; harmful with multimodal heads | RTC real +100/+200 ms | RTC real: could not run at +100/+200 ms (protective stop). BID: EMA 18.4 vs 29.5 vanilla under noise | — | per-step inference |
| BID | no | stochastic (diffusion/VQ) | small d | Franka/UR5, figure only, 20 trials | backward coherence loss | ~2× latency (N=16 batch) |
| RTC (inference-time) | no | flow/diffusion | +100/+200 ms real (π0.5, 50 Hz); Kinetix d≤4 | 480 real episodes (RTC paper) | throughput, speed | VJP per step. 27 ms extra (TT-RTC real), 1.2× FLOPs for SmolVLA, 2.6× runtime on Kinetix (Soft RTC) |
| PAINT (noise inversion) | no | flow (OT, near-straight) | Kinetix d 0–4; real remote LAN | 6 tasks × 20 trials, GR00T & π0. ≈RTC SR (e.g., 0.75 vs 0.75, 0.85 vs 0.75) | prefix consistency CON (0.023 vs 0.030) | N extra expert forward passes, no backward |
| Training-time RTC | yes (fine-tune; per-token time) | flow/diffusion | d 0–10 (≤200 ms @50 Hz) real; Kinetix d 0–4 | π0.6, 2 tasks, parity with RTC (figure only) | — | 0 at inference (108 vs 135 ms E2E) |
| Soft RTC (ActionPriorDenoising) | yes (1 epoch) | flow | Kinetix d 0–4 | 10 trials sorting: base 6/10, hard TT-RTC 9/10, soft 8/10 | commanded D1–D3, boundary jump (0.052 → 0.0285 → 0.0118) | ~1.0–1.07× |
| Legato | yes | flow | variable | 5 dual-arm tasks | NLDLJ, NSPARC (~10% better than RTC) | 0 extra |
| REMAC | yes (LoRA r=8, merged) | flow | Kinetix d 0–4; real +150 ms | π0 grasp tasks, figure only | completion | 0 |
| ACNet | adapter (~20% params) | flow/diffusion | Kinetix d 0–4; Meta-World d 0–15 | **SO-101, 50 demos: 17/20 naive → 20/20** | jerk around handoff (figure) | small encoder |
| VLASH | yes (offset fine-tune) | **any** (uses state input) | Kinetix d 0–4; LIBERO d 0–3; real d=2 @30 Hz | **SO-101 & R1 Lite with π0.5/GR00T** (figure only). Ping-pong 11/20 vs 0/20 | qualitative | 0; training step 3.26× faster via shared-obs packing |
| DEFLECT | yes (DPO post-train) | flow | d 0–7 | 3 dynamic tasks × 30 trials (conveyor 76.7 → 86.7 VLASH → 96.7) | — | 0 |
| FutureRTC | adapter, base frozen | any VLA with vision latent | d 5–20 LIBERO; 170/320 ms real | bimanual, 3 tasks × 20 (figure only) | kinematics (qualitative) | 5.19M params, 3.04 ms |
| Jetson-PI | module + scheduling + systems | VLM + action-expert VLA | Δ 1–9 LIBERO | X2-W cloth folding on Orin (figure only) | — | reduces latency 8.66× (systems) |
| A2C2 | residual head, base frozen | any | Kinetix d≤4+; LIBERO d≤10 (study to d=20) | none | — | 4.7 ms/step (laptop RTX 5080); 1.75× FLOPs per chunk if s=50 |
| πR2 | yes (staircase + fast/slow) | flow | d 1–3 ticks @25 Hz | 4 tasks × 20 (Catch Book 11/20 vs 5/20 TT-RTC vs 2/20 naive) | — | needs 2 GPUs |
| StreamingDP | yes | diffusion (per-token noise) | synchronous | real Push-T 20 trials: 0.85 vs DP 0.50 | oscillation (qualitative) | ~0.07 s vs 0.13 s DDIM-16 |
| FlashVLA | yes (multi-buffer fine-tune) | flow | d=1–2 real @30 Hz | Franka 3 × 15: 84.4 vs RTC 80.0 vs naive 75.6 | — | 2.43× faster per step. SmolVLA 19.7 → 10.1 ms |
| Latency-aware scheduling | no | any | 100–500 ms injected | ABB, 20 rollouts × 3 latencies | jerk within 9% of demo, duration within 13% | 0 |
| SAIL (EAG + scheduling + speed) | partly (reached-pose targets) | diffusion | real system latency | Franka/UR5, 10 trials × 7 tasks, up to 3.2× demo speed | SPARC, LDLJ, consistency | CFG (2 passes) |
| DVAC (adaptive horizon) | no | multi-step flow | synchronous | 3 tasks × 30 trials, 50 demos: place cube 0.800 (Fix15) / 0.533 (Fix40) / 0.867 | replan count | ~0 |

Fast generators and acceleration:

| Method | Retrain? | Evidence | Latency |
|---|---|---|---|
| Consistency Policy | distil from DP teacher | real 0.8 = 0.8, 0.7 vs 0.6 (10–20 trials) | 21 ms vs 192 ms DDIM-15 on laptop RTX 3070 Ti |
| SnapFlow | self-distil (VLM frozen) | LIBERO 98.75 (1-step) vs 97.75 (10-step); SmolVLA offline only | SmolVLA 178 → 50 ms (A800, unoptimised) |
| MP1 (MeanFlow) | from scratch | real 5 tasks, 20 demos (e.g., hammer 90 vs 70) | ~6.8 ms |
| OFP | from scratch | 56 sim tasks, 1-step ≥ 100-step | 17.6 ms |
| HybridFlow (2 NFE) | from scratch (MeanFlow) | real 80 trials/setting: 86.3 vs DDIM-16 63.8. **Plain 1-step MeanFlow 0/80, DDIM-2 0/80** | ~19 ms vs 152 ms (Jetson Thor) |
| ReactVLA (iMF) | from scratch | 2 real tasks × 20: ≈ SmolVLA | 38.6 vs 82.2 ms |
| TensorRT FP16 / INT8 (ACT) | no | SO-101 bimanual 19/20, 18/20, 19/20 | 114 → 17.9 → 12.7 ms (Orin Nano) |
| CUDA Graphs + buffers | no | — | Orin: reaction 1420 → 165 ms with scheduling |
| VLA-Cache | no | Kinova 82.1 → 84.6% | 64 → 52 ms (OpenVLA); only +5% control Hz |
| TurboVLA (LLM-free 0.2B) | new model | Piper 4 × 40 trials, 65 demos/task (87.5–92.5%) | 31.2 ms, 0.9 GB (RTX 4090) |

---

## 4. What the evidence says works at small scale

**4.1 The ~2 s latency is a deployment problem, not intrinsic to SmolVLA (confidence H).** Independent measurements of SmolVLA-class inference:

| Measurement | Source |
|---|---|
| 101 ms on a **laptop RTX 5080** | A2C2 |
| 74 ms (LIBERO) / 82 ms (real) | ReactVLA |
| 19.7 ms optimised, desktop-class GPU | FlashVLA |
| 178 ms, A800, unoptimised | SnapFlow |
| 405 ms, RTX 3090, LeRobot LIBERO eval path | AsyncInferenceStudy |

The same Jetson Orin runs 1.6× slower in its 30 W mode than in its 50 W mode (Jetson-PI Table 1), so power capping alone is a first-order effect. System work (CUDA graphs, static buffers) cut Orin reaction time ~3×. TensorRT FP16 cut ACT 6.4× vs eager PyTorch.

Which part dominates depends on the implementation:
- Vision/VLM prefill is 89.8% of SmolVLA FLOPs (AsyncInferenceStudy).
- Denoising is ~79% of unoptimised SmolVLA wall time (SnapFlow).
- For π0, VLAPerf models 10→1 denoising steps as only −26% end to end.

So profile the stages before choosing a fix.

**4.2 Naive async hurts, and the evidence is on our exact hardware class.**
- ACNet on SO-101 with 50 demos: naive 17/20 with visible oscillation at transitions vs 20/20 with the fix.
- Soft RTC, single arm: naive 6/10 vs 9/10 with training-time RTC; boundary jump 0.052 → 0.0285.
- FlashVLA: naive 75.6 vs sync 80.0.
- SmolVLA's own async lost 20 points on sorting.

Confidence M/H: several independent small real studies all point the same way.

**4.3 Cheapest effective continuity fixes are training-time and add zero inference cost.**
- **VLASH** state roll-forward plus offset fine-tuning:
  - Head-agnostic, tested on SO-101 and on SmolVLA (LIBERO: 79.1% at d=3 vs 79.0% sync).
  - Needs only a data-loader change, plus feeding the last queued action as the state.
- **Training-time RTC** (prefix conditioning with random delay):
  - ~10 lines of code; needs a flow head with per-token time.
  - Equals RTC on real robots, beats it at higher delay in simulation, and is the most robust to the choice of d_max (AsyncInferenceStudy).
  - Weakness: it degraded with long H=50 SmolVLA chunks at high delay.
- REMAC shows a LoRA variant works with 30 demos and tolerates mis-estimated delay.

**4.4 At our likely post-fix latency (≈100 ms at 10 Hz → d≈1–2), all continuity methods work.** The differences between methods mostly appear at d≥4 (AsyncInferenceStudy, FutureRTC, Jetson-PI, DEFLECT). The inpainting methods (IT-RTC, BID) fail when the overlap (H − d) is only 1–3 actions (DEFLECT Kinetix: ≤5%). So keep d small relative to the chunk.

**4.5 Averaging is not a continuity fix.**
- TE/EMA: RTC's real robot hit a protective stop. BID found EMA hurts under stochasticity (18.4 vs 29.5).
- Uniform TE hurt Tool Hang (42.2 vs 75.2, WhyDoesActionChunking).
- B-spline or TE smoothing leaves the prefix mismatch near naive (PAINT).

Our linear old→new fade is in this class. Confidence M/H.

**4.6 Execution horizon matters as much as the continuity method, and should be in seconds, not steps.**
- SmolVLA LIBERO, executed steps 1/10/30/50 → 80.3/82.8/70.8/51.8.
- A2C2: SmolVLA e=50 0.71 vs e=10 0.85 at d=0.
- DVAC real, 50 demos: Fix15 0.800 vs Fix40 0.533.
- KnowingWhenToStop real: fixed exec 10–50 swings 41.7–51.7.
- Executing 1 step (re-sampling every step) is also bad (SnapFlow n_act=1: 77/72; KnowingWhenToStop multi-sample: 18.3 real "stop-go").
- Adaptive truncation (DVAC, KnowingWhenToStop) beats the best fixed horizon by a few points with ~40% fewer replans.

Confidence M.

**4.7 Measure latency outside the model.**
- RealtimeVLAV2 measured camera 55 + readout 33 + proprio 50 + motion lag 150 ms.
- LatencyAwareIndustrial measured camera 82 ms and actuator 225 ms.

Both are cheap to measure (screen/LED clock, sinusoid tracking). This delay must enter d. Confidence M.

**4.8 Few-step generation: sim parity does not transfer to real without care.**
- HybridFlow real: plain 1-step MeanFlow scored 0/80, DDIM-2 0/80 and ReFlow-2 ≤10%, while its 2-NFE jump+refine scored 60–86% and DDIM-16 47–64%.
- HCP: a 5-step consistency student dropped to 38%.
- Positive results for ~1–5 step generators: Consistency Policy real parity at 21 ms on an 8 GB laptop GPU; ReactVLA 5-step iMF at SmolVLA-level success; SnapFlow (sim).

Confidence M/H that naive step cutting is risky.

---

## 5. Open conflicts

1. **Ranking of async methods is benchmark-dependent.**
   - AsyncInferenceStudy (the only controlled comparison): A2C2 best at high delay. TT-RTC most robust on short chunks but degrades with SmolVLA's H=50. IT-RTC best at d=0 on LIBERO. VLASH trades low-delay vs high-delay accuracy via d_max.
   - Jetson-PI: VLASH collapses at Δ≥7 (30.1% at Δ=9) while RTC holds 88.8%.
   - VLASH and DEFLECT: VLASH ≫ RTC on Kinetix.
   - FutureRTC reproductions put all baselines within ~2–6 points of naive on LIBERO.
2. **Is stale proprio enough, or do stale images matter?**
   - VLASH says state forwarding suffices at small delay.
   - FutureRTC and Jetson-PI need predicted vision latents at d≥5–10.
   - DEFLECT notes the effect is weak in quasi-static pick-and-place. That fits our pumpkin task: state forwarding is probably enough if d stays small.
3. **Temporal ensembling.**
   - Harmful in RTC (real), BID (under noise), WhyDoesActionChunking (uniform TE) and PAINT.
   - But the best inference-time baseline at high delay in FutureRTC's LIBERO table (π0.5 d=20: TE 74.8 vs RTC 73.7).
   - ACT's original gain was synchronous with a near-unimodal head.
4. **Soft vs hard prefix.** RTC finds soft masking better at inference time. Soft RTC finds training-time soft windows trade success for smoothness (L=2: high-delay solve 0.732 → 0.486).
5. **Short vs long execution horizon.**
   - Shorter is better for SmolVLA, π0.5, DP under noise (DEHP) and DVAC real.
   - Full chunk is better for X-VLA (KnowingWhenToStop). BCP: fixed shorter horizons gave no gain on RoboTwin.
   - Short-context DP wants long T_exec (RevisitingOpenLoop: T_o=2 best at T_exec=8, T_o=8 best at 2).
   - The optimum is model- and data-specific, so sweep it.
6. **Where the latency goes** (denoising vs prefill) differs across SnapFlow, AsyncInferenceStudy, VLAPerf and FlashVLA, because implementations differ.
7. **Does async improve or reduce success?**
   - VLASH claims async improves accuracy by removing stalls.
   - SmolVLA (78.3 → 73.3) and FlashVLA (80 → 75.6) found naive async lowers it.
   - Consistent reading: async plus a continuity/latency fix ≥ sync > naive async.
8. **Commanded vs reached targets.** SAIL: training on reached poses matters at high speed (Square −55% with commanded poses). RealtimeVLAV2 instead pre-amplifies commands for PD lag. Untested on backlash-prone servos.

---

## 6. Control rate, data fps and chunking

**d depends on control rate.** 100 ms latency is d=1 at 10 Hz but d=3 at 30 Hz. Many methods were validated only up to d≈4 (VLASH, TT-RTC sim, REMAC, ACNet Kinetix). Moving to 30 fps triples d for the same latency, and makes it more important to get latency down first.

**Chunk length in seconds changes with fps.**
- SmolVLA's n=50 is 5 s at our 10 fps.
- The pretraining data is mostly 30 fps SO-100 (~1.7 s). The temporal mismatch is my inference, noted in SmolVLA.md, and untested.
- The evidence favours executing about 0.5–1.5 s before re-querying:
  - KnowingWhenToStop real best ≈1.5 s at 20 Hz.
  - SmolVLA best at 10 of 50 steps.
  - DVAC real: 15 steps better than 40.

**Chunking at high rates.** WhyDoesActionChunking: at 50–60 Hz, delayed single-step policies fail. Treating 5-step sub-chunks as actions (effective 10–20 Hz) restores performance, which suggests ~10–20 Hz is a good effective decision rate for human demos.

**10 fps is a workable data rate.**
- HybridConsistencyPolicy logged at 10 Hz and executed at 10 Hz successfully.
- QuantACT8GB ran bimanual SO-101 at 10 Hz with ACT (19/20).
- At 10 fps the camera bounds observation age at ~100 ms, so going to 30 fps shortens observation staleness.

**Between policy steps, interpolate to the servo rate.** LatencyAwareIndustrial used linear interpolation between timestamped actions. RealtimeVLAV2 retimes chunks with a jerk-limited QP.

**Faster than demonstration is possible later.**
- Up to 3.2× real with SAIL.
- 1.5–2× without loss with VLASH action quantization (q=2 on pick-place).
- 3–4× in free space with RealtimeVLAV2.
- Precision phases need slow-down: interventions concentrate at sleeve folding at 2–3× (RealtimeVLAV2).

---

## 7. Recommended real-time execution stack for our SO-101 policy

Stages are ordered by cost. Confidence levels (H/M/L) reflect the strength of the evidence behind each step.

**Stage 0: Make inference fast and measure the delay budget. Do this before changing any algorithm.**
- **0a. Diagnose the ~2 s. Confidence H that ≤~100–150 ms is reachable for SmolVLA on this laptop.**
  - Checks: performance power mode on AC; a CUDA build that actually uses the RTX 5060 (no CPU fallback); bf16; torch.compile / CUDA Graphs; warm-up.
  - Profile per stage: preprocessing, vision/VLM prefill, denoising loop.
  - Evidence: 101 ms on a laptop RTX 5080 (A2C2); 19.7 ms optimised (FlashVLA); 1.6× from power mode alone (Jetson-PI); ~3× from CUDA graphs (Jetson-PI); 6.4× from TensorRT for ACT (QuantACT8GB).
- **0b. Measure non-model delays. Confidence M.**
  - Camera latency: film a screen showing the system clock.
  - Servo lag: command a sinusoid and fit the commanded-vs-measured time shift.
  - Add both to d (RealtimeVLAV2, LatencyAwareIndustrial).
- **0c. Log smoothness on every run. Confidence H as methodology.**
  - Commanded-action finite differences D1/D2/D3 and the chunk-boundary jump (Soft RTC).
  - Jerk / SPARC (SAIL, Legato).
  - With 10–30 trials per condition; the reference studies used 10–30.

**Stage 1: Execution bookkeeping. No retraining. Confidence M.**
- Timestamp each chunk with its observation time.
- Each control tick, send the action for (now + measured actuator latency); discard stale actions.
- At chunk arrival, switch at t+d onto the new chunk's index d. Do not linearly fade or temporally ensemble (§4.5).
- Delay estimate: max over a recent window of measured delays.
- Interpolate between 10 Hz actions to the servo loop.
- Evidence: LatencyAwareIndustrial, SAIL, RTC, REMAC.

**Stage 2: One cheap fine-tune that removes chunk-boundary jerk.**
- **2a. VLASH offsets. Confidence M/H.**
  - Fine-tune with offset augmentation (δ∈{0..d_max}, same image, shifted state and action targets).
  - At runtime, feed the last queued absolute joint target as the state.
  - Works with any head. Tested on SO-101 and with SmolVLA. Zero runtime cost.
  - Set d_max slightly above the measured post-fix delay. A wide d_max costs low-delay accuracy (AsyncInferenceStudy).
- **2b. Add training-time RTC prefix conditioning to the SmolVLA flow expert. Confidence M.**
  - Per-token flow time, clean committed prefix, postfix loss, random d.
  - Evidence: TT-RTC, REMAC (LoRA works), Soft RTC real, ACNet SO-101.
  - Keep hard prefix masking. Use a soft window of N=1–2 only if jerk remains.
- **2c. Training-free fallback: RTC or PAINT. Confidence M.** If fine-tuning is not possible, use RTC; PAINT has similar success and no backward pass. Both require small d relative to H.

**Stage 3: Execution horizon. Confidence M.**
- Keep predicting long chunks; VLAPerf finds longer chunks nearly free.
- Re-query after ~0.5–1.5 s of execution (at 10 Hz, ~5–15 actions of 50), and never down to 1 step.
- Sweep the horizon on the real robot. Optimum and variance are large and model-specific: swings of 10–35 points across KnowingWhenToStop, DVAC and RevisitingOpenLoop.
- Optional zero-cost adaptive truncation: DVAC (denoising variance of the 10-step flow expert) shortens execution near the grasp and place.
- Budget enough trials: BCP showed boundary timing alone moves success 82.5–93.7%.

**Stage 4: Only if needed.**
- **4a. Per-step residual correction (A2C2), ~20–32M params, ~5 ms/step on a laptop GPU. Confidence M, sim only.** Use if reactivity to moving objects matters or delay stays large.
- **4b. Fewer flow steps. Confidence M.**
  - Only via distillation or refinement (SnapFlow for SmolVLA, HybridFlow-style 2-NFE), always validated on hardware.
  - Naive 1–2 step sampling collapsed on real robots (HybridFlow).
- **4c. Change the model if SmolVLA cannot get below ~150 ms. Confidence M.**
  - LLM-free small policy: TurboVLA 0.2B, 31 ms, 0.9 GB.
  - Or an ACT/DP-size policy with TensorRT (12–18 ms even on an Orin Nano, SO-101).
- **4d. Later: faster-than-demo execution. Confidence L/M for SO-101.** VLASH action quantization q≈1.5–2, then SAIL/RealtimeVLAV2-style speed adaptation.

**Explicitly not recommended**
- Temporal ensembling or linear blending with a flow head (§4.5).
- Very short replanning without continuity handling (stop-go: KnowingWhenToStop MS 18.3%).
- Inference-time guidance if latency is already the bottleneck (it adds ~20–27 ms/call and widens d; VLASH, TT-RTC).
- Chasing larger delays with future-vision predictors (FutureRTC, Jetson-PI) before fixing latency.

---

## 8. Evidence quality caveats

- Most async papers evaluate on Kinetix (a 2D physics sim) and LIBERO. Real-robot studies are 10–30 trials per cell, often with figure-only results.
- Only three papers touch SO-101 in Track A: VLASH (figure-only), ACNet (20 trials) and QuantACT8GB (20 trials).
- Almost all use VLA-scale bases. Evidence specifically for SmolVLA:
  - VLASH LIBERO.
  - AsyncInferenceStudy LIBERO.
  - A2C2 LIBERO and its laptop latency measurement.
  - FlashVLA latency.
  - FutureRTC LIBERO.
- Cross-paper latency numbers vary by 20× for the same model depending on implementation. Only our own profiling settles our budget.
