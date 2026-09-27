# X-VLA — X-VLA: Soft-Prompted Transformer as Scalable Cross-Embodiment Vision-Language-Action Model (2025, arXiv 2510.10274)
Setup: Florence-Large VLM encodes ONLY the main fixed view + language. Wrist and other views go through a shared vision backbone, not the LLM. Proprio + noisy action + flow time are concatenated and linearly projected. Per-data-source learnable "soft prompts" (domain-specific params are 0.04% of the total). Backbone: a plain 24-layer, 1024-d self-attention transformer with flow matching; 0.9B params. Action space is ABSOLUTE EEF (xyz + Rotate6D + binary gripper via BCE). For pretraining, actions are downsampled to 30 anchor points over 4 s ("intention abstraction"). Pretraining: 290K episodes (AgiBot 141K, Droid 90K, RoboMind 57K; 7 setups, 5 robot types), 64×A100 for ~4 days, 200k iterations, batch 1024, ColorJitter. Adaptation is two-step: 1k iterations with only the new prompt + action heads, then joint fine-tuning at the same LR (batch 128, 40–60k steps typical). There is also a PEFT/LoRA variant with 9M trainable parameters. Real robots: WidowX (Bridge tasks, 10 trials each), AgileX bimanual cloth folding (1,200 DAgger-style demos), AIRBOT cloth-pick with 200 demos using PEFT.
Claim: soft prompts absorb embodiment and camera heterogeneity, enabling stable large-scale pretraining. A 0.9B model then adapts SOTA-level with full or even 1%-parameter tuning.
Evidence:
 - Sim: LIBERO avg 98.1 (Long 97.6). CALVIN ABC→D 4.43. Simpler-WidowX 95.8. Simpler-Google VM 80.4 / VA 75.7. RoboTwin-2.0 easy 70.0 / hard 39.0. VLABench 51.1. NAVSIM PDMS 87.3.
 - PEFT with 9M params: LIBERO 95.4 / 96.6 / 96.0 / 84.2 (S/O/G/L) and Simpler-WidowX 54.2, vs π0 full fine-tune at 96.8 / 98.8 / 95.8 / 85.2 and 55.7.
 - Data-efficient PEFT on LIBERO (50 → 10 demos per task): Spatial 96.6 → 95.2, Object 95.4 → 94.2, Goal 95 → 93.6, Long 84.2 → 81.5, avg 92.8 → 91.1.
 - Cloth folding: ~100% success, 33 folds/hour. π0-base fine-tuned (60 h on 4×A100) and ACT from scratch (~1M steps, 8×A100) "failed to match the throughput" (no numbers).
 - Real WidowX: beats baselines on all 5 generalization tasks (figure only).
 - Inference latency and memory are NOT reported.
Ablations:
 - Ablation path (Table 1; pretraining validation L1 error / Simpler-WidowX adaptation success):
   - Florence-base + DiT with no pretraining: 4.1
   - + custom (lower) LR for VLM and prompts: 39.6
   - + naive heterogeneous pretraining: 25.0 (−14.6, pretraining HURT)
   - + aligned actions / intention downsampling / balanced shuffling: 0.077 / 50.0
   - DiT → plain transformer encoder: 0.071 / 47.9
   - + encoding pipeline (wrist view kept out of the VLM): 0.053 / 64.6
   - + soft prompts: 0.041 / 73.8
   - + scaling to 0.9B: 0.032 / 89.6
   - + two-step adaptation: 95.8
 - Backbone validation error: DiT 0.077, MM-DiT 0.140, π0-style 0.056, X-VLA 0.041.
 - Scaling in model size, data diversity and data volume keeps improving validation error with no saturation at 0.9B / 290K (figure).
 - Soft prompts vs HPT-style projection vs language prompts: soft prompts have the most stable training curves (figure).
 - Multi-domain joint fine-tuning ≈ single-domain: Libero-Long 97.6 vs 98.1, WidowX 96.0 vs 93.8, CALVIN 4.42 vs 4.32.
 - Failed alternatives: domain-specific LoRA adapters (unstable) and embodiment-routed MoE (router collapse).
Failure/limitations: authors cite modest scale, weak supervision from low-dimensional actions, and that per-embodiment adaptation is still required. Critical read:
 - Real results are mostly figure-only.
 - No latency figures are given for a 0.9B flow model with multi-view encoders.
 - It relies on absolute-EEF actions, so SO-101 would need a calibrated FK/IK. Only Simpler-Google switched to relative xyz, "due to sensitivity of absolute parameterizations to domain shifts in perception", which is an admission relevant to camera shift.
 - Pretraining data has no SO-100/101.
 - The cloth result used 1,200 DAgger demos (not our regime).
Conflicts:
 - Naive heterogeneous pretraining hurting (−14.6) agrees with FLOWER (cross-action-space pretraining < scratch on Aloha) and explains why SmolVLA pretrains only on same-embodiment SO-100 data.
 - Keeping the wrist view out of the VLM (+16.7) is the opposite of SmolVLA, which feeds all views to the VLM.
 - Flow head with plain self-attention agrees with SmolVLA/FLOWER that generative heads are preferred in pretraining.
 - The 10-demo PEFT result (91.1) is strong evidence for fine-tuning pretrained VLAs in low-data settings, but only in sim.
Relevance:
 - 9M-parameter LoRA plus a frozen 0.9B bf16 backbone (~1.8 GB) is the most 8 GB-friendly fine-tuning recipe in this batch (inferred; VRAM not reported).
 - The wrist-view-to-vision-encoder-only design and the lower LR for pretrained modules are cheap, transferable tricks.
 - Actions must be converted to absolute EEF (SO-101 URDF FK) to benefit from pretraining. This is an extra error source with Feetech backlash.
 - Inference speed on a laptop GPU is unknown.
Decision impact:
 - Q13 data/pretraining: supports pretrained-VLA fine-tuning with 10–50 demos (PEFT 91.1 at 10 demos/task) — M (sim).
 - Q13 pretraining: weakens naive cross-embodiment pretraining without heterogeneity handling (−14.6) — M.
 - Q11 cameras: supports routing the wrist view to a separate vision encoder rather than through the VLM (+16.7 adaptation) — M (single ablation path, sim).
 - Q02 action space: X-VLA pretrains on absolute EEF but switches to relative xyz under camera change — L/M.
 - Q12 model size: supports ~0.9B with scaling still unsaturated; LoRA 9M ≈ π0 full fine-tune — M.
 - Q05 augmentation: ColorJitter in pre- and fine-training, plus RandomResizeCrop for the camera-shifted benchmark — L (not ablated).
