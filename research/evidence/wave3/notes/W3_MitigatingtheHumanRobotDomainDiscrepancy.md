# W3_MitigatingtheHumanRobotDomainDiscrepancy — Mitigating the Human-Robot Domain Discrepancy in Visual Pre-training for Robotic Manipulation (HR-Align) (2025, arXiv id not in text)
Setup: adapt frozen human-video-pretrained encoders (R3M ResNet-50 Ego4D; D4R MoCo on Kinetics) with a small adapter (1.6M = 6.4% params) trained contrastively on 56k paired human-robot videos from RH20T (4 A6000, 8k steps); then use as FROZEN backbone. Eval: Adroit 2 tasks (R3M protocol, 3 seeds), RLBench 18 language-conditioned tasks (RVT-style, 1800 demos), real xArm7 + one third-view Orbbec RGB-D, 5 tasks, 40 demos each, 20 episodes each, ACT-style keypose prediction head.
Claim: aligning robot-video features to paired human-video features adapts human-pretrained encoders to the robot domain; +7% avg success.
Evidence:
 - Adroit avg: D4R 63.0 -> 65.0; R3M 74.0 -> 81.3.
 - RLBench 18-task avg: D4R 55.3 -> 59.9; R3M ... -> +8.9 (stated).
 - Real 5 tasks (figure only): D4R-Align +13%, R3M-Align +11% avg over unadapted.
Ablations: vs full fine-tuning of R3M on the same robot videos: R3M-PreT 77.7, R3M-ClS 77.3 vs HR-Align 81.3 (Adroit avg) with 1.6M vs 25M trainable; adapter after last layer best; adapters at all 3 positions worse than single; language-guided feature pooling helps.
Failure/limitations: all encoders frozen downstream with small heads; gains modest (+2 to +9 pts); Adroit has 3 seeds only; real results figure-only; no comparison against modern general encoders (DINOv2, SigLIP) or end-to-end fine-tuned ImageNet ResNet — which other studies find competitive or better than R3M.
Conflicts: Assumes human-video pretraining (R3M) is a good base; several later studies find R3M/VC-1 underperform ImageNet/DINOv2 or scratch-trained encoders with augmentation on real robots. The result mainly says frozen R3M features have a domain gap that robot-video adaptation partly closes.
Relevance: Low-moderate. For SO-101 we would not use R3M; takeaway is that frozen human-video encoders need robot-domain adaptation, and a light adapter on the last layer is an efficient way to adapt a frozen encoder under 8 GB.
Decision impact:
 - Q03 vision encoder: weakens using frozen human-video encoders (R3M, MoCo-Kinetics) as-is; light adapter on last layer + robot-domain data helps (+2 to +9 pts) — L (sim mostly, modest gains, old baselines)
