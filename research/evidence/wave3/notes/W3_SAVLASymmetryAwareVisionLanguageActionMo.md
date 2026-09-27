# W3_SAVLASymmetryAwareVisionLanguageActionMo — SAVLA: Symmetry-Aware Vision-Language-Action Models for Robotic Manipulation (2026, arXiv 2609.16641)
Setup: built on GR00T N1.5 (SigLIP2 + Qwen3-1.7B, FROZEN backbone, layer-12 features); action head trained from scratch: SO(3)-equivariant flow-matching transformer (16 blocks, width 256, horizon 16, K=4 Euler steps, 103.3M params) vs budget-matched GR00T head (100.8M). Inputs: third-person + wrist image, proprio, language. Canonicalizer: 0.09M-param CNN picking among 8 rotations + table-plane homography warp. LIBERO 4 suites (500 eps × 3 seeds); rotation OOD ±30° (13 angles × 200 eps). REAL: SO-101 arm (our robot!), third-person + wrist cam, 3 tasks (pick-place, block stacking, block sorting), 50 demos/task, multitask training 40K steps bs16, 20 episodes/task.
Claim: equivariant flow head + canonicalization on a frozen VLM gives rotation robustness and data efficiency that augmentation doesn't match.
Evidence:
 - LIBERO avg: GR00T head 86.5 → SAVLA 91.6 (Long 66.7 → 79.3).
 - Rotation OOD mean over 13 angles (GR00T → SAVLA): Spatial 40.5→81.8, Object 26.0→53.9, Goal 41.5→90.4, Long 22.7→25.4.
 - Real SO-101 (50 demos/task, 20 eps): pick-place 70→75, stacking 60→70, sorting 55→70; avg 61.7→71.7. Real rotated scene ±10–30°: avg 47.9→57.1.
Ablations (LIBERO-Goal rotation mean):
 - rotation augmentation for baseline: none 41.5; homography-warped aug 69.1; re-rendered true-view aug 74.5; SAVLA (no aug) 90.4. Extrapolation ±35/45°: 1.9 / 24.0 / 59.2 / 64.5.
 - GR00T + canonicalizer 63.5; SAVLA w/o canonicalizer 46.0 → both components needed.
 - Oracle: GT angle 90.9; true canonical view 97.3 → remaining error from image warp approximation.
 - Data efficiency (avg 4 suites) 10%/25%/100% data: GR00T 48.3/66.1/86.5 vs SAVLA 57.1/71.9/91.6.
Failure/limitations: only gravity-axis rotation; canonicalizer uses known camera intrinsics/table plane; real eval small (20 eps, ±~10 pt CI), real rotation experiment protocol unclear. GR00T N1.5 3B backbone frozen — inference fits a bigger GPU; no latency reported.
Conflicts: Supports the frozen-pretrained-VLM + trained-from-scratch flow head recipe (like GR00T/SmolVLA). Warped-image rotation aug gives +27.6 pts — agrees with RoVi-Aug that geometric image aug helps camera/scene pose robustness, but here architecture > aug.
Relevance: Directly on SO-101 with 50 demos/task + scene + wrist cam: a frozen VLM backbone + ~100M flow head reaches 60–72% on simple pick/place/stack — a realistic baseline expectation for our pumpkin task with a GR00T-class model. Homography-warp augmentation (cheap, uses known table plane) is a practical way to get viewpoint/rotation robustness (+27.6 pts in sim).
Decision impact:
 - Q01 action head: flow-matching head, equivariant variant +10 pts real SO-101 (61.7→71.7, 20 eps) — confidence L/M (small real eval).
 - Q03 vision encoder: frozen pretrained VLM backbone works on SO-101 with 50 demos/task — confidence M.
 - Q05 augmentation: homography warp rotation aug 41.5→69.1 (re-rendered 74.5) under scene rotation — confidence M (sim).
 - Q13 data: symmetry prior's advantage grows at low data (+8.8 at 10%) — confidence M (sim).
 - Q12 model size: ~100M trainable head on frozen 3B backbone sufficient for 50-demo SO-101 tasks — confidence L.
 - Q14 robustness: scene rotation ±30° halves baseline success (86→41) — confidence M.
