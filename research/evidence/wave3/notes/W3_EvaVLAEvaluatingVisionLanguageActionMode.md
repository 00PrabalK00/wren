# W3_EvaVLAEvaluatingVisionLanguageActionMode — Eva-VLA: Evaluating Vision-Language-Action Models' Robustness Under Real-World Physical Variations (2025, arXiv 2509.18953)
Setup: LIBERO sim (Spatial/Object/Goal/Long), LIBERO-finetuned OpenVLA, OpenVLA-OFT, UniVLA, π0.5. Perturbations parameterized continuously and searched with CMA-ES (black-box, ~40–60 iterations): object 3D rotation (α,β,γ), point-light illumination (x,y,σ,I; no over/under-exposure), natural-image "patch" placed on the table texture (x,y). Real: AgileX Piper arm + one RealSense D435if third-person cam, 3 "put A into B" tasks, 50 clean demos each — qualitative only.
Claim: VLAs that score ~95% on LIBERO fail massively under physically plausible worst-case variations; adversarial training on found cases improves robustness.
Evidence (Table 1, avg failure rate over 4 suites; clean → random → optimized worst-case):
 - OpenVLA: clean 23.5; 3D rot 56.0 / 83.0; illumination 38.0 / 63.0; patch 33.0 / 71.0.
 - OpenVLA-OFT: clean 4.7; 3D 42.0 / 68.0; illum 26.0 / 48.0; patch 21.0 / 56.0.
 - UniVLA: clean 7.3; 3D 49.5 / 88.0; illum 12.5 / 34.5; patch 14.3 / 63.8.
 - π0.5: clean 4.0; 3D 35.0 / 86.0; illum 5.0 / 12.0; patch 12.0 / 46.0.
 - Even RANDOM (non-optimized) object rotations raise failure 30–40 points for all models; random illumination hurts OpenVLA/OFT (+14/+21) but barely π0.5 (+1).
Ablations:
 - Scaling the optimized perturbation distribution ×1 → ×10 (π0.5, Spatial): 3D failure 98 → 18; patch 75 → 17 → failures are specific configurations, not generic noise.
 - Adversarial training π0.5 (fine-tune with found worst cases): patch 45.5 → 24.3, illumination 12.3 → 6.3, 3D 85.8 → 56.8; clean failure 4.0 → 5.0.
Failure/limitations: sim only for numbers; worst-case search overstates typical deployment failure; real-robot part is qualitative (reports "unstable, jerky, oscillatory" motions under perturbation). LIBERO fine-tunes are notoriously overfit to fixed layouts.
Conflicts: agrees with the broad finding that LIBERO success does not imply robustness (LIBERO-PRO/Plus-style papers). π0.5's near-immunity to illumination vs OpenVLA's fragility suggests broader/co-trained pretraining helps photometric robustness, while object-pose/orientation change remains unsolved by any VLA → appearance robustness ≠ geometric robustness.
Relevance: our pumpkin will vary in orientation and appearance; random object rotation alone costs 30–40 points for SOTA VLAs → demos must cover object orientations. Illumination: a cheap lever (photometric aug / diverse lighting in demos). Adversarial/perturbation-augmented fine-tuning works without hurting clean performance.
Decision impact:
 - Q14 robustness: object pose/orientation shift is the most damaging variation (random rotations +30–40 pts failure for all VLAs); illumination robustness varies by model (π0.5 +1 vs OpenVLA +14) — confidence M (sim, LIBERO overfit models).
 - Q05 augmentation: training on perturbed scenes (lighting/patch/pose) cuts worst-case failure (patch 45.5→24.3, illum 12.3→6.3) at ~1-pt clean cost — confidence M (sim, one model).
 - Q13 data diversity: implies demos must span object orientations; count within a fixed layout does not buy pose robustness — confidence L (inferred).
