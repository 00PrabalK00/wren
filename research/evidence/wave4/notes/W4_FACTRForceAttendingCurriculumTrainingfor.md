# W4_FACTRForceAttendingCurriculumTrainingfor — FACTR: Force-Attending Curriculum Training for Contact-Rich Policy Learning (2025, arXiv 2502.17432)
Setup: Franka Panda arm(s) + OpenManipulator-X gripper; low-cost Dynamixel leader with force feedback; 4 contact-rich real tasks (bimanual box lift, non-prehensile pivot, fruit pick-place [wrist cam + gripper torque], rolling dough); 50 demos per task; ONE camera per task (front ZED2 RGB or wrist); ACT-style enc-dec transformer (6+6 layers, d=512, chunk 100), ViT-B/16 init from "Soup 1M" (Dasari et al.), fine-tuned; external joint torque as 1 force token; MSE on absolute joint targets; bs 128, lr 3e-4, 20–50k steps, RandomResizeCrop aug, RTX 4090, 2–6 h. Eval 5–10 trials per object, train and unseen test objects.
Claim: naively adding force to a BC policy under-uses it (overfits to vision); blurring vision with decaying intensity during training (curriculum) forces attention to force → much better generalization to unseen object appearance/geometry.
Evidence (test = unseen objects; train objects all ≈90–100% except dough):
 - Box Lift test: ACT vision-only 31.7%, ACT vision+force 58.3%, FACTR 91.7%.
 - Pivot test: 26.0 / 42.0 / 76.0%.
 - Fruit pick-place (wrist cam) test: 26.7 / 73.3 / 93.3%.
 - Rolling dough: vision-only 0% train & test; V+F 80/70; FACTR 90/80.
 - Average test: vision-only 21.3%, V+F 61.2%, FACTR 87.5%.
 - Expanded test set (Table VI): box lift 35/120, 68/120, 105/120; pivot 30/130, 76/130, 101/130; dough 0/60, 41/60, 46/60.
 - Recovery after knocking box down (test objects): vision-only 4/30, V+F 16/30, FACTR 27/30; vision-only robots "remain static" after perturbation.
Ablations:
 - Curriculum vs constant blur (pivot, 25 test trials): constant 15–17/25 vs decaying schedules 17–21/25; operator (blur/downsample), space (pixel/latent), scheduler (linear/cos/exp/step) no consistent winner.
 - Alternatives (pivot, Table V train/test %): FACTR 90.0/77.7; AdaNorm force conditioning 25.0/6.1 (unstable, overfits); best of 10 vision noise augmentation settings 85.0/65.0 (low aug → overfits vision, high aug → ignores vision).
 - Stated, NO numbers: "A key decision that greatly improves policy generalization is to EXCLUDE current arm joints from the proprioception" — forces the model to extract object information from images instead of predicting actions close to current state (copycat).
Failure/limitations: noisy joint-torque sensing limits fine force tasks; needs joint torque sensing; curriculum hyperparams task-dependent. Critical: 5–10 trials/object; Franka torque sensors far better than SO-101 Feetech load readings; generalization is only to object appearance/geometry, not lighting/camera.
Conflicts: Proprioception-exclusion claim aligns with copycat/causal-confusion literature (and Octo/"state is a shortcut" findings), conflicts with ACT/LeRobot default of feeding joint state. Heavy vision noise augmentation hurting agrees with others that over-augmentation removes needed signal.
Relevance: (1) Our failure "different-looking pumpkin" = unseen object appearance; the vision-only ACT drop train ~100% → test ~27% on wrist-cam fruit pick-place mirrors it. A non-visual contact signal (SO-101 Feetech present-current/load on gripper) could help grasp mode-switching, but sensor quality is unknown — low priority. (2) Cheap, testable tip: drop or heavily dropout joint-state input to reduce copycat. (3) ACT-size model + ViT-B pretrained, 50 demos, single camera, trains on one GPU in hours — feasible (ViT-B inference fits 8 GB).
Decision impact:
 - Q07 history/proprio: supports excluding current joint state from policy input to avoid copycat — confidence L (stated, no numbers).
 - Q14 robustness (novel objects): vision-only ACT generalizes poorly to unseen objects (train ~100% → test 21–32%) at 50 demos; extra non-visual modality with curriculum fixes much of it — confidence M (real, 4 tasks, 5–10 trials/object).
 - Q05 augmentation: vision noise aug is an inferior substitute (65 vs 77.7% test) and tradeoff-prone; decaying-blur curriculum > constant blur — confidence L-M.
 - Q01/Q02: MSE regression on absolute joint chunks (k=100) works well for 50 demos — confidence L (not ablated).
 - Q03 vision encoder: pretrained ViT-B (Soup-1M) fine-tuned works with 50 demos — confidence L (not ablated).
