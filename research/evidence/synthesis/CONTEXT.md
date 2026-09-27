# Full project context for the synthesis

## Who / goal
The user is building a SMALL, robust, real-time manipulation policy ("our own model") for a low-cost arm, after a fine-tuned SmolVLA performed poorly. They want a design grounded in the literature, with honest confidence levels, then they will build it with Claude. They care about: robustness (lighting / object appearance / camera shift), smooth real-time control (no jerks, low latency), and eventually language-conditioned multi-object tasks ("pick up the pumpkin" vs "pick up the green box").

## Hardware (exact)
- Arm: SO-101 follower (Feetech STS3215 servos, position mode; LeRobot sets P_Coefficient=16 (default 32), I=0, D=32; gripper Max_Torque_Limit 500 (50%), Protection_Current 250, Overload_Torque 25). Leader SO-101 for teleop (leader/follower). USB adapters: follower serial ...4307, leader ...4310. Backlash, jitter, gravity sag observed (follower wrist_flex ~6° below leader; follower wrist_flex calibrated range capped ~85° while leader reaches ~100°).
- Also available: LeKiwi omniwheel base (3 wheel motors IDs 7-9 on a separate board) — the follower arm can be mounted on it; teleop script exists (lekiwi_teleop.py). Not the current research focus.
- Cameras: wrist camera (USB, /dev/video2 on laptop, 640x480, MJPG). Scene camera: Intel RealSense (likely D4xx stereo, RGB + depth available) on a Jetson (Orin), streamed to the laptop as RTP-JPEG over UDP; currently RGB only (depth not streamed yet). Jetson reachable over Ethernet (10.42.0.81).
- Compute: laptop with RTX 5060 Laptop GPU 8 GB (sm_120, PyTorch 2.10 cu128 supports it, bf16 supported), 16 GB RAM. Was in power-saver mode during the first policy test (GPU throttled); now performance mode.

## Data collected so far
- LeRobot v3 dataset so101_pumpkin_v1: 51 episodes, 11,320 frames, 10 fps, task "Pick up the pumpkin and place it in the tray", two cameras (camera1 = scene, camera2 = wrist), 480x640, absolute joint targets (leader positions) as actions, 6-D state (follower joints, degrees; gripper 0-100). Videos H.264 (re-encoded with GOP 2). Recorded in ONE scene, daylight, ONE pumpkin (orange jack-o-lantern), fixed camera, one operator.
- Recording pipeline (Episode Studio: server.py + teleop_runner.py): 100 Hz leader→follower control loop in a separate process, 10 fps dataset capture, streaming GPU encoding; can record at higher fps (Jetson stream now 30 fps).

## What was tried and what failed
- SmolVLA (450M) fine-tuned from lerobot/smolvla_base on the 51 episodes (batch 16, target 20k steps; tested checkpoint step 6000 ≈ 8.5 epochs; loss ~0.030).
- Real-arm test failures: (1) "always misses" the pumpkin: hovers, opens/closes gripper; (2) test conditions differed from training: night lighting (scene brightness 55 vs 128 in training), a DIFFERENT pumpkin (pink with "NYU" letters), scene camera moved (monitor in view); (3) inference ~1.9 s per query (power-saver mode + fp32; literature says SmolVLA ~74-100 ms on similar GPUs), making synchronous execution stop-and-go; (4) with async inference + a linear fade between chunks, motion became "jumpy". SmolVLA 50-step chunks at 10 fps = 5 s chunks.
- Earlier (before custom runner): LeRobot record loop ran below 10 Hz with stalls → "misses commands every 10 s"; fixed by the separate-process 100 Hz control loop.

## Constraints for the design
- Train and run on the 8 GB laptop GPU (inference target: real-time, ideally <50 ms per query, control ≥10 Hz with smooth execution).
- Data budget: tens to ~150 demos per task, recorded by one person with the leader arm; willing to recollect with a better protocol (multiple pumpkins, lighting, camera jitter, recovery demos, possibly green screen, 30 fps).
- Depth from the RealSense can be added (needs Jetson pipeline change) if evidence supports it.
- Must be buildable in PyTorch within LeRobot conventions (LeRobotDataset v3), ideally as a LeRobot policy so the existing tools (training script, eval_real.py UI panel) work.

## Research performed (what the evidence base is)
- Harvest: 22,779 papers (OpenAlex + Semantic Scholar, 42 topics, 2016-2026) → 7,162 relevant robot-policy papers with abstracts (keyword filter).
- Abstract screening: ALL 7,162 screened by agents against 14 design decisions (Q01-Q14) → evidence cards (screen/cards_*.jsonl, screen/rcards_*.jsonl; relevance 2-3 only), plus per-batch summaries.
- Full-text deep reads (~440 papers): fulltext/notes (66, themed, highest quality), wave3/notes (252), wave4/notes (~120), realtime/notes (~43). Each note has Setup / Evidence / Ablations / Failure / Conflicts / Relevance / Decision impact. Ledgers: fulltext/LEDGER.md, wave3/LEDGER.md, wave4/LEDGER.md (one line per paper×decision with direction and confidence).
- Real-time decision-making track (requested separately by the user): realtime/TRACK_A_REPORT.md (execution: async/chunk continuity/latency) and realtime/TRACK_B_REPORT.md (architecture: monitors, dual systems, recovery).
- Known caveats: many real-robot results use 10-30 trials per cell; some tables were garbled in PDF extraction (notes flag this); screening cards are abstract-level only; notes by different agents vary in depth.

## Known conflicts already surfaced (must be adjudicated)
- Action head: generative (flow/diffusion/VQ/CVAE) vs plain L1/regression (ACT CVAE ablation, BAKU real, Octo, RDT vs OFT, VLA-Adapter, MINERVA, JEPA-Policy MIP, DEM "heads within 3 points").
- Action space: absolute joint vs chunk-wise delta vs step-wise delta (ACT, DP, ActionSpaceStudy, UMI, Real-ORL, χ0, ZETA, AhaRobot).
- Vision encoder: frozen vs fine-tuned vs from-scratch vs distilled small CNN; which pretraining (DINO/DINOv2/v3, SigLIP, MAE/SPA, Theia, CLIP); spatial tokens vs pooled.
- 3D: full-scene point cloud (DP3/iDP3 robust) vs collapses under background change (RISE/CAGE) vs object-centric/segmented 3D robust.
- Wrist camera: essential (MResT, robomimic, Hsu) vs hurts on mobile base (SEVO); naive fusion hurts OOD (Hsu).
- Temporal ensembling: helps (ACT, MINERVA sync) vs hurts (RTC, WhyChunking, PAINT, ImprovingGenBC) — depends on latency/multimodality.
- Proprioception input: helps (HPT) vs hurts generalization/copycat (Octo, FACTR, "Do you need proprio", HULC).
- Execution horizon: short vs full chunk; adaptive horizons.
- SmolVLA vs ACT on SO-101 (SmolVLA paper vs ArmnetBench/SEVO/SO101-Benchmark).
