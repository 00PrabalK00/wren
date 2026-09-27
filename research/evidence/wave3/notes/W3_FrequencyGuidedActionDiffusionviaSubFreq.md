# W3_FrequencyGuidedActionDiffusionviaSubFreq — Frequency-Guided Action Diffusion via Sub-Frequency Manifold Traversal (2026, arXiv 2605.27919)
Setup: plug-in to DP3 (point-cloud diffusion policy, U-Net). Train noise predictor also conditioned on a DCT low-pass cut-off f (f=f_base w.p. 0.2 else uniform, with k-f coupled sampling limiting high f at high noise); sample by interpolating eps(f_base) and eps(f_k) with linear schedules so the chunk is denoised coarse (low-freq) -> fine. 13 sim tasks (Robosuite 4, MimicGen 2, Adroit 3, DexArt 4), 3 seeds, 50 episodes, best checkpoint. Real: xArm two tasks (cup pick-place, mouse slide) vs DP3, figure only. Training/inference timing on RTX 4090.
Claim: steering diffusion through expanding sub-frequency manifolds suppresses high-frequency human-demo noise (jitter, pauses) giving smoother actions and higher success.
Evidence:
 - Robosuite+MimicGen avg: DP3 52.9, DiT-Policy 52.5, FreqPolicy 51.5, FGO 56.6 (Lift 88.7 -> 92.7, Stack 72.0 -> 79.3, Can 64.7 -> 66.0, Square 36.7 -> 36.7, 3-piece 35.3 -> 39.3, Stack3 20.0 -> 25.3; std 1–8 pts).
 - Adroit+DexArt avg: DP3 55.9, DiT 56.3, FreqPolicy 56.4, FGO 60.3.
 - Smoothness (Can approach phase): ATV x1e-3: DP3 14.83, DiT 14.84, FreqPolicy 15.25, FGO 14.76; JerkRMS: 50.87 / 51.01 / 46.91 / 40.79 (-20% vs DP3).
 - Cost (Adroit Hammer): training 0.47 GPU-h DP3 vs 0.48 FGO; inference per forward 39.49 ms DP3, 17.20 DiT, 33.49 FreqPolicy, 44.22 FGO (two eps evaluations per step).
 - Real: FGO > DP3 on both tasks (figure only, trial count not in main text).
Ablations (figure only, qualitative): p_base=0, no k-f coupled sampling, cosine schedules each lower SR on Lift/Door/Toilet; interpolation weight omega in (0,1) better than CFG-style extrapolation (omega>1).
Failure/limitations: authors: extra inference latency; occasional over-smoothing hurting precision. Critical: gains are +3–4 pts avg, often within seed std; smoothness measured on one task; the ATV barely changes (0.5%) — the gain is mostly in jerk; real results unquantified in text.
Conflicts: consistent with other smoothing/filtering work (ACG, temporal ensembling, action low-pass) that human-demo high-frequency noise transfers into jerky policies; contrasts with simpler alternatives (post-hoc low-pass filter of demos or of outputs, DCT tokenization in FAST) that were not compared.
Relevance: moderate for our jerk problem, but our jerk is mainly at chunk boundaries under async inference (inter-chunk discontinuity), which FGO does not address (it smooths within a chunk). Cheap takeaway: low-pass filtering targets in DCT space reduces within-chunk jitter from noisy SO-101 leader teleop; a simpler first step is to low-pass/smooth demo actions before training.
Decision impact:
 - Q01 action head: small support for frequency-structured diffusion (+3.7/+4.4 pts sim avg over DP3) — confidence L (sim, within-noise gains).
 - Q10 smoothness: supports spectral/low-pass structure to reduce jerk (JerkRMS 50.87 -> 40.79) at +12% inference cost; does not address chunk-boundary jumps — confidence L.
 - Q13 data quality: supports treating human-teleop high-frequency jitter as noise to be filtered — confidence L.
