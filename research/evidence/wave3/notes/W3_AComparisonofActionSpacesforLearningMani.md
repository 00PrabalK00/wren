# W3_AComparisonofActionSpacesforLearningMani — A Comparison of Action Spaces for Learning Manipulation Tasks (2019, arXiv 1908.08659)
Setup: simulated 7-DoF arm, model-free RL (PPO, SAC), state-based observations (joint pos/vel + object/goal relative poses, no images), 3 tasks (2 mm peg insertion, hammering, block pushing), 4 action spaces (gravity-compensated torque, joint PD, inverse dynamics, task-space impedance). No demos, no real robot.
Claim: impedance-controller references reduce RL sample complexity vs torque/PD across tasks and algorithms (ordering impedance > ID > PD > torque).
Low relevance: evidence is about RL sample efficiency with low-level torque-type interfaces in sim; our SO-101 only exposes servo position targets and we do imitation learning from 50–100 demos. Only weak transferable hint: higher-level task-space targets simplify learning when the controller absorbs dynamics — does not bear on absolute vs delta joint targets for BC. No ledger lines beyond a single L-confidence ~ on Q02.
Decision impact:
 - Q02 action space: ~ task-space (EE) targets easier than raw joint torque/PD for RL in sim — confidence L (RL, state-based, not position-controlled BC)
