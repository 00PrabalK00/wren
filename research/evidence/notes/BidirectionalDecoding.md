# BidirectionalDecoding — Bidirectional Decoding: Improving Action Chunking via Guided Test-Time Sampling (ICLR 2025, arXiv 2408.17355)
Setup: test-time only, applied to Diffusion Policy (Push-T, 5 Robomimic MH tasks, Franka Kitchen; 100 episodes × 3 seeds) and to VQ-BeT (LeRobot Push-T checkpoint, with injected temporally-correlated action noise). Each step samples N=16 chunks from the strong policy plus N from a weak early checkpoint, keeping K=3. Selection loss = backward coherence (decayed L2 to the previous chosen chunk over the overlap, ρ=0.5) + forward contrast (close to the strong policy's samples, far from the weak one's). Execution is closed-loop (action horizon 1), prediction length 16. Real: Franka "deliver into a moving cup" (150 demos, 50 clean + 100 diverse; wrist + third cam 256², 10 Hz) and UR5 dynamic cup picking with the UMI checkpoint (no fine-tune); 20 episodes per condition.
Claim: chunking trades reactivity for temporal consistency. Sampling many chunks and picking the one coherent with the past and likely under a strong model gives both.
Evidence:
 - Sim DP (Fig. 6): BID +32% relative over vanilla closed-loop, and +46% when combined with EMA (temporal ensembling). EMA hurts 2/7 tasks and warm-start hurts 3/7. Per-task values are figure only.
 - VQ-BeT Push-T success (vanilla-OL / BID-OL / vanilla-CL / BID-CL): noise 0.0 → 64.0 / 66.1 / 48.9 / 54.4. Noise 1.0 → 26.9 / 31.4 / 38.3 / 45.3. Noise 1.5 → 13.0 / 16.0 / 29.5 / 31.7. Open-loop chunk execution collapses under noise; closed loop is more robust.
 - EMA closed-loop at noise 1.5: 18.4 vs vanilla 29.5, so ensembling HURTS under stochasticity.
 - Cost vs samples (A5000): N=1 49.1% at 13.2 ms. N=8 52.9% at 25.2 ms. N=16 54.2% at 25.9 ms. N=32 54.4% at 26.8 ms. That is ~2× latency.
 - Real: BID keeps a similar success rate in the dynamic setting as in the static one. On dynamic picking it is ≥2× every baseline (vanilla open/closed loop, EMA). Numbers are figure only.
Ablations:
 - Backward only 41.4 → +positive 42.8 → +negative 42.7 → full BID 43.8 (VQ-BeT closed-loop avg over noise levels).
 - Distance metric (Square / Lift / Kitchen): vanilla 0.68 / 0.12 / 0.22. L2 0.76 / 0.58 / 0.64. L1 0.76 / 0.68 / 0.70. Cosine 0.73 / 0.70 / 0.61.
 - EMA decay: best rate differs a lot per task (Fig. 13), so no universal TE setting exists.
 - Context vs horizon (Push-T DP): longer ACTION horizon helps consistently; longer observation CONTEXT helps a little, then hurts (overfitting / spurious correlations).
 - 1-D theory sim: long horizon is best in deterministic environments, h=1 is best at high noise, and a middle horizon is best in between.
Failure/limitations: authors cite compute (batch sampling) as expensive for high-frequency control on low-cost robots, and the analysis is limited to short-context policies. Critical read:
 - It needs a stochastic policy (diffusion/VQ). It is useless for deterministic L1/ACT (z=0).
 - It needs a weak checkpoint.
 - It requires re-running the full policy every control step (horizon 1), which is exactly what we cannot afford at ~2 s latency.
 - Real-robot numbers are figure only with 20 trials.
Conflicts:
 - RTC reports BID is beaten by RTC and uses ~2.3× latency. BID does not handle inference DELAY, only the choice among samples.
 - Agrees with RTC/Legato that averaging chunks (TE/EMA) can produce invalid mixes when consecutive chunks come from different modes.
 - Partly agrees with ACT's TE gain: EMA helps in low-noise tasks but is brittle.
 - Supports SmolVLA's finding that frequent re-query beats long open-loop execution.
Relevance: the useful parts for us are the diagnosis and the cheap piece. The diagnosis: our jerk at chunk boundaries is probably mode-switching between independently sampled chunks, and linear blending can make it worse. The cheap piece is backward coherence alone: sample a few chunks in one batch and pick the one closest to the currently executing chunk on the overlap. Our flow head could do this with a batch of 4–8 at modest extra cost if latency is first brought to ~100 ms. It does not solve the delay itself; RTC/Legato do.
Decision impact:
 - Q10 async/smoothness: supports coherence-based sample selection over naive blending/TE; weakens TE/EMA under stochasticity (18.4 vs 29.5) — M (sim, strong numbers; real figure-only).
 - Q06 chunking: supports long prediction horizon with frequent re-query; no single best execution horizon — M.
 - Q07 history: longer observation context can hurt (overfit) — L/M (Push-T only).
 - Q01 action head: benefits require a stochastic generative head (diffusion/flow/VQ) — M.
