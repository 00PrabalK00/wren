# SafeFlowMPC — Predictive and Safe Trajectory Planning for Robot Manipulators with Learning-based Policies (2026, arXiv 2602.12794, TU Wien)
Setup: flow-matching trajectory model (temporal U-Net) conditioned on robot/end-effector state + goal pose (state-based, not vision); fine-tuned on a "safety dataset" (demos projected onto the safe manifold); during each flow step, a suboptimal real-time-iteration (RTI) MPC projection enforces joint/collision constraints (convex collision-free sets around key points); safe terminal constraint guarantees a safe trajectory always exists. All online planners run at 10 Hz. Real KUKA 7-DoF: grasp with dynamically changing grasp position, human-robot handover. Sim: 100 evaluation trajectories.
Claim: interleaving flow sampling with a cheap suboptimal MPC projection yields demo-like motions with guaranteed constraint satisfaction in real time.
Evidence (Table I qualitative from text; numeric cells garbled in extraction):
 - SafeFlowMPC: higher success than BoundMPC (pure MPC) with shorter trajectory durations; plain FM is faster but has much lower success due to collisions; BC fast but fails.
 - Solving the projection to optimality (IPOPT) gives similar success but much higher, highly variable planning time that "frequently violates the real-time property" — suboptimal RTI is the enabler.
Failure/limitations: state-based goals (no raw vision policy); requires kinematic/collision models; 10 Hz planning rate; KUKA with good tracking.
Conflicts: PACS argues for path-consistent braking rather than projection; SafeFlowMPC modifies the path but does so INSIDE the generative process (so outputs stay near the learned distribution) — both avoid post-hoc action modification.
Relevance to SO-101: low direct relevance (no vision, needs precise model). Lesson: if constraints are needed, bake them into the sampling (guidance/projection per denoise step) and use bounded-time suboptimal solvers, not full NLP.
Decision impact:
 - MPC-in-the-loop for our pick-place — NOT NEEDED — M; if used, prefer bounded-time (RTI/suboptimal) solvers — M.
