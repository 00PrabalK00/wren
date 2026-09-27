# W3_DiffusionVLAGeneralizableandInterpretabl — Diffusion-VLA: Generalizable and Interpretable Robot Foundation Model via Self-Generated Reasoning (DiVLA) (2024, arXiv 2412.03293)
Setup: Qwen2-VL backbone (2B / 7B / 72B) + diffusion action head; autoregressive reasoning text + "reasoning injection" (FiLM-like reuse of reasoning tokens in the policy head); loss L_diff + 10·L_ntp. Pretrained on DROID (2B/7B) or OXE+DROID (72B). Real Franka with 2 external ZED cams + RealSense D435i wrist cam (3 views); bimanual AgileX. Multi-task: 5 tasks, 50–160 demos each (160/120/50/100/100), 77 in-dist trials + 45 visual-generalization trials per method. Sorting: 500 demos. No data augmentation used. Inference: 2B 82 Hz, 7B 42 Hz on A6000 (vLLM; 74/30 Hz without), OpenVLA-7B 5 Hz.
Claim: VLM reasoning + diffusion head yields a generalizable, fast VLA; reasoning injection and scale both help.
Evidence (Table 4, successes/trials):
 - Multi-task in-dist (77 trials): DP 30/77, TinyVLA 40, Octo 28, OpenVLA 38, DiVLA-2B 68/77.
 - Visual generalization (distractors, colorful background, colored lighting; 45 trials): DP 4/45, TinyVLA 13, Octo 7, OpenVLA 12, DiVLA-2B 26/45.
 - Zero-shot bin picking 102 unseen objects: DP 8.9%, Octo 19.6%, TinyVLA 23.5%, OpenVLA 28.4%, DiVLA 63.7%.
 - Sorting avg: DiVLA 66.2%; DP drops to 9.2% in cluttered-mixed vs DiVLA 60%.
 - Bimanual bussing seen: DiVLA 72.9% vs DP 45.8% vs OpenVLA 0%.
Ablations:
 - Reasoning injection removed (in-dist 5 tasks): avg 83.6 → 50.3 (Task 3: 90.9 → 27.3).
 - Model scale (Table 10): Sorting 66.2 / 74.9 / 82.4, Bin picking 63.7 / 66.7 / 75.9 for 2B / 7B / 72B (pretraining data also differs for 72B).
 - Camera count (OpenVLA): 3 views 45.3 vs 1 view 12.7 avg on sorting (Table 7).
 - View shift (new camera positions, sorting, 5 trials): DP 0, OpenVLA 0, DiVLA-2B 60%.
 - 8-bit / 4-bit quantization: "significant degradation" (no numbers).
Failure/limitations: VQA confusions (toy dragon→tiger, color reliance); small trial counts for OOD (9 per task, 5 for view shift); DP baseline configuration (encoder, aug) under-specified, likely no augmentation — DP 4/45 under visual change reflects an unaugmented from-scratch policy. 72B scale confounded with more pretraining data.
Conflicts: agrees with other VLA papers that pretrained VLM backbones are far more robust to lighting/background/distractor than from-scratch DP. Contradicts the idea that quantization is free for deployment. The reasoning-injection gain is large but self-reported with 11-trial cells.
Relevance: 2B is already beyond our 8 GB GPU for training with full finetune (Qwen2-VL-2B + diffusion head; LoRA might fit, inference ~fine). Most useful takeaways: (1) an unaugmented DP collapses under lighting/background shift (our exact failure), (2) multi-view (incl. wrist) strongly helps, (3) camera shift kills DP/OpenVLA. Also note 4/8-bit quantization hurt — relevant if we try to shrink a VLA onto the laptop.
Decision impact:
 - Q12 model size: supports larger pretrained VLA for generalization (2B→72B: sorting 66.2→82.4) but none fit 8 GB training — confidence M (confounded with pretraining data).
 - Q14 robustness: from-scratch DP w/o augmentation collapses under lighting/background/distractors (4/45 vs 26/45 VLA) — confidence M.
 - Q11 cameras: 3 views vs 1 view OpenVLA 45.3 vs 12.7; camera shift → DP 0% — confidence M.
 - Q10 latency: quantization to 8/4-bit degrades VLA performance (qualitative); 2B VLA 74–82 Hz on A6000 — confidence L.
 - Q01 action head: ~ diffusion head vs OpenVLA discrete tokens (DiVLA 68/77 vs OpenVLA 38/77) but confounded by backbone/reasoning — confidence L.
 - Q08 language: reasoning-text injection 50.3→83.6 in-dist — confidence L (11 trials/task, big VLM only).
