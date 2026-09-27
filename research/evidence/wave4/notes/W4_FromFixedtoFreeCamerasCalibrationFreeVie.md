# W4_FromFixedtoFreeCamerasCalibrationFreeVie — From Fixed to Free Cameras: Calibration-Free View-Robust Vision-Language-Action Model (CamVLA) (2026, arXiv 2607.05396)
Setup: π0 (3.2B) and GR00T N1.7 backbones; single third-person RGB 224×224, NO wrist cam (deliberately excluded). Action = delta EE pose expressed in the CAMERA frame + a 3-layer MLP "geometric head" on image-encoder features regressing the 6-DoF hand-eye matrix (MSE, λ=0.1, GT extrinsics only as training labels); base action = R·Δp_c, R·Δr_c (translation of extrinsics cancels for delta actions). Sim: RLBench 6 tasks, front camera orbited −90°..90°; train on 15° grid, test on unseen 5° grid; 100 demos per task per view; 50 episodes. Real: Franka FR3, 5 calibrated D435i training viewpoints, 100 demos/task/view (!), 5 tasks, 20 episodes per task/offset on 3 test cams rotated 0/5/10/15°. 30 Hz collected, trained/run at 10 Hz, execute 20 steps per inference. Latency 61→62 ms on RTX 4090. Training 8×H100.
Claim: predicting actions in the camera frame plus self-estimated extrinsics makes VLAs robust to uncalibrated camera shifts.
Evidence:
 - Motivation (Fig. 1): π0 trained on one view on RLBench: 65.3% at train view → 6.3% at 15° rotation.
 - RLBench unseen views (Table 1, mean): π0 33.2 → +CamVLA 51.4; GR00T 28.4 → 38.4.
 - Real (Table 2, mean over 5 tasks × 3 cams; 0°/5°/10°/15°): π0 63.3/53.3/39.3/16.0 vs π0+CamVLA 79.0/68.0/55.3/29.3; GR00T 64.7/52.0/35.7/14.7 vs +CamVLA 80.7/72.3/53.0/33.0. NOTE: baseline trained with 5 views × 100 demos still collapses by 15°.
 - Hand-eye error real: 0° 1.35 cm/2.49°, 10° 7.91 cm/5.98°, 15° 27.2 cm/9.39°.
Ablations:
 - Training view density (sim): 15° interval π0 33.2 / CamVLA 51.4 / GT-extrinsics 52.3; 30° 25.5/34.0/40.0; 45° 16.8/21.2/26.3 → view coverage in training dominates; even GT extrinsics degrade with sparse views (visual representation shift is the main cause).
 - Action frame (Table 7): base-frame action 33.2 vs camera-frame action 51.4–52.3 (GT or predicted extrinsics nearly identical).
 - Rotation noise injected into extrinsics: 64.0 (0°) → 63.3 (1°) → 58.7 (5°); still ≥ π0 baseline (36.0) up to ~12°.
 - Geometric head features: image encoder (51.4) vs VLM backbone (53.5, but unstable pose), detached gradients hurt (42.6 / 20.9).
Failure/limitations: needs multi-view training data with calibrated extrinsics (5 views × 100 demos/task in real — far more than our budget); only ±15° real; single third-person cam, no wrist; objects at FOV boundary fail; π0-scale model.
Conflicts: Agrees with E0 (spherical warp aug) and others that fixed-view policies collapse under small camera rotations. Unlike augmentation approaches, needs extrinsics labels and multi-view data. Suggests the wrist cam (which they excluded) is itself an important robustness source — other papers (e.g. MResT, wrist-cam studies) show wrist views are invariant to scene-camera shifts.
Relevance: Our SO-101 uses joint-position actions (no EE frame). Direct application limited; but key facts: (1) a ~10–15° camera rotation can drop a strong VLA from 63% to 16% even with 5-view training; (2) keep the camera physically fixed/re-registered (fiducial/jig) — cheapest fix; (3) if EE-delta actions were used, camera-frame deltas help. Our wrist cam provides a view-invariant channel and should be kept.
Decision impact:
 - Q14 robustness (camera shift): real π0 63.3→16.0 at 15° despite 5-view training; CamVLA 79.0→29.3 — H for "camera shift is catastrophic", M for the fix
 - Q02 action space: camera-frame delta EE actions beat base-frame deltas under view shift (51.4 vs 33.2 sim) — L/M (sim; requires EE control + extrinsics)
 - Q11 cameras: training view density strongly determines novel-view success (15°:33→51, 45°:17→21); multi-view training alone insufficient — M
 - Q13 data: 5 views × 100 demos/task still brittle beyond 10° → data diversity in camera pose is expensive; prefer physical fixture + augmentation — L
