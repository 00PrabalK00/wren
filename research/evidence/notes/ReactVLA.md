# ReactVLA — ReactVLA: Fast and Lightweight Reactive Robot Manipulation via Improved Mean Flow Action Generation (2026, arXiv 2606.14255)
Setup: frozen SigLIP2 image encoder (256 tokens/view, agent + wrist, 256×256), SmolVLM text encoder for language, 1 proprio token. A 16-block "Attention Residual" transformer (hidden 768, 8 heads, SwiGLU 2048, RoPE) predicts H=16 × 7-D RELATIVE actions and executes K=8. Improved Mean Flow (iMF) head with JVP correction, Pseudo-Huber loss (δ=1). 2 sampling steps in sim, 5 steps on the real robot. 0.39B params total, with no robot pretraining. Benchmarks: LIBERO (SmolVLA protocol, multi-task over 40 tasks); RoboIMI (custom bimanual MuJoCo, 2 tasks, scripted demos, 3 cams, 100 rollouts); real Diana-7 arm with 2 tasks × 50 teleop demos, wrist + third-person cams, 60 Hz joint targets, 20 trials/task. GPUs are not named, and different benchmarks were run on different GPUs.
Claim: mean-flow one-to-few-step generation plus attention residuals gives SmolVLA-level success at ~4× lower latency.
Evidence:
 - LIBERO avg / latency: ReactVLA 88.0 at 18.3 ms. SmolVLA-0.45B 87.3 at 74.1 ms. SmolVLA-0.24B 82.8 at 71.1 ms. π0 86.0 at 93.4 ms. OpenVLA 76.5 at 115 ms. DP 72.4 at 178.8 ms. (Baseline success numbers are copied from the SmolVLA paper; latencies appear to be their own measurements.)
 - RoboIMI reward (peg-in-socket / transfer / latency): ACT 289.6 / 115.6 / 4.5 ms. DP 1019.4 / 319.2 / 398 ms. ReactVLA 1513.6 / 526.2 / 15.1 ms. SmolVLA failed to converge (0 reward).
 - Real Diana-7, 50 demos each: Orange P&P 95% ReactVLA vs 95% SmolVLA. Block Stack 90% vs 75%. Latency 38.6 ms vs 82.2 ms.
Ablations:
 - AttnRes → standard residuals: LIBERO 88.0 → 28.7 (from the training curve; a suspiciously large drop).
 - Pseudo-Huber → MSE: loss spikes and unstable training from second-order JVP gradients (figure only; the final SR gap is qualitative).
 - Steps: 2 in sim, 5 on the real robot "for smoothness" (no step-count sweep reported).
Failure/limitations: authors say real evaluation is a controlled tabletop with few demos, and latencies are not comparable across benchmarks (different GPUs). Critical read:
 - Only 2 real tasks, 20 trials each, one lab.
 - SmolVLA was likely fine-tuned without its community pretraining (not stated). ACT was trained on scripted RoboIMI data and DP took 398 ms, so baseline tuning is unclear.
 - The iMF training needs JVP (second-order gradients), which is memory-heavy.
 - No code/weights are mentioned apart from a project page.
 - Execution is synchronous (queue drained, then re-infer). There are no async or chunk-boundary experiments, and the smoothness claims are qualitative.
Conflicts: agrees with SmolVLA/FLOWER that a small flow-type head on frozen/pruned VLM features is enough. It differs from RTC's approach: ReactVLA attacks latency by cutting steps (mean flow), while RTC hides latency via inpainting. They could be combined, although inpainting guidance with 1–2 steps is untested. The huge AttnRes effect is not corroborated anywhere.
Relevance: this is the most directly useful latency data point. SmolVLA-class models run at ~70–80 ms on a normal GPU, so our 2 s is a deployment bug. A 2–5 step mean-flow head is a plausible drop-in to cut head latency further, but the VLM/encoder forward then dominates. With a frozen SigLIP2 and ~100M trainable head, fine-tuning on 8 GB looks plausible (not tested).
Decision impact:
 - Q10 latency: supports few-step flow (mean flow, 2–5 steps) to get <40 ms real-robot latency at equal success — M (2 real tasks, unnamed GPUs).
 - Q01 action head: supports mean-flow/iMF as a fast generative head; Pseudo-Huber needed for stability — L/M.
 - Q12 model size: ~0.39B with frozen encoders is enough for 50-demo tasks — M.
 - Q06 chunking: H=16, execute 8 with synchronous re-query works at 60 Hz — L (no sweep).
