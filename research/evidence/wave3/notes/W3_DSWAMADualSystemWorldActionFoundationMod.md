# W3_DSWAMADualSystemWorldActionFoundationMod — DSWAM: A Dual-System World Action Foundation Model for Fine-Grained Robot Manipulation (2026, arXiv 2607.04927)
Setup: System 1 = WAM executor built on Wan2.2-TI2V-5B video model + flow-matching action expert, trained with action loss + future-video-latent flow loss (co-training), NO video generation at inference; pretrained on 5,000+ h real dual-arm data; optional System 2 = 4B VLM subtask planner (5 frames @1 Hz, updated every 2 s). Real: ALOHA-style dual arm, 3 cams, DeMaVLA folding protocol (shirt/skirt/pants/towel, 2 garments x 10 trials each). Sim: RoboTwin 2.0 50 tasks. Inference RTX 5090: PyTorch 198.2 ms -> TensorRT BF16 73.8 ms; async + RTC.
Claim: WAM-style (video co-trained) execution beats matched VLAs; optional subtask planner helps coarse multi-step instructions; TensorRT+async RTC make it real-time.
Evidence:
 - RoboTwin 2.0 avg clean/rand: pi0 65.92/58.40, pi0.5 82.74/76.76, DeMaVLA 88.42/86.78, Motus 88.66/87.02, Fast-WAM 91.88/91.78, DSWAM 92.38/91.90.
 - Real folding (matched data/robot, 20 trials per garment): avg SR pi0 ~76.3, DeMaVLA 92.5, DSWAM 96.3; time 2'26'' / 2'18'' / 1'44''. Pants DeMaVLA 75 -> DSWAM 90.
 - Subtask-level vs raw coarse instruction (sorting task): 75.7% SR, 3.53 mistakes/rollout -> 100%, 0.65 mistakes.
 - Sync TensorRT vs async TensorRT+RTC (easy garments, 10 trials): shirt 100/100% (1'47'' -> 1'28''), pants 70 -> 100% (1'50'' -> 1'08'').
Ablations: no ablation of video co-training weight (the key WAM claim rests on comparison with a different model, DeMaVLA, with matched data); async+RTC vs sync (above); subtask supervision (above).
Failure/limitations: 5B+ model, 5,000 h pretraining; 10–20 trials per cell; WAM-vs-VLA comparison changes the whole backbone, not just the auxiliary loss, so the "video co-training" benefit is not isolated.
Conflicts: Consistent with Fast-WAM/GigaWorld-Policy view that world-model supervision helps at training time without inference-time imagination. Async+RTC gain agrees with PAINT/RTC results.
Relevance: Low for model choice (far beyond 8 GB). Useful datapoints: (1) async + RTC improved pants 70 -> 100% and cut time ~20–40% vs synchronous execution on real robot; (2) TensorRT BF16 gave 2.7x speedup at cosine sim 0.9998 — for our laptop, compiling (TensorRT/torch.compile) is a cheap latency lever; (3) for a later multi-object language task, conditioning on subtask-level instructions sharply reduced mistakes.
Decision impact:
 - Q10 latency/async: supports async execution + RTC over synchronous chunk execution (pants 70 -> 100%, faster) and TensorRT BF16 (198 -> 74 ms) — confidence M (real but 10 trials).
 - Q09 aux objectives: video co-training (world-model loss) associated with better execution, but not isolated — confidence L.
 - Q08 language: subtask-level instructions vs coarse instruction 75.7 -> 100% SR — confidence L-M (one task).
