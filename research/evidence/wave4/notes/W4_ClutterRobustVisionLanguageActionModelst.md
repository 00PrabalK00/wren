# W4_ClutterRobustVisionLanguageActionModelst — Clutter-Robust VLA Models through Object-Centric and Geometry Grounding (OBEYED-VLA) (2025/26, arXiv 2512.22519)
Setup: Real UR10e + Robotiq 2F-85; 2 RealSense cams (over-shoulder base + wrist), 1280x720 → 720x540 → 224x224; teleop at 10 Hz, execution 10 Hz. 8 grocery objects x 250 demos = 2000 clean single-object pick-place-into-bin demos (+600 toppled demos in appendix). Policy pi0 / pi0-FAST LoRA fine-tuned 50k it, bs128, 4xA6000. Frozen perception: YOLO11-Seg (fine-tuned on auto-labelled demos + LVIS), Qwen3-VL-8B set-of-mark grounding (2xA6000), Depth Anything v2 masked depth. Execute H=10 of predicted chunk. 100 rollouts per config (50 for background tests), 95% CI.
Claim: feeding the VLA only task-relevant objects (masked) rendered as (estimated) depth instead of raw RGB makes a policy trained on clean scenes robust to distractors, background shift, absent targets and unseen objects.
Evidence:
 - Distractors (seen objects): at 0 distractors all methods ≥80%; with more distractors pi0/pi0-FAST/pi0.5/GR00T N1.5 collapse to <10%, OBEYED >90% with 1 and ~80% with 7 (figure; "4x over strongest baseline" averaged).
 - Absent-target rejection: OBEYED ~95%; pi0.5 ≤~40%; others ~10-15%. Baselines grasp the wrong object in >75% of mismatched-instruction trials (Fig 2 heatmap): end-to-end action FT erodes language grounding.
 - Spatial ("left object"): OBEYED ~75%, >40 pts over best baseline (pi0-FAST).
 - Background shift (tablecloth, backdrop, colored papers, both): OBEYED pi0 ≥80% all conditions; baselines drop ~10-15 (papers) and further 5-15 (tablecloth); pi0.5 ~0 under color papers. Shifts in the tabletop region near the object dominate; distant backdrop change mild.
 - Unseen objects (1 target + 4 unseen distractors): OBEYED pi0-FAST best, OBEYED pi0 ~5 pts lower; pi0.5/GR00T near fail (figure).
 - Toppled objects (Table VII): upright 93.8/92.7/85.0/79.2 (0/1/4/7 distr), toppled 93.6/89.3/87.8/… (partly truncated).
Ablations (Table II, pi0; cols = 4 distractors seen / spatial / 4 distractors unseen):
 - baseline pi0 raw RGB: 5±3.9 / 20±10.3 / 11±3.7
 - single-stage object masking, RGB: 71±5.4 / 37±3.8 / 57±3.3  ← most of the gain comes from simple masking of irrelevant pixels
 - two-stage (base-view crops guide wrist matching), RGB: 83±2.0 / 70±2.5 / 70±2.6
 - single-stage + masked depth: 69±2.4 / 43±2.9 / 69±2.7
 - full (two-stage + masked depth): 85±6.9 / 73±11.4 / 78±6.7. Depth mainly helps unseen objects (+8 to +12), little on seen clutter.
 - Execution horizon H (Table VI, 10 Hz, 4 distractors): pick / pick-place: H=5 88/81; H=10 87/85; H=15 77/76; H=20 56/56. Short H truncates the release; long H overshoots/collides.
 - Runtime (Table III): seg 0.04 s, VLM grounding 0.41 s, depth 0.18 s, pi0 0.15 s, pi0-FAST 0.53 s; cycle 0.78 s (pi0) / 1.16 s; parallel 0.62/0.99 s. Rollout time with gating+parallel 29.83 s vs raw pi0 26.45 s.
Failure/limitations: depends on segmentation/VLM/depth; fails under dense clutter/occlusion (merged masks, base-view occlusion). Heavy compute (8B VLM on 2 A6000s). Only short pick-place. Critical: baseline trained on single clean object scenes – evaluation shift is extreme by design, so baseline collapse overstates typical gap; 2000 demos (20-40x our budget). Depth here is monocular estimated depth rendered as colormap, not sensor depth.
Conflicts: Agrees with BFA++ and other "remove background" results; contradicts the view that pretrained VLA backbones are inherently robust to distractors/background — end-to-end fine-tuning erodes grounding (consistent with TRI co-training study). Chunk result agrees with ACT-style ~1 s execution horizon being optimal and the dip at long open-loop horizons.
Relevance: HIGH. Our failures (new lighting, different pumpkin, background) are exactly appearance overfitting. A cheap version is feasible for us: segment pumpkin + tray + gripper (fixed task, no VLM needed – e.g. a small YOLO-seg / color seg / SAM2 track from first frame) and mask everything else, optionally feed masked RealSense depth (real depth, removes monocular estimator cost). Object masking alone gave 5→71% in clutter. Masked depth helps novel-object appearance (different-looking pumpkin). Adds 40-200 ms per step of perception on laptop; need tracking not per-frame VLM.
Decision impact:
 - Q14 robustness: object-centric masking of inputs dramatically improves distractor/background/novel-object robustness (pi0 4-distr 5→85, unseen 11→78) — confidence H (100 real trials/config, CIs).
 - Q04 depth: masked depth over masked RGB improves unseen-object generalization (70→78, 57→69) but not seen clutter — supports depth for appearance invariance — confidence M.
 - Q05 augmentation: alternative to augmentation — input-space masking removes background dependence without clutter data — supports segmentation masking/background removal — confidence M-H.
 - Q06 chunking: at 10 Hz, execute 10 steps (1 s) best: H=5 81, H=10 85, H=15 76, H=20 56 — confidence M (one setting).
 - Q08 language: end-to-end VLA FT grasps any object regardless of instruction (off-diagonal pick rate >75%) → language conditioning via VLA fine-tune is unreliable; explicit grounding needed for 2nd object — confidence H.
 - Q10 latency: perception pipeline adds ~0.5 s/step; must track/gate VLM calls — confidence M.
