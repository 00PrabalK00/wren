# W3_PRISMPerformerRSIMLEforSinglepassMultise — PRISM: Performer RS-IMLE for Single-pass Multisensory Imitation Learning (2026, arXiv 2602.02396)
Setup: from-scratch policy (no pretrained encoders, 44.4M params vs 91.8M UNet DP): per-timestep multisensory fusion (wrist RGB always, optional static RGB, depth, tactile, proprio, audio, text) → context tokens; Performer (FAVOR+ linear attention) generator with learned query tokens + latent z outputs a full action sequence in ONE pass; trained with batch-global rejection-sampling IMLE (K=16 candidates, Charbonnier distance, EMA-calibrated ε, small soft top-K' term). Inference: K candidates in one batch, pick by proxy (closest to current pose / last executed action), execute Ta, replan. Sim: MetaWorld 50 (NFE=1 comparisons), CALVIN (10% of env D, multisensory), Robomimic PH (200 demos, wrist RGB + proprio). Real: Unitree Go2 + D1 arm (H=8 obs, Tp=16, Ta=8, K=5), 15 and 35 demos, 50 trials/method; UR5 tabletop tasks. Latency on A100.
Claim: single-pass IMLE generator with batch-global rejection keeps multimodal coverage without iterative sampling, giving higher success, far lower jerk, and 30–50 Hz control.
Evidence:
 - MetaWorld (NFE=1 except DP): Easy/Med/Hard/VHard: PRISM 96.4/85.5/58.0/85.8; DP (10 NFE) 83.6/31.1/9.0/26.6; Flow Matching (1 NFE) 61.4/20.6/13.4/36.0; IMLE Policy 75.6/60.4/43.5/76.0; DP3 (10 NFE) 89.0/72.7/38.0/75.8; FlowPolicy 92.1/73.6/46.2/80.0.
 - CALVIN 10% data: success PRISM 65.2 vs IMLE 56.2, Flow 44.4, DP 36.4 (±s.e. 4–9); jerk 0.052 vs DP 3.783, Flow 1.148, IMLE 1.053; mode-switch rate 0.101 vs 0.515/0.586/0.276.
 - Robomimic PH avg: PRISM 0.922 vs DP (15 NFE) 0.85, Flow 0.85, IMLE 0.87; AdaFlow 0.956 slightly better (near-unimodal PH data).
 - Latency (A100): To=8,Tp=16: DP (10 NFE) 142.3 ms, Flow (5 NFE) 73.8 ms, PRISM (K=8) 15.0 ms; To=16,Tp=32: 285.7 / 147.6 / 31.2 ms.
 - Real (figure only, qualitative): +10–25% over DP/Flow/IMLE on parking, peg insertion, pick-place; 15 → 35 demos: +10% parking, +20% peg, +30% pick-place; tabletop +15–20%; 30–50 Hz sustained.
Ablations:
 - Modality dropout at eval (CALVIN, Fig. 3): full 65.2; drop wrist RGB 41.5; drop proprio 15.8; drop depth 66.2 (no loss); removing wrist RGB + proprio → near-complete failure.
 - Candidates K saturate ~16; FAVOR+ features up to m=512 help; batch-global rejection + EMA ε reduces midpoint collapse and mode switches (figures only).
 - Failure breakdown (CALVIN failures ≈34% of trials): mode-switching flicker between near-equal candidates 10–15%, high-jerk 5–10%, occlusion 8–12%.
Failure/limitations: batch-global ε sensitive to batch size/heterogeneity; no pretrained encoders (fair comparison, but hurts robustness); real results only in figures. My read: CALVIN numbers are from a custom multisensory 10% split, not standard protocol; baselines' low NFE (1-step flow) handicaps them vs their best settings; jerk comparison partly reflects candidate-selection + chunk execution rather than head type.
Conflicts: agrees with ManiFlow/consistency/1-step heads that iterative denoising is unnecessary for good control; disagrees with "flow at 1 NFE is fine" — plain 1-NFE flow collapses here (Flow Matching Policy 13.4% Hard) unless consistency-trained (ManiFlow). Depth-redundant finding agrees with several 2D-vs-depth studies when a wrist cam exists; proprio critical conflicts with papers warning of proprio shortcut/copycat (ManiFlow masks proprio) — task-dependent.
Relevance: moderate-high: small (44M) from-scratch single-pass multimodal head that runs ≤16 ms on A100 — fits 8 GB and latency goals; best-of-K with proximity-to-last-action selection is a simple chunk-boundary smoother. Wrist RGB is the single most important camera; depth adds little when wrist RGB present.
Decision impact:
 - Q01 action head: supports single-pass IMLE (or other 1-NFE multimodal heads) over DP/1-step flow: MetaWorld Hard 58.0 vs DP 9.0, Flow-1NFE 13.4 — confidence M (sim, custom baselines).
 - Q10 latency/smoothness: 15 ms vs DP 142 ms, Flow 74 ms (A100); jerk 0.05 vs 1.1–3.8; candidate selection by continuity with last action — confidence M.
 - Q11 cameras: wrist RGB most critical (drop → 65.2 to 41.5); proprio critical (→15.8) — confidence M (sim eval-time dropout, not retrained).
 - Q04 depth: depth redundant given wrist RGB (drop depth 66.2 vs 65.2) — confidence L-M.
 - Q13 data: 15 → 35 real demos gives +10–30 pts — confidence L (figure only).
 - Q12 model size: 44M-param scratch policy competitive — confidence L.
