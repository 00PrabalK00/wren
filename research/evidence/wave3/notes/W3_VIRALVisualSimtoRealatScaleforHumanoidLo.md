# W3_VIRALVisualSimtoRealatScaleforHumanoidLo — VIRAL: Visual Sim-to-Real at Scale for Humanoid Loco-Manipulation (2025, arXiv id not in text)
Setup: Unitree G1 29-DoF + 3-finger hands; single RealSense D435i RGB (head); Isaac Lab tiled rendering; privileged PPO teacher (16 L40S GPUs) → RGB+proprio student via DAgger/BC mix (up to 64 GPUs); 200 sim teleop demos only used for reference-state resets; policy 50 Hz over HOMIE whole-body controller; inference on RTX 4090. Real eval: 59 consecutive loco-manipulation cycles; generalization shown qualitatively.
Claim: large-scale visual domain randomization + teacher-student distillation + real-to-sim alignment yields a zero-shot RGB humanoid pick-place policy near expert-teleop reliability.
Evidence: real 54/59 consecutive cycles; expert teleop 100% @ 21.4 s/cycle vs VIRAL 20.2 s; non-expert teleop 73%. Generalization over tray/object pos, table height/type, tablecloth colour, lighting, object category — video/figure only, no numbers.
Ablations (mostly figures; sim eval):
 - Visual randomization (200 episodes, normalized to full=1.0): no randomization → 0.649 (−35.1%); removing any single component (materials, dome lighting, camera extrinsics) also degrades (per-component values figure only); image-quality jitter, object colour, camera delay "smaller gains".
 - Vision backbone: DINOv3 converges faster and reaches higher success than alternatives (figure only, alternatives not named in text).
 - History: feed-forward history and LSTM > single-step; longer windows help (figure only).
 - DAgger vs BC: pure BC (α=1) brittle, fails to self-correct in Isaac→MuJoCo and real; α=0.5 adopted.
 - Delta vs absolute action space (teacher RL): only delta solves task (figure only) — RL-exploration effect, not IL.
 - Reference state init: without RSI teacher <10% vs ~95% with.
 - Multi-object (10) vs single-object training: multi-object higher on every test object (figure only).
Failure/limitations: authors argue sim-to-real for general manipulation is out of reach near-term; "a few days of teleop data can often outperform months of sim-to-real engineering"; hardware backlash/friction poorly modelled. Critical read: most ablations are sim-evaluated with figures only; needs 16–64 GPUs.
Conflicts: delta-action result is for RL exploration and should not be generalized to IL (ACT reports absolute better for leader/follower IL). DAgger > BC matches classic compounding-error theory and supports recovery data in IL.
Relevance: low-moderate. We will not do sim-to-real. Transferable: the randomization ranking (lighting, materials/background colours, camera extrinsics dominate) points to which augmentations matter for our lighting/camera-shift failures; DINO-family backbone preferred; object diversity in training matters for "different-looking pumpkin".
Decision impact:
 - Q05 augmentation: supports lighting + material/colour + camera-extrinsic randomization (none → −35%) — confidence L (sim-eval, sim-to-real context).
 - Q03 vision encoder: DINOv3 > others for student — confidence L (figure only, alternatives unnamed).
 - Q07 history: history (FF or LSTM) > single-step — confidence L (figure only, RL-distilled student).
 - Q13 data diversity: multi-object training generalizes better than single object — confidence L (figure only).
 - Q14 robustness: RGB policy robust to lighting/tablecloth/object changes when trained with heavy DR — confidence L (qualitative).
