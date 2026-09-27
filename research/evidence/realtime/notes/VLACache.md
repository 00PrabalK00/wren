# VLACache — VLA-Cache: Efficient VLA Manipulation via Adaptive Token Caching (Xu et al., NeurIPS 2025, arXiv 2502.02175)
Setup: training-free: reuse KV of visual tokens that changed little between consecutive frames, but always recompute task-relevant tokens (high decoder attention) and adapt reuse ratio per layer by attention entropy. Tested on OpenVLA, OpenVLA-OFT (LIBERO), CogACT (SIMPLER), and real Kinova Jaco2 with OpenVLA (4 tasks).
Evidence:
 - Component ablation (OpenVLA, LIBERO-Spatial): baseline 84.4% / 51.56 ms; reuse all static tokens 74.2% / 31.03 ms (−10.2 pts!); + evict task-relevant tokens 82.6% / 31.03 ms; + layer-adaptive 83.8% / 32.22 ms.
 - LIBERO avg (OpenVLA): 75.0% → 74.7%, latency 51.91 → 31.83 ms, FLOPs 1.864 → 1.355 T; SparseVLM 64.7% at 83.39 ms; FastV 73.3% at 53.28 ms.
 - CogACT SIMPLER (matching): 74.8 → 74.4%, 54.29 → 39.63 ms.
 - Real Kinova (OpenVLA): avg 82.1 → 84.6%, latency 64.16 → 51.85 ms, control 4.02 → 4.21 Hz. Dynamic background PickPot: baseline 95→80%, VLA-Cache kept 80% with −42% FLOPs, −35% latency.
Ablations: above.
Failure/limitations: gains are largest for big LLM decoders with many visual tokens; control-frequency gain only +5% on the real robot (other pipeline costs dominate). Critical read: naive token reuse costs 10 points — caching must keep gripper/object tokens fresh.
Conflicts: consistent with VLAPerf (prefill dominates) and Jetson-PI (cache VLM state, re-run the cheap action expert).
Relevance: low-moderate for SmolVLA (only 64 visual tokens/frame after pixel shuffle; wins will be small) — more important is the lesson that end-to-end control rate barely moves (4.02→4.21 Hz) when non-model overheads dominate.
Decision impact:
 - Q10 acceleration: token caching gives ~1.3–1.7× model speed at ~0–1 pt loss on large VLAs, little end-to-end gain — M.
