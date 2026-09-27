# SPA — 3D Spatial-Awareness Enables Effective Embodied Representation (2024, arXiv 2410.08208)
Setup: largest frozen-representation benchmark: 268 tasks, 8 simulators (VC-1 suite, Meta-World, LIBERO, RLBench, etc.), single- and multi-task BC; 9+ encoders at ViT-L (MoCoV3, MAE, DINOv2, CLIP, EVA, InternViT-6B, MVP, VC-1, R3M-style), plus ViT-B comparisons. SPA = ViT pre-trained with multi-view differentiable neural rendering (color + depth + semantic). Real: Koch low-cost arm (LeRobot-family), 50 demos/task, FROZEN encoders, 25 rollouts/task.
Findings:
 - SPA best/second-best on 11/13 benchmarks; top-3 on 65.5% of tasks vs MAE 46.8%, VC-1 46.0%.
 - Vision-SOTA ≠ embodied-SOTA: DINOv2 WORSE than MoCoV3 and MAE despite 10× data (frozen eval). MAE strong (reconstruction → 2D spatial awareness).
 - Multimodal (CLIP/SigLIP-style) generally POOR for embodied control, except EVA (CLIP+MAE).
 - Human-interaction data (MVP, VC-1) no advantage over ImageNet MAE → diversity/convergence matter more.
 - Embodied performance correlates with zero-shot camera-pose estimation ability (3D awareness).
 - Real low-cost arm, frozen encoders, 50 demos: SPA consistently best (numbers in Table 8).
Limitations: frozen evaluation only (the DP paper shows fine-tuning changes rankings/levels); sims dominate; no lighting/appearance-shift test.
Conflicts: challenges my "DINOv2" pick. With frozen features DINOv2 is mid-pack; MAE/SPA better. Fine-tuned regime (DP paper) differs.
Relevance: SPA-B/L weights are public; real test on a Koch arm (same family as SO-101) with 50 demos. If we keep a pretrained ViT, prefer SPA or MAE-family init over DINOv2/SigLIP; and fine-tune at low LR (DP).
Decision impact:
 - vision init: SPA-B or MAE-B over DINOv2-S / SigLIP — SUPPORTED (frozen) — M; still fine-tune at low LR — M.
