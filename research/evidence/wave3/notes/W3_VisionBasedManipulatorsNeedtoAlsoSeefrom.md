# W3_VisionBasedManipulatorsNeedtoAlsoSeefrom — Vision-Based Manipulators Need to Also See from Their Hands (2022, ICLR, arXiv 2203.12677)
Setup: Sim PyBullet Panda cube grasping (84x84 RGB, 4-DoF EE-pos + gripper), algorithms DAgger / DrQ / DAC; shifts = table height, distractors, table texture. Real: Franka Panda, sponge grasping among distractors, 100x100 RGB, 4-DoF EE position + gripper, BC on 360 VR-teleop demos, 20 episodes per shift. Meta-World 6 tasks (DrQ-v2 RL) with hand-centric observability high/moderate/low; OOD = initial object positions outside training support; 20 test envs. Small conv encoders (DrQ-style).
Claim: A wrist (hand-centric) camera generalizes OOD far better than a third-person camera when it gives sufficient observability; when it doesn't, use both but regularize the third-person stream (VIB) because it causes overfitting.
Evidence:
 - Sim cube grasp OOD aggregate (Table 1, IQM): DAgger hand 97.5 vs third 69.3; DrQ hand 99.3 vs third 46.9.
 - Real BC (Table 8, 20 eps each; both 85% in-distribution): table height -0.05/-0.025/+0.025/+0.05 m: hand 50/80/85/65 vs third 10/60/35/0; unseen distractor sets 1/2/3: hand 55/55/45 vs third 40/10/20; unseen table textures: hand 50/25/10 vs third 5/15/5. Aggregate (Table 2) mean 52.0 vs 20.0, IQM 53.3 vs 15.8 (45% relative reduction in OOD failure).
 - DAC: hand-only fully generalizes in-distribution with 5 demos; third-person lower even with 25 demos (figure).
 - Meta-World OOD (Table 3, IQM): hand 73.7, third 56.6, both naive 66.3, both + VIB(third) 87.7 (best per task), VIB on both 58.2, two third-person views + VIB 34.5, both + L2 on third 69.8.
Ablations:
 - Adding third-person to hand (naive): 73.7 → 66.3 IQM OOD → third view causes overfitting when hand view suffices, but is required on low hand-observability tasks (reach-hard, peg-insert-side-hard).
 - Bottleneck on third view: +21 IQM over naive fusion; bottlenecking the wrist view too hurts (58.2); L2 regularizer weaker (69.8).
 - Replacing wrist with a second third-person view (+VIB): 34.5 → the gain is from the wrist perspective itself, not from having 2 views.
 - Remove DrQ image augmentation: training fails to converge even with the wrist camera → augmentation still needed.
Failure/limitations: authors: wrist view fails if target not visible from hand; VIB weight tuned on a test-distribution validation sample (optimistic). Critical read: small low-res (84–100 px) from-scratch encoders; real result is one task, 20 eps/shift, no augmentation reported for real BC; no pretrained encoders; OOD shifts are table geometry/texture/distractors, not lighting or camera pose shift of the third-person camera specifically (though a wrist view is immune to scene camera moves by construction).
Conflicts: consistent with ACT/ALOHA/DP practice (wrist cams help), and with reports that policies over-rely on scene cameras and break under scene-camera shifts. Some later works (e.g. large VLAs) find adding a wrist cam gives modest gains in-distribution; this paper's effect is mainly OOD, which is exactly our failure mode.
Relevance: high. Our pumpkin pick-place: wrist cam sees target during approach/grasp, but tray location likely needs the scene cam (moderate observability). Suggests: keep wrist cam as the primary stream, give the RealSense scene stream a bottleneck/dropout (VIB, heavy augmentation, or view-dropout) to curb overfitting to lighting/camera pose; test wrist-only as a baseline.
Decision impact:
 - Q11 cameras: strongly supports wrist camera; naive wrist+scene fusion hurts OOD vs wrist-only (73.7 vs 66.3), bottlenecked scene stream best (87.7) — confidence H for direction (sim + real), M for magnitude.
 - Q14 robustness: wrist view raises real OOD mean 20→52% under table height/distractor/texture shifts at equal in-dist 85% — confidence M (1 real task, 20 eps).
 - Q05 augmentation: removing image aug prevents convergence even with wrist cam — confidence M (RL setting).
 - Q09 auxiliary/regularization: VIB (KL bottleneck) on scene-camera features improves OOD +21 IQM — confidence M (RL, tuned on test-dist validation).
