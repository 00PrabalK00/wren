# MaskedActionChunking (REMAC) — Real-Time Robot Execution with Masked Action Chunking (Wang et al., ICLR 2026, arXiv 2601.20130)
Setup: LoRA (rank 8, action expert only, merged after training → zero inference overhead) fine-tune of a pretrained flow policy with (i) prefix masking over random delays (one model for all delays), (ii) self-conditioned curriculum: training target mixes ground truth with the frozen pretrained policy's own predictions (γ~Bernoulli(σ), σ annealed) to mimic test-time conditions, (iii) an extra correction loss L∆. Plus prefix-preserved sampling at inference. Sim: Kinetix (12 tasks), ALOHA sim Transfer Cube / Insert Box. Real: π0 (P=50, h=8, 10 steps), 200 demos, 15 Hz, end-to-end delay 122–140 ms (d=2–3; 76–80 ms model + LAN + I/O), grasp tasks Easy/Medium/Hard with narrowed gripper range, injected +75/+150 ms.
Claim: besides inter-chunk discontinuity, async fails from INTRA-chunk inconsistency (executed prefix misaligned with current perception); training on masked prefixes fixes it.
Evidence:
 - Kinetix component table (SR d=0/1/2/3/4): Naive 0.828/0.702/0.639/0.525/0.451; +LoRA only 0.825/0.710/0.630/0.510/0.428 (no gain from parameters alone); +prefix masking 0.863/0.825/0.752/0.729/0.636; +self-conditioned curriculum 0.848/0.837/0.805/0.762/0.710; +L∆ (full) 0.888/0.879/0.859/0.817/0.779.
 - Composable: +BID 0.888/0.880/0.862/0.821/0.781; +RTC 0.888/0.879/0.864/0.826/0.791 (small gains).
 - Robust to wrong delay estimate (Table 7, d=4): RTC 0.588; REMAC 0.760; REMAC with noisy/fluctuating delay 0.757; +spikes 0.757. REMAC with corrupted delays > RTC with exact delays.
 - Real (Table 3 / Fig. 4 figure only): higher completion progress than Sync, Naive, TE, RTC under +0/+75/+150 ms on Grasp-Hard.
 - Data (App. Table 4): 30 vs 200 trajectories gives only mild degradation.
 - ALOHA sim (Tables 5/6) gains small and noisy (e.g., Insert Box 0.14–0.20 range for all).
Failure/limitations: flow-policy only; real numbers figure-only; ALOHA sim gains within noise; generalisation unchanged (fails on novel language like base).
Conflicts: agrees with TT-RTC/Legato (training-time prefix conditioning) and adds self-conditioning to close exposure bias; FutureRTC reproduces REMAC only ~1–2 pts above naive on LIBERO at d≥5 — gains may not transfer to long-delay/long-chunk regimes.
Relevance: moderate-high: LoRA on the action expert is 8 GB-friendly; works with 30 demos; robust to jittery delay estimates — our laptop latency varies. Use max delay over a recent window as the delay estimate (RTC practice they follow).
Decision impact:
 - Q10 async: training-time prefix masking with random delay, fine-tuned by LoRA — SUPPORTED — M (Kinetix large N; real figure only).
 - Q10 latency jitter: prefix-conditioned training tolerates ±1–2 step delay misestimation — M.
