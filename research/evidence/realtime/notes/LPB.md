# LPB — Latent Policy Barrier: Learning Robust Visuomotor Policies by Staying In-Distribution (NeurIPS 2025, arXiv 2508.05941)
Setup: base diffusion policy trained on expert demos only; an action-conditioned latent dynamics model (frozen policy visual encoder + predictor of future latent after action chunk) trained on experts + automatically generated rollouts from intermediate policy checkpoints (no human labels). Test time: latent OOD score = distance of current latent to nearest expert-demo latents; if above threshold, gradient-steer the denoising so that predicted future latents move toward nearest expert latents (CBF-inspired "barrier"). Sim with 20% of demos: Robomimic Square/Transport/Tool Hang, Push-T; LIBERO-10 (50 demos per task). Real: UMI Cup Arrangement (pre-trained DP, wrist cam, UR5) with OOD initial poses; Belt Assembly (NIST board, ARX arm).
Claim: separate "precise imitation" (expert-only policy) from "OOD recovery" (dynamics model trained on cheap rollouts) and steer at inference.
Evidence:
 - Sim (Table 1, SR, 20% demos) Expert BC → LPB: Square 0.56 → 0.65; Transport 0.68 → 0.85; Tool Hang 0.27 → 0.39; Push-T 0.51 → 0.65; LIBERO-10 0.65 → 0.75. Mixed BC (experts+rollouts) and Filtered BC are worse or equal to Expert BC; CQL 0.0 on several.
 - Injected action noise (p up to 0.4, Transport): LPB highest SR at all noise levels (figure only).
 - Real Belt Assembly: 0.55 → 0.75. Cup Arrangement with OOD initial poses: improvement (figure only).
 - Dynamics data source (Table 2): policy rollouts 0.85/0.39 vs noisy demos 0.73/0.30 vs epsilon-greedy 0.71/0.30 (Transport/Tool Hang).
Failure/limitations: requires test-time gradient through dynamics model (latency not reported in text I found); needs many autonomous rollouts to train dynamics (easy in sim, costly on a real arm); real results limited in trial counts.
Conflicts: agrees with Rewind-IL/FAIL-Detect that distance to expert latent manifold is a meaningful OOD signal; differs in response: steer continuously instead of stop/rewind. Mixing rollouts into BC data hurts (supports keeping BC data clean).
Relevance to SO-101: conceptually attractive (a "barrier" around demo latents), but the dynamics-model + gradient steering adds training and inference cost and requires autonomous rollouts on the real arm. The cheap part — nearest-neighbour latent OOD score on the policy encoder — is reusable as a monitor.
Decision impact:
 - Latent nearest-neighbour OOD score as a trigger — SUPPORTED — M.
 - Full LPB steering on our setup — POSSIBLE later — L (cost, rollouts needed, latency unknown).
