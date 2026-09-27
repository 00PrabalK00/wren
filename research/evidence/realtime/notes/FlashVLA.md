# FlashVLA — Streaming Action Decoding for Fast and Asynchronous VLA Inference (Li, Tang, Liu; UCSD/MIT, Aug 2026, arXiv 2608.27384; code z-lab/flashvla)
Setup: flow-matching VLA decoder keeps a STREAMING BUFFER of N action chunks at staggered noise levels with chunk-wise causal attention; every inference step advances each chunk by one denoising step and pops one clean chunk (diffusion-forcing style), so 10-step quality costs ~1 step per call and each new chunk is conditioned on chunks already in flight. Multi-buffer joint fine-tuning adapts pretrained VLAs to partially populated buffers (cold start). CUDA Graphs, packed linears, max-autotune for all methods. Sim: LIBERO (2,000 eps), RoboTwin 2.0 (50 tasks). Cross-arch: SmolVLA, LingBot-VLA. Real: Franka, 30 Hz, RTX A4000, 50 Gello demos/task (22K–68K frames), 3 tasks × 15 trials, 3-point rubric; π0.5 sync / naive async / RTC vs FlashVLA, all with 2-step delay.
Evidence:
 - π0.5 profile: action decoding = 75% of per-step time on RTX 4090 (two views, unoptimised).
 - Latency (Table 2, optimised baselines): RTX 4090 2 views 45.8 → 26.7 ms, 3 views 55.4 → 36.8; RTX 5090 37.0 → 20.3, 44.8 → 27.1 ms.
 - LIBERO async d=1 (Table 1): success 96.9 → 97.8, time per step 53.8 → 22.1 ms (2.43×); VLASH 1.15× speedup at comparable success; StreamingVLA 1.70× but −2.0 success.
 - Sync success: LIBERO avg 96.9 → 97.9 (Long +3.8); RoboTwin 50-task avg 86.0 → 90.5 (long-horizon tasks +36.6).
 - Reaction (30 Hz target): time-to-first-action 80.0 (π0.5) / 62.1 (FASTER) → 37.1 ms; expected time-to-react 130.0 / 112.1 → 70.4 ms.
 - SmolVLA (Table 5): inference 19.7 → 10.1 ms (1.95×); success sync 80.1 (unchanged), async d=1 79.5.
 - Real Franka (Fig. 5): avg score sync 80.0%, RTC 80.0%, naive async 75.6%, FlashVLA 84.4%; completion 1.3× faster than sync, 1.2× faster than RTC; FlashVLA latency 67.3 ms on RTX A4000 (≈2 control periods at 30 Hz).
Ablations: buffer depth / fine-tuning variants in appendix (not extracted).
Failure/limitations: requires fine-tuning with a new attention pattern and buffer; cold-start warm-up passes while the robot holds still; real 15 trials per task with rubric scores. Critical read: real gains are modest (84.4 vs 80.0) and figure-level; SmolVLA gains are latency-only.
Conflicts: same streaming/rolling idea as StreamingDP and πR2 (staircase); VLASH co-author — argues continuity comes "for free" without future-state conditioning. Naive async < sync on the real robot (75.6 vs 80.0), consistent with SmolVLA's async success drop.
Relevance: HIGH for latency facts: SmolVLA needs only ~19.7 ms per inference when properly compiled (GPU not restated for Table 5; 4090/5090-class) — two orders of magnitude below our 2 s. Streaming decoding is a later-stage option; first make the plain model fast.
Decision impact:
 - Q10 latency: optimised SmolVLA ≈ 20 ms per call on a desktop-class GPU; CUDA Graphs + compile are standard baselines — M/H.
 - Q10 async: streaming multi-chunk decoding gives continuity + ~2× speed — M (sim large N; real 15 trials).
 - Q10: naive async lowered real score vs sync (75.6 vs 80.0) — M.
