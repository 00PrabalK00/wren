# AsyncFastSlow — Asynchronous Fast-Slow VLA Policies for Whole-Body Robotic Manipulation (DuoCore-FS) (Astribot, 2025, arXiv 2512.20188)
Setup: real Astribot whole-body robot. Slow = 3B VLM (autoregressive reasoning action tokens via RVQ-VAE whole-body tokenizer, Jacobi parallel decoding) at 1–3 Hz writing text/fusion-query embeddings to a "bridge buffer"; fast = pi0-small-style transformer diffusion decoder reading the LATEST buffer + current visual features + proprio at 25–30 Hz. Jointly trained end-to-end with cross-timescale sampling (slow input sampled from an earlier frame than fast input to simulate async lag). Popcorn-scooping 4-subtask task, 20 trials ID, 10 OOD; anomaly scenarios 8 trials each.
Claim: truly asynchronous fast/slow with a latent buffer gives 3× the rate of comparable-size VLAs and better success.
Evidence:
 - In-distribution (Table 1) overall SR / inference Hz: pi0 85% (17/20) @12.5 Hz; slow-only 55% (11/20) @3.27 Hz; DuoCore-FS 90% (18/20) @32.3 Hz.
 - OOD (Table 2): pi0 overall weak (e.g., 20% (2/10) first subtask) vs DuoCore-FS higher; small n.
 - Anomalies (cup fell over / upside down / taken away → expected behavior: return home and idle): pi0 22/24 (91.7%) vs DuoCore-FS 23/24 (95.8%) — both mostly fine; anomaly handling was TRAINED (demonstrated) behavior, not a monitor.
 - Language following (Table 4): 1/7 vs 3/7.
 - Tokenizer (Table 5): FAST tokens avg 81 / max 205 → 0.95 Hz, 0% success; RVQ-VAE avg/max 36 → 3.27 Hz, 83.3%.
Ablations: tokenizer only; no ablation of buffer staleness or cross-timescale sampling.
Failure/limitations: commercial, code for Astribot customers; tiny trial counts; single main task; no reaction-time measurement despite "responsiveness" claim.
Conflicts: agrees with FiS/RoboDual/HiRT pattern (slow latent, fast decoder with fresh obs). Anomaly result shows that a monolithic pi0 can also "recover" when recovery behavior is in the demos — i.e., data, not architecture, drives this recovery.
Relevance to SO-101: The "train the fast policy against deliberately stale slow context" trick (cross-timescale sampling, also RoboDual latency-aware training) is the transferable idea. Also: demonstrating the anomaly response (return home / re-grasp) in the dataset makes even a flat policy handle it — cheap for us.
Decision impact:
 - Put recovery behaviors (object moved, dropped) into the teleop demos — SUPPORTED — M (this + RDP "proactively recorded reactive behaviors" + REBOOT/RaC in W3).
 - If using any cached slow features, train with randomized staleness — SUPPORTED — M.
