# W3_RevisitingEnergyBasedModelsasPoliciesRan — Revisiting Energy Based Models as Policies: Ranking Noise Contrastive Estimation and Interpolating Energy Models (2023, arXiv 2309.05803)
Setup: sim only — 2D toy densities, path planning, Push-T (136 human demos, Chi et al. data), ResNet+spatial-softmax encoder + transformer, all models capped at ~3.3M params, Npred=16 / execute 8, 2-frame context; eval 256 seeds × 32 rollouts. No real robot.
Claim: EBMs trained with ranking NCE + learnable negative sampler + interpolation (I-R-NCE) match/beat diffusion; IBC's InfoNCE objective is biased (explains IBC failures).
Evidence: Push-T score: I-R-NCE 0.884±0.005; I-R-NCE(2-stage) 0.880; NF 0.866; Diffusion 0.864; Diffusion-ϕ 0.860; R-NCE 0.824. Path planning: drawing ℓ=48 samples/step and picking highest likelihood vs ℓ=1 cuts collision/cost substantially for all models (e.g. one model cost 0.220→0.500 when going to ℓ=1).
Ablations: interpolation (I-R-NCE vs R-NCE) 0.824→0.884; sampling multiple candidates + ranking helps all generative models. Notes ~3.3M-param policies suffice for Push-T (orders of magnitude smaller than DP).
Failure/limitations: sim only, differences between generative heads on Push-T are ~2 points; EBM training complex (3 components, NF sampler prone to posterior collapse). Argues CVAE cannot rank samples (ELBO not a valid ranking score).
Conflicts/Relevance: Agrees with DP paper that IBC underperforms; gives no reason for us to adopt EBMs over flow/diffusion (marginal gain, much more complexity). Small-model sufficiency on Push-T mildly supports small heads.
Decision impact:
 - Q01 action head: EBM(I-R-NCE) ≈ diffusion ≈ NF (0.86–0.88), IBC-style EBM weakened — confidence L (sim, one task, tiny gaps).
