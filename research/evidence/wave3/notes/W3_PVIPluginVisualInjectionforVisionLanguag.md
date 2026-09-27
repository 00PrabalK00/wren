# W3_PVIPluginVisualInjectionforVisionLanguag — PVI: Plug-in Visual Injection for Vision-Language-Action Models (2026, arXiv id not in text)
Setup: Sim RoboTwin 2.0 bimanual (Aloha-AgileX-like), 3 RGB views (env + 2 wrist) 480x640, joint-space 14-D state/action, action chunk 16; 50 demos/task; single-task fine-tune on 20 tasks (injection comparison) and 10 tasks (encoder study), multi-task 20/50-task mixtures; 100 rollouts/task. Base GR00T N1.5-3B; PVI adds frozen V-JEPA2 (1.0B) or DINOv2-Giant encoder + trainable copy of the DiT action expert (0.59B), zero-init residual injection; 4.3B total, 0.90B trainable. Trained on 4-8 H20 GPUs. Real: Airbot dual-arm cloth folding, qualitative only (no success rate, demo count not stated).
Claim: VLM backbones attenuate geometric/temporal cues; injecting a separate (frozen) visual encoder's features directly into the action expert via a zero-init side branch gives large gains; temporal video features (V-JEPA2) beat static DINOv2.
Evidence:
 - Injection strategy (20 tasks, V-JEPA2 fixed): GR00T baseline 35.7; Concat 43.6; ControlVLA/ControlNet/ReferenceNet-style 34.4-37.4; PVI 59.7.
 - Encoder study (10 tasks): baseline 39.8; PVI@DINOv2 (single frame) 56.8; PVI@V-JEPA2 (8 frames @4fps) 69.4; both 68.9.
 - Multi-task 50 demos/task: 20-task 61.15 -> 69.15; 50-task 61.32 -> 63.56 (gain shrinks as task count grows).
Ablations:
 - Temporal context frames at 4 fps (V-JEPA2): 2f 71.6, 4f 71.8, 8f 69.4, 16f 66.6 -> 0.5-1 s of history is optimal; longer history slowly hurts.
 - Freeze projector 55.3 vs 69.4 trained -> aux-feature alignment must be learned.
 - No zero-init 71.8 (vs 69.4) -> zero-init not needed for final performance.
Failure/limitations: all quantitative results are sim; real robot is a single qualitative demo; no robustness (lighting/camera) eval; compute is 4-8 datacenter GPUs; 4.3B total params — infeasible on 8 GB. Baseline GR00T fine-tune is only 35.7-39.8, so gains partly compensate for a weak base-VLA fine-tune on 50 demos. Adding DINOv2 at single frame already +17 pp, meaning much of the gain is "give the action head a dense spatial visual encoder" rather than temporality per se.
Conflicts: History helps here (+12.6 pp V-JEPA2 8f vs DINOv2 1f), unlike copycat/causal-confusion findings where frame stacking hurts BC; difference: history enters via a FROZEN pretrained video encoder (no shortcut to learn proprio-copying) and tasks are multi-phase bimanual with state aliasing. Consistent with SeedPolicy note (naive frame stacking degrades, structured temporal state helps).
Relevance: Directly speaks to our SmolVLA fine-tune: VLM visual tokens may lose geometric detail; adding a frozen dense encoder (DINOv2-S/B) feature path to the action expert is a plausible cheap fix. Scale (V-JEPA2-g, DINOv2-g) is not laptop-friendly; would need small variants — untested. Pumpkin pick-place is single phase, where temporal gains are expected to be smaller.
Decision impact:
 - Q03 vision encoder: supports adding frozen dense self-supervised features (DINOv2 +17 pp, V-JEPA2 +30 pp) beside VLM features — M (sim only, 100 rollouts x 10 tasks, giant encoders)
 - Q07 history: supports short history (2-4 frames @4 fps, 0.5-1 s) via frozen video encoder; longer (16f) degrades — L/M (sim, bimanual multi-phase)
 - Q12 model size: weak evidence that a 3B VLA fine-tuned on 50 demos underperforms without extra visual path (35.7%) — L
