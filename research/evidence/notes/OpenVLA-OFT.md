# OpenVLA-OFT — Fine-Tuning VLAs: Optimizing Speed and Success (2025, arXiv 2502.19645)
Setup: OpenVLA 7B fine-tuned with LoRA; LIBERO 4 suites × 500 demos (filtered, delta EE actions); real ALOHA bimanual, 3 cams (top + 2 wrist), 14-D ABSOLUTE joint targets, 25 Hz, chunk K=25 executed fully open-loop before re-query; tasks with 20 / 30 / 45 / 300 demos; trained on 8×A100/H100 for 50–150K steps.
Claim: parallel decoding + action chunking + continuous actions + L1 regression (+FiLM for language) → 97.1% LIBERO, 26× throughput, beats π0, RDT-1B, DP, ACT on ALOHA.
Evidence:
 - LIBERO: PD&AC +14% over autoregressive OpenVLA; continuous +5% over discrete; L1 ≈ diffusion — authors attribute this to the HIGH-CAPACITY 7B backbone modeling the distribution ("even with simple L1").
 - ALOHA (rubric % completion): OFT+ best overall; π0 strongest baseline (better closed-loop recovery); RDT-1B follows language but ignores visual feedback (keeps pouring after missing bowl — over-reliance on proprioception); Diffusion Policy from scratch matches/exceeds RDT-1B on folding/scooping (20–45 demos) but weak on 300-demo "put X into pot"; ACT (with FiLM-EfficientNet+CLIP text) lowest, "less precise".
 - FiLM ablation: without FiLM, language following = 33% (chance) on both language tasks — wrist-camera multi-view setups create spurious visual correlations; FiLM essential.
 - Latency (A100, 3 imgs): OFT+ 77.9 Hz throughput; ACT 84M, DP 157M faster.
Failure/limitations: needs 7B model + multi-GPU training; open-loop execution of full 25-step chunks; LIBERO result on filtered (near-zero-action removed, failures removed) data.
Conflicts: L1-regression success depends on a 7B pretrained backbone and cleaned data; ACT (from scratch, human data) shows L1-without-latent collapses. So "L1 is enough" does NOT transfer to a small from-scratch/partially-pretrained policy.
Relevance: absolute joint targets used successfully on leader-follower ALOHA (like SO-101). Language via FiLM is necessary with wrist cams. Small-data (20–45 demos) from-scratch Diffusion Policy is competitive with 1B+ VLAs on folding/scooping.
Decision impact:
 - action_head (small model): L1 regression — WEAKENED for our regime — M/H.
 - language: FiLM mandatory when adding language + wrist cam — SUPPORTED strongly — H.
 - action_space: absolute joint targets work on leader/follower arms — SUPPORTED — M.
 - small-from-scratch viability: DP from scratch competitive at 20–45 demos — SUPPORTED — M.
