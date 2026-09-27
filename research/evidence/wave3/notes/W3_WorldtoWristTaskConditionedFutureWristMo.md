# W3_WorldtoWristTaskConditionedFutureWristMo — World-to-Wrist: Task-Conditioned Future Wrist Modeling for Fine-Grained Robot Manipulation (W2-VLA) (2026, arXiv 2608.05369)
Setup: Qwen3-VL-4B + DiT flow-matching head (StarVLA), ~4.97B params; frozen V-JEPA 2.1 ViT-L encodes wrist history and (train-only) future wrist clips; a 4-layer predictor forecasts future wrist latents from 16 VLM "latent modeling tokens" + wrist history; Q-Former adapter feeds 32 future-aware tokens to the action head. Auxiliary structured CoT (subtask/reasoning/wrist evidence) text loss at training only. Chunk 8 (LIBERO) / 16 (RoboTwin, real). LIBERO multi-task (1,693 traj), RoboTwin 2.0 (50 demos/task, 100 trials Easy/Hard). Real: Mobile-ALOHA-style bimanual, 3 tasks x 100 teleop demos, 30 standard + 30 OOD trials (clutter, lighting, background) per task.
Claim: predicting task-conditioned future WRIST latents (not pixels, not main view) gives better fine-grained/contact manipulation, at real-time speed.
Evidence:
 - LIBERO avg 98.5 (Spatial 99.6, Object 99.8, Goal 99.2, Long 95.2) vs strongest baseline 97.2.
 - RoboTwin 2.0 Easy/Hard: W2-VLA 60.71 / 18.21 vs UP-VLA 52.92 / 15.16, StarVLA-OFT 50.38, StarVLA-GR00T 48.80, pi0 Hard 16.34.
 - Real avg success standard: W2-VLA 70.0, VLA-JEPA 54.4, pi0 41.1; OOD (clutter/light/background): W2-VLA 52.2 vs VLA-JEPA 37.8. Plug insertion OOD 33.3 vs 10.0. 16-step chunk in 183 ms on robot (87 Hz action rate).
Ablations (LIBERO avg):
 - w/o wrist predictor 97.5 (Long 95.2 -> 93.6); w/o CoT supervision 98.0; full 98.5.
 - Explicit CoT decoding at inference: 1,550–1,615 ms per chunk, 97.6–98.1% vs latent tokens 98.6–148.7 ms, 98.0–98.5% — reasoning text at inference costs >10x latency with no gain.
 - Latent tokens 4/8/16/32: 98.0/98.1/98.5/98.4.
 - Future prediction target: main view only 97.7 (102 ms), both 98.0 (133 ms), wrist only 98.5 (111 ms).
Failure/limitations: gains on LIBERO are ~1 pt on a saturated benchmark; Hard RoboTwin still only 18%; real results in figure with 30 trials; 5B model; OOD drop 70 -> 52 even for the best model.
Conflicts: Supports DSWAM/Fast-WAM line that future-prediction auxiliary losses help without inference-time imagination; and CAIP-style finding that action-proximal (wrist/hand) signals are more informative than static main view. Contrasts with papers where main-view future prediction is used (e.g., VPP/GR-2) — here wrist future is better and cheaper.
Relevance: Low-moderate (model too big). Transferable idea for a small policy: an auxiliary loss predicting future WRIST-camera features (e.g., frozen DINOv2/V-JEPA embedding of wrist frame k steps ahead) is the most useful future-prediction target; don't decode language reasoning at inference (10x latency).
Decision impact:
 - Q09 aux objectives: future wrist-latent prediction +1.0 avg / +1.6 Long on LIBERO; wrist target > main-view target (98.5 vs 97.7) — confidence L-M (sim, saturated).
 - Q11 cameras: wrist view carries the action-relevant dynamics; model built around it improves real OOD 37.8 -> 52.2 vs VLA-JEPA — confidence L-M.
 - Q10 latency: explicit CoT decoding costs ~1.5 s per chunk with no success gain — confidence M.
 - Q14 robustness: real OOD (clutter/light/background) costs ~18 pts even for best 5B model with 100 demos — confidence L-M.
