# RoboEngine — Plug-and-Play Robot Data Augmentation (2025, arXiv 2503.18738)
Setup: DROID-style Franka, one third-person RGB, absolute pose; Diffusion Policy with DINOv2-Base encoder, obs horizon 1, ColorJitter+RandomCrop on all methods; 50 demos in ONE scene; eval in 6 completely new scenes; tasks Fold Towel, Put Mouse on Pad.
Method: Robo-SAM (EVF-SAM fine-tuned on 3.8k-image RoboSeg dataset) segments robot+task objects without green screen/calibration; background replaced by fine-tuned background-diffusion (physics/task-aware scenes); alternatives in toolkit: textures, ImageNet images, inpainting.
Evidence: RoboEngine +210% over no generative aug, +20% over best baseline; Texture/ImageNet/Background all substantially > none (Texture slightly best of the simple ones, consistent with GreenAug); inpainting-only small changes → weak + slowest (3.9 s/frame). Scaling augmented demos helps with diminishing returns; mixing original+augmented ≈ augmented-only.
Limitations: no temporal consistency across frames; single view only; no 3D.
Relevance: gives a no-green-screen path for existing so101_pumpkin_v1 data (off-the-shelf segmentation of SO-101 + pumpkin needed; wrist-cam segmentation weaker per GreenAug). Even simple texture/ImageNet background replacement gives big OOD gains.
Decision impact: background-replacement augmentation (texture/ImageNet at minimum) — SUPPORTED — M/H.
