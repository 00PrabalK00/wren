# W3_RethinkingthePracticalityofVisionlanguag — Rethinking the Practicality of Vision-language-action Model: A Comprehensive Benchmark and An Improved Baseline (LLaVA-VLA / CEBench) (2026, arXiv 2602.22663)
Setup: CALVIN ABC→D (Franka sim, 1000 eval rollouts), RoboTwin 2.0 sim (36 tasks, 400 traj/task, 8 eval tasks × 100 trials, seen + domain-randomized DR), real Cobot-Magic mobile bimanual (Piper arms), 8 real tasks × 200 demos, cams 480×640 @30 Hz, 100 real episodes/task (fixed-base), 10 (mobile). Model: LLaVA-OneVision-0.5B, first+third-person images vertically concatenated into ONE image, proprio tokenized as text-like tokens, discrete action tokens (256 bins), chunk 5. Post-train on 8×H100, fine-tune on 1×4090.
Claim: a 0.5B VLM-based VLA without robot-dataset pre-training (in-domain multi-task post-training + task fine-tune) matches 7B VLAs and is far more robust than ACT/DP/TinyVLA under visual DR.
Evidence:
 - CALVIN Avg.Len: LLaVA-VLA 0.5B 3.65–3.68 vs same arch 7B 3.75; OpenVLA 7B 3.27; RoboFlamingo 3B 2.47; 3D Diffuser Actor 3.35; GR-1 3.06.
 - RoboTwin (8 tasks avg, seen/DR): ACT 7.1/0.5; DP 34.5/0.6; LLaVA-VLA 40.3/28.6; RDT (1B, pretrained) 48.9/11.4.
 - Real fixed-base bimanual, 200 demos/task, seen/DR (DR = new tabletop color/texture + distractors): ACT 18.6/3.0; TinyVLA 17.5/4.2; LLaVA-VLA 44.2/30.7. Stack bowls 58/40 vs ACT 30/10.
Ablations (CALVIN unless noted):
 - Multi-view as separately tokenized images → merged single composite image: Avg.Len 1.50 → 3.68.
 - Proprio via MLP projector → proprio tokenizer: 3.09 → 3.68.
 - Chunk size 1/5/12/20: 2.25 / 3.68 / 3.35 / 0.70 (sharp collapse at 20 for this autoregressive discrete model).
 - Discrete (256-bin tokens) vs continuous diffusion head: 3.68 vs 3.70 (no difference).
 - 256 vs 1024 bins: 3.68 vs 3.65.
 - RoboTwin pre-training vs in-domain post-training curriculum: open laptop 20% → 38%, lift pot 18% → 39%.
 - Mobile: plain value tokens vs direction+value tokens: 2/10→4/10, 1/10→4/10 (10 trials).
Failure/limitations: ACT/DP collapse to ~0 under DR (both sim and real); authors attribute LLaVA-VLA robustness to VLM pretraining but there is no ablation of backbone init vs scratch. Chunk-size and discrete-vs-continuous ablations are CALVIN-only. "Pre-training" comparison details unclear (only 2 tasks). No latency numbers reported. 200 demos/task is 2–4× our budget. Real success still modest (44% seen).
Conflicts: Chunk collapse at 20 steps conflicts with ACT's gains up to k=100 — different model (autoregressive tokens, 30 Hz?/CALVIN) and CALVIN's closed-loop needs; suggests chunk optimum is architecture-dependent. Discrete ≈ continuous agrees with FAST/VQ papers claiming tokenization is fine when chunked. ACT's near-zero DR robustness agrees with many reports that from-scratch ResNet policies are brittle to background/lighting change.
Relevance: Our failure set (lighting, new pumpkin appearance) matches their DR; evidence that pretrained VLM visual features (SigLIP-based) survive tabletop/distractor change far better than ACT's ImageNet ResNet18 — but a 0.5B VLA still is heavy for 8 GB at interactive latency. The "one composite image" trick for scene+wrist is cheap token-wise.
Decision impact:
 - Q03 vision encoder: supports pretrained VLM (SigLIP-family) features over ACT-style ResNet for visual shift — confidence M (confounded: whole model differs, real 100 trials).
 - Q12 model size: supports small (0.5B ≈ 7B) — confidence M (CALVIN only for size ablation).
 - Q01 action head: discrete tokens ≈ diffusion head when chunked (3.68 vs 3.70) — confidence L (sim, one benchmark).
 - Q06 chunking: chunk 5 best, 20 collapses for AR token VLA — confidence L (sim, architecture-specific).
 - Q11 cameras: wrist+third-person needed; merged composite image >> separate token streams (1.50 → 3.68) — confidence L/M (sim).
 - Q14 robustness: ACT/DP ~0% under background/distractor DR, VLA 30.7% real — confidence M.
