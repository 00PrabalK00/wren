# W3_SelectivePerceptionforRobotTaskAwareAtte — Selective Perception for Robot: Task-Aware Attention in Multimodal VLA (2025/26, arXiv id not in text)
Setup: real 6-DoF arm + gripper (7-D joint state, absolute target-joint actions), wrist RealSense D435 + external RealSense L515 (640x480 RGB) + thermal cam and/or Digit tactile; 15 Hz; 3 long-horizon industrial tasks (battery sorting by heat, wire selection by 0.4 mm thickness, valve operation); 50 demos/task; π0 base with LoRA on VLM + action expert (flow matching), plus a small camera router (wrist image + prompt → softmax weights over non-wrist views, wrist always on) supervised by VLM (Qwen3-VL) auto-labels, λ=0.1; 10 trials/task.
Claim: dynamically gating auxiliary views/sensors by a wrist-cam+prompt router beats static fusion of all modalities in long-horizon multimodal tasks.
Evidence (Table I, avg over 3 tasks, 10 trials each): RGB only (no thermal/tactile) 0.00%; static fusion of all modalities 10.00±17.32%; router with Wrist+State input 30.00±26.46%; router Ext.cam+Prompt 73.33±15.28%; router Wrist+Prompt 83.33±11.55% (Task1 90%, Task2 90%, Task3 70%). VLM labels 83.33% vs human labels 86.67% (Fig. 6).
Ablations:
 - Router input: wrist+prompt 83.3 > external+prompt 73.3 > wrist+state 30.0 (raw state as router input acted as noise; on Task 1 below baseline).
 - Static all-modality fusion vs router: 10% → 73–83%.
 - No compute/latency numbers despite "inference efficiency" claim (none found in text).
Failure/limitations: failures = object drops in transport, grasp failures. My read: tasks are constructed so RGB is insufficient (thermal/tactile needed) — "RGB only 0%" is by design; 10 trials per cell, std devs huge; the static-fusion baseline at 10% with π0+LoRA and 50 demos is suspiciously weak (possibly under-tuned); no robustness tests.
Conflicts: consistent with other reports that naively adding modalities/views to a VLA can hurt in low-data fine-tuning (irrelevant inputs as distractors). Supports wrist camera as the most task-phase-informative view.
Relevance: low-moderate. We have no thermal/tactile. The transferable insight: with 50 demos, adding extra input streams can dilute signal; wrist view carries phase/contact information better than a fixed external cam; concatenating raw proprio state into a gating module hurt. π0 base is far above our 8 GB budget.
Decision impact:
 - Q11 cameras: supports wrist cam as primary/anchor view (wrist+prompt 83.3 vs external+prompt 73.3 as router input) — confidence L (10 trials, indirect use).
 - Q07/proprio input: weakly weakens feeding raw state into auxiliary modules (30% vs 83%) — confidence L (single architecture, noisy).
