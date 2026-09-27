# W4_PatchPolicyEfficientEmbodiedControlviaDe — Patch Policy: Efficient Embodied Control via Dense Visual Representations (2026, NYU; arXiv id not in text)
Setup: frozen pretrained ViT (DINOv2 ViT-S real; WebSSL/DINOv3/V-JEPA2/SigLIP2 compared in sim) → ALL patch tokens × T frames fed to a transformer policy with block-causal mask (bidirectional within frame, causal across frames); heads VQ-BeT or DP. Sim: Push-T (206 demos), LIBERO-Goal (50/task), BlockPush (1000), OGBench Cube; 100 rollouts, 3 seeds. Real: Franka, Tool Hanging (50 demos, 2 wrist cams), Pen Collection (52 demos, 2 wrist cams), Cable Insertion (101 demos, wrist+side, 2 mm tolerance); 20 trials. Policy trainable params 9–30M; total 40–52M with ViT-S.
Claim: lightweight policies consuming frozen dense patch features beat global-pooled (CLS/avg/DynaMo) features by ~40% relative and beat fine-tuned OpenVLA-OFT with ~0.7% of the parameters.
Evidence:
 - Sim (Push-T / LIBERO-Goal / BlockPush(max 2) / Cube(max 2)): DP+WebSSL CLS 0.68/0.99/0.99/0.21; DP+WebSSL AvgPool 0.79/0.98/1.34/0.21; DP+WebSSL Patch 0.80/0.98/1.65/1.73; VQ-BeT Patch 0.68/0.94/1.68/1.68; ACT (ResNet-18 patch, scratch) 0.64/0.93/0.15/0.69; OpenVLA-OFT 0.59/0.95/1.43/1.50. (Cube column parse from line-split table; ordering verified against text.)
 - Real (final stage, 20 trials; DINOv2-patch VQ-BeT / DINOv2-CLS VQ-BeT / ACT / OpenVLA-OFT): Cable fully inserted 0.70 / 0.60 / 0.35 / 0.30; Pen 3rd placed 0.85 / 0.65 / 0.65 / 0.60; Tool placed 0.90 / 0.70 / 0.85 / 0.65.
 - Zero-shot pickup of 10 unseen objects (100 trials): CAP global features 79% → patch 87%.
 - Latency (H200): VQ-BeT DINOv2 11.0 ms, VQ-BeT WebSSL(ViT-L) 21.4 ms, ACT 8.6 ms, OpenVLA-OFT 61.7 ms, DP variants ~422–452 ms (many denoising steps).
Ablations:
 - Encoder (frozen, VQ-BeT; Push-T/LIBERO/BlockPush/Cube): DINOv2 0.69/0.96/1.20/1.35; DINOv3 0.65/0.95/0.96/0.96; WebSSL 0.68/0.94/1.68/1.68; V-JEPA2 0.65/0.86/1.46/1.36; SigLIP2 0.51/0.83/0.99/1.17. DP head same ranking (SigLIP2 worst: Push-T 0.64 vs DINOv2 0.81). Ranking consistent across heads.
 - Patch compression (Push-T): 256 → 64 → 16 → 4 → 1 patches: 0.69 → 0.52 → 0.53 → 0.51 → 0.48.
 - Attention mask (Push-T/Cube): block-causal ≥ full/token-causal (DP Cube full 1.10 vs token-causal 0.11 vs block-causal 1.24).
 - Policy size (Push-T): VQ-BeT 25.6M→51.6M: 0.50→0.69; DP 22.8M→40.4M: 0.07→0.83 (bigger transformer trunk better).
Failure/limitations: frozen encoders only (no fine-tuning comparison); longer sequences raise training cost; in-distribution eval only (no lighting/camera shifts except zero-shot pickup). Critical read: real OFT baseline fine-tuned on only 50–100 demos; ACT baseline had proprio removed from CVAE encoder for "consistency" which may handicap it; 20 trials.
Conflicts: supports DINOv2 over SigLIP for control (contrasts with VLA practice of SigLIP backbones, e.g. SmolVLA); agrees with papers showing global pooling/CLS destroys spatial detail. Agrees with LPS/HoloBrain that small models can match big VLAs in-domain.
Relevance: very actionable for 8 GB: frozen DINOv2 ViT-S (~22M) patch tokens precomputed once → train a ~10–30M transformer head fast; ~11 ms inference. Caveat for our 2-camera setup: 256 patches × 2 cams × T frames is long; T=1–2 keeps it cheap. Robustness to lighting/camera not tested, but DINOv2 features are known to be more photometrically stable than scratch ResNet.
Decision impact:
 - Q03 vision encoder: supports frozen DINOv2 (or WebSSL) dense patch tokens over SigLIP2/V-JEPA2 and over scratch ResNet-18 (ACT) — M-H (sim 3 seeds ×4 envs + real 3 tasks).
 - Q03 (pooling): weakens CLS/global-avg pooling; 256→1 patch drops Push-T 0.69→0.48 — M.
 - Q12 model size: supports ~40–50M total policy beating 7.6B OFT (real cable 0.70 vs 0.30); within small range, larger trunk helps (DP 22.8M 0.07 vs 40.4M 0.83) — M.
 - Q10 latency: VQ-BeT/transformer heads 8–21 ms vs DP ~420 ms with many steps — M (prefer few-step head).
 - Q01 action head: VQ-BeT vs DP comparable on patch features — L.
