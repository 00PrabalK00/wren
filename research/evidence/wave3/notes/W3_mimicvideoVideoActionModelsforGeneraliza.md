# W3_mimicvideoVideoActionModelsforGeneraliza — mimic-video: Video-Action Models for Generalizable Robot Control Beyond VLAs (2025, arXiv 2512.15692)
Setup: Video-Action Model: Cosmos-Predict2 2B latent video DiT (LoRA-finetuned on robot video), frozen; separate flow-matching action decoder trained from scratch that cross-attends to intermediate video-model features at a chosen video flow time tau_v (tau_v=1 → one backbone pass, real-time). Baseline: pi0.5-style VLA (PaliGemma 3B + same action decoder, knowledge insulation) trained on identical data. Sim: SIMPLER-Bridge (4 tasks), LIBERO Spatial/Object/Goal (50 demos/task). Real: bimanual Panda + 16-DoF mimic hands, 1 workspace cam (+4 wrist cams for baseline variant), ~500 episodes/task, 2 tasks; DiT-Block Policy baseline (ViT-S DINO per camera + 8-block DiT, ~155M).
Claim: Conditioning the action decoder on a pretrained video model's (dynamics-aware) latents gives ~10x sample efficiency and better performance than conditioning on a VLM.
Evidence:
 - SIMPLER-Bridge avg: pi0.5-style VLA (scratch) 35.4; mimic-video 46.9; with per-task tau_v 56.3; FLOWER 45.0, ThinkAct 43.8, OpenVLA 14.6.
 - LIBERO avg: DP (scratch) 79.7; pi0.5-style 85.9; mimic-video 93.9; OpenVLA-OFT 96.9.
 - Real bimanual dexterous (Packing / Handover %): DiT-Block (workspace cam only) 11.0 / 30.0; DiT-Block + 4 wrist cams 42.6 / 74.1; mimic-video (workspace cam only) 72.0 / 93.0.
 - Sample efficiency (LIBERO, figure): mimic-video with 10% data reaches the VLA's max; 1 episode/task → 77% avg.
Ablations:
 - tau_v (how much the future video is denoised): best performance at intermediate noise; action reconstruction MSE lowest at tau_v≈0.4 and rises sharply toward full video reconstruction (tau_v=0) — full-fidelity future video is NOT needed (figure only).
 - Video vs VLM backbone with identical decoder and data: 93.9 vs 85.9 LIBERO; 46.9 vs 35.4 SIMPLER.
Failure/limitations: 2B video backbone + LoRA adaptation on 200 h of robot video; real tasks use ~500 demos; latency not quantified in text; few real tasks; trial counts for real not clear in extracted text.
Conflicts: Supports "future-prediction / world-model features help control" (Q09) at large scale, but the effect comes from a huge pretrained video model; small-scale auxiliary future-prediction losses in other papers give only small gains (e.g. ProgVLA/SAP +1–2 pts). The wrist-camera ablation of the DiT baseline agrees with most wrist-cam papers (large gain under occlusion).
Relevance: Model is not deployable on 8 GB laptop with our latency needs. Useful facts: (1) a 155M DINO ViT-S + DiT policy benefits hugely from wrist cameras in occlusion-heavy grasping (11→43%, 30→74%); (2) dynamics-aware pretrained features are more sample-efficient than VLM features — if we ever use a pretrained backbone, a video/world-model backbone is the better prior.
Decision impact:
 - Q11 cameras: adding wrist cams to a ViT-S DINO DiT policy: 11.0→42.6 and 30.0→74.1 (real) — supports wrist camera — confidence M.
 - Q09 auxiliary objectives / world models: video-model conditioning > VLM conditioning (LIBERO 93.9 vs 85.9, SIMPLER 46.9 vs 35.4, controlled) and partial (not full) future denoising is optimal — supports dynamics-aware representations, not pixel-accurate prediction — confidence M (large-scale only).
 - Q03 vision encoder: video-pretrained features > image-text VLM features for control, with same decoder — confidence M.
 - Q12 model size: n/a for 8 GB (2B backbone) — confidence L.
