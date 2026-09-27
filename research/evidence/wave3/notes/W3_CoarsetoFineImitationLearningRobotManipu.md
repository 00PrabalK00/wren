# W3_CoarsetoFineImitationLearningRobotManipu — Coarse-to-Fine Imitation Learning: Robot Manipulation from a Single Demonstration (2021, arXiv 2105.06411)
Setup: Sawyer 7-DoF at 30 Hz, single wrist camera 64x64 RGB; 1 human demo per task + 2x50 self-supervised approach trajectories (robot moves camera around object to label bottleneck pose); small 4-conv + 4-FC CNN regressing 3-DoF (x, y, yaw) bottleneck pose (MSE); 8 real tasks, 20 object poses each in a 40x40 cm area, +-45 deg rotation.
Claim: approach = linear IK path to a CNN-estimated "bottleneck" pose; interaction = open-loop replay of the demo's EE velocities; learns tasks from one demo.
Evidence (Table II, % over 20 poses; VS / VS+correction / Filtering / Filtering+correction): Bottle 65/100/85/100, Plate 25/95/25/80, Screwdriver 20/70/10/60, Lid 65/100/85/100, Hammer 35/40/50/65, Scoop 55/95/90/100, Knife 15/10/0/10, Plug 5/10/10/45; average 35.6 / 65.0 / 44.4 / 70.0. Residual RL baseline from the single demo solved no task.
Ablations:
 - Second "last-inch" network trained only on near-object wrist views: avg 44.4 -> 70.0 (filtering), 35.6 -> 65.0 (VS).
 - Fusing sequential predictions (Kalman-style filtering with constant prior uncertainty) vs per-frame visual servoing: 35.6 -> 44.4; target reaching mean pos error ~5.2 mm (filtering prior) vs 5.7 mm (VS) vs 13.9 mm (first image only). Constant (prior) uncertainty beat dropout/learned uncertainty.
Failure/limitations: open-loop interaction phase; textureless objects (knife rack 10%) and contact-rich plug fail; assumes static object, top-down approach, tabletop 3-DoF pose; no lighting/background variation tested (authors note illumination/background break the axiom).
Conflicts: none direct with modern BC; it is a structured alternative, not an end-to-end policy. Consistent with wrist-camera literature that near-object wrist views give the precision.
Relevance: Low-moderate. Useful ideas: (1) the robot itself can collect self-supervised wrist-camera data around the pumpkin to train a pose/precision module without extra human demos; (2) specialized fine-alignment from wrist views close to the object is a big lever (+26 pts). Not a policy architecture we would adopt.
Decision impact:
 - Q11 cameras: supports wrist camera for final-approach precision (last-inch wrist correction +25.6 pts avg) — confidence L (single-demo pose-estimation pipeline, not BC).
 - Q07 history: temporal fusion of predictions over frames reduces error (35.6->44.4) — L (state estimation, not policy history).
