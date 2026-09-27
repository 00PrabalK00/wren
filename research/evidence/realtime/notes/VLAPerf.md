# VLAPerf — How Fast Can I Run My VLA? Demystifying VLA Inference Performance with VLA-Perf (Jiang et al., NVIDIA Research, Feb 2026, arXiv 2602.18397)
Setup: analytical roofline performance model for arbitrary VLA × hardware × network combinations (BF16/FP16, batch 1), validated against real π0 Triton kernels on RTX 4090 (73–83% fidelity). Studies model scaling, denoising steps, chunk size, long context, async inference, dual-system pipelines, device vs edge vs cloud. No robot experiments.
Evidence:
 - Validation (π0, 10 flow steps, chunk 63, RTX 4090): roofline vs real Triton 14.7 vs 20.0 ms (1 cam), 22.5 vs 27.3 (2 cams), 30.4 vs 36.8 ms (3 cams).
 - π0 E2E (Table 3; vision / VLM / action / total): Jetson Thor 6.06/20.30/26.20/52.57 ms (19.0 Hz); RTX 4090 4.02/19.79/7.25/31.06 ms (32.2 Hz); H100 6.15 ms; B100 3.18 ms.
 - Denoising steps (π0 on 4090-class, relative to 10 steps): action-expert latency 50 steps 5.0×, 20 2.0×, 5 0.50×, 1 0.10×; TOTAL VLA latency 50 → 2.15×, 20 → 1.29×, 5 → 0.86×, 1 → 0.74× (chunk 50). Cutting 10→1 steps saves only ~26% end to end because vision+VLM prefill dominate.
 - Chunk size: total latency nearly flat from chunk 5 to 50 (≈0.85–1.0×) — longer chunks are almost free.
 - Action expert is memory-bound on all GPUs (OI 54); vision/VLM compute-bound on desktop/datacenter GPUs, memory-bound on Thor.
 - Async (Table 8): speedup of async over sync grows with network latency (1.04× on 10G Ethernet, 5.99× on 5G, 13.79× on 4G+slow cloud); on-device with low latency async gives little throughput benefit.
 - Dual-system (Table 9): on Thor, S2 capped at 5 Hz gives 1.46× (27.8 Hz vs 19.0 Hz).
Failure/limitations: analytical, ignores kernel launch/OS overhead (source of the 17–27% gap), no accuracy.
Conflicts: none with measurements; consistent with AsyncInferenceStudy (vision prefill 89.8% of SmolVLA FLOPs) and SnapFlow (denoising ~79% of SmolVLA latency on A800, unoptimised) — the split depends heavily on implementation.
Relevance: high for diagnosis: a 3B π0 should take ~31 ms on a 4090 when properly implemented; SmolVLA (0.45B) on a laptop RTX 5060 should therefore be well under 100 ms — ~2 s indicates CPU fallback, eager-mode Python overhead, fp32, power capping, or preprocessing, not intrinsic cost. Also: chunk size is nearly free; step reduction gives limited end-to-end gain for VLM-heavy models.
Decision impact:
 - Q10 latency: fix the software path first; steps matter less than prefill for VLM-based policies (10→1 steps = −26% total for π0) — M/H (validated model).
 - Q06 chunking: longer predicted chunks cost almost nothing at inference — M.
 - Q10 async: on-device async mainly buys smoothness, not throughput — M.
