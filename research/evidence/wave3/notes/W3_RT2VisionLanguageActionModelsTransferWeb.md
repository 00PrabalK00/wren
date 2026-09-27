# W3_RT2VisionLanguageActionModelsTransferWeb — RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control (2023, arXiv 2307.15818)
Setup: Everyday Robots mobile manipulators, RT-1 dataset (~130k demos, 700+ tasks), actions as 256-bin discrete text tokens (delta EE pos/rot + gripper + terminate), single camera; models RT-2-PaLI-X 5B/55B and RT-2-PaLM-E 12B, co-fine-tuned with web VQA data; served from a multi-TPU cloud: 55B at 1-3 Hz, 5B ~5 Hz. Eval: >200 seen tasks + >280 unseen-generalization tasks (objects, backgrounds, environments; easy/hard); ~6k real trials total. Language-Table sim: PaLI 3B.
Claim: VLMs fine-tuned to emit action tokens (VLA) keep in-distribution performance of RT-1 and roughly double generalization to unseen objects/backgrounds/environments, plus emergent semantic reasoning.
Evidence (numbers in main text; per-category bars are figure-only, full tables are in an appendix not present in our extraction):
 - Seen tasks: RT-2 ~ RT-1 (35M), other baselines lower.
 - Unseen objects/backgrounds/environments average: RT-2 (both variants) ~2x RT-1 and MOO, ~6x VC-1 and R3M (frozen pretrained reps feeding an RT-1 backbone).
 - Emergent skills (symbols, reasoning, humans): RT-2-PaLI-X >3x RT-1 average.
 - Language-Table sim: RT-2-PaLI-3B 90 +-10 vs LAVA 77 +-4, RT-1 74 +-13, BC-Zero 72 +-3.
Ablations (Fig 6b, figure-only, qualitative): training the 5B model from scratch -> "very poor"; fine-tuning on robot data only < co-fine-tuning with web data (both 5B and 55B); 55B > 5B on generalization.
Failure/limitations: authors: no new motor skills beyond robot data; high compute, real-time inference a bottleneck (suggest quantization/distillation). Critical read: enormous robot dataset; latency (1-5 Hz from TPU cloud) is incompatible with smooth control on our laptop; single-step tokenized actions; unseen-category gains are semantic/visual, not precision.
Conflicts: supports "pretrained VLM backbone -> better OOD visual generalization" (consistent with OpenVLA, pi0) but conflicts with small-data findings where large models overfit/are slow; frozen VC-1/R3M much worse, consistent with Decomposing-gap and MimicPlay findings. Large models from scratch fail — consistent with low-data overfitting concerns (Q12).
Relevance: explains why a VLM-based policy (our SmolVLA) is attractive for novel pumpkin appearance/background, but RT-2's own cost (5B-55B, 1-5 Hz) confirms latency is the price; the transferable lesson for us is "pretrained VLM/vision features + co-training or regularization to avoid forgetting", not the model size. Our 2 s latency with SmolVLA is in the same regime as RT-2-55B, which ran slow, quasi-static tasks.
Decision impact:
 - Q12 model size: larger pretrained VLA generalizes better (55B > 5B), but big models from scratch are very poor — supports pretrained initialization over scale-from-scratch — M (huge real eval, but figure-only numbers, huge data regime).
 - Q03 encoder: web-pretrained VLM >> frozen VC-1/R3M (~6x) for OOD objects/backgrounds — M.
 - Q14 robustness: VLM pretraining + co-fine-tuning ~2x unseen objects/backgrounds/environments vs RT-1 — M.
 - Q10 latency: 55B 1-3 Hz, 5B ~5 Hz even on cloud TPUs — large VLAs are latency-bound — M.
 - Q01/Q02: discrete 256-bin delta-EE tokens sufficient for quasi-static pick-place at 1-5 Hz — L.
