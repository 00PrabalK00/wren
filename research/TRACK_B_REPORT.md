# Track B: Architectures and mechanisms for reactive decision making (SO-101 focus)

Scope: hierarchical fast/slow policies, reflex and safety layers, re-plan triggers, runtime failure detection and recovery, MPC and sampling control combined with learned policies, event vision, and servo-level control.
Sources:
- 19 new full-text notes in `realtime/notes/`: HiRobot, FastInSlow, HiRT, RDP, AsyncFastSlow, HiPolicy, Sentinel, FIPER, FAILDetect, RewindIL, LPB, PathSafetyFilter, SafeFlowMPC, GPC, ParallelSMPC, StreamVLA, RCNF, AAC, VPSTO.
- Reused notes, not re-read:
  - Hierarchical: W3 RoboDual (TowardsSynergistic), DP-VLA (ADualProcessVLA), EMS (FastandAccurate), fulltext GR00T-N1.
  - Reactive within a chunk: W3 πR2, TubeDiffusionPolicy.
  - Runtime safeguard: W3 ActFovea.
  - Execution horizon: W3 BCP (ContinueorReplan), KnowingWhentoStop, DEHP, ThinkingWhileMoving.
  - Event vision: W3 E-VLA.
  - Recovery data: W3 REBOOT.
  - Servos: W3 AhaRobot.
  - Continuation: fulltext RTC, Legato, BidirectionalDecoding, StreamingFlowPolicy, ReactVLA.
- Chunk-continuation and async-inference mechanics belong to Track A (notes such as AsyncInferenceStudy, RevisitingOpenLoop, VLASH, A2C2 in the same folder). This report only refers to them.

Rule: every number below comes from a paper note. Rows marked "our assessment" are judgments about feasibility on our hardware and are not claims from any paper.

---

## 1. Taxonomy

**A. Hierarchical fast/slow (System 1 / System 2)**
- **A1: Semantic planner over a VLA.** A VLM emits language subcommands to a low-level VLA. Examples: Hi Robot (clock plus user-event trigger) and StreamVLA (triggered when a subtask completion state is reached).
- **A2: Slow latent plus fast decoder.** A big VLM writes a latent that goes stale, and a small or fast head reads it together with fresh observations. Examples: RoboDual, HiRT, DP-VLA, GR00T-N1 (VLM plus DiT), DuoCore-FS (AsyncFastSlow), Fast-in-Slow (FiS), where the fast head shares the VLM's last blocks.
- **A3: Model switching.** A big model is used sparsely and a small distilled model runs every step, with a learned switch. Example: EMS.
- **A4: Slow chunk generator plus fast feedback decoder at control rate.** A per-step loop runs inside the chunk. Examples: RDP (latent chunk at 1–2 Hz, tactile decoder under 1 ms), Tube Diffusion Policy (streaming feedback flow), and πR2 (fast proprio conditioning with slow cached vision).
- **A5: Multi-rate chunks inside one policy.** Example: HiPolicy (coarse-to-fine frequencies with entropy selection).

**B. When to re-query or re-plan (triggers)**
- **B1: Fixed clock or fixed execution horizon.** Hi Robot uses 1 s. FiS found a 1:4 slow:fast ratio best. Most DP/ACT deployments do this.
- **B2: Uncertainty from sample spread.** Examples: AAC, HiPolicy, FIPER's ACE score. There is negative evidence in W3 (BCP; the multi-sample baseline in Knowing-When-to-Stop).
- **B3: Model-internal signals.** Examples: cross-attention entropy (Knowing-When-to-Stop, W3) and a learned continue/replan head (BCP and DEHP, both trained with RL).
- **B4: Progress or completion mismatch.** The current embedding is compared with an expected phase or goal. Examples: StreamVLA gating and Rewind-IL checkpoint peaks.
- **B5: External events.** Examples: user utterances (Hi Robot) and anomaly-monitor alarms (RC-NF, Rewind-IL).

**C. Runtime failure detection (all calibrated on successful rollouts only)**
- **C1: Action self-consistency.** Examples: STAC (Sentinel; batch-sampled, cumulative) and TIDE (Rewind-IL; single-sample overlap of successive chunks).
- **C2: Observation novelty or density in the policy embedding.** Examples: RND-OE (FIPER), logpZO flow density (FAIL-Detect), and nearest-neighbour latent distance (LPB).
- **C3: Object and robot state density.** Example: RC-NF (SAM2 point tracks plus proprio, normalizing flow).
- **C4: VLM progress judge.** Examples: the GPT-4o video QA in Sentinel and the VLM baselines in RC-NF. These take seconds.
- **C5: Cross-modal consistency wrapper.** Example: ActFovea (W3).

**D. Responses: recovery and safety**
- **D1: Re-query immediately and flush the action queue.** Example: Rewind-IL restart.
- **D2: Rewind to a verified checkpoint, then retry.** Examples: Rewind-IL; RC-NF "homing".
- **D3: Steer back to the demo manifold.** Example: LPB, which gradient-steers the denoising with a latent dynamics model.
- **D4: Path-consistent braking or time-scaling.** Example: PACS. The contrast is action-modifying filters such as CBFs and clipping, which PACS and ActFovea show hurt success.
- **D5: Constraint projection inside generation.** Example: SafeFlowMPC.
- **D6: Recovery behaviour demonstrated in the data.** Examples: DuoCore-FS anomaly handling, RDP's "proactively recorded reactive behaviors", REBOOT.

**E. Model-based and sampling control at runtime**
- Examples: VP-STO (via-point CMA-ES MPC at 12.5–20 Hz on a real arm), ParallelSMPC (MJX MPPI/MTP at 8–10 Hz on an RTX 5090 with mocap), GPC (flow policy trained from sampling predictive control, warm-started, 100–1000 Hz in sim), and SafeFlowMPC (10 Hz).

**F. Perception latency.** Example: E-VLA, which uses an event camera on an SO100 wrist with SmolVLA to handle low light and blur.

**G. Servo and cascade level.** Examples:
- Latency matching, i.e., dropping stale actions (RDP, UMI).
- Time-indexed trajectory publishing with interpolation at 50 Hz–1 kHz (ParallelSMPC, RDP at over 500 Hz).
- Trapezoidal or C1 target profiling, backlash preload and stiction dithering on the same STS3215 servos (AhaRobot, W3).

---

## 2. Comparison table

Loop rates and sizes are as reported. "8 GB" is our assessment for an RTX 5060 laptop.

| Paper | Architecture | Loop rates | Model sizes | Decision trigger | Real-robot evidence | Failure / recovery behaviour | Feasible on 8 GB? |
|---|---|---|---|---|---|---|---|
| Hi Robot | A1 VLM→π0 | high level ≈1 Hz | 2× PaliGemma-3B | 1 s clock OR user utterance | 3 platforms, 20 trials/task/method; IA +40% vs GPT-4o (figure) | reacts to verbal corrections; low level not monitored | No |
| StreamVLA | A1 in one 3B model | ctrl 50 Hz; latency 244→128 ms | 3B | completion-image mismatch (τ=0.5) | 20 trials: 90/70/55 vs π0.5 45/35/15 (interference task last) | interference → System 2 re-plan (55%) | No (the gating idea is portable) |
| RoboDual (W3) | A2 OpenVLA + DiT specialist | 3.9 Hz generalist, 15 Hz specialist, 20 Hz ctrl | 7B + 20M trainable | fixed ratio; latency-aware training | 15 runs; gen. avg 70.0 vs OpenVLA 41.7; 5 demos 73.3% | none explicit | Specialist yes, generalist no |
| HiRT | A2 InstructBLIP-7B + ViT | VLA 4.1 Hz → HiRT 9.8 Hz | 7B + small | async, fixed | moving target 1 cm/s: 75% vs VLA 48%, DP 18% | faster loop tracks moved object | No (idea yes) |
| FiS-VLA | A2 shared blocks | 21.9 Hz (chunk 1); 117.7 Hz "theoretical" (chunk 8), 4090 | 7B | ratio 1:4 best (0.69 vs 0.60/0.63/0.61) | 100 demos/task; 68 vs 59, 74 vs 61 over π0 | none; lighting −29 to −46% | No |
| DuoCore-FS | A2 3B VLM + π0-small decoder | slow 1–3 Hz, fast 25–30 Hz (32.3 Hz) | 3B | latest buffer; cross-timescale training | 18/20 vs π0 17/20; anomalies 23/24 vs 22/24 | demonstrated "return home" | No |
| EMS (W3) | A3 π0 + small BC-ViLT/ACT | π0 ~10 Hz, S1 ~100 Hz | π0 + small | RL switch (15% big-model calls) | real stack bowls: ACT 60, π0 100, EMS 70% | switch at grasps/errors | Small part yes |
| RDP | A4 LDP + tactile decoder | slow 1–2 Hz, fast 20–30 Hz, robot >500 Hz | DP-scale; AT <1 ms | every step (tactile) | 50–80 demos; peeling 0.44→0.95; after-contact perturb 0.19→0.88 | reacts to pushes inside chunk | Yes (but needs a force signal) |
| πR2 (W3) | A4 fast proprio / slow vision | 25 Hz, ~140 ms/call | GR00T-N1.7 | per tick | catch book 11/20 vs sync 4/20 | reacts inside chunk | No (needs 2 GPUs) |
| Tube DP (W3) | A4 DDIM + streaming | >100 Hz vs DP ~25 Hz | 172.8M | per step | reorientation 96 vs 60% (25 eps) | reacts to pushes (qualitative) | Yes |
| HiPolicy | A5 multi-rate DP/DP3 | 15 Hz ctrl | DP-scale | entropy (N=100, +2 ms) | 8 tasks × 10: 85 vs DP 60% | shorter chunks when uncertain | Yes |
| AAC | B2 on GR00T N1.5 | +~20 ms at N=20 (A800) | GR00T | entropy → chunk size | 50 demos/task: 67→82% avg | re-plan sooner when uncertain | Head-only yes |
| Sentinel | C1 STAC + C4 VLM | VLM 14 s response | DP + GPT-4o | cumulative consistency / video QA | real 10+10 rollouts: TPR 1.00, TNR 0.90 | detect only | STAC yes (batch cost); VLM no |
| FIPER | C1+C2 RND-OE AND ACE | "little runtime" | small RND | windowed AND, conformal | 2 real tasks; acc 0.78, TWA 0.65 | detect/predict only | Yes |
| FAIL-Detect | C2 logpZO flow density | per step | small CNF | conformal band | 50 hardware rollouts; top-1 8/12 | detect; STAC (256 samples) too slow on HW | Yes |
| Rewind-IL | C1 TIDE + D2 rewind | 30 Hz robot; +0.22 ms | ACT (+VLM offline) | TIDE > conformal threshold | AgileX Piper, 50 demos: perturbed 18.3→76.7% | rewind to checkpoint, clear queue, retry | Yes, best match |
| RC-NF | C3 object points + robot NF | <100 ms response | NF + SAM2 | NLL > threshold (α=0.05) | FR3 + RealSense, π0 (qualitative) | homing, then hand back to policy | Borderline (SAM2) |
| LPB | C2 + D3 latent steering | not reported | DP + latent dynamics | latent NN-distance | belt assembly 0.55→0.75 | steer to demo manifold | Maybe (needs rollouts) |
| ActFovea (W3) | C5 wrapper | not reported | π0 | consistency checks | sim only | safe hold; clipping costs clean SR | Idea yes |
| PACS | D4 path-consistent brake | shield 1 kHz | any DP | reachability violation | 3 HRI tasks; +37% vs CBF | slow/stop along path | Principle yes |
| SafeFlowMPC | D5 projection per flow step | 10 Hz | U-Net FM | every plan | KUKA handover/grasp (qualitative) | constraint-safe re-plan | Not needed |
| VP-STO | E sampling MPC | 12.5–20 Hz | no learning | receding horizon | Franka, qualitative | re-plans to moving target | Primitives only |
| ParallelSMPC | E MJX MPPI/MTP | plan 8–10 Hz (RTX 5090), servo 50 Hz/1 kHz | sim model | receding horizon | FR3 Push-T, 6 seeds | — | No |
| GPC | E→learned flow | 100–1000 Hz (sim) | small | every step, warm-start | none | — | Needs a sim |
| E-VLA (W3) | F event camera | 30 Hz sync | SmolVLA + 13M | — | SO100: 20 lux 0→90% | robust to dark and blur | Needs a DAVIS camera |
| AhaRobot (W3) | G servo control | ESP32 PID 66 Hz | ACT/π0 | — | STS3215, 0.72 mm repeatability | π0 chunk discontinuities knocked tools over | Yes (firmware/host) |

---

## 3. What works at small scale (≤ ~0.5B params, one consumer GPU)

1. **Keep the fast loop small and frequent. Put the "slow" part only where it earns its cost.**
   - Every A2/A3 paper finds that the fast component carries the motor precision:
     - RoboDual's 20M-trainable specialist at 15 Hz.
     - EMS's ~100 Hz BC-ViLT.
     - Hi Robot's expert-human high level, where "failures stem more from reasoning than actuation".
   - HiRT gives the one real controlled test with a moving object: the success gap is driven by loop rate (4 Hz VLA 48% vs ~10 Hz HiRT 75%).
   - For a single pick-place task with no language ambiguity, no paper shows that a 3–7B slow model is needed. Their gains are semantic: instruction following, distractors, new objects.
   - Confidence M. Stated plainly, the evidence supports this indirectly: no paper tests "single task, small model, with vs without System 2".

2. **Cheap failure monitors built from the policy itself work, calibrated on about 10–50 successful rollouts.**
   - Rewind-IL is the closest match to our setup: a low-cost arm, ACT, 50 demos, and 30 Hz.
     - Its TIDE monitor costs 0.22 ms.
     - Detection balanced accuracy is 0.95, against 0.83 for FAIL-Detect and 0.59 for RND.
     - With rewind-and-retry, success under human perturbation goes from 18.3% to 76.7%.
   - FIPER and FAIL-Detect confirm that embedding-novelty scores work, but only with windowing and AND-logic. Per-step thresholds or novelty alone cause false alarms: the PCA-kmeans TNR was 0.24, and FAIL-Detect had a TNR of 0.08 on the towel task.
   - Confidence M/H for "self-consistency plus conformal threshold" as the primary monitor.

3. **Recovery by going back to a known state works better than modifying actions.**
   - Evidence for going back:
     - Rewind-IL: rewind to a checkpoint.
     - RC-NF: homing, after which the policy re-targets the moved ball.
     - DuoCore-FS: demonstrated return-home.
   - Evidence against modifying actions:
     - PACS: braking along the path beats a CBF by 37% on hardware.
     - ActFovea: clipping and smoothing cost about 11 points of clean success.
     - RDP: temporal ensembling (TE) with τ=0.2/0.5/0.8 gave 30%/0%/100% grasp success, so it is fragile.
   - Confidence M.

4. **A per-step feedback path inside a chunk beats shorter chunks and beats temporal ensembling, when a fast signal exists.**
   - RDP's Table V: chunk 2 gives 20% grasp success; TE is fragile; the slow-fast design gives 100% and a score of 0.50.
   - Tube DP (W3) shows the same pattern.
   - Both rely on tactile or force input, which SO-101 lacks. The Feetech present-load reading is untested as a substitute.
   - Confidence M for the architecture. Confidence L for our available signal.

5. **Adaptive commitment (execution horizon) is worth a little compute if a floor prevents stop-go.**
   - AAC: real 67→82%. N≤10 samples cost about 1 ms on an A800 (83.0 ms at N=1 vs 84.3 ms at N=10).
   - HiPolicy: sampling N=100 costs +2 ms because conditioning is computed once.
   - Against: Knowing-When-to-Stop's multi-sample truncation gave stop-go pauses and 18.3% success on a real robot, and BCP found uncertainty triggers marginal.
   - Confidence L/M.

6. **Latency matching and time-indexed execution are basic requirements at the executor level.**
   - Latency matching means discarding actions whose timestamps have already passed. RDP calls it "essential" (figure-only).
   - The executor should interpolate a timestamped trajectory: ParallelSMPC at 50 Hz and 1 kHz, RDP at over 500 Hz.
   - The executor should profile targets: AhaRobot uses trapezoidal/C1 profiling on STS3215 servos.
   - Confidence M.

7. **Recovery behaviour in the demos is cheap and helps.**
   - DuoCore-FS: even flat π0 handled anomalies it had seen demonstrated, 22/24.
   - RDP recorded reactive behaviours on purpose.
   - REBOOT allocates recovery demos to the phases where the policy fails.
   - Confidence M.

---

## 4. Conflicts and open disagreements

- **Uncertainty/entropy as a trigger.**
  - Positive: AAC (real +15 points), HiPolicy (+25% speed at −4 points success), FIPER (ACE helps failure prediction).
  - Negative:
    - BCP (W3): marginal gains at high runtime.
    - Knowing-When-to-Stop (W3): multi-sample truncation gave stop-go and 18.3% real success.
    - Sentinel: DP output variance is a poor failure signal in multimodal tasks.
  - Resolution in the notes: entropy works for horizon selection when a minimum-magnitude or minimum-length guard exists (AAC) and when sampling is cheap. It is unreliable alone as a failure alarm, which FIPER addresses by requiring AND with novelty.
- **Cumulative vs windowed vs per-step monitoring.** Cumulative scoring (STAC in Sentinel) is accurate but late. FIPER says a window is best. Per-step scoring (FAIL-Detect's logpZO as used by FIPER) gives many false alarms. FAIL-Detect's own results show logpZO winning with time-varying CP bands.
- **Monitor ranking depends on the paper.**
  - FAIL-Detect puts STAC at the bottom and says it is too slow on hardware.
  - Rewind-IL puts FAIL-Detect below TIDE and says it over-triggers on deformables.
  - RC-NF beats FAIL-Detect on LIBERO-Anomaly.
  - No neutral benchmark exists. Each method won on its authors' own tasks.
- **Fixed vs event-gated slow updates.** Hi Robot says a simple 1 s clock "works well". FiS finds a fixed 1:4 ratio optimal. StreamVLA shows event gating is faster and better.
- **Inpainting vs warm-start for continuity.** RTC and Legato help under 0.1–0.3 s delays (Track A). GPC finds inpainting hurts at 1–10 ms replanning, where warm-start wins. The two results are consistent if the method is matched to the delay regime.
- **Separate vs shared fast model.** RoboDual, EMS and GR00T keep System 1 as a separate small net. FiS argues that sharing VLM blocks is better, but only against π0/CogACT at 7B scale.

---

## 5. Recommended decision architecture for our SO-101 system

Constraints: SO-101 with Feetech STS3215 position servos; RealSense scene camera plus wrist camera; 50–150 demos; RTX 5060 8 GB; must react to moved objects and failed grasps. Our current SmolVLA has about 2 s latency and jerks at chunk boundaries.

**L0: Servo executor (host, 50–100 Hz; our assessment of the rate)**
- Hold a timestamped action trajectory and interpolate by wall-clock time (ParallelSMPC, RDP).
- When a new chunk arrives, drop the actions that are already in the past (latency matching, RDP/UMI).
- Apply a C1/trapezoidal target profile, and optionally backlash preload and stiction dithering (AhaRobot, same servos).
- Safety reflex: joint, workspace and velocity limits, plus a servo load/current spike check. On violation, time-scale the playback (slow or freeze along the same path) instead of editing the path (PACS; ActFovea shows editing costs success).
- Confidence: M.

**L1: Fast visuomotor policy (the only learned motor layer)**
- Use a small chunked flow or diffusion policy (ACT/DP-scale up to ~0.4B, e.g. ReactVLA-like) on scene RGB-D plus the wrist camera.
- Re-query at ≥10 Hz with a short execution horizon, especially near grasp and place.
- Evidence:
  - HiRT: loop rate decided moving-target success.
  - DEHP (W3): short horizons in precision phases.
  - RoboDual: the specialist does the precision work at 15 Hz with 20M trainable parameters.
- Chunk continuation follows Track A: RTC or Legato for delays of a few steps, warm-start if replanning every 1–2 steps (GPC).
- Include recovery segments in the demos: re-grasp after a slip, re-approach after the pumpkin is moved (DuoCore-FS, RDP, REBOOT).
- Confidence: M/H that small is enough for a single task; M for the rate.

**L2: Monitors (every policy step; all calibrated on about 10–30 successful rollouts with conformal thresholds)**
- (a) TIDE inter-chunk discrepancy, from the overlap of successive chunks (single sample, ~0.2 ms; Rewind-IL). This is the primary alarm. Confidence M/H.
- (b) Embedding novelty on the policy's own vision encoder: RND (FIPER) or nearest-neighbour latent distance (LPB). Use a sliding window and AND it with (a) or with entropy, to avoid alarms on benign novelty such as lighting changes (FIPER). Confidence M.
- (c) Optional: action entropy from N≤10 batched samples of the head, to shorten the execution horizon when uncertain, with a minimum-length floor (AAC, HiPolicy; beware stop-go per Knowing-When-to-Stop). Confidence L/M.
- (d) Phase/checkpoint tracker: store encoder embeddings of key demo frames (pre-grasp, grasped-and-lifted, above tray) and track the latest reached checkpoint by cosine similarity (Rewind-IL; StreamVLA's completion gating is the same idea). Confidence M.
- (e) A grasp-success check from the servos: gripper position stopped short of closed plus gripper load. This is our proposal and no paper here tests it. Confidence L.

**L3: Response policy (a small rule table: finite-state logic, not learned)**

| Condition | Response | Source | Confidence |
|---|---|---|---|
| Discrepancy or novelty alarm | Flush the queue and re-query immediately | Rewind-IL | M |
| Alarm persists, or (e) says the grasp failed | Rewind to the last checkpoint action (e.g., pre-grasp pose), clear policy memory, retry | Rewind-IL | M; RC-NF homing is the cruder version |
| K retries fail | Stop (safe hold) and ask the human | FIPER/ActFovea framing | M |

Record these episodes as new recovery demos (REBOOT, RaC direction).

**L4: Slow layer, optional**
- Not needed for the single pumpkin task (M).
- If a second object or language instruction is added, use a small VLM or goal selector at about 1 Hz or on events (Hi Robot trigger rule; StreamVLA gating). Train the fast policy against deliberately stale slow context (RoboDual latency-aware training; DuoCore-FS cross-timescale sampling).
- On one 8 GB GPU, expect contention between the slow and fast models. πR2 needed separate GPUs, and FiS could not run its two systems in parallel on its hardware.
- Do not use cloud VLM monitors in the control loop: GPT-4o took 14 s in Sentinel.
- Confidence: M.

**Explicitly not recommended**
- 3–7B dual systems on 8 GB (FiS, HiRT, RoboDual generalist).
- Runtime physics-sampling MPC. It needs object state or mocap and an RTX-5090-class GPU for 8–10 Hz (ParallelSMPC, VP-STO).
- Temporal ensembling or action clipping as the reactivity or safety fix (RDP, ActFovea).
- Event cameras: we have no DAVIS sensor. E-VLA is relevant only if low light becomes the dominant failure.

---

## 6. Gaps and caveats

- No paper tests a monitor-plus-rewind stack on an SO-100/101-class arm. Rewind-IL on the AgileX Piper is the closest. E-VLA used an SO100 but addresses perception, not decision-making.
- No paper tests servo load or current as a fast feedback signal for a learned policy on hobby servos. RDP and Tube DP use tactile or force sensors.
- Most real-robot evaluations use 10–20 trials per cell. Many headline numbers are figure-only: Hi Robot, HiRT's frequency sweep, LPB Cup Arrangement, SafeFlowMPC, VP-STO, and GPC.
- Monitor comparisons are not neutral. Each paper's method wins on its own tasks.
- Monitor compute on our laptop GPU is unmeasured. The reported overheads (0.22 ms TIDE, ~1 ms for N≤10 sampling, +2 ms HiPolicy) come from A800/4090-class GPUs.
