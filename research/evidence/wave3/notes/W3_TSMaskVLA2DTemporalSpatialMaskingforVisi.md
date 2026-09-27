# W3_TSMaskVLA2DTemporalSpatialMaskingforVisi — TS-Mask VLA: 2D Temporal–Spatial Masking for Vision-Language-Action Model with Effective Bridging (2026, arXiv 2607.09818)
Setup: 0.5B VLM backbone (LoRA-finetuned) + discrete (masked) diffusion action expert over discretized action tokens, "Bridge Attention" conditioning on multiple VLM layers, 2D (time x action-dim) masking, step-unroll loss; chunk length 8; trained on a single RTX 4090. LIBERO 4 suites, CALVIN ABC→D. Real: UR5e + Robotiq, front RealSense D435i + wrist D435i (RGB), 3 tasks (place apple, pull tissue, flip pan), 20 trials/task; demo count not stated in extracted text.
Claim: Multi-layer bridging + 2D temporal–spatial masking makes a 0.5B discrete-diffusion VLA match/exceed 3–7B VLAs.
Evidence: LIBERO avg 95.7 (vs pi0 +1.5, FlowVLA +7.6); CALVIN avg len 4.19 (OpenVLA-OFT 4.10, Seer 3.98, MoDE 4.01). Real: figure only, qualitative: TS-Mask > pi0 and OpenVLA-OFT on all 3 tasks, average success values in the ~0.5–0.7 range (bar values not reliably attributable).
Ablations:
 - 1D vs 2D masking (LIBERO Spatial/Object/Goal/Long): 94.6/98.4/95.2/85.0 vs 95.4/99.4/96.2/91.6 (Long +6.6).
 - Step-unroll strength (LIBERO-Spatial): none 90.8, λ=0.5 95.4, λ=1.0 91.5.
Failure/limitations: single-seed benchmark numbers, baselines imported; real results figure-only, no robustness split (authors claim position/background shifts without numbers); discrete tokenization of actions.
Conflicts: Discrete-token action heads performing well at 0.5B conflicts with HiFlow's finding that continuous flow beats VQ tokens — difference: masked/discrete diffusion with parallel decoding vs AR VQ; both are sim-dominant claims.
Relevance: Marginal. Shows a 0.5B VLA trainable on a single 24 GB GPU (LoRA) — still heavy for an 8 GB laptop at inference. No evidence on our robustness axes.
Decision impact:
 - Q01 action head: masked discrete diffusion with structured (2D) masking competitive on LIBERO/CALVIN; 2D vs 1D masking +6.6 on Long — weak support that discrete heads can work — confidence L (sim, single seed).
 - Q12 model size: 0.5B VLA ≥ 7B VLAs on LIBERO/CALVIN — supports smaller backbones — confidence L.
