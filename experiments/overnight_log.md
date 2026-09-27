# Overnight training log (2026-09-26 → 27)

Runs (100 episodes, 19,832 frames; episodes 76 and 92 excluded as empty):
- act_pumpkin_v2 — ACT baseline, 80k steps, batch 8, checkpoints every 10k
- so101flow_pumpkin_v2 — our flow policy v1, 60k steps, batch 16, checkpoints every 5k

## 2026-09-26 23:24 — start
- Server, wrist camera and Jetson colour stream shut down for the night to free RAM; free RAM now 7226 MB available.
- ACT: 1030/80000
- so101flow: 1319/60000

## 2026-09-27 00:10 — manual check (user asked)
- Both runs alive, no errors, no new memory kills. RAM ~6.9 GB available.
- ACT v2: 5.5k/80k, loss 10.2 → 0.42 (step 6k). No checkpoint yet (first at 10k).
- so101flow v2: 6.4k/60k, loss 1.65 → 0.114 (step 6k). Checkpoint 005000 saved.
- Jetson offline test, so101flow 5k (recorded frames): model 294 ms (bf16 296 ms, no gain), round trip 321 ms;
  chunk error vs demo 5.1 deg (mean over 1.6 s); switch disagreement 13.0 deg plain → 2.6 deg with RTC.
- Fix: RemotePolicy load timeout 120 → 300 s (first so101flow load on the Jetson took 125 s).
- TODO: Jetson speed. bf16 didn't help, so it's probably kernel-launch bound (slow ARM CPU). Try fewer flow steps
  (8 → 4), CUDA graphs / torch.compile, or MAXN power mode.

## 2026-09-27 00:47 — scheduled check
- Both runs alive, 0 errors, no new memory kills (the 2 on record are the 21:57 crash). RAM 6.5 GB available, GPU 7.1 GB used.
- ACT v2: 9.4k/80k, loss 0.274. First checkpoint (10k) is imminent.
- so101flow v2: 10.9k/60k, loss 0.085. Checkpoints 5k, 10k.
- Jetson offline test, so101flow 10k: model 289 ms, round trip 315 ms; chunk error vs demo 3.1 deg (5k: 5.1);
  switch disagreement 7.4 deg plain → 1.5 deg with RTC (5k: 13.0 → 2.6).
- No action needed.

## 2026-09-27 02:06 — manual check (user asked)
- Both alive, 0 errors, no memory kills since the crash. RAM 6.9 GB available.
- ACT v2: 17.5k/80k, loss 0.183, checkpoint 10k. Estimated finish ~11:40.
- so101flow v2: 20.0k/60k, loss 0.055, checkpoints 5k/10k/15k/20k. Estimated finish ~08:50.
- Jetson offline test, so101flow 20k: chunk error vs demo 1.7 deg (10k: 3.1); switch disagreement 5.0 → 1.2 deg with RTC; model 288 ms.

## 2026-09-27 03:47 — scheduled check: DISK FULL, both runs crashed, fixed and resumed
- Both runs died writing checkpoints (ACT at 30k, 03:29; so101flow at 25k, 02:49): "No space left on device" (174 MB free of 439 GB).
- Damage: so101flow 025000 empty (deleted); ACT 030000 model OK but optimizer state incomplete (state deleted, model kept for testing). `last` → 020000 for both.
- Freed 6.4 GB, only my own or regenerable data:
  - paper PDFs in the lit-review scratch (reports and notes are safe in ~/So101/research);
  - optimizer state of older checkpoints of these two runs (all models kept).
- Not touched (your call): SmolVLA runs 3 × 13 GB in ripple-research/outputs/train, ~/.cache 44 GB, ~/Downloads 11 GB.
- Prevention:
  - so101-prune-checkpoints unit keeps optimizer state only in each run's newest complete checkpoint (every 5 min);
  - so101flow now saves every 10k (was 5k).
  - Expected remaining growth ~4 GB against 6.6 GB free.
- Resumed both from 020000 (100 episodes, same config): ACT 60k steps left (~9.8 h, ~13:40), so101flow 40k left (~5.9 h, ~09:50).
- Lost progress: ACT 20k→30k (~1.5 h), so101flow 20k→25k (~45 min).

## 2026-09-27 04:02 — manual check (user asked)
- Both running since the 03:52 resume, no new errors or memory kills. Disk 86 GB free after cleanup (was 174 MB).
- ACT v2: 21k/80k, loss 0.168, ETA ~13:50. so101flow v2: 21k/60k, loss 0.054, ETA ~09:55.

## 2026-09-27 06:47 — scheduled check
- Both alive, 0 new errors, no memory kills. Disk 86 GB free, RAM 6.8 GB available.
- ACT v2: 38k/80k, loss 0.117, checkpoints 10k/20k/30k (the 30k model is from before the crash). ETA ~13:35.
- so101flow v2: ~40k/60k, loss 0.030, checkpoints 5k–30k (40k saving now). ETA ~09:45.
- Jetson offline test, so101flow 30k (with CUDA graphs + jetson_clocks): model 84 ms, round trip 108 ms;
  chunk error vs demo 1.7 deg; switch disagreement 4.2 deg plain → 1.0 deg with RTC.

## 2026-09-27 09:47 — scheduled check: so101flow v2 FINISHED
- so101flow v2 done at 09:43: 60k steps, final loss 0.018, checkpoints 5k–60k.
- ACT v2: 57k/80k, loss 0.099, checkpoints 10k–50k. ETA ~11:45.
- Jetson disk had filled up (9.9 MB free) with checkpoint copies from each test (3.4 GB) plus the pip cache from the torch install (0.9 GB).
  - Removed both; 3.6 GB free now. Restarted the policy server (its GPU allocator was in a bad state).
  - eval_real.sync_to_jetson now keeps only the checkpoint in use on the Jetson.
- Jetson offline tests (recorded frames; they were in training, so optimistic):

  | ckpt | demo error (deg) | switch disagreement plain / RTC (deg) |
  |---|---|---|
  | 40k | 1.3 | 3.9 / 0.9 |
  | 50k | 1.0 | 2.0 / 0.7 |
  | 60k | 1.0 | 1.7 / 0.7 |

- Laptop CUDA-graph path verified: 59.5 ms graph vs 64.4 ms eager (with ACT training alongside); same outputs.
- Candidates for arm trials: 60k, 50k, 40k (research: pick by real trials among 60/80/100% of training).

## 2026-09-27 12:47 — scheduled check: BOTH RUNS FINISHED
- ACT v2 finished 11:41: 80k steps, final loss 0.086, checkpoints 10k–80k (the 30k model is pre-crash; the others are complete).
- so101flow v2 finished 09:43 (see above).
- Same Jetson offline test (recorded training frames, 1.6 s horizon):

  | policy | round trip | model | demo error | switch disagreement |
  |---|---|---|---|---|
  | ACT v2 80k | 92 ms | 71 ms | 1.4 deg | 1.7 deg (no RTC) |
  | so101flow v2 60k | 108 ms | 84 ms | 1.0 deg | 0.7 deg with RTC (1.7 plain) |

- Caveat: this test is on frames seen in training and is open-loop.
  - It misses closed-loop drift: on the real arm ACT v1 showed 20°+ switch jumps even though offline agreement looked fine.
  - The real comparison needs arm trials (FINAL_REPORT section 7 protocol).
- Stopped the checkpoint pruner and the 3-hourly check (training done).
