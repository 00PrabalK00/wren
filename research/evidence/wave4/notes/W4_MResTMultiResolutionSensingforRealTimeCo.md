# W4_MResTMultiResolutionSensingforRealTimeCo — MResT: Multi-Resolution Sensing for Real-Time Control with Vision-Language Models (2024, arXiv 2401.14502)
Setup: Third-person cam → FROZEN pretrained VLM (MDETR ~150M or CLIP ViT-B) at ~5 Hz; wrist cam → ResNet-18 from scratch + FiLM language at ~20 Hz; force-torque + proprio → linear at ~75 Hz; camera-specific small transformers with cross-attention, cached features reused at higher rates; MLP head; ~250M total; delta EE actions (no chunking); 224×224, random-crop shift 8. Asymmetric augmentation: third-person crop/shift only; wrist cam crop + strong color jitter + grayscale. Sim: MT-Coarse (MuJoCo, ~1000 demos multi-task, 20/env), MT-Precise (4 RLBench, ~100/task), MT-Dynamic (ballbot, 50/task); 20 rollouts per task, top-5 avg over checkpoints. Real: Franka, leap-motion teleop, pickup (2 train objects × 60 demos, eval on 8 novel shape/color objects) and peg insertion (50 demos), 2 seeds. GTX-1080Ti.
Claim: combining a slow frozen VLM on the global view with fast small nets on wrist cam/FT gives precise, reactive, and semantically generalizable multi-task control.
Evidence:
 - vs baselines (Table 1; Coarse/Precise/Dynamic): RT-1 81.0/12.5/4.5; BC-Z 74.1/7.8/4.8; MResT 82.0/55.0/73.6.
 - Remove camera (Table 2): no wrist (π−Ih) 74.5/7.7/65.8; no third-person (π−I3) 41.0/29.6/27.5; no FT 81.8/56.1/33.2; full 82.0/55.0/73.6.
 - Real (Table 5, pickup / peg-insert): no wrist 7.5 / 10.0; no third-person 20.0 / 12.5; no FT 67.5 / 42.5; full 75.0 / 67.5. Real BC-Z 12.5 (train) / 5.0 (novel); RT-1 0/0; MResT 75.0 / 71.1 (novel objects).
 - Robustness train/heldout (Table 4): third-person-only frozen VLM 74.5/7.1 (Coarse visual); third-person fine-tuned 81.8/25.8; multi-res with fine-tuned VLM 82.4/45.6; multi-res frozen VLM 82.0/72.3. Precise visual: 7.7/4.5, 15.6/9.2, 56.4/31.9, 55.0/48.1.
Ablations:
 - Temporal (Table 3): 5 Hz single-rate 82.0/53.4/4.2; 20 Hz 81.0/56.2/12.2; multi-rate 73.6 on Dynamic only — quasi-static tasks insensitive to rate. Real peg insert: 5 Hz 45.0, 20 Hz 62.5, multi-res 67.5. Cameras at 5 Hz + FT 75 Hz on Dynamic: 33.4 vs 73.6.
 - Pixel-level aug on wrist: ≈ +15% heldout on MT-Coarse (figure; train unchanged).
 - Cross-attention vs concat fusion: ≈ +8% (figure).
 - ImageNet init instead of VLM for third-person: train matches but heldout "decreases tremendously" (figure only).
Failure/limitations: 2 seeds, 20 rollouts; restricted start distributions (no orientation change); no action chunking (single-step actions at 75 Hz); force-torque not available on SO-101; 2024-era baselines.
Conflicts: Strong frozen-encoder result for novel objects contrasts with papers showing fine-tuned encoders win in-domain (e.g. LoRA-SP needs vision adaptation) — difference: here generalization to novel objects is the target and a detection-style VLM (MDETR) supplies object grounding; in-domain train performance is equal. Asymmetric aug (color jitter on wrist only) is consistent with ChromaGuard finding that color jitter destroys color semantics — MResT keeps the language/color-grounded third-person stream un-jittered.
Relevance: Our "different-looking pumpkin" failure: evidence that a frozen, language-grounded global encoder on the scene cam + a small task-trained wrist encoder generalizes to novel object appearance (71% on 8 unseen objects vs 5% BC-Z) with ~120 demos. Also both cameras are essential (removing either drops real success to 7.5–20%). Multi-rate design (cache slow encoder features, run fast head) is an architectural answer to our latency issue.
Decision impact:
 - Q11 cameras: both scene and wrist cams essential; real pickup 75 vs 7.5 (no wrist) vs 20 (no scene) — M/H (real + sim consistent)
 - Q03 vision encoder: frozen language-grounded VLM on global view generalizes to held-out objects far better than fine-tuned (72.3 vs 45.6 heldout) with equal train — M
 - Q05 augmentation: asymmetric aug (strong color jitter/grayscale only on wrist; crop only on scene) +~15% heldout — L/M (figure)
 - Q10 latency: multi-rate (slow encoder cached at 5 Hz, fast wrist/proprio path) matches or beats single rate; 5 Hz camera-only is bad for reactive/contact tasks (real insert 45 vs 67.5) — M
 - Q14 robustness (novel objects): 71.1% on 8 unseen shape/color objects from 2 training objects — M
