# W3_DeFMLearningFoundationRepresentationsfro — DeFM: Learning Foundation Representations from Depth for Robotics (2025/26, ETH RSL; arXiv id not in extracted header)
Setup: DINOv2-style self-distillation on 60M curated depth images (real sensors incl. RealSense/Kinect/ZED + simulated), ViT-L/14 teacher distilled into 3–30M-param students (ResNet-18/50, EfficientNet, RegNet, ViT-S). Input = 3-channel log-depth normalization (relative, mid-range /log10, far-range /log100) preserving metric scale. Robot evals are all RL / teacher-student: Habitat point-goal nav, B2W wheeled-legged nav (real deployments, qualitative), Kuka-Allegro dexterous grasping in Isaac Lab (sim only, 2000 eps), ANYmal ladder climbing (sim). No imitation learning, no parallel-gripper manipulation, no real manipulation.
Claim: a depth-only foundation encoder, used frozen, beats RGB foundation models applied to depth and matches/exceeds from-scratch task encoders.
Evidence:
 - Dexterous grasp (Table IX, success normalized to teacher, ResNet-18): Frozen — ImageNet 0.658 / DINOv3-distilled 0.653 / DeFM 0.809 (train noise); under Kinect noise shift 0.004 / 0.208 / 0.486. Fine-tuned — scratch 0.777 / ImageNet 0.795 / DINOv3 0.824 / DeFM 0.894; Kinect noise 0.725 / 0.737 / 0.784 / 0.876.
 - Habitat nav SPL Gibson/MP3D (Table VII): scratch ResNet-50 0.899/0.780; frozen DINOv2 ViT-S 0.865/0.710; DINOv3 0.880/0.743; DeFM ViT-S 0.888/0.759; DeFM ResNet-50 0.884/0.751; Theia 0.628/0.483.
 - Ladder climbing: frozen DeFM 90.14% vs scratch CNN 90.45%.
 - GraspNet-1B depth segmentation mIoU (ViT-L, linear): DINOv2 24.26, RADIOv3 25.18, DINOv3 23.89, DeFM 27.85.
Ablations: fine-tuning > frozen for every encoder on grasping; frozen encoders collapse under an unseen depth-noise model (ImageNet frozen 0.66 → 0.004), fine-tuned ones barely drop (DeFM 0.894 → 0.876).
Failure/limitations: critical read: no imitation learning and no RGB-vs-depth comparison for manipulation (grasping student uses depth in all arms); manipulation results are sim-only; gains over scratch encoders are small when fine-tuned (0.894 vs 0.777 is the largest). Relevant mostly as a depth-encoder option.
Conflicts: agrees with the general trend that fine-tuning pretrained encoders beats frozen for control (and that frozen features + small head overfit to training-sensor statistics); DINOv3 surprisingly decent on depth.
Relevance: low-moderate. If we add the RealSense depth channel, a small pretrained depth encoder (DeFM ResNet-18, ~11M) is a better init than ImageNet ResNet on colormapped depth, and must be fine-tuned (not frozen) to survive sensor-noise shift. Does not tell us whether depth beats RGB for our pick-place.
Decision impact:
 - Q04 depth: if depth used, use a depth-pretrained encoder with metric log-normalization; depth features robust to lighting by construction (argued, not tested vs RGB) — confidence L (sim RL only).
 - Q03 vision encoder: fine-tuned > frozen (grasp 0.894 vs 0.809; under noise shift 0.876 vs 0.486) — confidence M for direction (sim).
 - Q14 robustness: frozen encoder + head is brittle to sensor-noise shift; fine-tuning restores robustness — confidence L-M.
