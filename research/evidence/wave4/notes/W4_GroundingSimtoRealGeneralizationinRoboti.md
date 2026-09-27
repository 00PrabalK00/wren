# W4_GroundingSimtoRealGeneralizationinRoboti — Grounding Sim-to-Real Generalization in Robotic Manipulation: An Empirical Study with Vision-Language-Action Models (2026, arXiv 2603.22876)
Setup: OpenVLA-OFT (7B Llama2, SigLIP+DINOv2, L1 regression chunks; LoRA r=32, 20–30k steps, 8×H100) trained ONLY in sim (RoboTwin 2.0, Cobot Magic embodiment), 100 sim demos/task, 5 bimanual tasks; single front RealSense D435 RGB 640×480; zero-shot real eval on Piper robot, one factor varied at a time (base, 3 backgrounds, 3 lights, seen/unseen objects, 2/4/8 distractors), 3×3 position grid; >10k real trials (20–120 per cell). RL: GRPO (SimpleVLA-RL, discrete-token head), chunk 25.
Claim: for zero-shot sim2real VLAs, spatial randomization (camera pose, table height) matters most; frame-wise randomization > episode-wise; photorealism helps up to a medium threshold; RL fine-tuning adds robustness.
Evidence (Table 1, real SR averaged over conditions; held fixed: 100 demos, OFT recipe, episode-wise DR):
 - Click Bell real: Clean 2.7%, BG 11.5, LT 12.3, TD 3.1, CamPose 23.5, TableHeight 36.9, TH+CP+BG 47.7, TH+CP+LT 44.2, All 49.7.
 - Place Empty Cup real: Clean 5.4, BG 10.2, LT 8.6, TD 6.9, CP 17.5, TH 24.8, All 41.0.
 - Stack Bowls real: Clean 26.2, BG 40.4, LT 31.5, TD 27.3, CP 42.3, TH 49.6, All 63.1.
 - Pick Dual Bottles real: Clean 1.5, BG 12.3, LT 7.3, CP 16.2, TH 15.4, All 23.8. Beat Hammer ≤11.5 everywhere.
 - Frame-wise vs episode-wise (Table 2, real): CP +8.4/+8.1/+2.7/+6.9/+3.4 pts; BG +3.5/+12.9/+5.0/+4.6/+1.9; LT +2.3/+0.4/+0.4/+1.1/0.0.
 - RL (Table 3): avg real SR SFT 5.6% → SFT+RL (clean) 33.4% → SFT+RL+DR 42.8%.
 - Real-factor sensitivity (appendix): distractors cause the largest drop; lighting variation the smallest (e.g. Click Bell All-factors: base 15/20, BG 30/60, Light 39/60, Distractor 14/60, Object 31/60).
 - Rendering: photorealism gains saturate beyond medium (figure only; Table 7 e.g. Click Bell base Default 15/20, Medium 14/20, Low 3/20).
Ablations: as above (factor-wise DR, granularity, fidelity, RL).
Failure/limitations: sim-only training; 7B model; single camera; camera pose DR only ±1 cm; spatial "table height" gains may partly reflect sim2real geometric calibration mismatch rather than general robustness. Beat Block Hammer essentially unsolved.
Conflicts: Lighting having small effect contrasts with our observed lighting brittleness — but here the backbone is a big SigLIP+DINOv2 VLA already somewhat lighting invariant; with a small model, photometric aug likely matters more. Agrees with other papers that geometric/viewpoint augmentation (random shift/crop) is among the most useful augmentations.
Relevance: Indirect (sim2real, not real-demo BC). Transferable lessons for our augmentation design: (a) viewpoint/geometric perturbation of the scene camera is the single most valuable randomization — direct analogue to our "slightly moved camera" failure: add random crop/shift/small perspective warp to the RealSense stream; (b) per-frame (not per-episode) randomization is better; (c) distractors are the worst real shift — include clutter in some demos. Uses the same RealSense D435 at 640×480.
Decision impact:
 - Q05 augmentation: supports geometric/viewpoint augmentation (camera pose) as highest-value, combined with appearance aug; per-frame > per-episode randomization — confidence M (large real n, but sim2real setting and 7B VLA).
 - Q14 robustness: distractors = largest real-world drop, lighting smallest for a big pretrained VLA — confidence M.
 - Q11 cameras/viewpoint: camera-pose randomization +10–20 pts real SR over clean from single ±1 cm factor — confidence M.
 - Q09 aux/RL: RL fine-tuning in sim raises real avg 5.6→33.4% — confidence L for us (needs sim twin).
