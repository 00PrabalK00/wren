# W3_LearningtoGraspontheMoonfrom3DOctreeObse — Learning to Grasp on the Moon from 3D Octree Observations with Deep RL (2022, arXiv 2208.00818)
Setup: sim-trained RL (TQC) grasping of lunar rocks; octree (40 cm cube, depth 4, 2.5 cm leaves) vs 2-channel depth+intensity 128x128 image, matched ~315k-param feature extractors, 2 stacked frames; zero-shot sim-to-real on a rover arm with a RealSense D435 at 15 Hz; real eval n=25 per variant.
Claim: 3D octree observations + full domain randomization transfer better than image observations.
Evidence (Table II, zero-shot real success, n=25): image/reduced DR 12%, image/full DR 20%, octree/reduced DR 8%, octree/full DR 32%.
Ablations: full DR lowered sim success (training instability) but raised real success; octree only wins when combined with full DR.
Failure/limitations: RL, not IL; only 25 trials; single object category (rocks); timeouts from repeated failed grasps; camera pose randomized in sim which octree (world frame) is invariant to by construction.
Conflicts: consistent with 3D-input papers (DP3/iDP3) that 3D helps viewpoint invariance, but the effect here is small and non-significant at n=25 (8 vs 12% reduced DR).
Relevance: low. Our setup is IL from 50–100 real demos. The only transfer is the idea that a calibrated 3D representation is invariant to camera pose, which matters for our "slightly moved camera" failure.
Decision impact:
 - Q04 3D vs RGB: ~ weak support for calibrated 3D input under camera/visual shift — confidence L (RL sim-to-real, n=25)
 - Q05 augmentation: + heavy randomization improves transfer despite lower in-domain score — confidence L
