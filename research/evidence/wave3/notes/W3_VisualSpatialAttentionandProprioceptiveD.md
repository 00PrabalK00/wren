# W3_VisualSpatialAttentionandProprioceptiveD — Visual Spatial Attention and Proprioceptive Data-Driven Reinforcement Learning for Robust Peg-in-Hole Task Under Variable Conditions (2023, RA-L, arXiv 2312.16438)
Setup: Real Denso VM-60B1 industrial arm, anchor-bolt peg-in-hole into concrete (0.2 mm clearance), camera ROI 64x64 px around the peg tip + F/T sensor. Offline DDQN (discrete search actions) trained on a pre-recorded force/position "hole map" + images of ONE hole under room light only; 4000 episodes; trained on GTX 1070Ti 8 GB in ~2.3 h. Inputs: last 6 steps of images/attention points + F/T + depth + actions. Test: 12 unseen holes x 16 start positions x 3 lighting conditions (room, left flood light, bottom flood light — the latter two cast misleading shadows); offline 5760 tests/model, online real robot tests.
Claim: A spatial-attention-point network (CNN + soft-argmax keypoints, trained end-to-end with RL and a next-image prediction/reconstruction loss) is robust to unseen harsh lighting, while an autoencoder-feature model is not.
Evidence (online real robot, SR % room/left/bottom; avg SR, CT):
 - P-RL (proprioception/force only): 87.4 avg, 11.6 s.
 - AE-RL (pretrained autoencoder features): 91.4 / 19.4 / 57.1 → avg 56.0, 6.2 s.
 - SAP-RL (pretrained SAP, frozen): 92.8 / 92.6 / 92.2 → 92.5.
 - SAP-RL-E (end-to-end with image-prediction head): 94.5 / 91.6 / 95.5 → 93.9, 8.2 s.
 - Offline: AE-RL 91.4 / 22.6 / 59.5 (57.8 avg); SAP-RL-E 97.4 / 95.8 / 99.1 (97.4 avg).
Ablations: feature type (holistic AE latent vs soft-argmax keypoints) under lighting shift is the key ablation: 56–58% vs 92–97%. End-to-end vs pretrained SAP: small gain (+1.4 online). Vision vs force-only: vision generalizes better to 4 mm start offsets (P-RL 79.4% at 4 mm).
Failure/limitations: RL with discrete search actions, not imitation; tiny 64x64 ROI camera and a 2D search task; shadows are the only visual nuisance; no distractors/new objects; AE baseline is weak (few thousand weights). Still, it is a genuine unseen-lighting real-robot test with hundreds of trials.
Conflicts: Supports the long-standing claim that spatial-softmax/keypoint bottlenecks (Levine et al., DP's ResNet+spatial softmax) are more lighting-robust than global latent vectors; consistent with object-centric/keypoint robustness papers. Contrasts with the finding that pure pixel-level features from large pretrained ViTs are robust enough — not tested here.
Relevance: For our lighting failures, a spatial-softmax (keypoint) bottleneck on the image encoder is a cheap architectural prior worth trying (ResNet18 + spatial softmax as in DP/robomimic) versus global-pooled features. Small model, trained on 8 GB GPU.
Decision impact:
 - Q14 robustness (lighting): keypoint/soft-argmax features trained under one lighting hold 92–95% under unseen shadowed lighting; autoencoder latent drops to 19–57% — supports spatial-softmax/keypoint bottleneck — confidence M (real, many trials, but narrow task).
 - Q09 auxiliary objectives: next-image prediction through keypoints end-to-end gives small gain (92.5 → 93.9) — confidence L.
 - Q03 vision encoder: global reconstruction (AE) features are lighting-fragile — weakens reconstruction-pretrained global latents — confidence L.
