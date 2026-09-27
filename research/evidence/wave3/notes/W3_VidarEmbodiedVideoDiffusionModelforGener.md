# W3_VidarEmbodiedVideoDiffusionModelforGener — Vidar: Embodied Video Diffusion Model for Generalist Manipulation (2025, arXiv id not in text)
Setup: Aloha-style bimanual (14-D joints), 3 RGB cams. Video model Vidu 2.0 / Wan2.2 (5B) / HunyuanVideo (13B), continued pretraining on ~750K multi-view bimanual episodes (Agibot, RoboMind, RDT), fine-tuned on target robot: real 20 min of demos = 232 episodes over 81 tasks (~3/task); sim RoboTwin 2.0 multi-task 50 tasks x 20 (low) or 50 (standard) demos, 100 episodes each. Actions from Masked Inverse Dynamics Model (U-Net mask + ResNet-50, 92M, Huber loss + L1 mask sparsity). Open-loop: one 60-frame (7.5 s @8fps) video generated once; ~25 s on 8x A100 in the cloud; GPT-4o picks best of K=3. Training 64 GPUs x 64 h. Real eval: 3-5 trials per task.
Claim: internet+embodied video prior + lightweight masked IDM adapts to a new robot with ~20 min demos and generalizes to unseen tasks/backgrounds.
Evidence:
 - RoboTwin multi-task avg (clean / randomized): low-data pi0.5 25.0/9.2 vs Vidar 60.0/15.7; standard pi0.5 44.8/14.2 vs Vidar 65.8/17.5. Trained clean -> randomized collapses for both (<18%).
 - Real (Table 2): seen 68.2 (VPP 4.5, UniPi 36.4); unseen tasks 66.7 (13.3, 6.7); unseen backgrounds 55.6 (0.0, 22.2).
 - vs pi0.5 with 2,307 real episodes (Wan2.2 version): seen 69.3 vs 34.3; unseen tasks 67.1 vs 12.9 (5 trials/task-ish).
Ablations:
 - MIDM vs plain ResNet IDM: offline test accuracy (unseen) 49.0 vs 24.3 (train both 99.9) -> classic overfit of plain CNN to background; real unseen-background success 55.6 vs 22.2.
 - Mask sparsity lambda: 1e-1 7.1, 1e-2 39.9, 3e-3 49.0, 1e-3 40.7, 1e-4 24.4 test accuracy.
 - Test-time scaling (best-of-3 via GPT-4o): seen 45.5 -> 68.2, unseen tasks 33.3 -> 66.7, unseen bg 44.4 -> 55.6.
Failure/limitations: open-loop 7.5 s execution, 25 s generation on datacenter GPUs + GPT-4o; real trials 3-5 per task so every number has +-20-30 pt uncertainty; failures from motion prediction misalignment and gripper misalignment. Requires camera views that show the arm fully (IDM assumption).
Conflicts: RoboTwin clean->randomized drop to ~15% for both pi0.5 and Vidar shows large pretrained priors do NOT solve visual domain shift when fine-tuning data is clean — agrees with SeedPolicy note (all policies <5% on randomized). The pi0.5 comparison favors Vidar, but pi0.5 fine-tune settings may be suboptimal.
Relevance: Whole pipeline impossible on 8 GB laptop and far too slow. Transferable idea: a learned sparse spatial attention mask (L1-regularized soft mask over pixels before the action regressor) doubled held-out accuracy under background change at low data — a cheap trick for our scene camera. Also: clean-only training does not generalize to randomized scenes even with huge priors -> need scene diversity/augmentation in our own 50-100 demos.
Decision impact:
 - Q14 robustness: supports learned sparse pixel masking to ignore background (IDM test acc 24.3 -> 49.0; real unseen bg 22.2 -> 55.6) — L/M (offline metric solid; real 3 trials/task)
 - Q14 robustness: clean-only fine-tuning collapses on randomized scenes even for pi0.5 / 5B video prior (60 -> 15.7) — M (sim, 100 eps x 50 tasks)
 - Q10 latency: open-loop video-generation policies (25 s/plan) are incompatible with our latency needs — H
 - Q12 model size: big pretrained priors help unseen tasks in multi-task low-data but not visual randomization — L
