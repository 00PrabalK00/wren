# W3_ActFoveaRuntimeSafeguardingforVLAPolicie — ActFovea: Runtime Safeguarding for VLA Policies via Spatiotemporal Visual-Action Consistency (2026, arXiv n/a in text)
Setup: sim only, LIBERO (Spatial/Object/Goal/10 = 40 tasks), frozen π0 checkpoint (flow matching, action chunks, prefix h_t executed then re-query), exterior + wrist views; 50 episodes/task → 2,000 episodes per method×scenario cell. Training-free runtime wrapper (foveation masks from kinematics, consistency monitor, candidate-observation bank, action-chunk verifier, safe-fail hold).
Claim: a plug-in monitor that checks consistency between images, proprioception and action chunks recovers most of the loss from visual overlays, visual delay and chunk drift without retraining.
Evidence (Table 1, averaged over 4 suites; undisturbed ~92.6–93.0):
 - Visual overlay (checker pattern blended into both cams): Base 49.3 → ActFovea 90.3 (+41.0, NRR 93.7%).
 - Visual feedback delay (both cams held 3 frames behind proprio): Base 76.2 → 86.0 (+9.8).
 - Smooth action-chunk drift: Base 83.1 → 90.1 (+7.0).
 - Frozen-observation replay: Base 3.05% success, 96.95% unprotected failure; ActFovea 100% timely safe failure (2.0 actions after detection vs 259.2 without hold).
 Table 2 (training-free baselines; Undisturbed / Drift / Delay / Overlay):
 - Base VLA 93.0 / 83.1 / 76.2 / 49.3
 - Action Clip/Smoothing 82.2 / 70.4 / 70.2 / 30.9
 - Fixed Short Horizon (replan after shorter prefix) 91.7 / 89.9 / 70.7 / 32.4
 - Timestamp-only Hold 93.1 / 84.9 / 0.0 / 48.5
 - ActFovea 93.8 / 90.1 / 86.0 / 90.3
Ablations (Table 4, gains vs disturbed base): w/o action verification: drift −1.2, delay +2.3 (vs +7.0/+9.8 full), overlay +42.8; w/o threat typing: delay +4.3, overlay −7.6; w/o recovery bank overlay −33.3; w/o candidate expansion −31.7.
Failure/limitations: sim-only; disturbances are synthetic and injected by the authors (checker overlay, exact 3-frame delay, templated drift) so the detector is tuned to known perturbation families; many hand-set constants; no real robot; no latency cost reported for the monitor itself; "safe failure" is motion suppression, not collision guarantees.
Conflicts: The finding that fixed action clipping/smoothing costs ~11 pts clean success is a cautionary counterpoint to naive post-hoc smoothing used to hide chunk-boundary jerks (cf. temporal ensembling in ACT, which helped slightly there). Shorter execution horizon helps against action drift (consistent with closed-loop re-query findings, e.g. Diffusion Policy/Bidirectional Decoding) but did not help against stale observations.
Relevance: Directly quantifies that a 3-frame observation lag (stale image vs current proprio) costs ~17 pts for a strong VLA — our async SmolVLA setup with ~2 s latency has far larger lag; supports timestamp-aligning observations and minimizing latency rather than relying on robustness. Naive output smoothing is harmful; if we smooth at chunk boundaries it must be something like RTC/inpainting that stays consistent with the policy. Overlay result is about occlusion-style corruption, not lighting shifts.
Decision impact:
 - Q10 latency/async: stale observations (3-frame lag) cost 93→76% even for π0; generic action smoothing drops clean SR 93.0→82.2 — supports minimizing obs–action lag and against naive low-pass smoothing — confidence M (large N, but sim + synthetic lag)
 - Q06 chunking/execution horizon: shorter executed prefix recovers drift (83.1→89.9) at small clean cost (93.0→91.7) — supports shorter execution horizon / more frequent re-query — confidence M
 - Q14 robustness: training-free observation repair recovers localized overlay corruption 49→90 — ~ runtime monitors as complementary safety layer — confidence L (synthetic overlay only)
