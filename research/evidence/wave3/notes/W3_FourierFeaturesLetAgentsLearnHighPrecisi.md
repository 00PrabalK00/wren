# W3_FourierFeaturesLetAgentsLearnHighPrecisi — Fourier Features Let Agents Learn High Precision Policies with Imitation Learning (2026, arXiv id not in text)
Setup: EDM diffusion policy, same backbone, only observation encoder varied (PointPatch, PointPatch-attn, PCM, DP3, PointTransformer, PointMap, RGB via ConvNeXt-V2 nano, PointPatch+RGB, +pretrained). Sim: RoboCasa 16 atomic tasks x 50 human demos (2 static + in-hand cam, no color in point clouds), ManiSkill3 4 tasks x 500 scripted demos (1 static cam). 5 seeds x 3 ckpts, 50/100 rollouts, IQM + bootstrap CI. Real: 4 long multi-phase tasks (Jia et al. 2025a; cup stacking, drawer, folding, ...), 2 static Zed Mini + wrist RealSense D405, 75-102 demos/task, 16 rollouts/task. Fourier map: L=16 log-spaced wavelengths 4 m -> 2 cm, 96 features/point. Points cropped (<2 m), 32768 random then 1 cm voxel downsample; VariableJitter sigma up to 1-5 mm.
Claim: Point cloud encoders suffer spectral bias on slowly varying Cartesian xyz; NeRF-style Fourier positional mapping of xyz gives large, consistent gains for any point cloud encoder.
Evidence:
 - RoboCasa PointPatch avg 13% -> 34% with FF (CloseDrawer 34->72, TurnOffSinkFaucet 28->63, OpenDrawer ~0->12). DP3 and PCM same trend (figure only). ManiSkill3: minor gains only for PointPatch variants (saturation).
 - Real (PointPatch+RGB, 16 rollouts/task): aggregate normalized score 14.8% -> 40.2% with FF; all 4 tasks improved; biggest on Cup-Stacking (w/o FF knocks cup over), smallest on Folding. Benefit grows as cup diameter shrinks (Table 9, numbers not in extracted text).
 - Unimodal (point-cloud-only or RGB-only) real policies "were not successful" in early experiments -> RGB+point cloud needed for color-dependent goals.
Ablations (8 RoboCasa tasks, PointPatch, 5 seeds):
 - Jitter/FF (Table 1): FF+VariableJitter 41.4±2.4; FF no jitter 39.9; FF random jitter 38.9; no FF no jitter 17.5; no FF random jitter 17.0; no FF VariableJitter 18.5. -> FF is the whole effect; point jitter augmentation ~1-2 pts.
 - Log-spaced fixed frequencies > Gaussian random FF, learned freqs or SPE (numbers not extracted).
 - L 8/16/32 and lambda_min: robust, 16 slightly best (figure).
 - Point cloud size: benefit shrinks sharply at ~2k points (coarser voxels); baseline unaffected by size (figure).
 - Destroying fine geometry with 5 cm jitter: FF still 24% vs 13% no-FF -> benefit partly from learning dynamics.
Failure/limitations: Smallest cups unsolved by either. No lighting/camera-shift tests. Real: 16 rollouts per task, only one architecture compared; baseline "catastrophically unable to learn" suggests the non-FF baseline might be under-tuned. RoboCasa absolute success rates low (34%).
Conflicts: Consistent with iDP3/DP3-style claims that 3D helps precision, but refines them: plain xyz point encoders (DP3 max-pool) underuse geometry — which may explain papers finding point clouds only task-dependently better than RGB. Supports hybrid RGB+3D (their real system needed both). Contrasts with "depth doesn't help" findings from RGB-D-channel concat approaches.
Relevance: If we add RealSense depth (Q04), do NOT feed raw xyz into an MLP/PointNet; apply a fixed Fourier mapping (cost-free), keep enough points (>>2k; they use 1 cm voxels), crop workspace, and combine with RGB tokens (pumpkin color/identity). Wrist cam RGB retained. Lightweight (ConvNeXt nano + point patches) — plausibly 8 GB feasible. Pumpkin pick-place is low-precision, so the benefit may be smaller for us (Folding, least precise, gained least).
Decision impact:
 - Q04 3D/depth: point cloud + RGB with Fourier xyz encoding 14.8 -> 40.2 real; RoboCasa 13 -> 34 — supports 3D only if encoded with Fourier features; plain xyz encoders weak — confidence M (5 seeds sim, 16 real rollouts)
 - Q05 augmentation: point jitter adds only ~1-2 pts (41.4 vs 39.9) — ~ neutral for point jitter — confidence M
 - Q11 cameras: real setup 2 static + wrist; unimodal failed, multimodal RGB+PC needed — L
