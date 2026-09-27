# W4_UADUnsupervisedAffordanceDistillationfor — UAD: Unsupervised Affordance Distillation for Generalization in Robotic Manipulation (2025, Stanford; arXiv id not in text)
Setup: affordance model = frozen DINOv2 + language-FiLM decoder trained on VLM-auto-labeled renders of 3D objects; used as observation channel for an RVT-style keyframe multi-view transformer policy (RGB-D point coords + affordance map, 6-DoF EE keyframes + gripper). Sim OmniGibson 3 tasks (pour, open, insert), 10 scripted demos/task, 15 trials per task×generalization setting. Real Franka, 2 Orbbec RGB-D side cams, 3 tasks, 10 kinesthetic demos/task, 10 trials/task; A40 training 8–16 h at batch 3; random-crop aug.
Claim: task-conditioned affordance maps as the policy's visual input yield generalization to new instances/categories/instructions from 10 demos.
Evidence: Sim comparisons vs vanilla RGB, DINOv2 (1×1-conv to 3 channels), CLIP similarity, Voltron — FIGURE ONLY, qualitative: UAD best across pose/instance/category/instruction settings; e.g., inserts white markers after training on black. Real: 73% average over 3 tasks (no real baseline).
Ablations: none numeric in text beyond the figure.
Failure/limitations: static-frame affordance, no motion-level generalization; single-object training renders. Critical read: keyframe policy (not closed-loop continuous control); DINOv2 baseline crippled by squeezing to 3 channels; no real baselines; numbers figure-only.
Conflicts: consistent with object-centric/attention-grounding papers (AFP, Spotlighting) that task-relevance-filtered inputs improve appearance generalization.
Relevance: low-moderate. The idea (feed a language-conditioned relevance map of "pumpkin"/"tray" as an extra channel) is aligned with our appearance-shift problem, but evidence is figure-only and on keyframe policies; not directly actionable.
Decision impact:
 - Q14 robustness: ~ task-conditioned affordance/relevance maps as input help novel instances (figure only) — L.
 - Q03 vision encoder: ~ frozen DINOv2 + light decoder as relevance prior — L.
