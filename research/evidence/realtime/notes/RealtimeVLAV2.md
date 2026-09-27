# RealtimeVLAV2 — Realtime-VLA V2: Learning to Run VLAs Fast, Smooth, and Accurate (Yang et al., Dexmal, Mar 2026, arXiv 2603.26360; tech report)
Setup: systems report on a DOS W1 platform (RealSense D435 + Airbot Play lightweight arm, position-controlled CSP with PD tracking), VLA served on a remote GPU with RTC-style async. Tasks: fold shirt, place-into-fixture (0.2 mm margins), pick-and-latch. No controlled success-rate tables; outcome = timings and qualitative videos.
Method: (1) CALIBRATE delays: camera exposure (LED strip on system clock), readout (timestamps), proprio read delay, and robot motion lag (robot sways sinusoidally in front of a screen showing phase bars; filmed at 120 fps; sub-frame phase estimation; ±5 ms). (2) Align image and joint readings at training/inference via a history buffer. (3) Pre-amplify commands to compensate PD tracking lag (first-order lag model q_{k+1}=a q_k+(1−a) y_k) via a small MPC ("Spatial Optimization") with limits on velocity/acceleration/jerk. (4) Temporal Optimization: QP (OSQP) re-times the chunk's waypoints to spread acceleration without changing the path (compatible with RTC prefix matching). (5) Learned Speed Adaptation from human "throttle" interventions during rollouts (iterated daily), capped at 3–4× demo speed.
Evidence:
 - Measured delays on their system: readout 33 ms, camera 55 ms, proprio 50 ms, motion lag 150 ms (i.e., ~290 ms of non-inference delay).
 - Task times (Fig. 1): shirt folding demo 75.3 s → VLA 18.9 s (human 19.0 s); place into fixture 89.5 → 37.8 s (human 37.6); pick and latch 98.6 → 42.6 s (human 36.0).
 - Speed-up sweep (fold shirt, figure): interventions rise sharply at 2–3× and concentrate in specific precision stages (sleeve folding).
 - Post-processing flattens acceleration/jerk profiles (Fig. 8, qualitative).
Ablations: pre-amplification effect shown qualitatively (Fig. 3); failure-prediction (Q-style) speed model abandoned due to overfitting (qualitative).
Failure/limitations: no success rates, no trial counts, no baselines — engineering evidence only.
Conflicts: agrees with LatencyAwareIndustrial/SAIL that non-inference delays (camera, proprio, actuator lag) are of the same order as inference and must be measured; agrees with SAIL that PD-tracking lag of lightweight arms makes commanded ≠ reached.
Relevance: high for method, low for proof. SO-101 Feetech servos are low-gain position loops with backlash — tmotion is likely large. The sinusoid-and-screen calibration and the first-order-lag model are directly reusable; the time-reparameterisation QP is a model-agnostic smoother that does not break RTC-style prefix conditioning.
Decision impact:
 - Q10 latency budget: measure camera/proprio/motion delays (they totalled ~290 ms here) — M (engineering measurement).
 - Q10 smoothing: re-time (not reshape) chunks with a QP and compensate tracking lag with a small MPC — L/M (no controlled comparison).
