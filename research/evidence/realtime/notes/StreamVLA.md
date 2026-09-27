# StreamVLA — Breaking the Reason-Act Cycle via Completion-State Gating (2026, arXiv 2602.01100)
Setup: unified 3B VLA (pi0.5-style backbone) with an autoregressive System-2 head (text sub-goal + imagined image of the sub-task COMPLETION state, Infinity-based generator) and a flow-matching System-1 action head; trained on 24 A800. Gating module (~2% params) computes a semantic discrepancy d_t between current observation and the locked completion image each step; d_t > τ (0.5) → Skip Mode (reuse locked plan, only action head); d_t ≤ τ → sub-task done → Full Mode (re-plan). Forced update at t=0. Real robot controlled at 50 Hz via CAN, third-person USB webcam + wrist RGB; 20 trials per task. Sim LIBERO, RoboTwin 2.0 (100 trials/task).
Claim: gate slow reasoning on predicted sub-task completion (a time-invariant goal anchor) instead of a clock; skip it most of the time.
Evidence:
 - Latency: System 2 skipped 72% of the time → average 244 ms → 128 ms (−48%).
 - LIBERO avg 98.5% (vs OpenVLA-OFT 97.1). RoboTwin 2.0 Easy 71.3 / Hard 37.2 vs pi0.5 62.7 / 33.8, RDT 55.0 / 26.0.
 - Real (Table III; Spelling / Insertion / Interference-Spelling): OpenVLA-OFT 40/35/10; pi0.5 45/35/15; WALL-OSS 15/25/5; StreamVLA 90/70/55. In interference (letters moved/removed by human), the observation–goal mismatch "unlocks" System 2, which re-plans.
 - Ablation: continuous re-planning every step shows diminishing returns vs gating (text); removing text planning LIBERO-Long 96.6 → 93.5.
Failure/limitations: large training compute; interference recovery 55% still; "emergent" recovery depends on the planner recognizing the changed scene; no small-model variant.
Conflicts: Hi Robot uses a fixed 1 s clock; FiS found fixed 1:4 ratio best; StreamVLA argues event-gated is both faster and better. Consistent with Rewind-IL/Sentinel: discrepancy between expected and observed state is the trigger signal.
Relevance to SO-101: the model itself is too big, but the TRIGGER DESIGN is cheap to replicate with small parts: store the embedding of the "goal/completion" frame(s) of each phase from the demos (e.g., grasped, above tray), compare the current embedding, and re-query/advance/rewind on mismatch. This is the same machinery as Rewind-IL's checkpoint library.
Decision impact:
 - Event-triggered (progress/completion-mismatch) re-planning rather than fixed clock — SUPPORTED — M (real, but large-model context).
