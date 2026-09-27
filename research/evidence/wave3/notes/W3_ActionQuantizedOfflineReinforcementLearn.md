# W3_ActionQuantizedOfflineReinforcementLearn — Action-Quantized Offline Reinforcement Learning for Robotic Skill Learning (SAQ) (2023, arXiv 2310.11731)
Setup: SIM ONLY, low-dimensional STATE observations (no images). D4RL (locomotion, antmaze, adroit, kitchen) + Robomimic PH (lift, can, square, tool-hang, transport; 200 proficient-human demos/task, binary reward). State-conditioned VQ-VAE learns K discrete action codes per state (codebook 16–128); offline RL (CQL/IQL/BRAC) and BC run over the discrete codes. No real robot, no latency numbers.
Claim: learned state-conditioned action discretization (VQ-VAE) makes offline-RL constraints exact and improves CQL/IQL/BRAC 2–3x on narrow human-demo data.
Evidence (Robomimic PH, Table 2, success %, lift/can/square/tool-hang/transport → avg):
 - unimodal Gaussian BC (theirs): 59.5/31.7/19.3/1.9/0.3 → 22.5
 - SAQ-BC (discrete VQ codes): 90.1/66.4/45.3/3.5/3.2 → 41.7
 - Robomimic-paper BC (GMM head, tuned, checkpoint-selected): 100/95.3/78.7/17.3/29.3 → 64.1
 - IQL 24.3 → SAQ-IQL 46.9; CQL 16.8 → SAQ-CQL 42.7 (Robomimic CQL 27.2).
 - D4RL: SAQ improves averages in every domain family, largest on narrow expert/human data (adroit, kitchen, medium-expert).
Ablations:
 - State-conditioned vs unconditioned VQ (D4RL medium-replay avg): SAQ-CQL 74.5 vs 7.2; SAQ-IQL 47.1 vs 6.7; SAQ-BRAC 54.2 vs 6.6 → a state-agnostic action codebook collapses.
 - Codebook size 16/32/64/128 on hopper-expert: flat (~103–112) → insensitive.
Failure/limitations: needs good state-action coverage; unclear for online fine-tuning. Critical read: state-based sim only; their BC baseline is a deliberately weak unimodal Gaussian; SAQ-BC (41.7) is still far below the tuned GMM BC from Robomimic (64.1) → discretization beats a unimodal head but does not beat a proper multimodal continuous head.
Conflicts: consistent with the general "unimodal Gaussian/MSE head underfits multimodal human demos" story (ACT CVAE ablation, Diffusion Policy). Does not support VQ over GMM/diffusion; VQ-BeT/NAC-style discrete heads claim more, but with chunking and images.
Relevance: low. No vision, no chunking, no real robot. Only a weak data point for Q01 that multimodal/discrete heads beat unimodal regression on human teleop data (Robomimic PH is real human teleop in sim).
Decision impact:
 - Q01 action head: weakens unimodal Gaussian/MSE single-step regression; ~ for VQ discrete (beats unimodal, loses to tuned GMM) — confidence L (state-based sim, no chunking).
