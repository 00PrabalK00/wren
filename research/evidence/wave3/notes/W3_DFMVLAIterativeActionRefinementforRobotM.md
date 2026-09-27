# W3_DFMVLAIterativeActionRefinementforRobotM — DFM-VLA: Iterative Action Refinement for Robot Manipulation via Discrete Flow Matching (2026, arXiv 2603.26320)
Setup: unified discrete VLA initialised from UniVLA (Emu3-based, robot-video pretrained; parameter count not stated in text — multi-billion class), VQ image tokens (625/image, third-person + wrist), actions as tokens (FAST BPE or their Metric-Aligned Action Tokenizer, 2001-bin uniform grid with distance-preserving embeddings); decoding = discrete flow matching (CTMC Euler, 14 refine + 2 greedy steps) so tokens can be revised; 8x H100. Sim: CALVIN ABCD→D (1000 rollouts), LIBERO (50/task), LIBERO-Plus (7 perturbation dims). Real: AgileX bimanual (2x 6-DoF), 1 fixed + 2 wrist RGB cams, 6 tasks, 100 demos/task, 5k steps, 40 trials/task.
Claim: discrete action decoding that can revise earlier tokens (DFM) beats autoregressive and masked discrete-diffusion decoding, and matches/exceeds continuous flow VLAs.
Evidence:
 - CALVIN (Table 1): DFM-VLA 4.58 avg len vs UP-VLA 4.42, MODE 4.39, UniVLA 4.24; w/o embedding-guided velocity 4.42; w/o MAAT 4.44.
 - LIBERO avg (Table 2): 98.0 vs π0.5 96.8, OpenVLA-OFT 95.3, π0 94.2. LIBERO-Plus total: 77.8 vs π0.5 75.7, OFT 69.6, π0 53.6; light 90.8 (π0.5 97.3), background 88.6 (π0.5 94.6), camera 75.0 (π0.5 70.3, OFT 56.4, π0 13.8).
 - Real (Table 6, avg of 6 tasks, 40 trials each): π0-FAST 47.5, Dream-VLA (discrete diffusion) 57.1, π0.5 (continuous flow) 70.8, DFM w/o embed 68.3, DFM-VLA 73.3.
Ablations:
 - Decoding paradigm, same architecture (Table 4, CALVIN): AR 4.28, discrete diffusion 4.42, DFM 4.60, DFM+adaptive KV cache 4.58 at 121 tokens/s vs AR 50.2 (2.4x faster).
 - Data scale (Table 5, CALVIN): 10% data AR 1.71 / DD 2.84 / DFM 3.21; 50%: 3.01 / 3.88 / 4.03; 100%: 4.18 / 4.32 / 4.58 — iterative refinement helps most at low data.
 - Refine/greedy split (Table 3, total 16): 16/0 → 4.47 & 96.8; 15/1 → 4.49 & 97.2; 14/2 → 4.58 & 98.0; 12/4 → 4.53 & 96.4.
 - Velocity field: embedding-guided converges faster than aux head (LIBERO: figure, head 93.5 @30k vs embed 95.7 @20k).
 - LIBERO-Plus: full vs w/o embed +8.6 total; vs w/o MAAT +4.4.
Failure/limitations: no failure analysis; huge models/compute (8x H100); real baseline comparisons across different pretrained VLAs are confounded by pretraining; no latency in ms. My read: margins over π0.5 real (+2.5) are within noise of 40-trial cells.
Conflicts: supports the view that naive discrete token decoding (π0-FAST AR, masked diffusion) underperforms continuous flow in real control (47.5/57.1 vs 70.8), consistent with π0 vs π0-FAST reports; refinement closes the gap. LIBERO-Plus camera-shift: all methods much worse on camera/robot-init perturbations than on light/background — camera viewpoint is the hardest shift (agrees with LIBERO-Plus/other robustness studies).
Relevance: low-moderate for our small-model design (not deployable on 8 GB). Takeaways: (1) if we tokenise actions, use a metric-aware tokenizer and a refinable decoder; otherwise continuous flow is the safer default; (2) camera viewpoint shift is the weakest robustness axis even for strong VLAs (π0 13.8% under camera perturbation).
Decision impact:
 - Q01 action head: weakens AR/masked discrete tokens (real 47.5/57.1) vs continuous flow (70.8) or refinable discrete flow (73.3); at 10% data AR 1.71 vs DFM 3.21 — confidence M (real 240 trials/method, confounded backbones; sim matched ablation).
 - Q14 robustness: LIBERO-Plus camera perturbation is the hardest axis (π0 13.8, OFT 56.4, π0.5 70.3, DFM 75.0) vs light (85–97) — confidence M (sim benchmark, many methods).
 - Q11 cameras: evidence that 1 fixed + wrist cams per arm suffice for strong real results — confidence L (no camera ablation).
