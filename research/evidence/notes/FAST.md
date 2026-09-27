# FAST — FAST: Efficient Action Tokenization for Vision-Language-Action Models (2025, arXiv 2501.09747)
Setup: tokeniser pipeline:
 - Quantile-normalise each action dim (1st/99th → [−1,1]).
 - Per-dim DCT over the chunk, then scale-and-round (γ=10).
 - Flatten low-frequency-first, interleaving dims, then BPE (vocab 1024).
FAST+ is a universal BPE trained on ~1M 1-second chunks (joint, EE and cam-frame versions of π datasets plus DROID/Bridge/OXE/ALOHA, padded to 32 dims). Backbones: π0 (PaliGemma-3B) autoregressive, and OpenVLA-7B (modified to multi-image + 1 s chunks). Full fine-tune, no freezing. 224² images: 1 third-person + 1 wrist per arm. State is 256-bin text. LR 5e-5 constant after 1k warm-up, AdamW (0.9, 0.95), no weight decay, grad-clip 1, EMA 0.999. Decoding is greedy, except temperature 0.7 on bimanual tasks.
Tasks: LIBERO (4 suites, 40k iters), Table bussing (UR5, 20 Hz), T-shirt fold (bi-ARX, 50 Hz), grocery bagging and toast (20/50 Hz, generalist only), laundry (50 Hz), DROID zero-shot (15 Hz, 16 tasks / 44 trials in unseen scenes). DROID training: 75k success episodes, 240k iters @ batch 256 ≈ 4 days on 8×H100.
Claim: per-dim/per-timestep binning fails at high control frequency because consecutive tokens are nearly redundant. DCT+BPE compression fixes this, and π0-FAST matches diffusion π0 with up to 5× less training compute.
Evidence:
 - Tokens per 1 s chunk, naive → FAST (Table I):
   - BridgeV2 (7-D, 5 Hz): 35 → 20 (1.75×)
   - DROID (7-D, 15 Hz): 105 → 29 (3.6×)
   - Bussing (7-D, 20 Hz): 140 → 28 (5.0×)
   - Shirt fold (14-D, 50 Hz): 700 → 53 (13.2×)
   - FAST lands at ~30 tokens per arm per second regardless of frequency.
 - Toy spline task: binning MSE grows with sampling rate (25 → 800 samples per sequence) until the model just copies the first action. DCT stays low at all rates (figure only).
 - Policy success (Fig 6, mean ± 95% CI, figure only): naive binning "unable to make progress" on Bussing (20 Hz) and T-shirt (50 Hz). FAST ≥ FSQ (a learned VQ-style tokeniser), with the gap largest on dexterous high-frequency tasks. FAST+ ≈ per-dataset FAST.
 - π0-FAST vs diffusion π0, single-task (Fig 9): comparable on small datasets (LIBERO, T-shirt; <50 h). On Bussing (large), FAST reaches high performance in 3× fewer steps. On DROID, diffusion π0 "often ignores the language instructions".
 - Generalist (10k h π0 mix): π0-FAST matches π0 on 5 tasks including laundry with 5× fewer GPU-hours. It clearly beats a compute-matched π0 (Fig 15).
 - Inference: diffusion π0 < 100 ms per 1 s chunk on a 4090, vs π0-FAST ≈ 750 ms, because 30–60 tokens are decoded through the full 2B LM (vs 10 steps through a 300M expert). The authors say this did not hurt static tasks but made eval slow.
Ablations:
 - OpenVLA + FAST+ vs OpenVLA naive on T-shirt folding: large improvement (figure only). The effect is backbone-agnostic.
 - FAST without BPE: worse than FAST but better than naive. The many repeated 0-tokens dilute the signal and slow inference.
 - Flattening order: low-frequency-first across dims is chosen because it gives "more stable rollouts" (not quantified).
 - Tokeniser hyperparameters (scale, vocab) are "not very sensitive". Compression–fidelity sweeps (Fig 12): FAST is less efficient than FSQ at low fidelity but scales much better to high fidelity.
Practical data notes (DROID appendix):
 - Joint-VELOCITY + absolute-gripper action space, 15-step chunks, 8 or 15 steps executed open-loop.
 - Filtered all-zero-action idle timesteps. Random choice among the two external cams during training, no calibration, so the policy works from new viewpoints.
 - Temperature 0.7 was needed on bimanual tasks to "move out of the home position" because the data had stationary idle chunks at episode start.
Failure/limitations: slow autoregressive inference (750 ms), only static manipulators tested, and FAST was not combined with diffusion decoding. Critical read:
 - All policy results are bar charts.
 - The DROID zero-shot claim covers 44 trials across 16 tasks, with partial credit.
 - The FAST vs diffusion comparisons use a 3B backbone. At small scale with 50–100 demos there is no evidence that tokenisation beats a continuous head. On small datasets the two tie.
Conflicts:
 - Supports RTC, SmolVLA and π0 in that continuous flow heads are the practical choice for real-time use. FAST's speed advantage is TRAINING convergence, not inference.
 - VQ-BeT and other learned-VQ tokenisers vs FAST: here the analytical DCT beats learned FSQ at high fidelity.
 - The idle-frame issue matches our own data concern: SO-101 episodes start with stationary frames.
Relevance:
 - For a 10–50M continuous-head policy, FAST itself is not needed.
 - Transferable ideas: (1) At 30 fps, per-timestep targets are highly redundant. A DCT/low-frequency parameterisation of the chunk (predict the first k DCT coefficients per joint instead of H raw steps) could smooth output and is cheap. I infer this from the compression result; it is not tested with regression heads here.
 - (2) Filter idle/no-op frames at episode start, or policies learn to hover at home.
 - (3) Quantile normalisation.
 - (4) Randomising the external camera during training lets the policy transfer to new viewpoints without calibration (DROID). This is weak evidence for camera-shift robustness via multi-view training.
 - Moving from 10 to 30 fps raises redundancy: token heads suffer, while continuous chunk heads do not in principle.
Decision impact:
 - Q01 action head: weakens per-timestep binned discrete tokens at ≥20 Hz (naive binning makes no progress on 20/50 Hz tasks). FAST ≈ diffusion on small data but ~7× slower inference (750 vs ~100 ms) — H for "avoid naive binning", M for "continuous head preferred for latency".
 - Q10 latency: autoregressive token decoding 750 ms vs 10-step flow expert < 100 ms per chunk (4090) — H.
 - Q13 data: filter idle/zero-action frames. Stationary starts cause hovering (needed temperature 0.7 as a workaround) — M.
 - Q11 cameras: training on randomly one of two external views gives zero-shot operation from unseen viewpoints (DROID, qualitative + 44-trial eval) — L/M.
 - Q06 chunking: 1 s chunks for all rates. DROID 15 steps @ 15 Hz, executing 8–15 — L (not ablated).
