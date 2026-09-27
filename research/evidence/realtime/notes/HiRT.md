# HiRT — HiRT: Enhancing Robotic Control with Hierarchical Robot Transformers (CoRL 2024, arXiv 2410.05273)
Setup: slow = InstructBLIP-7B (LoRA everywhere) producing a latent from a single image + instruction at low frequency; fast = latent-conditioned small policy (EfficientNet-B3 in sim, ViT-B/16 real) with image-history context and FiLM + conditioned MAP pooling; runs asynchronously, no proprio input. Sim: Metaworld (20 tasks, 20 attempts), Franka-Kitchen (100/task). Real: Franka Panda, 2000 trajectories of quasi-static tasks; dynamic test = target moved at ~1 cm/s during execution.
Claim: a slowly updated VLM latent guiding a fast visual policy keeps VLA-level generalization at ~2× control rate and wins on dynamic tasks.
Evidence:
 - Metaworld seen tasks (Table 1): RT-1 65.8 @20.1 Hz; DP @4.6 Hz; Vanilla-VLA (RT-2 reimpl.) 73.8 @4.1 Hz; HiRT 76.4 @9.8 Hz.
 - Real dynamic tasks (Table 2, seen / unseen / avg SR, time on static version): DP 20/15/18, 10.38 s; RT-1* 25/10/18, 14.22 s; Vanilla-VLA 55/40/48, 9.25 s; HiRT 80/70/75, 6.18 s. Baseline "misses the blue block due to long inference time and high latency".
 - Franka-Kitchen ablation (Table 3): removing image context (-IC) collapses some tasks (Ldoor 43→0, Micro 79→18); removing conditioning layers (-CD) ≈ −20% SR.
 - VLM update frequency sweep: figure 4 (trade-off curves; values figure only).
Failure/limitations: 7B slow model; trial counts for real dynamic test not stated in text found (percent granularity 5 → ~20 trials); dynamic motion only 1 cm/s; no proprio; DP baseline at 4.6 Hz seems poorly tuned (DP normally fast with DDIM).
Conflicts: agrees with RoboDual/FiS: fast layer must see fresh images with history; the slow latent can be stale.
Relevance to SO-101: the one real-robot controlled test of "moving target" reactivity in this family shows closed-loop rate matters (VLA 4 Hz → 48% vs HiRT ~10 Hz → 75%). Supports making the fast loop as frequent as possible; the 7B slow part is not needed for our single task.
Decision impact:
 - Increase re-query rate of the visuomotor loop to handle moved objects — SUPPORTED — M (one real study, slow object motion).
 - 7B slow latent: INFEASIBLE / unnecessary on 8 GB — H.
