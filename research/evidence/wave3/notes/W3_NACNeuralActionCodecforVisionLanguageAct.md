# W3_NACNeuralActionCodecforVisionLanguageAct — NAC: Neural Action Codec for Vision-Language-Action Models (2026, arXiv 2606.21372)
Setup: Action tokenizer study with a SMALL shared policy: from-scratch transformer (d=256, 4 layers, 4 heads), observation history 2, action horizon 32, execute 16 steps, 500 training demos (sim), batch 256, 50k steps, top-k=10 sampling. Tokenizers: per-dim Bin, FAST (DCT+BPE), VQ-VLA, OAT (FSQ+registers), NAC (SEANet conv encoder + 2-scale RVQ, 1024 codes, Vocos/ISTFT decoder, DAC adversarial discriminator; 12 tokens per chunk). Continuous baseline: Diffusion Policy (DDIM 10 steps) with same backbone. Sim: LIBERO-10 and RoboMimic, 8 seeds × 50 trials/task. Real: 8 tasks × 10 trials (robot model not stated in text; scenes reset with tape markers).
Claim: audio-codec-style learned tokenizer (RVQGAN) gives the best discrete action space for autoregressive policies.
Evidence (Table 2, success %: LIBERO-10 / RoboMimic / Real 8 tasks):
 - Bin 3.95 / 7.56 / 6.25
 - Diffusion Policy 25.48 / 27.25 / 22.5
 - FAST 38.02 / 28.38 / 40.0
 - VQ-VLA 10.85 / 21.44 / 31.25
 - OAT 44.17 / 31.94 / 40.0
 - NAC 49.73 / 33.94 / 50.0
 - Real per-task (Table 6) NAC vs DP: weighing 70 vs 40, grapes 90 vs 30, marker 100 vs 30, two blocks 50 vs 0, three blocks 30 vs 0, chess 0 vs 0, stone 10 vs 0, towel 40 vs 80 (DP wins deformable towel).
Ablations (LIBERO-10 success / recon MSE, Table 1):
 - Recon loss: MSE 49.2; DCT 47.85; spectrogram 48.3 (best recon 0.0002); L1 44.78; mel-spectrogram 0 → recon quality ≠ policy quality; audio-perceptual loss destroys it.
 - Discriminator: DAC 49.45, MPD 46.28, MRD 45.68, none → 0 (complete failure).
 - Decoder head: ISTFT 48.3 vs linear 42.1.
 - Tokens/chunk: NAC 12 vs Bin 224 vs FAST 36; decode latency a few ms on RTX 4090 (slower than FAST, faster than VQ-VLA).
Failure/limitations: chunk length × action dim must divide downsampling ratios; real robot unspecified; 10 trials/task. Critical read: the DP baseline is weak (25% LIBERO-10 with 500 demos is far below typical DP/ACT numbers ~ 50–90% reported elsewhere) — tiny 4-layer backbone, DDIM-10, shared hyperparams tuned for AR tokens; so "NAC > DP" is not a fair verdict on diffusion heads. Brittleness: removing the discriminator → 0% shows a fragile recipe.
Conflicts: contradicts common finding that diffusion/flow heads beat discrete tokens in small-data single-task BC (e.g., DP paper, VQ-BeT comparisons mixed). Agreement: naive per-dim binning is terrible (OpenVLA-style), FAST-style compression helps AR policies.
Relevance: moderate for Q01 only if we go autoregressive. For our 50–100 demo, 8 GB setup, the evidence that a small AR transformer over learned codes can beat a small DP on real tasks (50 vs 22.5) is notable, but the DP config is suspect and NAC adds a GAN-trained tokenizer stage (fragile). Chunk 32 / execute 16 with history 2 is a reasonable small-policy config.
Decision impact:
 - Q01 action head: supports learned-codec discrete tokens (NAC) over binning (6.25 real), FAST and VQ; reports > small DP (50 vs 22.5 real) — confidence L/M (DP baseline appears under-tuned; 10 trials/task).
 - Q01 action head: naive per-dimension binning fails (LIBERO-10 3.95%) — confidence H (consistent with literature).
 - Q06 chunking: config used horizon 32, execute 16, obs history 2 (no ablation) — confidence L.
 - Q10 latency: 12 tokens/chunk (vs 224 bin, 36 FAST) keeps AR decoding cheap; decoder ms-level on 4090 — confidence L.
