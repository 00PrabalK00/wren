# W4_WARPEDWristAlignedRenderingforRobotPolic — WARPED: Wrist-Aligned Rendering for Robot Policy Learning from Egocentric Human Demonstrations (2026, arXiv 2604.10809)
Setup: Human demos recorded with a helmet GoPro (monocular RGB, 30 Hz); scene scan -> SfM + 3D Gaussian Splat; hand (HaMeR/MANO) + object (Grounding DINO, SAM2, SAM3D mesh, MegaPose) tracked by joint hand–object optimization; retargeted to gripper; photoreal wrist-view (fisheye) images rendered by 3DGS. Augmentation x10: object retexturing, object translation, initial gripper pose, scene scale, wrist-camera intrinsics/extrinsics perturbation; Gaussian noise on images. Policy: Diffusion Policy, wrist camera ONLY, CLIP ViT-B/16 (pretrained), 224x224, obs horizon 2, action horizon 8–12, 50 denoising steps, relative EE xyz + 6D rotation + binary gripper, 10 Hz rollout at 0.33x demo speed. Real: xArm7, GoPro wrist cam, 5 tasks, 30 demos/task, 20 trials; 4xV100.
Claim: wrist-view observations synthesized from egocentric human videos train policies as good as teleop data with 5–8x less collection time.
Evidence (Table I, x/20; Rotate Box / Pour Mug / Bottle from Rack / Wipe Brush / Can on Plate):
 - Teleoperation (VR, 30 demos): 16 / 19 / 16 / 15 / 19.
 - Alter baseline (inpainted hand-cam): 7 / 3 / 0 / 0 / 8.
 - WARPED: 20 / 18 / 17 / 11 / 17; with background distractors: 18 / 15 / 17 / 9 / 17.
 - Teleop 15 + WARPED 15 co-training: 19 / 20 / 17 / 11 / 20.
 - Novel objects (x/10, Obj1/Obj2): Rotate teleop 8/2 vs WARPED 10/8; Bottle 4/2 vs 8/5; Wipe 7/4 vs 7/2; Can 9/9 vs 10/9.
 - OOD scenes (Can on Plate, 50 demos over 20 tabletops, ViT-L/14, 4 unseen scenes): 16/20.
 - UMI vs WARPED (train/novel obj x/10): Can 9/10 vs 8/9; Rotate Box 2/0 vs 10/10.
 - Collection time: teleop 15–32 min vs WARPED 3.3–5.3 min per task (30 demos).
Ablations:
 - No augmentation: 0 / 17 / 0 / 0 / 8 vs full 20 / 18 / 17 / 11 / 17 -> augmentation (object/gripper pose, appearance, camera intrinsics/extrinsics) is essential for rendered data.
 - Hand–object optimization vs FoundationPose tracking: Rotate 17 vs 11, Can 17 vs 2.
Failure/limitations: rigid objects, quasi-static scene only; fails if object fully occluded; small flat objects (brush) hard to track; policy starts with object in wrist FOV (initial condition simplified); 20 trials; single scene except the OOD experiment. Wrist-only policy.
Conflicts: Wrist-only policy works for these tasks when the robot is initialized near the object — consistent with "wrist cam alone generalizes better to novel objects/scenes" findings (e.g., UMI), but tasks here avoid global localization. Supports view/appearance augmentation literature (Q05) — augmentation, not the rendering itself, made rendered data usable.
Relevance: Moderate for Q05/Q11/Q13. For SO-101: (1) wrist-camera-centric policy with relative EE actions + strong augmentation generalized to novel object instances better than teleop-trained policy (a different-looking pumpkin is our failure case); (2) 3DGS scene + object re-rendering with retexturing and camera extrinsic perturbation is a heavy but powerful augmentation route; (3) human-hand egocentric data collection is 5–8x faster — possible way to raise diversity cheaply. Pipeline complexity (many foundation models) is high.
Decision impact:
 - Q05 augmentation: object pose/appearance/gripper-pose/camera-extrinsics augmentation of rendered demos is essential (no-aug 0/20 on 3 of 5 tasks) — confidence M (real, 5 tasks x 20 trials)
 - Q11 cameras: wrist-only diffusion policy reaches teleop-level success and better novel-object generalization (Rotate Obj2 8 vs 2) — confidence L-M (initialized with object in wrist view)
 - Q13 data: 30 human-video demos x10 augmentation ≈ 30 teleop demos; mixing 15+15 matches/exceeds teleop; collection 5–8x faster — confidence M
 - Q14 robustness: background distractors small drop (e.g., Pour 18 -> 15); novel objects better than teleop-trained; 16/20 in unseen scenes with 50 multi-scene demos — confidence L-M
 - Q02 action space: relative EE pose + 6D rotation used (no ablation) — confidence L
 - Q03 encoder: pretrained CLIP ViT-B/16 (no ablation) — confidence L
