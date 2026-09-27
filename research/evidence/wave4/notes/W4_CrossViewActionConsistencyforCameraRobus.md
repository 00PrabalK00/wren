# W4_CrossViewActionConsistencyforCameraRobus — Cross-View Action Consistency for Camera-Robust Vision-Language-Action Policies (2026, arXiv id not in text)
Setup: π0.5-style VLA (pretrained VL trunk + flow-matching action expert), single scene RGB 224×224 + language + proprio, WRIST STREAM MASKED (experimental control), H=10, 10k steps, batch 192 pairs, 6× RTX PRO 6000. Sim: 338,575 same-state pairs rerendered from 2,000 LIBERO demos (40 tasks); eval LIBERO-Plus camera track (4,797 rollouts/seed, 3 seeds). Real: RealMan RM-75 7-DoF, delta EE actions @15 Hz, 3 synchronized RealSense D435i (640×480, 15 fps) scene cams C0–C2, 70 demos/task (with domain randomization), 3 tasks, held-out cams H0–H2, 10 rollouts per task×placement (90/condition/method).
Claim: an auxiliary loss making flow-velocity predictions agree between two synchronized views of the same state yields camera-pose robustness beyond simply training on mixed-camera data, with no inference change.
Evidence:
 - LIBERO-Plus camera track (ID / Camera): nominal-only 91.1 / 16.8; naive mixed-camera SFT 78.7 / 74.7; FM-only on same pairs 93.6±0.4 / 79.8±0.8; proposed 94.2±0.8 / 87.2±0.4. Per-category C1 distance 72.7→81.9, C2 spherical 79.9→87.9, C3 rotation 87.2→90.6. Nominal-only policy on camera perturbation: C1 1.1%.
 - Real (single scene RGB, no wrist): seen cams FM 80/90 vs proposed 79/90; held-out cams 48/90 (53.3%) → 67/90 (74.4%). Battery 17→23/30, Headphone 5→14/30, Laptop 25→30/30. H2 (higher/top-down) gap largest: 11/30 → 20/30.
Ablations:
 - Remove cross-view term, same pair data: camera 87.2 → 79.8 (−7.4pp; all seeds separated; bootstrap 6.5–8.3pp).
 - Shuffled pairs in the consistency loss: camera 25.8, ID 50.8 (collapse) → needs true same-state pairs.
 - λCV 0.05 / 0.10 / 0.20 / 0.50 → 81.1 / 80.9 / 73.6 / 68.1 (exploratory regime): too strong hurts.
 - Pair-consistent vs independent spatial augmentation: 84.9 vs 80.9.
 - Restricted camera support: gains extrapolate on azimuth, distance, rotation; WORSE than FM-only at held-out 15° elevation; restricted support lowers nominal success.
 - Feature-level invariance alternatives (VGGT canonical tokens, bottleneck) failed: 15.3% camera; bottleneck 67.4 vs FM 71.4.
Failure/limitations: needs synchronized multi-camera demos (not usable with existing single-cam data); thin objects/depth ambiguity still fail (headphone 16/30 held-out failures). Critical read: wrist camera deliberately masked, so absolute robustness gains would be smaller in a normal wrist+scene setup; large VLA only; naive mixed-camera SFT surprisingly hurts ID (91.1→78.7).
Conflicts: agrees with CLASS that camera-diverse data alone gives only partial invariance and an explicit consistency objective adds more. Nominal-only VLA collapses to 16.8% under camera perturbation — consistent with our SmolVLA observation of camera-shift fragility. Feature-level invariance failing contrasts with CLASS (representation-level contrastive works for ResNet+DP) — difference: huge VLA trunk offers bypass paths.
Relevance: very relevant to our "slightly moved camera" failure. Practical recipe for us: record demos with 2 synchronized scene cams (RealSense + a cheap second cam) and add a cross-view consistency loss on the action head output (for ACT: L1 between chunk predictions from two views; for flow head: velocity agreement at same t, ε). Even simpler: the pure multi-view FM-only baseline already gets 53% held-out vs presumably near 0 single-view. And keep the wrist camera (masked here, which inflates the problem).
Decision impact:
 - Q11 cameras: supports multi-camera synchronized training for viewpoint robustness; single fixed-view training collapses (16.8%) — H for the problem, M for real transfer (90 rollouts).
 - Q09 auxiliary objectives: supports cross-view action-consistency loss (+7.4pp sim, +21pp real held-out) — M.
 - Q14 robustness (camera shift): mixed-camera data alone insufficient; action-level consistency needed; elevation extrapolation fails — M.
 - Q05 augmentation: pair-consistent augmentation > independent (84.9 vs 80.9) — L.
