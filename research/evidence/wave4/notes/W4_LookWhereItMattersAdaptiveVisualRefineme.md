# W4_LookWhereItMattersAdaptiveVisualRefineme — Look Where It Matters: Adaptive Visual Refinement for Vision-Language-Action Models (AtVLA) (2026, arXiv 2608.02197)
Setup: pi0 (3B PaliGemma: SigLIP-So400m + Gemma-2B, 300M flow action expert), LoRA r=32, 224x224. Adds 4 learnable register tokens in SigLIP (trained only with action loss), plus uncertainty-gated cropping: sample K=4 action chunks, disagreement (std over translational dims of executed steps) > τ -> attention-rollout saliency -> crop re-encoded at 224 and appended to KV-cached prefix. 3-stage curriculum (20K register, 10K crop align, 40K joint). Train 8x RTX 6000 Ada; deploy RTX 4090 24 GB. Sim: LIBERO 4 suites, SimplerEnv Google robot. Real: Franka FR3 with a SINGLE third-person RealSense D435i (no wrist cam), Kitchen + Building Blocks suites (10 task categories), 20 trials each; demos per real task not stated in main text.
Claim: embodied fine-tuning creates high-norm attention artifacts in the VLA vision encoder; registers absorb them (cleaner attention), and uncertainty-gated high-res crops recover fine geometry; real SR 46.5% -> 69.0% vs pi0.
Evidence:
 - LIBERO Spatial/Object/Goal/Long: pi0 96.8/98.8/95.8/85.2 (avg 94.2); pi0+Registers 98.8/99.0/98.0/93.1; pi0+Cropping (external VLM crops) 96.5/98.2/96.7/93.3; AtVLA 99.3/99.4/98.3/96.5 (avg 98.4).
 - SimplerEnv Google PCC/MoveNear/OpenClose: pi0 88.0/80.3/56.0; +Registers 88.2/80.5/56.0; +Cropping 90.0/79.2/56.9; AtVLA 91.3/81.6/57.5.
 - Real (single view): pi0 46.5% -> AtVLA 69.0% average (abstract); per-cell table is flattened (10 columns) and I cannot reliably map columns; direction: AtVLA ≥ both single-component variants on every column, registers-only already well above pi0, Octo/OpenVLA near 0 on long-horizon columns.
 - Compute: crop triggered on ~30% of replanning steps; total ~1.4–1.6x pi0 compute (estimate from assumed per-pass costs; exact latency in appendix, truncated).
Ablations:
 - Remove learned registers from pi0+Registers at test: LIBERO 93.2/92.1/92.2/81.3, avg −4.45 (registers carry task info, not just artifact sinks).
 - Linear probes: registers give highest object-location/depth/surface-normal probe scores (>0.70) vs CLS and pooled patches.
 - Number of registers: too few (<4) can be WORSE than pi0 baseline; saturates at 4 (figure only).
 - Mixing ImageNet/CC3M for separate visual adaptation "noticeably disrupted" robot capabilities (qualitative).
 - External-VLM crops (no embodied training) help less; inaccurate crops can hurt; crop useless when object fills frame (Open/Close drawer).
Failure/limitations: LIBERO near-ceiling; real demo counts and per-task numbers unclear; 20 trials; 3B model on 4090 — K=4 action samples per replan adds cost. No lighting/camera-shift tests. Only a single third-person view — cropping is a substitute for a wrist cam; no comparison vs adding a wrist camera.
Conflicts: Agrees with ViT-registers literature (Darcet et al.). Suggests the common "fine-tune the vision encoder" practice for VLAs corrupts patch features unless capacity (registers) is added — nuance for Q03. Uses action-sample disagreement as an uncertainty signal, same idea as other ensembling/uncertainty gating works.
Relevance: Low-moderate. We have a wrist cam, which already provides close-range detail; our model will be far smaller than pi0. Transferable bits: (1) if we fine-tune a ViT encoder (e.g., DINOv2/SigLIP) end-to-end on 50–100 demos, add a few register tokens (DINOv2-reg variants exist) — cheap; (2) sample-disagreement from a flow/diffusion head is a free uncertainty signal that could gate extra computation or slow down.
Decision impact:
 - Q03 vision encoder: when fine-tuning a ViT encoder on robot data, register tokens help (LIBERO avg 94.2 -> ~97.2 registers-only; removing them −4.45) — confidence L-M (sim near ceiling + real single-view)
 - Q11 cameras: with a single third-person view, adaptive high-res crops of the interaction region substitute for missing close-range detail (real 46.5 -> 69.0) — confidence L (no wrist-cam comparison)
 - Q12 model size: 3B pi0 base, 4090 24 GB deploy — not usable on 8 GB — confidence M
 - Q10 latency: uncertainty gating keeps extra compute to ~30% of replans (1.4–1.6x) — confidence L
