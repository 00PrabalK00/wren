# W4_SLIM05BLearningActionGroundedPredictiveL — SLIM-0.5B: Learning Action-Grounded Predictive Latents for Robot Manipulation (2026, arXiv 2608.09771)
Setup: 472M trainable params: DINOv2-B/14 (86.6M, fine-tuned, lr 1e-5) on scene + wrist views at 224x224, 16-layer two-stream Mixture-of-Transformers (378M, d=768) over observation latents + continuous action tokens, frozen T5-small language via cross-attention, proprio token. Flow matching, 4 sampling steps, chunk 8 (LIBERO) / 12 (CALVIN). Stage 1 (3 epochs): JEPA-style masked trajectory prediction — inverse dynamics (flow-denoise actions given Z_t and Z_{t+H}) + forward dynamics (predict Z_{t+H} from Z_t and actions vs stop-grad EMA encoder target), λ_IDM:λ_FDM = 0.125:1. Stage 2: plain flow-matching policy (no future input). No embodied pretraining. Trained 8x H100. Sim: LIBERO (50 rollouts/task), LIBERO-Plus zero-shot (10,030 cases), CALVIN ABC->D. Real: 5 tasks (carrot to bowl, stack 3 plates, toast from toaster, stack blocks, wipe whiteboard), 150 demos/task, one multitask model, nominal + background/lighting/distractor, 10 trials per task-condition, partial-credit progress. Robot type not stated in extracted text.
Claim: a compact 0.5B policy with action-grounded latent pretraining (IDM+FDM in latent space) matches/exceeds 3–7B VLAs and WAMs at 3–6x lower latency.
Evidence:
 - LIBERO: SLIM 97.5 vs OpenVLA-OFT 97.1, pi0 94.1, RIPT-VLA 97.5.
 - LIBERO-Plus zero-shot overall: SLIM 77.45 (camera 70.73, robot 36.90, language 87.57, light 94.75, background 92.01, noise 86.07, layout 83.21); OpenVLA-OFT 69.6 (camera 56.4); pi0 69.3 (camera 61.0); RIPT-VLA 68.4. Fast-WAM/VLA-JEPA rows are flattened; not relied on.
 - CALVIN ABC->D avg length: SLIM 4.556 vs FLOWER 4.53, UnifiedVLA 4.41, DreamVLA 4.44, VPP 4.33, GR-1 3.06.
 - Latency (H100, BF16, eager, batch 1, 2 views): SLIM 60.6 ms / 4.26 GiB peak / 491 GFLOPs per chunk; pi0.5 193.1 ms / 7.94 GiB / 4715 GFLOPs; Fast-WAM 360.6 ms / 13.63 GiB / 2090 GFLOPs.
 - Real (progress score, figure): SLIM highest average under nominal, distractor and lighting; background: SLIM 49 vs pi0.5 54 vs Fast-WAM 2 (only these numbers stated in text; others figure only).
Ablations:
 - Stage 1 (masked trajectory prediction) vs Stage-2-only: consistent improvement on LIBERO-Plus and CALVIN (figure only, qualitative).
 - IDM:FDM ratio 0:1 ... 1:1 — 0.125:1 best, degrades at extremes (figure only).
 - EMA target encoder vs none: LIBERO-Plus 77.45 vs 66.82; CALVIN 4.556 vs 4.382; no-EMA collapses latent (effective rank 61.28 -> 13.95; token cosine 0.071 -> 0.352) despite lower future-latent MSE (0.166 vs 0.245).
Failure/limitations: single model scale; real results mostly figure-only with 10 trials per cell and partial credit; 150 demos/task (more than our 50–100); training on 8xH100. Stage-1 benefit on real robot not ablated. Background shift remains the hardest real OOD axis.
Conflicts: Consistent with LAWA/DynaMo/other future-prediction auxiliaries (Q09) but argues latent-space prediction beats pixel/video prediction for OOD (Fast-WAM collapses to 2 under real background shift). Contrasts with "bigger VLA is more robust": 0.47B no-embodied-pretraining model beats 3–7B pretrained VLAs on LIBERO-Plus camera shift. Fine-tuned DINOv2 (low LR) as the encoder — agrees with pro-DINOv2 findings.
Relevance: High as an architecture template: ~0.5B (could shrink the MoT) with DINOv2-B + wrist + scene cams, flow matching with 4 steps, chunk 8–12, 4.3 GiB inference memory and 60 ms on H100 (laptop 5060 perhaps ~3–5x slower -> ~200–300 ms, still far better than our 2 s). Stage-1 IDM+FDM latent pretraining on our own demos is cheap (3 epochs) and requires no extra labels. Training 0.47B on 8 GB would need LoRA/grad-checkpointing or a smaller trunk.
Decision impact:
 - Q09 auxiliary objectives: supports latent forward+inverse dynamics pre-stage with EMA target (EMA vs none 77.45 vs 66.82 LIBERO-Plus) — confidence M (sim ablations; real not ablated)
 - Q12 model size: 0.47B policy matches 3–7B VLAs on LIBERO/CALVIN and beats them on LIBERO-Plus — confidence M
 - Q10 latency: 60.6 ms vs pi0.5 193 ms vs Fast-WAM 361 ms on H100; 4.26 GiB — fits our memory budget for inference — confidence M
 - Q03 vision encoder: fine-tuned DINOv2-B/14 at low LR (1e-5) as sole encoder works — confidence L (no encoder ablation)
 - Q14 robustness: camera shift 70.7 vs pi0 61.0 / OFT 56.4 (LIBERO-Plus); real background shift still hardest (49) — confidence L-M
 - Q01 action head: flow matching with 4 steps suffices (no ablation) — confidence L
