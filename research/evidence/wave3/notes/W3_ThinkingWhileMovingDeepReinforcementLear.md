# W3_ThinkingWhileMovingDeepReinforcementLear — Thinking While Moving: Deep Reinforcement Learning with Concurrent Control (2020, ICLR; arXiv 2004.06089)
Setup: Value-based RL (DQN on concurrent Cartpole/Pendulum; QT-Opt vision grasping on 7-DoF arm, sim with procedurally generated objects + real bins). Concurrent mode = next observation taken while previous action still executing. Q-function conditioned on "concurrent knowledge": previous action, action-selection time t_AS, or Vector-to-Go (VTG = remaining part of the previous action not yet executed at observation time).
Claim: conditioning the policy/critic on the in-flight action (VTG or prev action + delay) recovers blocking-mode performance while acting concurrently, giving faster, smoother motion.
Evidence:
 - Sim grasping (Table 1): blocking unconditioned 92.72% success, 132.1 s episode, action completion 92.3%; concurrent unconditioned 84.11% / 83.77% (high variance +-7.6-9.3); concurrent with VTG / prev action ~92.55-93.49%, episode 83.0-90.8 s (31.3% faster than blocking).
 - Real grasping (Table 2): blocking 81.43% success, policy duration 22.6 s; concurrent + VTG 68.60%, 11.5 s (49% faster). Authors call success "comparable" but it is 12.8 pts lower (trial count not given).
 - Toy tasks: VTG is the least hyperparameter-sensitive feature; frame-stacking past actions/observations helps only nominally (figure only).
Ablations: unconditioned vs VTG vs prev-action+t_AS in concurrent mode (above); frame stacking vs VTG (Pendulum, figure-only).
Failure/limitations: value-based RL only; requires measurable delay and remaining action; real results thin. Critical read: real success dropped; speed gain partly from skipping deceleration stops.
Conflicts: Early version of the idea behind RTC / "inpainting the committed prefix" and bidirectional decoding in chunked BC: tell the policy what is already committed during inference latency. Agrees that naive async (unconditioned) degrades success.
Relevance: Our async inference with ~2 s latency jerks at chunk boundaries: supports conditioning the next chunk on the actions that will still execute during inference (prefix/VTG conditioning or RTC-style inpainting) instead of blind switching. Evidence is RL, not BC.
Decision impact:
 - Q10 async execution: supports conditioning on in-flight/committed actions for concurrent control — sim success 84 -> 93% with VTG, 31% faster episodes — confidence L/M (RL, sim; real success lower).
 - Q07 history: frame-stacking past observations/actions gives only nominal gains vs explicit in-flight-action feature — L.
