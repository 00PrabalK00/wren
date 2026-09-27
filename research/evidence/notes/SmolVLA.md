# SmolVLA — SmolVLA: A vision-language-action model for affordable and efficient robotics (2025, arXiv 2506.01844)
Setup: SmolVLM-2 (SigLIP + SmolLM2) with the top half of the LLM layers dropped (first 16 layers are kept); 64 visual tokens/frame (no tiling, pixel shuffle); images resized to 512×512; state goes in as 1 token to the VLM. Flow-matching action expert (~100M params, hidden 0.75×d, alternating cross- and causal self-attention). Chunk n=50, 10 flow steps. Main model is 450M params total. The VLM is FROZEN and only the expert is trained. Pretraining uses 481 community LeRobot datasets (22.9K episodes, 10.6M frames, almost all SO-100), task text re-annotated with Qwen2.5-VL-3B, and cameras manually renamed into a fixed order (top, wrist, side). Pretraining is 200k steps at batch 256 on 4 GPUs; the whole project used ~30k GPU-h. Fine-tuning: 200k steps for real tasks (the authors say far fewer are enough), batch 64 in sim. Real robots: SO-100 with 3 tasks (pick-place, stack, sort) using top+wrist cams, and SO-101 pick-place-lego using top+side cams. Each task has 50 demos (10 per start position × 5 positions). Real eval uses SYNCHRONOUS inference with partial-credit scoring. The trial count per real task is not stated in the main text.
Claim: a 0.45B VLA pretrained on <30k community episodes matches or beats π0 (3.3B) and ACT on low-cost arms, and async inference makes execution ~30% faster.
Evidence:
 - LIBERO avg (VLM init only, no robot pretraining): SmolVLA-0.24B 82.75, 0.45B 87.3, 2.25B 88.75. π0 (robot-pretrained) 86.0, π0 (PaliGemma init) 71.8, OpenVLA 76.5, DP 72.4, Octo 75.1.
 - Meta-World avg: SmolVLA 0.24B 56.95, 0.45B 57.3, 2.25B 68.24. π0 47.9–50.5, TinyVLA 31.6, DP 10.5.
 - Real SO-100 (Table 3): ACT (single-task) 70/50/25, avg 48.3. π0 (multi-task FT) 100/40/45, avg 61.7. SmolVLA (multi-task) 75/90/70, avg 78.3.
 - Real SO-101 lego (single-task): ACT 70 in-distribution / 40 OOD position. SmolVLA 90 / 50.
 - Compared with π0, SmolVLA trains ~40% faster and uses 6× less memory. No absolute inference latency or GPU-memory numbers appear in the main text.
Ablations (LIBERO; VLM frozen, no robot pretraining unless noted):
 - Pretraining and multi-task (real SO-100): single-task with no pretraining 40.0, multi-task with no pretraining 51.7, multi-task with pretraining 78.3. Pretraining adds +26.6 and multi-task adds +11.7.
 - Head: flow matching 80.25 vs L1 regression 75.25 (reconstructed from split table; long-horizon suite 53 vs 38).
 - Attention between VLM and expert: CA 79.0, SA 74.5, interleaved CA+SA 85.5. Among action tokens: causal 74.5 vs bidirectional 67.5 (LIBERO-Long 40 vs 23). The authors say SA gives smoother chunks on the real robot (qualitative only).
 - State goes to the VLM prefix, not the expert: CA 80.3 vs 73.3. SA 53.3 (prefix) vs 74.8 (suffix), so the effect is not consistent across the two variants.
 - VLM depth: N=8 layers 75.0, 16 78.5, 24 79.5, 32 (all) 80.3, skip every 2nd 75.5. A 256M VLM gives 75.8, so skipping layers of a bigger VLM beats using a smaller VLM.
 - Expert width: ×1.0 82.3, ×0.75 77.5, ×0.5 80.3, ×0.25 73.8 (non-monotonic).
 - Chunk size n: 1 → 50.0, 10 → 84.0, 30 → 78.5, 50 → 80.3, 100 → 74.5.
 - Executed steps before re-observing: 1 → 80.3, 10 → 82.8, 30 → 70.8, 50 → 51.8. Frequent re-querying clearly matters.
 - Async vs sync (real, Fig. 5): success 78.3 sync vs 73.3 async. Sorting drops 70 → 50 async; the async hyperparameters were tuned on pick-place and reused. Completion time 13.75 s sync vs 9.70 s async. Cubes placed in 60 s: 9 sync vs 19 async.
Async mechanism: the client pops from an action queue. When |queue|/n < g it sends a new observation, but only if joint-space distance from the last sent observation > ε, or if the queue is empty. The server returns a chunk, which is merged on the overlap by an aggregation f that the main text leaves unspecified. There is NO inpainting or continuity constraint, so the join between old and new chunk is whatever f does. Idle time is avoided when g ≥ (E[latency]/Δt)/n.
Failure/limitations: authors list SO-100-only pretraining, small data (23k eps), a VLM trained on OCR/document tasks, and short-horizon tasks only. Critical read:
 - Real trial counts are not given, and scores use partial credit.
 - ACT was trained single-task against multi-task SmolVLA. Single-task SmolVLA WITHOUT pretraining (40) is BELOW single-task ACT (48.3), so the whole advantage comes from pretraining plus multi-task.
 - The SO-101 OOD test covers only new positions: no lighting, object or camera shift.
 - Async costs success on the longest task.
 - The pretraining data is overwhelmingly 30 fps SO-100 teleop. Our 10 fps data makes n=50 a 5 s chunk instead of ~1.7 s, which is a temporal mismatch with the pretrained prior (my inference, not tested in the paper).
Conflicts:
 - SO101-Benchmark (ACT 33.75 ≈ SmolVLA 32.5 on harder SO-101 tasks) disagrees with the ACT 48.3 vs SmolVLA 78.3 result here. Likely causes: the benchmark used per-task single-task fine-tuning and harder tasks, while this paper's own advantage depends on multi-task training.
 - Flow > L1 agrees with FLOWER (3.33 vs 4.44) and ACT's CVAE finding, but conflicts with VLA-Adapter/OFT (L1 > DiT when fine-tuning a big backbone).
 - Async here has no continuity handling. RTC shows naive merging/TE causes oscillation at high latency, which matches our observed chunk-boundary jerk.
 - ReactVLA measured SmolVLA at 74 ms (LIBERO) and 82 ms (real). Our ~2 s is ~25× worse, which points to a deployment problem (CPU fallback? a PyTorch/CUDA build without Blackwell sm_120 support on the RTX 5060? no bf16/compile? fp32 at 512² with 10 steps?) rather than to the model.
Relevance: this is the only paper here with SO-100/101 data, and its pretraining matches our embodiment. Frozen VLM + 100M expert should fine-tune on 8 GB (bf16, small batch). BUT the real gains come from multi-task training plus in-domain pretraining, and robustness to lighting, object appearance or camera shift was never tested, which is exactly where our fine-tune breaks. The async stack as published has no chunk-boundary fix.
Decision impact:
 - Q01 action head: supports flow over L1 (+5 LIBERO avg, +15 on long) — M (sim, frozen-VLM setting).
 - Q06 chunking: supports chunk 10–50 steps and re-querying every ≤10 steps (51.8 → 82.8) — M/H (clean monotone ablation, but sim only).
 - Q10 latency/async: supports async queueing for throughput (+42% speed, 2× cubes/min) but weakens async-without-continuity for success (sorting 70 → 50) — M.
 - Q12 model size: supports ~0.45B with frozen VLM, keeping early VLM layers. Scaling 0.24 → 2.25B gives only +6 LIBERO — M.
 - Q13 data: supports multi-task pooling (+11.7) and in-embodiment pretraining (+26.6) at 50 demos/task — M (few trials).
 - Q03 vision: frozen SigLIP-based VLM works when paired with robot pretraining; without pretraining, single-task is below ACT — M.
 - Q14 robustness: no evidence (position-only OOD) — L.
