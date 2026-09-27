# W3_OrderedActionTokensforVisuomotorPolicyLe — Ordered Action Tokens for Visuomotor Policy Learning (OAT) (2026, arXiv 2607.21670)
Setup: Learned action tokenizer (transformer registers + FSQ + nested dropout so every token prefix decodes to a full chunk). Evaluated (a) lightweight regime: fixed 5M-param Transformer policy, autoregressive token generation, LIBERO-Long / RoboMimic / MetaWorld / RoboCasa (50 rollouts per task) + 2 real tasks (fixed-base ARX-5, ONE Logitech webcam, 10 Hz, chunk 32x7, median episode 98 steps, 20 trials each; #demos not given in extracted text); (b) VLM regime: PaliGemma2 3B / Qwen3VL 2B as AR policies or token co-training (TC) with flow-matching expert. Chunk horizon 32 at 10-20 Hz, execute half.
Claim: good action tokens need compression + total decodability + coarse-to-fine ordering; OAT satisfies all three and beats Bin/FAST/QueST as a policy interface.
Evidence (Table 5, same 5M Transformer, success %; real = /20):
 - LIBERO-Long: Bin 14.4, FAST 23.0, QueST 48.2, OAT(1/2/4/8 tokens) 11.7/39.8/46.4/56.3
 - RoboMimic: Bin 39.5, FAST 24.0, QueST 66.9, OAT8 73.1; MetaWorld: 14.5/7.1/17.9 vs OAT8 24.4; RoboCasa: 27.7/13.2/52.3 vs OAT8 54.6
 - Real P&P Ball: Bin 4/20, FAST 8/20, QueST 11/20, OAT1..8 7/11/13/16 of 20; Real Stack Cups: Bin 8/20, FAST 6/20, QueST 8/20, OAT 3/9/12/16 of 20.
 - VLM AR: best OAT16 63.7 (PaliGemma2), 56.8 (Qwen3VL); Bin poor despite near-perfect reconstruction. TC: OAT 59.0 vs QueST 59.4 vs ACodec 58.3 (PaliGemma2); OAT 62.5 best avg on Qwen3VL — i.e., TC gains are small/backbone-dependent.
Ablations:
 - Remove ordering (no nested dropout, OAT×): consistently lower, roughly at OAT2-OAT4 level (figure only).
 - Action horizon Ha 8→64 at fixed token count: success drops as Ha grows (compression); more latent tokens mitigate (figure only, LIBERO-Long).
 - Codebook size: non-monotonic, best at ~1000-2000 codes; larger vocab hurts (Table 6).
 - Grouped (power-of-two) decoding: 16→5 policy calls; post-hoc regrouping drops 79.7→66.3, matched OATpow2 80.8 (PaliGemma2 LIBERO).
Failure/limitations: No continuous baseline (diffusion/flow/L1/CVAE) in the lightweight comparison, so it only ranks tokenizers against each other — cannot say tokens beat a small flow/ACT head. Real eval: 2 tasks, 20 trials, single webcam, no distribution shift. Tokenizer adds a second training stage.
Conflicts: Consistent with FAST/VQ literature that naive binning is poor for chunked prediction; contradicts nothing directly. Absolute numbers (LIBERO-Long 56% for 5M AR) are well below published continuous small policies (e.g. DP/ACT-class results on LIBERO), hinting discrete AR is not the best choice for a small from-scratch policy — but not tested here.
Relevance: Low-moderate. Useful only if we choose a discrete/AR head; for SO-101 with 50-100 demos and 8 GB, a continuous head (ACT/flow) is simpler. Real setup (single cheap webcam, 10 Hz, 32-step chunks) resembles ours, and shows a 5M-param policy can reach 80% on real pick-place with good action representation.
Decision impact:
 - Q01 action head: if using discrete tokens, use learned ordered tokens (OAT8 16/20 vs Bin 4/20, FAST 8/20 real) — weakens naive binning/FAST for small policies — M (controlled, but no continuous baseline)
 - Q06 chunking: longer action horizon at fixed token budget reduces success; execute-half protocol at 32 steps/10 Hz — L
 - Q12 model size: 5M-param transformer reaches 16/20 on two real tasks — L
