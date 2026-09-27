# W3_pimathbfR2ReactiveRealtimeFlowPolicies — πR2: Reactive Real-time Flow Policies (2026, arXiv 2607.26055)
Setup: Sim: MuJoCo Leap-hand cube reorientation, state-based, 200 RL-expert demos at 50 Hz, Conditional U-Net 1D flow head, H=16, 3 seeds x 100 episodes. Real: xArm6 + 12-DoF XHand, ONE overhead 640x480 RGB camera (no wrist cam), proprio incl. joint torques + fingertip forces, fine-tuned GR00T-N1.7 (VLM + Eagle-2 frozen; only DiT action head trained), 100-300 demos/task at 25 Hz, chunk H=50 absolute joint targets (2 s), 4 tasks x 20 trials, 8x A5000/A6000 training, deploy on 1-2 A5000.
Claim: diffusion-forcing-style per-position noise schedule ("staircase": in-flight actions clamped clean as inpainting, ramped interior, noise tail) + splitting conditioning into fast (proprio, fresh every tick) and slow async (vision-language, cached, with learned staleness embedding) makes a large flow VLA reactive at 25 Hz with 1 NFE per call.
Evidence (Table 1, real, SR /20 and progress):
 - Don't Spill: Sync (h=10) 4/20 (16/80), Naive-async+TE 7/20 (30/80), Train-time RTC 9/20 (45/80), πR2 10/20 (55/80)
 - Tidy Up Book: 4/20, 7/20, 8/20, πR2 12/20 (prog 9/40, 15/40, 18/40, 24/40)
 - Insert Box: 11/20, 12/20, 10/20, πR2 16/20 (prog 56, 61, 53, 68 /80)
 - Catch Book: 4/20, 2/20, 5/20, πR2 11/20
 - Latency: GR00T VLM+preproc ~60 ms + 4-step DiT ~80 ms = ~140 ms/call; baselines d=4-5 ticks (@25 Hz), πR2 d=1-2 (~4x faster replanning).
 - Sim (latency study, mean of 3 seeds): πR2 w/ async 0.43/0.42/0.45 vs naive-async 0.33/0.29/0.22 vs train-time RTC 0.36/0.32/0.19 at d0 = 1/2/3 ticks — gap widens with delay.
Ablations:
 - Execution horizon (sim, zero delay): standard flow degrades as h grows 1→8; πR2 (1 NFE/call) matches flow at h∈{1,2} (figure only).
 - πR2 without async fast/slow split sits between (effective delay 1.0 d0 vs 0.25 d0) — figure only.
 - Synchronous inference: robot pauses → jittery chunk boundaries (ball rolls away). Naive async + temporal ensembling: smoother but less precise. RTC: smooth but reacts late, biased toward continuing its motion, over-grips (120 N vs 50 N).
Failure/limitations: needs 2 GPUs at deploy (VLM worker and action head on separate GPUs to avoid contention); does not handle external comm latency; real tasks rely heavily on force/torque proprio that SO-101 lacks (Feetech servos give position and load estimates only). Critical read: 20 trials/task, some gaps small (Don't Spill 10 vs 9); dexterous hand tasks.
Conflicts: Agrees with RTC/Train-time RTC literature that sync inference causes chunk-boundary jerk and inpainting in-flight actions fixes continuity; goes further that RTC's commitment to in-flight actions hurts reactivity. Agrees with ACT TE being smoother but blurrier (precision loss).
Relevance: HIGH for our Q10 problem (jerky chunk boundaries with async inference, ~2 s latency). Directly transferable ideas regardless of model size: (1) train-time conditioning on the d in-flight actions (Train-time RTC / staircase) so new chunks start continuous; (2) randomize d during training so one model handles variable laptop latency; (3) cache vision features asynchronously and refresh proprio every tick. Our chunk boundary jerk under async is exactly the "naive async" row. With a small policy (<100M), the simpler fix is making inference fast enough (<1 tick) so async is barely needed.
Decision impact:
 - Q10 latency/smoothness: supports train-time in-flight-action conditioning with randomized delay over naive async/TE and sync (Catch Book 11/20 vs 5/20 RTC vs 2/20 naive async) — M/H (real, controlled, same base model)
 - Q06 chunking/TE: temporal ensembling in async mode smooth but imprecise; shorter execution horizon better for reactive tasks — M
 - Q01 action head: 1-NFE flow per call with per-position noise schedule is viable (no multi-step cost) — M
 - Q12 model size: large VLA backbone forces async; latency cost 140 ms/call even on A5000 — M (argues for small policy on 8 GB)
