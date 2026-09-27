# W4_SpotlightingTaskRelevantFeaturesObjectCe — Spotlighting Task-Relevant Features: Object-Centric Representations for Better Generalization in Robotic Manipulation (2025/26, IROS; arXiv id not in text)
Setup: FROZEN encoders + identical multi-task transformer policy (T past obs, proprio, language, MLP head). Encoders: DINOv2 ViT-B dense (196 tok), VC-1 (global), Theia (dense), R3M (global), ResNet-50 ImageNet (dense 49), SAM+DINOv2, DINOSAUR* (DINOv2 + slot attention, 10 slots, COCO) and DINOSAUR-Rob* (slots trained on BridgeV2+Fractal+DROID). Sim: MetaWorld (3 seeds × 50 rollouts; shifts: distractors, textures, lighting), LIBERO-90 (ID only). Real: Franka, 4 tasks, 50 teleop demos/task, 12 rollouts per task per generalization level (~1000 rollouts total).
Claim: slot-based object-centric representations (10 tokens) are far more robust to lighting/texture/distractor shifts than global/dense features, and benefit from robot-video pretraining.
Evidence:
 - MetaWorld generalization (Distractors / Textures / Lighting / Overall): DINOv2 0.11/0.03/0.39/0.18; VC-1 0.06/0.00/0.23/0.10; Theia 0.65/0.28/0.48/0.47; R3M 0/0/0/0; ResNet-50 0.04/0.00/0.22/0.10; DINOSAUR* 0.21/0.48/0.71/0.46; DINOSAUR-Rob* 0.46/0.36/0.65/0.49.
 - Real generalization (Distractors / Textures / Overall): DINOv2 0.06/0.08/0.07; VC-1 0.03/0.02/0.03; Theia 0.06/0.08/0.07; R3M 0/0/0; ResNet-50 0.15/0.10/0.12; DINOSAUR* 0.27/0.29/0.28; DINOSAUR-Rob* 0.37/0.44/0.41.
 - Real in-domain (text): DINOSAUR-Rob* 56%, ResNet-50 "on par", DINOSAUR* 48% (+20 over DINOv2); other per-model ID values figure only.
Ablations:
 - Slot pretraining data (MetaWorld/LIBERO/Real): BridgeV2 0.75/0.73/0.45; Fractal 0.72/0.58/0.38; DROID 0.74/0.72/0.26; mix D+B+F 0.76/0.77/0.56.
 - Slot count K (MetaWorld, trained K=10): K=4 OOD 0.34; K=10 ID 0.76; K=14–20 ID ~0.61, OOD up to 0.60 (trade-off).
 - Dense > global features for ResNet-50/DINOv2 (stated, not tabulated).
 - SAM+DINOv2 appearance-only object tokens (no position) fail to learn.
Failure/limitations: slot merging under clutter; capacity trade-off. Critical read: all encoders frozen — a fine-tuned or augmented ResNet/DINOv2 baseline would likely be much stronger OOD; real shifts are distractors & textures only (lighting only in sim); 12 rollouts per cell; no photometric-augmentation baseline.
Conflicts: DINOv2 frozen dense is brittle to texture here (0.03 MetaWorld) whereas PatchPolicy found frozen DINOv2 patches best in-distribution — both can be true (in-dist vs OOD). ImageNet ResNet surprisingly strong real ID (consistent with CLASS/ACT findings that ImageNet ResNet is a solid baseline). Agrees with AFP that task-relevance filtering is the key to distractor robustness.
Relevance: our failures (lighting, pumpkin appearance, camera) are appearance shifts where object-centric bottlenecks helped most in sim (lighting 0.39→0.71 vs DINOv2). But slot models need extra pretraining infra and 50 demos/task real gives only ~0.4 OOD. A cheaper analogue: crop/mask around detected objects, or AFP-style attention supervision.
Decision impact:
 - Q03 vision encoder: frozen global encoders (R3M, VC-1) poor; frozen dense DINOv2 brittle OOD (real 0.07); slot bottleneck on DINOv2 improves real OOD 0.07→0.28–0.41 — M (real ~1000 rollouts but frozen-only).
 - Q14 robustness: supports object-centric bottleneck for texture/lighting/distractor shift — M.
 - Q05 augmentation: ~ no augmentation baseline; gains may overlap with photometric aug — L.
 - Q13 data diversity (pretraining): mixed robot-video pretraining > any single dataset (real 0.56 vs 0.26–0.45) — L.
