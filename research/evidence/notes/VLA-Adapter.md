# VLA-Adapter — VLA-Adapter: An Effective Paradigm for Tiny-Scale Vision-Language-Action Model (2025, arXiv 2509.09372)
Setup: Prismatic VLM on Qwen2.5-0.5B (DINOv2 + SigLIP vision), NO robot pretraining, with 64 learnable ActionQuery tokens. The policy has 24 layers, one per VLM layer, and each layer's "Bridge Attention" does three things: cross-attends to that layer's raw VL features (gated by learnable tanh(g), init 0), cross-attends to ActionQuery + proprio, and self-attends. Starting from zero actions, it regresses an 8-step chunk with L1 loss in ONE forward pass. Policy 97.3M params; 197.2M trainable in total with LoRA on the VLM. Inputs: third-person + wrist 224². Training: batch 16, 150k steps, LoRA, 4×H100. Benchmarks: LIBERO (50 trials per subtask), CALVIN ABC→D. Real: 6-DoF Synria Alicia-D leader/follower (SO-101-like), Logitech C920e third view + RealSense D405 wrist, 4 task types, 10 trials each, with randomized object positions.
Claim: how VL features are bridged to the policy matters more than backbone size. With all-layer raw + query features, a 0.5B VLM with no robot pretraining matches OpenVLA-OFT (7B).
Evidence:
 - LIBERO avg: VLA-Adapter 97.3 (Spatial 97.8, Object 99.2, Goal 97.2, Long 95.0). Pro version 98.5. OpenVLA-OFT 97.1, π0 94.2, SmolVLA 88.8 (as cited), GR00T N1 93.9, DP 72.4.
 - CALVIN ABC→D Avg. len: 4.42 (Pro 4.50) vs OFT 4.10, Seer-Large 4.28, MoDE 4.01.
 - Efficiency (8-step chunk; GPU not stated): OpenVLA 4.2 Hz / 0.240 s. OFT without wrist/proprio 109.7 Hz / 0.073 s. OFT 71.4 Hz / 0.112 s. VLA-Adapter 219.2 Hz / 0.0365 s.
 - Training VRAM at batch 8: 24.7 GB vs 62 GB for OFT (Fig. 1).
 - The abstract claims "8 hours on a single consumer-grade GPU", but no GPU model, VRAM or step count backs it in the text.
 - Real: beats ACT and a 0.5B+OFT variant on pick / move / stack / long-horizon (figure only, 10 trials each).
Ablations (LIBERO-Long):
 - Bridge style, same backbone:
   - last-layer raw (RoboVLMs style) 85.8
   - last-layer query (OFT style) 90.2
   - middle-layer raw (GR00T style) 88.4
   - all-layer raw (π0 style) 90.6
   - all-layer query 92.6
   - both (ours) 95.0
 - Single-layer raw features: middle layers are best (layer 9 → 89.8, 13 → 88.4, 24 → 85.8).
 - Single-layer query features: deeper is better (layer 1 → 78.2, 24 → 90.2).
 - Backbone: 0.5B+OFT 85.8 → +ours 95.0. 7B LLaMA2+OFT 87.5 → 95.2. OpenVLA-7B (robot-pretrained) + OFT 94.5 → 95.4. Larger backbone and robot pretraining add ≤0.4 on top of the bridge.
 - FROZEN backbone: OFT 0.0, SmolVLA 77.0, VLA-Adapter 86.4 (only ActionQuery + policy trained).
 - Injection gating: learnable raw + full query 95.0. Other combinations 91.0–92.6.
 - Number of ActionQuery tokens: 64 is best; too few or too many hurt (figure).
 - L1 vs DiT policy (same bridge): 95.0 vs 91.6, and L1 is faster.
Failure/limitations: authors note real-world generalization is limited by the tiny scale and lack of embodied pretraining. Critical read:
 - Almost all numbers are LIBERO/CALVIN (sim, near-saturated).
 - Real results are figure-only with 10 trials and no robustness shifts.
 - The consumer-GPU claim is unsupported: stated VRAM is 24.7 GB at batch 8.
 - The chunk is only 8 steps, with no async discussion.
 - The latency GPU is unnamed.
Conflicts:
 - L1 > diffusion here agrees with OpenVLA-OFT, but conflicts with SmolVLA (flow 80.25 > L1 75.25), FLOWER (flow 4.44 > L1 head 3.33) and ACT (L1 collapses on human data without CVAE). Plausible resolution: LIBERO demos are fairly unimodal per task, and the L1 policy here gets very rich multi-layer conditioning. Our multimodal human teleop data is closer to ACT's warning.
 - Frozen-backbone result (86.4 vs SmolVLA 77.0) suggests SmolVLA's "first-N-layers only" bridge underuses the VLM.
 - Agrees with SmolVLA/FLOWER that intermediate layers carry the action-relevant features.
Relevance: the real rig (6-DoF leader/follower, D405 wrist cam + webcam) is close to SO-101. A 36 ms single-pass L1 policy would remove sampling latency entirely. But fine-tuning at 24.7 GB/batch 8 does NOT fit 8 GB as published; it would need a frozen VLM (86.4 on LIBERO-Long), batch ≤2, and gradient checkpointing. The frozen variant is realistic on 8 GB (inferred, not tested). Robustness to lighting, object or camera shift is untested.
Decision impact:
 - Q12 model size: supports 0.5B VLM + ~100M policy being enough. Backbone scaling adds little once the bridge is good (+0.2 at 7B) — M (sim).
 - Q03 vision/features: supports using multi-layer (esp. middle-layer) VLM features plus learnable query tokens rather than last-layer or first-N-layers — M.
 - Q01 action head: supports an L1 one-pass chunk head when conditioning is rich (95.0 vs DiT 91.6) — M (LIBERO-Long only; conflicts with SmolVLA/FLOWER/ACT).
 - Q10 latency: single-pass regression gives 36 ms / 219 Hz chunk throughput — M (GPU unstated).
 - Q13 data: no robot pretraining needed for LIBERO-level tasks — L/M (sim).
