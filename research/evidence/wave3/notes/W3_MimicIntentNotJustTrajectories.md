# W3_MimicIntentNotJustTrajectories — Mimic Intent, Not Just Trajectories (MINT) (2026, arXiv 2602.08602)
Setup: Action tokenizer (SDAT): 1D-CNN VAE with multi-scale residual quantization (scales e.g. [1,2,4]), trained with scale-wise DCT/spectral reconstruction so the 1-token coarsest scale = low-frequency "intent", finer scales = execution residuals; policy does next-scale autoregression (cross-entropy over codebook 512). Two policies: MINT-30M (from scratch decoder, frozen SigLIP+DINOv2 features, frozen BERT via FiLM) and MINT-4B (pi0.5 PaliGemma backbone + 300M action expert). Chunk 16 (LIBERO). Sims: LIBERO (joint multi-suite, 30k iters), CALVIN ABC->D, MetaWorld (50 demos/task), LIBERO-Plus. Real: Piper-X 6-DoF, dual RGB cams, 3 tasks x 20 demos at 10 Hz (+1 zero-shot task), 20 trials each, MINT-4B vs ACT, pi0, pi0.5*; results only as violin plots. 4xH200.
Claim: spectrally disentangled multi-scale action tokens (intent -> execution) improve success, sample efficiency and robustness; intent tokens enable one-shot transfer.
Evidence:
 - LIBERO avg (Spatial/Object/Goal/Long): from scratch — DP 72.4, SmolVLA 88.8 (93.0/94.0/91.0/77.0), MINT-30M 97.1 (98.6/99.2/97.4/93.2), L90 97.4. Pretrained — pi0.5 96.9, MINT-4B 98.3.
 - LIBERO-Plus avg (Table X): pi0 56.1, pi0-FAST 62.5, OpenVLA-OFT 71.4, pi0.5 65.0, MINT-30M 69.5, MINT-4B 80.1. Camera: pi0.5 53.0, MINT-30M 61.4, MINT-4B 72.2. Light: pi0.5 83.1, MINT-30M 92.2, MINT-4B 96.6. Background: 77.3/77.1/88.9. Robot init pose: 50.3/41.2/42.4 (MINT worse).
 - CALVIN avg len: pi0.5 4.15, MINT-4B 4.57. MetaWorld avg: DP 10.5, pi0 50.8, MINT-4B 67.2.
 - Learning efficiency (Table VII, success vs iterations): at 2k iters ACT 0.21 vs MINT-30M 0.43; at 10k ACT 0.65 vs MINT-30M 0.95.
 - One-shot transfer (Table III avg): replay 0.11, one-shot fine-tune 0.17, intent-token injection 0.77.
 - Real (figure only, qualitative): MINT-4B statistically better than ACT/pi0/pi0.5* on Place Banana and Stack Blocks; also better on unseen Stack Cups.
Ablations:
 - Reconstruction objective (CALVIN len / LIBERO-Long %): terminal time-domain 4.36/87.8; + terminal spectral 4.41/88.2; scale-wise time-domain 4.06/82.8; scale-wise spectral 4.54/93.4.
 - Action ensembling (CALVIN / LIBERO-Long): none 4.09/85.8; ACT temporal ensemble 4.32/89.2; action-similarity ensemble 4.10/90.4; intent-similarity ensemble 4.57/93.2.
 - Number of scales: (1) 2.12/42.8; (1,4) 4.06/78.4; (1,2,4) 4.46/93.6; (1,2,3,4) 4.57/92.2; (1,2,4,6,8) 4.32/88.6.
 - Chunk horizon: 8 -> 3.74/80.6; 16 -> 4.47/93.2; 32 -> 4.49/86.6; 64 -> 4.26/87.4.
Failure/limitations: sim-heavy; real results only in plots with 20 demos/task; LIBERO-Plus gains partly from bigger backbone; the robustness (light 92) for MINT-30M rests on frozen SigLIP+DINOv2 features, not on the tokenizer per se (no same-encoder continuous-head ablation on LIBERO-Plus). Robot-init-pose robustness worse than pi0.5.
Conflicts: A discrete-token head beating diffusion/flow contrasts with the common finding that continuous heads beat binned tokens (e.g., OpenVLA vs OFT). Difference: learned multi-scale VQ tokens with coarse-to-fine autoregression, not per-dim binning. Temporal ensembling helps here (+3.4 on LIBERO-Long) unlike PAINT's real-robot finding (TE slow/poor for pi0) — LIBERO sim has no latency and short chunks.
Relevance: Moderate. MINT-30M is a plausible small-model recipe for 8 GB: frozen SigLIP+DINOv2 features + ~30M decoder + FiLM language; it beat SmolVLA (450M) on LIBERO (97.1 vs 88.8) and pi0.5 on LIBERO-Plus average (69.5 vs 65.0), with strong lighting robustness (92.2). Chunk-size sweet spot 16 steps (at LIBERO 20 Hz ≈ 0.8 s). Ensembling based on chunk similarity (downweight stale chunks with different intent) is a cheap smoothing trick.
Decision impact:
 - Q01 action head: supports learned multi-scale (coarse-to-fine) discrete action tokens with spectral loss; ablation shows spectral scale-wise loss 93.4 vs 82.8 time-domain — confidence L-M (sim).
 - Q06 chunking/ensembling: chunk 16 best (8: 80.6, 32: 86.6, 64: 87.4); intent-weighted ensemble 93.2 > temporal ensemble 89.2 > none 85.8 — confidence M (sim, 2 benchmarks).
 - Q12 model size: 30M from-scratch policy on frozen encoders reached LIBERO 97.1 (> SmolVLA 88.8) and LIBERO-Plus 69.5 (> pi0.5 65.0) — confidence M (sim).
 - Q03 vision encoder: frozen SigLIP+DINOv2 concat as input to a small policy gives strong light/background robustness (92.2/77.1) — confidence L-M.
 - Q14 robustness: camera shift still the weakest axis for small model (61.4) — confidence L.
