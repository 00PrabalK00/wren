# W3_ZevaEgoEgocentricMidTrainingwithInContex — Zeva-Ego: Egocentric Mid-Training with In-Context Causal Learning for Robot Manipulation (2026, arXiv id not in text)
Setup: π0.5 (~3B) mid-trained on up to 10K h egocentric video (EgoDex, EgoVerse, Ego4D, Egocentric-10K) and/or 2K h AgiBot robot data; unified 16-D EEF schema, actions in chunk-anchored camera frame; Action-Centric Encoder turns frame pairs into action-token supervision. ICCL = frozen-parameter memory of action–effect transitions conditioning the flow-matching action expert across repeated attempts. Eval: RoboTwin 2.0 (100 rollouts/task), LIBERO-PRO, real ARX dual-arm ChemLab-Evo 3 atomic tasks (20 randomized episodes/task).
Claim: egocentric video is a scalable substitute for robot data (~4–5 h ego ≈ 1 h robot), task-matched human videos boost low-data real post-training, and in-context action–effect memory improves success across repeated attempts without gradient updates.
Evidence:
 - RoboTwin (clean+random→random): π0.5 63.8% → 75.3% with 10K h ego vs 74.7% with 2K h robot mid-training.
 - Real ChemLab-Evo (tube / beaker / pour / avg): π0.5 95/60/65/73.3; Zeva 100/70/80/83.3; Zeva-Ego 90/70/95/85.0; LingBot-VA 71.7 avg; Fast-WAM 76.7 avg.
 - Real low-data (figure; text numbers): with 10 robot demos + 50 task-matched human videos recorded from the SAME robot main camera, PickTube +55 pts and PlaceBottle +40 pts over robot-only; "~1.5 task-matched ego episodes ≈ 1 robot demo".
 - ICCL: RoboTwin success 58% (attempt 1) → 89% (attempt 4) with frozen parameters (figure).
 - Ego task diversity at fixed budget: narrow ≈ intermediate, broad → 70.2% (figure).
Ablations: PIM (cross-attempt memory) removal loses the cross-attempt gains (figure only); ACE token geometry correlation 0.801 held-out, 0.724 zero-shot EgoVerse.
Failure/limitations: most ablations figure-only; huge compute (π0.5 + 10K h video); ICCL gains require repeated attempts on the same initialization (real eval used fixed init across attempts), which is a reset-and-retry setting, not a single-shot deployment. 20 real episodes per task.
Conflicts: consistent with other human-video co-training work (e.g. EgoMimic/MimicPlay) that task-matched human demos help most in the low-robot-data regime. Diversity > repetition agrees with data-diversity scaling papers.
Relevance: low-moderate. Model far too big for 8 GB. One cheap transferable idea: record the human hand doing the pumpkin→tray motion in front of our scene camera (fast, no teleop) as auxiliary data — but exploiting it needs an action-token/latent-action head we do not have; the +40–55 pt gains came at 10 robot demos, not 50–100.
Decision impact:
 - Q13 data: task-matched human videos (50) add +40–55 pts at 10 robot demos; ~1.5 human ≈ 1 robot demo — confidence L (figure, large VLA, needs latent-action machinery).
 - Q13 diversity: broad task coverage beats repeated narrow data at fixed budget — confidence L (sim, figure).
 - Q12 model size: n/a (3B VLA) — L.
