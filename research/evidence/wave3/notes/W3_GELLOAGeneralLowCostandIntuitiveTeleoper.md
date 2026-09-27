# W3_GELLOAGeneralLowCostandIntuitiveTeleoper — GELLO: A General, Low-Cost, and Intuitive Teleoperation Framework for Robot Manipulators (2023, arXiv 2309.13037)
Setup: Teleop hardware paper; no policy learning. Scaled (alpha=0.5) kinematic replica leader arms with Dynamixel XL330 encoders (<$300) for UR5, xArm7, Franka; joint-space direct mapping (no IK); rubber-band joint regularization. User study: 12 novices, bimanual UR5, 5 tasks, GELLO vs 3D SpaceMouse vs VR controllers.
Claim: Kinematically equivalent joint-space leader devices give more reliable and faster demonstration collection than Cartesian low-cost devices.
Evidence (Table II success, Hat/Mask/Banana/Towel/USB/Avg): GELLO .92/.92/1.0/.92/.83/.92; 3D mouse .75/.58/.67/.58/.58/.63; VR .92/.83/.75/.58/.50/.72. GELLO fastest completion times (figure only). Failure modes (Table III): SpaceMouse/VR many self-collisions and timeouts; GELLO fewest.
Ablations: joint regularization (springs) prevents elbow drop (Fig. 3, figure only).
Failure/limitations: No downstream policy results — says nothing directly about learned-policy quality; 12 users, 12 trials/task/device.
Conflicts: None with learning papers; consistent with ACT/ALOHA use of leader-follower rigs.
Relevance: SO-101 already uses leader/follower joint-space teleop (same paradigm), so this only confirms our data collection interface is the better low-cost choice for demo success/throughput. No evidence on our 14 architecture decisions.
Decision impact:
 - Q13 data quality: joint-space leader teleop avg success .92 vs VR .72 vs SpaceMouse .63 for novices — supports keeping leader/follower collection — confidence M (user study, not policy)
