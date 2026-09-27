# W3_SAFEPrunerSemanticAttentionGuidedFutureA — SAFE-Pruner: Semantic Attention-Guided Future-Aware Token Pruning for Efficient Vision-Language-Action Manipulation (2026, arXiv 2605.29662)
Setup: training-free visual-token pruning for VLAs (OpenVLA, OpenVLA-OFT, CogACT, π0.5); LIBERO (2000 episodes), SIMPLER (CogACT), real Astribot S1 dual-arm with 2 wrist + 1 head camera, π0.5 fine-tuned on 200–1,000 VR demos, 3 tasks. Latency = VLM backbone per step, RTX 4090 (sim) / RTX 3090 (real).
Claim: forecasting deep-layer token saliency from previous timesteps (attention on the same semantic entity persists across steps) allows aggressive pruning with <1.5% success loss and up to 1.89× speedup.
Evidence:
 - Real π0.5: FLOPs 2.264T → 1.543T; backbone latency 80.36 → 43.56 ms; success 81.3 → 79.3% (FastV: 56.93 ms, 69.0%).
 - SIMPLER CogACT VM: 74.8 → 74.5%, 1.73× speedup, 37.4% FLOPs; VA 61.3 → 61.9%, 1.67×.
Ablations (OpenVLA-OFT LIBERO): vanilla 96.8% / 3.970T / 70.25 ms; shallow-only pruning 94.5%; + forecast (fixed keyframes) 95.8%; full 96.4% / 1.722T / 37.22 ms. Quantization (HiF8) compatible: −56.4% FLOPs, −38.1% memory at comparable success.
Failure/limitations: only backbone latency reported (not action expert / end-to-end); pruning at >70% risks losing core tokens; gains modest vs simpler pruning in sim.
Conflicts/Relevance: Only relevant if we keep a VLA. Useful calibration: π0.5 (~3B) VLM backbone runs ~80 ms/step on a desktop 3090 — so our ~2 s SmolVLA (450M) latency on the laptop 5060 is far above what the model size implies and points at a pipeline problem (fp32/CPU fallback, image preprocessing, network hops, too many flow steps) rather than an inherent limit. Token pruning/quantization can halve latency further.
Decision impact:
 - Q10 latency: visual-token pruning gives ~1.8× backbone speedup with ~2 pt real success loss; VLA backbones are ~40–80 ms on desktop GPUs — confidence M (real, but backbone-only timing).
