# MP1 — MeanFlow Tames Policy Learning in 1-step for Robotic Manipulation (Sheng et al., AAAI 2026, arXiv 2507.10543; code LogSSim/MP1)
Setup: DP3-style point-cloud policy with a MeanFlow head (learns interval-averaged velocity u(z_t, r, t) via the MeanFlow identity → genuine 1-NFE, no consistency loss, no teacher), CFG retained at 1 NFE, plus a "Dispersive Loss" repelling state embeddings. Sim: 3 Adroit + 34 Meta-World tasks, 3 seeds. Real: ARX R5 dual-arm, RealSense L515, 5 tasks, 20 demos each, horizon 16, obs stride 2 (trials per task not stated; percentages in 10% steps suggest 10).
Evidence:
 - Sim avg success: MP1 78.9±2.1 vs FlowPolicy (1-NFE consistency flow) 71.6±3.5; +10.2 over DP3.
 - Inference (Table 2): MP1 ≈ 6.8 ms avg (7.1–7.4 ms Adroit); FlowPolicy ~12–15 ms; DP3 (10 NFE) ~92–145 ms.
 - Real (Table 5, SR / completion time): Hammer MP1 90%/18.6 s, FlowPolicy 70%/22.3, DP3 70%/31.1; Drawer close 100/8.8, 90/15.7, 80/20.2; Heat water 90/23.4, 60/31.1, 70/38.8; Stack block 80/27.2, 50/29.6, 60/35.1; Spoon 90/22.6, 80/26.7, 70/28.3.
Ablations: Dispersive loss removal: −4–5 pts avg over 10 tasks (e.g., Coffee Pull 62 vs 92). Flow ratio (fraction r≠t): ratio 0 (= plain flow matching) lower; ratios 0.25–0.75 similar; ratio 1.0 collapses (e.g., Pen 0, Assembly 0). Few-shot (2–20 demos): MP1 > FlowPolicy especially at few demos (figure).
Failure/limitations: point-cloud input (needs depth — we have RealSense); JVP training cost; small real N. Critical read: completion-time gains reflect fewer retries/fewer steps, not only inference (6.8 vs 12 ms is negligible at 10 Hz); DP3 baseline run at 10 NFE.
Conflicts: agrees with ReactVLA (iMF) and SnapFlow that 1–2-step mean/shortcut flow heads match multi-step quality; contrasts with Hybrid Consistency Policy's collapse of aggressive few-step distillation (DDPM teacher) — MeanFlow trained from scratch avoids the teacher.
Relevance: moderate: shows a 1-NFE generative head at ~7 ms, trainable from scratch on 20 demos — for a small SO-101 policy the head is not the bottleneck either way; relevant if we build a small non-VLA policy and want RTC-style inpainting cheaply.
Decision impact:
 - Q10 fast generator: MeanFlow 1-NFE head (≈7 ms) ≥ consistency-flow and ≥ 10-step DP3 in success — M (37 sim tasks, small real).
 - Q01 head: mixing r≠t for 25–75% of samples is necessary; 100% collapses — M.
