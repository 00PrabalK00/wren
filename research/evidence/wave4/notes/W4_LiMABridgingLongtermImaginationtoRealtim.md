# W4_LiMABridgingLongtermImaginationtoRealtim — LiMA: Bridging Long-term Imagination to Real-time Dexterous Manipulation via Asynchronous Diffusion (2026, arXiv 2609.28431, CoRL 2026)
Setup: Bimanual 2×UR5 + 2×22-DoF SharpaWave hands; 3 RealSense D435 (head + 2 wrist); VIVE tracker + glove teleop; 6 tasks (2 short, 4 long-horizon), 100 demos/task, 20 trials/task. Model: slow "Future Dreamer" = Cosmos-Predict2 2B video DiT (Wan2.1 VAE tokens, frozen T5-XXL) predicting multi-view future latents + coarse action; fast "Motion Refiner" = 1B DiT from scratch, initialized from dreamer intent via latent Schrödinger bridge (I2SB); dreamer refreshed every 4 refiner updates; 32-step chunk. H100 inference.
Claim: asynchronous slow-imagination / fast-refinement WAM keeps world-model foresight while cutting latency 45.8% vs Cosmos-Policy.
Evidence (Table 1, SR, 20 trials): Stack cup GR00T N1.6 85 / VPP 80 / InternVLA-A1 90 / Cosmos-Policy 80 / LiMA 90; Roll T-shirt 70/55/75/60/75; Cook rice 70/55/70/60/80; Make sandwich 65/50/65/60/70; Make coffee 55/50/50/55/60; Assemble package 50/40/50/45/50. Chunk latency (H100): 270 / 225 / 360 / 600 / 325 ms (column alignment inferred from extracted text; Cosmos 600 and LiMA 325 confirmed in prose).
Ablations:
 - Bridge (3 seeds × 20 trials): Cook Rice / Stack Cup: w/o future visual intent 61.7 / 76.7; Gaussian init + cross-attn 70.0 / 78.3; flow matching 73.3 / 83.3; I2SB bridge 78.3 / 93.3.
 - Components (SR, latency): full 80%, 0.325 s; w/o adaptive modulation 60%; w/o multi-action tokens 55% (jittery grasping); w/o fast–slow async 80% but 0.45 s.
 - Denoising steps 5/10/15/20: 65/80/85/80% at 0.23/0.325/0.43/0.51 s.
 - Slow:fast compute ratio 1:9/2:8/3:7/4:6: 50/65/80/70%.
 - OOD (Cook Rice, background/object/lighting/clutter): figure only, qualitative — LiMA higher than GR00T N1.6 and Cosmos-Policy; 70% on novel object instances.
Failure/limitations: authors: degrades under severe occlusion; latency unoptimized. Critical: 3B total params on H100 — infeasible on 8 GB laptop; gains over GR00T N1.6 are 0–10 pts at 20 trials (within noise for most tasks); asynchronous design did not improve success, only latency.
Conflicts: consistent with other WAM notes (world-model aux gives some robustness but heavy latency). Removing future visual intent costs 17 pts on Cook Rice — supports future-prediction auxiliaries for long-horizon tasks, less so for short pick-place (Stack cup LiMA ≈ baselines).
Relevance: low for direct use. Transferable ideas: (1) fast low-level policy initialized from a slower plan (bridge / warm-start denoising from previous chunk) is conceptually related to chunk-boundary smoothing; (2) more denoising steps not monotonic (20 < 15).
Decision impact:
 - Q10 latency: async slow/fast split cuts chunk latency 0.45 → 0.325 s with equal SR; but WAMs still 225–600 ms on H100 — weakens video-WAMs for laptop — confidence M.
 - Q09 aux objectives: future visual intent worth +16.6 (Cook Rice) / +16.6 (Stack Cup) pts in their architecture — L (large model, 3 seeds).
 - Q12 model size: 3B-parameter WAM ≈ GR00T on short tasks; no benefit for simple pick-place — L.
