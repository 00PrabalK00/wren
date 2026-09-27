# KnowledgeInsulation — Knowledge Insulating Vision-Language-Action Models: Train Fast, Run Fast, Generalize Better (2025, arXiv 2505.23705)
Setup: π0 architecture (PaliGemma 3B backbone + 300M flow action expert with width 1024 / mlp 4096 / depth 18). H=50, τ via adaRMSNorm, π0 Beta τ-schedule.
Proposed recipe ("ours"):
 - (1) Joint training: the backbone predicts FAST tokens (CE) while the expert does flow matching on continuous actions. The two action representations are masked from each other, and the backbone never attends to the expert.
 - (2) STOP-GRADIENT on the backbone keys/values as seen by the expert, so flow gradients never reach the VLM. This allows loss weight α=1.
 - (3) Co-training with VLM data (captioning, VQA, detection) and robot-planning data.
Inference uses only the expert (continuous, fast). Training cost is +20% per step.
Baselines retrained on the same data:
 - π0 (flow only, full gradient)
 - π0-FAST (autoregressive)
 - OpenVLA-OFT-style parallel decoding (without FiLM)
 - Transfusion (diffusion in the shared backbone)
 - HybridVLA-like (AR tokens CAN attend to diffusion inputs)
 - joint-training without stop-grad, with and without VLM data
 - frozen backbone
 - naive tokens instead of FAST as the representation objective
Real tasks, 10 episodes per task per policy, two-sided t-tests: items-in-drawer (single arm, unseen env), table bussing (12 objects, language-commanded), T-shirt folding (bimanual), and 4 mobile-manipulation tasks in unseen homes. Also DROID (same 44-trial protocol as FAST) and LIBERO.
Claim: gradients from a randomly initialised continuous action expert damage the pretrained VLM (worse language following, slow convergence). Training the backbone on discrete tokens while stop-gradding the expert gives fast training, fast inference, and better generalisation.
Evidence:
 - DROID (unseen scenes): ours 0.55±0.09, π0 0.49±0.09, π0-FAST 0.45±0.09.
 - LIBERO (Spatial / Object / Goal / Long / 90):
   - OpenVLA-OFT 97.6 / 98.4 / 97.9 / 94.5 / –
   - π0 96.8 / 98.8 / 95.8 / 85.2 / –
   - π0-FAST 96.4 / 96.8 / 88.6 / 60.2 / –
   - ours-from-scratch 96.6 / 97.2 / 94.6 / 84.8 / 92.7
   - ours fine-tuned from generalist 98.0 / 97.8 / 95.6 / 85.8 / 96.0
   - Also listed: BAKU Long 86.0 / 90 90.0; MoDE Long 94.0 / 90 95.0.
   - Ours is WORSE than OFT on Long (85.8 vs 94.5).
 - Convergence (generalist bussing, Fig 6b): π0 needs 7.5× as many training steps as ours or π0-FAST to reach similar performance (figure; the ratio is stated in the caption).
 - Items-in-drawer (unseen env, Fig 4): ours > all baselines on task progress AND language following. π0 and joint-training without stop-grad ignore language. π0-FAST keeps language following but fails to open the drawer precisely and moves slowly. HybridVLA and frozen backbone are "not viable". Figure only.
 - Bussing specialist (Fig 5): ours best. Joint-training is also good. π0-FAST needs 2× wall-clock per task. Transfusion is good but slower. OFT-style parallel decoding follows language and is fast but has the lowest task performance. π0 struggles with language.
 - Inference rates: π0 action expert ≈ 10 Hz vs autoregressive VLA 1.3 Hz (π0-FAST ≈ 750 ms per chunk on a 4090).
Ablations:
 - Freezing the pretrained VLM and training only the new expert gives 0% on items-in-drawer and shirt folding (Fig 4a, Fig 8). The authors conclude "VLM representations are insufficient for robotics".
 - Stop-grad vs no stop-grad: no stop-grad harms language following. This harm largely disappears IF VLM data is co-trained. For the generalist, removing VLM data hurts joint-training (no stop-grad) most.
 - Discrete representation objective: naive per-step tokens as the auxiliary objective is better than continuous-only but worse than FAST. Naive tokens subsampled with stride 5 beat dense naive tokens.
 - AR tokens attending to continuous actions (HybridVLA) significantly hurts. Keeping the two representations mutually masked matters.
 - VLM co-training matters most for OOD objects ("OOD follow rate", mobile, Fig 7).
 - State as text vs continuous projection: both work (Fig 10, appendix).
Failure/limitations: authors cite +20% training compute and language following that is "still far from perfect" because of data correlations. Critical read:
 - Nearly all real results are bar charts over 10 trials.
 - Every experiment is 3B-backbone + 300M-expert with hundreds to thousands of hours of data.
 - The "freezing gives 0%" result uses PaliGemma features with no robot pretraining, on hard dexterous tasks. It says nothing about frozen self-supervised vision encoders (DINOv2) in small policies.
 - LIBERO-Long gains are absent.
Conflicts:
 - vs SmolVLA: SmolVLA trains ONLY a 100M expert on a FROZEN SmolVLM (first 16 layers) and works well on SO-100 and LIBERO (87.3). Here freezing gives 0%. Likely reasons: (a) SmolVLA pretrains the expert on 23k in-embodiment episodes; (b) its tasks are simpler and lower-frequency; (c) it uses mid-layer features, not last-layer ones. GR00T likewise freezes the LLM but UNFREEZES the vision encoder and reads layer 12.
 - vs OpenVLA-OFT/VLA-Adapter: those fine-tune the backbone jointly with an L1/parallel head and do well on LIBERO (OFT 94.5 on Long, beating ours). Here OFT-style is worst on real bussing. The data regime and task dexterity differ.
 - vs π0.5: this paper is the single-stage formalisation of π0.5's two-stage recipe and agrees with it.
Relevance for a ~10–50M policy on a pretrained vision encoder:
 - The transferable mechanism is gradient interference: a freshly initialised generative head, early in training, sends noisy gradients into a pretrained encoder and destroys useful features.
 - Cheap analogues (my extrapolation, not tested at small scale): lower backbone LR or warm-up freeze of the encoder; an auxiliary deterministic action loss on the encoder features (L1 regression or coarse-binned/DCT targets) that shapes the representation, with stop-grad from the flow head; a flow head that reads detached features.
 - Their evidence that "frozen = 0%" argues AGAINST fully frozen generic features for precise manipulation. "Full gradient from a flow head" converges slowly (7.5× steps).
 - The "discrete tokens converge faster than flow" finding suggests pairing flow with an auxiliary regression/classification loss for sample-efficient training on 50–100 demos. This is plausible but unverified at our scale.
Decision impact:
 - Q03 vision: weakens a fully frozen pretrained backbone for precise tasks (0% on drawer/shirt). Supports fine-tuning the backbone with a clean, stable learning signal and protecting it from gradients of a freshly initialised generative head — M (large-model evidence, mechanism likely transfers).
 - Q01 action head: supports flow expert at inference + auxiliary discrete/deterministic action objective for representation learning (π0 flow-only needs 7.5× more steps; DROID 0.55 vs 0.49) — M for large models, L for 10–50M.
 - Q09 aux objectives: supports an auxiliary action-token objective (FAST > stride-5 naive > dense naive > none) with the two heads masked from each other — M.
 - Q10 latency: small expert ≈ 10 Hz vs autoregressive 1.3 Hz. Autoregressive π0-FAST takes 2× wall-clock per task — M/H.
 - Q08 language: gradients from a new expert erode language following. VLM-data co-training or stop-grad restores it — M (relevant only if we add a second language-conditioned task).
