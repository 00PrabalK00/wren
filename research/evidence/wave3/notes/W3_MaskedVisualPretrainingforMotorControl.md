# W3_MaskedVisualPretrainingforMotorControl — Masked Visual Pretraining for Motor Control (MVP) (2022, arXiv 2203.06173)
Setup: SIM ONLY (IsaacGym PixMC: Franka and Kuka+Allegro; reach, cabinet, pick, move — 8 tasks), single egocentric camera, PPO RL (no demos), frozen ViT-S MAE encoder (CLS token → 128-d) + proprio → MLP [256,128,64], delta joint actions; 15 runs per task/model (3 LR × 5 seeds). All results are figures only.
Claim: MAE pretraining on in-the-wild human-object-interaction images (HOI, ~700k frames) yields frozen features that beat supervised ImageNet encoders for RL from pixels.
Evidence (figures only, qualitative): MVP beats supervised ImageNet ViT on 7/8 tasks, up to +80 abs success; matches oracle state on 5/8. Supervised baseline flat at 0 on pick/move tasks.
Ablations (figures only):
 - HOI vs ImageNet MAE pretraining data: HOI better on 7/8 tasks.
 - Random frozen encoder: 0 on 6/8 tasks.
 - Unfrozen (end-to-end RL) encoder: unstable/NaN, 0 success even from MAE init (RL-specific).
 - ViT-B vs ViT-S: larger encoder did NOT improve.
 - MAE vs CLIP ViT-B: MAE better "promising signal"; MoCo-v3 non-trivial but weaker.
 - Distractors (color/shape): marginal drop; size distractor → ~50% (scale ambiguity, single camera).
 - Stability: MVP far less sensitive to LR than supervised encoder.
Failure/limitations: sim, RL, figures only; end-to-end finetune failure is an RL-optimization artifact, not evidence for BC.
Conflicts: later work (R3M, VC-1 CortexBench, Dasari et al. "Unbiased look at datasets for visuo-motor pretraining", H-InDex) found ImageNet ResNet or even in-domain training competitive and MAE-ViT not uniformly best; H-InDex (in this set) finds frozen ImageNet RN50 81.3 > MVP 63.1 on Adroit. For BC with demos, fine-tuned encoders usually beat frozen.
Relevance: low for our BC + fine-tuning setting. Only relevant point: frozen pretrained features beat random/scratch when the downstream signal is weak; bigger encoder not better.
Decision impact:
 - Q03 vision encoder: supports self-supervised (MAE) pretrained > supervised ImageNet ViT when FROZEN under RL (figure only); weakened by later contradicting studies — confidence L.
 - Q12 model size: ViT-B not better than ViT-S for frozen features — confidence L (figure only, preliminary).
