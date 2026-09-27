# W3_ActionMapRobotPolicyLearningviaVoxelActi — ActionMap: Robot Policy Learning via Voxel Action Heatmap (2026, arXiv 2606.06904)
Setup: Drop-in action head for VLAs: OpenVLA-OFT (Prismatic-7B, LoRA r=32) and pi0.5. LIBERO 4 suites (500 episodes/suite, seed 7) + real Franka FR3, 3 tasks (Pick 225 demos, Sweep 200, Insert 275; plus 50-demo subsets), front + wrist cams, 10 trials/cell (5 seen, 5 unseen object locations). Delta (per-step velocity) EE action grids: translation 48x48x24 (real 48^3), rotation Euler 24^3 (real 16^3), gripper 2 bins; chunked (T slots). Training on 2xH200, 10k steps (LIBERO), 4k steps real.
Claim: replacing point-estimate heads (L1 regression / flow matching) with a factored voxel-heatmap classification head trained with Gaussian-blob soft labels (cross-entropy) and decoded by top-k soft-argmax improves success, precision and low-data efficiency.
Evidence:
 - LIBERO avg, matched 10k steps: OFT L1 89.1% -> heatmap 97.3% (Long 67.2 -> 94.5 / 93.8 depending on decoder). pi0.5 flow 96.9% -> 98.5% at 30k steps (Long +4.8).
 - Real Franka (OFT backbone), full data: pooled 20/30 vs 7/30. Per task (figure bars): Pick 8/10 vs 5/10 (full), Sweep 7/10 vs 3/10-ish, Insert 5/10 vs 0/10; 50 demos: pooled 14/30 vs 4/30, Insert 0/10 both. (bar-to-task mapping partially read from figure text; pooled numbers are stated in text.)
 - Grasp position error on Pick: heatmap 4.8 mm (full) / 15.0 mm (50 demos) vs L1 16.7 / 35.5 mm (2-3x tighter).
 - LIBERO-Spatial data fractions (OFT): 10% (43 demos) heatmap 93.2% vs L1 67.2%; on pi0.5 both >92% at all fractions, heatmap small lead.
Ablations:
 - Decoder (11 variants: hard argmax, soft-argmax temps, top-k, means): 4-suite avg spread 0.75%, Long spread 3.2% -> insensitive.
 - Grid resolution (3 levels) x blob sigma (0.05-0.20): all within 6.4% band; mid grid + sigma 0.10 best; both coarser and finer grids worse.
 - Convergence: heatmap loss plateaus by ~2k steps at 10% data while L1 still decreasing at 10k.
Failure/limitations: grid size grows polynomially with resolution; only delta-action grids tested; Euler-angle grid. Critical read: gain over flow matching (pi0.5) is small (+1.6 on saturated LIBERO); real-world only vs L1 head, 10 trials/cell, huge 7B backbone; the pi0.5 real comparison is in a truncated appendix (not read). Baseline OFT at 10k steps is under-trained relative to its published 50-150k steps, which inflates the L1 gap. No lighting/camera shift tests.
Conflicts: Agrees with ACT (plain L1 regression of human data is weak) and with PerAct/RVT heatmap literature; conflicts with OpenVLA-OFT's claim that L1 regression is sufficient — the gap appears mainly at low data / few steps, which is our regime. Versus flow matching the advantage is marginal, so it does not overturn diffusion/flow heads.
Relevance: For 50-100 demos, precision grasp of a pumpkin: evidence that a distributional head (any non-point-estimate) beats L1 regression at 50 demos (14/30 vs 4/30) on real robot. The head is a cheap MLP, compatible with small models and 8 GB GPU, and single-pass (no iterative denoising latency) — attractive for latency. But heavy backbone in their tests; 3D voxel grid over joint space for 6-DoF SO-101 would need a factorization (per-joint 1D bins more natural).
Decision impact:
 - Q01 action head: weakens plain L1/MSE regression; supports distributional heads (heatmap/discretized soft-label classification, flow) — confidence M (real robot but 10 trials/cell, 7B backbone, under-trained baseline).
 - Q01 action head: heatmap vs flow matching ~ roughly tie (+1.6 on LIBERO) — L.
 - Q13 data quantity: 50 demos insufficient for a two-stage precision insert for either head (0/10); pick works at 50 with good head — M.
 - Q10 latency: single-pass classification head avoids flow/diffusion iterative steps with similar accuracy — L (not measured).
