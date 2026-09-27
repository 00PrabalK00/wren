# W3_AStudyonEnhancingtheGeneralizationAbilit — A Study on Enhancing the Generalization Ability of Visuomotor Policies via Data Augmentation (2025, arXiv n/a in text)
Setup: sim RoboMimic/robosuite, 6 tasks (Stack, StackThree, Square, HammerCleanup, Threading, ThreePieceAssembly), MimicGen-style trajectory augmentation from a few human demos, plus scene randomization during DATA GENERATION (not image aug): camera pose (100 Fibonacci poses on a sphere cap), lighting colour (each RGB channel intensity 0–0.5, dim), 17 table textures, table height, 5 robot embodiments. Policy: CNN-based Diffusion Policy, 3rd-person + wrist RGB, EE-pose proprio. 50 rollouts per task/condition. Real: SO-101 + third-person RealSense D435i, PPO CNN policy trained in ManiSkill3 (Grasp Cube) zero-shot sim-to-real, inference on RTX 3050 Ti.
Claim: MimicGen-style data lacks visual/scene diversity; each randomization factor is needed to generalize along that factor; randomization aids sim-to-real on SO-101.
Evidence (Table I; baseline MimicGen-trained DP → DP trained with the matching randomization; Normal = original env):
 - Normal: Stack 1.00, StackThree .76, Square .58, HammerCleanup .96, Threading .64, ThreePiece .68.
 - Camera-pose test: .82→1.00, .48→.78, .10→.60, .06→1.00, .02→.72, .00→.62.
 - Lighting test: 1.00→.94, .50→.64, .46→.68, .92→.96, .26→.66, .22→.68.
 - Texture test: .26→.90, .16→.74, .04→.48, .20→1.00, .06→.58, .02→.80.
 - Table-height test: .96→.94, .58→.66, .42→.52, .58→.66, .10→.86, .36→.76.
 - Real SO-101 (Table III, PPO sim-to-real grasp cube): no randomization 0.28 → randomization (camera pose, lighting, object colour, table height) 0.44; trial count not given.
Ablations (Table II, 6-task avg; train with ONE factor, test under each factor):
 - Test camera: w/o .25, CPA .77, LCA .24, TTA .28, THA .16, CEA .30
 - Test lighting: w/o .56, CPA .28, LCA .76, TTA .45, THA .63, CEA .52
 - Test texture: w/o .12, CPA .08, LCA .16, TTA .75, THA .18, CEA .20
 - Test height: w/o .50, CPA .17, LCA .53, TTA .39, THA .73, CEA .56
 → Each factor mainly fixes its own axis; camera-pose-only randomization HURT lighting (.56→.28) and height (.50→.17) generalization; texture-only hurt lighting (.56→.45). Authors' "mutually reinforcing" claim is not supported by their own table except weakly for cross-embodiment/height.
Failure/limitations: authors: no real-sim alignment → large visual/dynamics gap; complex tasks don't transfer. Critical: sim-only for the BC study; real result is a different algorithm (PPO) with unknown trial count; "baseline" camera shift is from a sphere of 100 poses — much larger than our "slightly moved camera"; wrist camera present in all runs yet camera-pose baseline still collapses to 0–10% on precise tasks.
Conflicts: Agrees with the general finding that visual robustness must be covered in training distribution (e.g., "Decomposing the generalization gap" / Xie et al. 2024: camera pose and background hardest). Contradicts optimistic claims that randomizing one factor generalizes to others.
Relevance: HIGH on our failure list (lighting, camera shift, appearance) and hardware (SO-101 + RealSense). For real teleop data we cannot re-render, but the lesson maps to: collect demos under varied lighting/table cloths/camera jitter, and/or apply matching image-space augmentation for each factor; don't assume camera-pose robustness gives lighting robustness. Texture shift (0.12 avg) was the most catastrophic for the non-augmented policy — analogous to "different-looking pumpkin"/tablecloth.
Decision impact:
 - Q05 augmentation: factor-matched randomization: camera .25→.77, light .56→.76, texture .12→.75, height .50→.73 avg; cross-factor transfer weak or negative (CPA hurts light .56→.28) — supports augmenting EACH expected shift explicitly — confidence M (6 tasks × 50 rollouts, sim)
 - Q14 robustness: unaugmented DP drops Normal ~.77 avg → texture .12, camera .25 — camera and texture/appearance are the most damaging shifts — confidence M (sim)
 - Q11 cameras: even with wrist cam, third-person camera-pose shift collapses precise tasks (Square .10, Threading .02) — weakens "wrist cam alone gives viewpoint robustness" — confidence M
 - Q13 data diversity: diversity in generated data (poses/lighting) beats trajectory-only augmentation — supports diversity over count — confidence M
