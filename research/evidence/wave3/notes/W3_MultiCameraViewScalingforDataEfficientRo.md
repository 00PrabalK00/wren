# W3_MultiCameraViewScalingforDataEfficientRo — Multi-Camera View Scaling for Data-Efficient Robot Imitation Learning (2026, arXiv 2604.00557)
Setup: Diffusion Policy with a DINOv3-base encoder (LoRA fine-tuned) in sim (robomimic Square/Can/Lift, N=10/25/50 demos). Every demo is recorded by 1, 3 or 5 synchronized cameras 15° apart (front CamF, ±15° left/right/up/down), and each view is treated as a separate pseudo-demo. Inference uses CamF only unless noted. Real: FANUC CRX-10iA teapot pouring, 2 fixed cams (left/right), DP with ResNet18 + spatial softmax, N=25/50 (trial count not stated). Actions are delta EEF pose chunks in base, camera or EEF frame.
Claim: extra synchronized views used as pseudo-demos act like scene diversity, and they improve data efficiency and viewpoint robustness at no teleop cost.
Evidence (Table I, success; single view CamF base-frame vs 5 views base / camera-frame):
 - Square: N=10 0.14 -> 0.18/0.18; N=25 0.26 -> 0.42/0.39; N=50 0.42 -> 0.55/0.58.
 - Can: N=10 0.18 -> 0.32/0.37; N=25 0.54 -> 0.65/0.68; N=50 0.72 -> 0.80/0.85.
 - Lift: N=10 0.69 -> 0.80/0.85.
 - Camera shift at test (Table IV, Can): single-view-trained policy CamF 0.18 / CamFL 0.00 / CamFU 0.01 (N=10) and 0.54 / 0.07 / 0.05 (N=25). Five-view-trained policy: 0.37/0.30/0.37 (N=10) and 0.68/0.66/0.77 (N=25).
 - Real pouring (Table VI): single-view train 0.45 (N=25) / 0.70 (N=50); both-views train 0.50 / 0.75; + multiview action aggregation at inference 0.85 / 0.85.
Ablations:
 - Action frame (Table II, Square, CamF only): base 0.14/0.26/0.42 vs EEF-frame 0.06/0.25/0.32. With 5 views: base 0.18/0.42/0.55 vs EEF 0.09/0.27/0.41. EEF-frame deltas are consistently worse (moving origin).
 - Camera-frame actions slightly beat base-frame when multiple views are used (they need extrinsics).
 - View selection (Table III): very different views (front+top+side) gave no gain (0.17/0.24/...), and 30° spacing helped less (0.18/0.26/0.44) than 15°. Extra training views only help if they are near the deployment view distribution.
 - Multiview composition at inference (Table V) adds gains on top.
Failure/limitations: mostly sim with scripted-ish robomimic data. The real experiment has only 2 views and gains of +5 pts (the trial count is not given, so the +5 is likely within noise). Camera-shift test is in sim only.
Conflicts: agrees with DP/ACT experience that single fixed-view policies overfit to the viewpoint. A 15° shift drops success to ~0, which is a strong quantitative statement of our "slightly moved camera" failure. EEF-frame worse than base-frame conflicts mildly with papers favouring gripper-frame actions (e.g. cable routing, UMI), but those pair EEF-frame with wrist cameras. Here the input is a third-person view, so a moving-origin action frame mismatches the fixed image frame.
Relevance: high. We have one scene RealSense + wrist cam. Cheap version: mount 2–4 extra cameras (even cheap webcams) near the deployment viewpoint during teleop only, and train a view-agnostic scene-camera branch on random views. This directly targets the moved-camera failure without more teleop. It needs no depth. Keep base-frame (or joint) actions for the scene-cam policy.
Decision impact:
 - Q11 cameras / viewpoint robustness: + record demos with several extra cameras near the deployment view (±15°) and train on random views; single-view policy collapses under a 15° shift (0.54 -> 0.07) while the multi-view-trained one holds (0.68 -> 0.66) — confidence M (sim for shift test)
 - Q14 robustness (camera shift): + same evidence — confidence M
 - Q02 action space: - EEF-frame deltas with third-person cams (0.06–0.32 vs 0.14–0.42 base frame) — confidence M
 - Q05 augmentation: + real extra views beat nothing, but far-off views (top/side) add nothing, so view augmentation should stay near deployment pose — confidence M
 - Q13 data: + multi-view pseudo-demos roughly equal 2x demos at N=10–25 — confidence M
