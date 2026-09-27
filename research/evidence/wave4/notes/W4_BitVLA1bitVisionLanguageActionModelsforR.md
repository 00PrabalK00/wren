# W4_BitVLA1bitVisionLanguageActionModelsforR — BitVLA: 1-bit Vision-Language-Action Models for Robotics Manipulation (2025/26, arXiv 2506.07530)
Setup: BitNet b1.58 2B4T ternary LLM + SigLIP-L (224px, 256 tokens) compressed to 1.58-bit weights/INT8 activations via Quantize-then-Distill (teacher = BF16 SigLIP, MSE hidden-state alignment); OXE ~1M-sample robot pretraining (discrete 256-bin tokens, 14 days on 16 H800), then OpenVLA-OFT-style fine-tune: parallel decoding, L1 regression of action chunks, causal attention kept. ~3.0B params, 1.4 GB memory. LIBERO (500 demos/suite, chunk 8, wrist+external cam + proprio). Real: Franka + ONE third-person RealSense D435i, SpaceMouse teleop, 50 demos per task, 3 tasks + 3 OOD variants, 20 eval positions (4×5 grid), chunk 10, inference on remote A800 server.
Claim: a natively ternary VLA matches OpenVLA-OFT (7.7B) on LIBERO and real tasks with 11× less memory and 4.4× lower latency.
Evidence:
 - LIBERO avg (Table I): BitVLA 96.0 (1.4 GB); w/o robot pretraining 94.8; OpenVLA-OFT 97.1 (15.4 GB); π0 94.2 (7.0 GB); SmolVLA 88.8 (4.6 GB); GR00T-N1 93.9. LIBERO-Long: BitVLA 92.8, w/o pretrain 87.6, π0 85.2, SmolVLA 77.0.
 - PTQ (Table II): OpenVLA-OFT INT8 96.7 (7.7 GB), INT4 96.9 (4.7 GB); OpenVLA INT4 72.7 → OFT-style models survive 4-bit PTQ well.
 - Latency (A100, 3×224 imgs, chunk 25; Fig. 6): BitVLA 73 ms / 341 Hz; π0 86 ms; Diffusion Policy 90 ms; RDT-1B 297 ms; OpenVLA-OFT+ 321 ms.
 - Real world: figure only, qualitative: BitVLA > π0 on all 3 tasks, ≈ OpenVLA-OFT; BitVLA without robot pretraining "near-zero success on most tasks" with 50 demos.
Ablations:
 - Robot pretraining removed: LIBERO −1.2 avg (−5.2 Long); real-world near-zero (figure) → pretraining critical at 50 demos real.
 - Bi-directional instead of causal attention mask → "noticeable drop" on real tasks (no numbers).
 - Distillation loss in Quantize-then-Distill: VQA avg 42.4 → 50.8 (vs BF16 53.0); 10B vs 5B tokens 51.5 vs 50.8.
Failure/limitations: real-world numbers only in bar charts; only 20 trials/task; inference remote on A800 (laptop latency not measured, though 1.4 GB would fit 4 GB laptop GPUs per authors); pretraining cost is enormous (not reproducible for us); requires BitBLAS custom kernel for speed.
Conflicts: "w/o pretraining ≈ near zero at 50 real demos" contrasts with ACT/DP trained from scratch working well at 50 demos — BitVLA w/o pretrain is a 3B LLM-based model fine-tuned on tiny data (overparameterized, no robot prior), so the lesson is "large VLM-based policies need robot pretraining", not "small from-scratch policies fail". Latency: DP 90 ms on A100 vs our observed SmolVLA 2 s on laptop suggests our 2 s is implementation/async-overhead dominated rather than intrinsic.
Relevance: Mostly an efficiency paper. Useful datapoints: (a) 4-bit/8-bit PTQ of an OFT-style VLA costs ~0 on LIBERO → quantizing is a cheap latency/memory fix if we stay with a VLA on 8 GB; (b) SmolVLA scores lowest among small VLAs on LIBERO-Long; (c) L1 chunk regression head with large pretrained backbone works (OFT recipe). Not practical to reproduce BitVLA training ourselves; weights are released, but model is still 3B and needs custom kernels.
Decision impact:
 - Q12 model size: supports compressing (PTQ INT8/INT4 or ternary) a pretrained VLA rather than shrinking training data regime; SmolVLA weaker than π0/BitVLA on LIBERO-Long (77 vs 85–93) — L (sim, numbers from original papers)
 - Q10 latency: ternary/INT8 3B VLA 73 ms vs OpenVLA-OFT 321 ms, DP 90 ms on A100 — M (A100, not laptop)
 - Q01 action head: L1 regression of chunks (OFT recipe) with large pretrained backbone reaches 96% LIBERO — L (sim, not isolated)
 - Q13 data: VLA-scale model without robot pretraining near-zero with 50 real demos → do not fine-tune a big un-pretrained backbone on 50 demos — L (figure only)
