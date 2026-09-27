# W3_EquivariantDescriptorFieldsSE3Equivarian — Equivariant Descriptor Fields: SE(3)-Equivariant Energy-Based Models for End-to-End Visual Robotic Manipulation Learning (2023, ICLR; arXiv 2206.08321)
Setup: Sim only (PyBullet), keyframe pick and place poses from colored point clouds; SE(3)-equivariant EBM (Tensor Field Nets / SE(3)-Transformers) with MCMC sampling; 10 demos (upright poses) for mug-hanging, bowl and bottle pick-and-place; test unseen instances / lying poses / distractors / all combined. Baseline SE(3)-Transporter Nets.
Claim: end-to-end SE(3)-equivariant EBM learns 6-DoF pick-place from 5-10 demos and generalizes OOD.
Evidence: Table 1 garbled in text; legible values show EDFs ~0.97-1.00 vs SE(3)-TNs 0.36 in some cells. Table 2 (unseen instances+poses+distractors): EDF type-0..3 descriptors 1.00 success, 5.1 s inference vs NDF-like type-0-only 0.84, 5.7 s (i9 + RTX 3090). SE(3)-TNs fail on multimodal mug demos (had to be trained on unimodal subset).
Ablations: higher-order (orientation-sensitive) descriptors vs type-0 only: 1.00 vs 0.84.
Failure/limitations: >10 h training (per Diffusion-EDFs), ~5 s inference, not real-time, no trajectories, occlusion-sensitive; sim only, oracle demos.
Conflicts: none with our core literature; same line as Diffusion-EDFs.
Relevance: Very low for SO-101 closed-loop BC with 8 GB GPU and latency constraints; keyframe EBM with seconds-long MCMC. Only a weak data point for Q04 and that non-probabilistic methods break with multimodal demos (Q01).
Decision impact:
 - Q04 3D input: point-cloud equivariant keyframe models generalize to unseen poses from 10 demos — confidence L (sim-only, keyframe).
 - Q01 action head: weak support for probabilistic heads under multimodal demos (SE(3)-TNs fail on multimodal mug demos) — L.
