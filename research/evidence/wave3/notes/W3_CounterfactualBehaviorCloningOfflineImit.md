# W3_CounterfactualBehaviorCloningOfflineImit — Counterfactual Behavior Cloning: Offline Imitation Learning from Imperfect Human Demonstrations (2025, arXiv n/a in text)
Setup: Counter-BC = Gaussian-policy BC with 2-layer MLP (CNN for Car Racing), loss minimizes policy entropy within a radius Δ (=0.4 on unit-normalized actions) around each demonstrated action. Envs: Intersection, Cartpole, Car Racing (96×96 images), Robomimic Can multi-human (state-based, 300 demos from 6 operators of mixed skill), real air hockey robot with in-person teleop demonstrators; baselines BC, BCND, ILEED, etc.; ~5× BC training time.
Claim: letting the learner "move" noisy human actions within a small neighborhood to reach a low-entropy, simpler policy beats plain BC and label-free weighting methods on imperfect human data.
Evidence: all main results are figure-only (qualitative): Counter-BC ≥ baselines across noise types and dataset sizes, including real human demos and air hockey (more hits). No tables with exact numbers in extracted text.
Ablations: Δ trades simplicity vs fidelity (1-D toy, figure only); recommended Δ 0.2–0.5.
Failure/limitations: stated: struggles with multimodal policies (entropy minimization collapses modes); Δ hand-tuned; low-dimensional continuous actions. My read: unimodal Gaussian MLP, state inputs mostly, no chunking, no modern visuomotor baselines.
Conflicts: opposite philosophy to generative heads (diffusion/CVAE) that model demo multimodality; relevant only if our human noise is jitter rather than genuine multimodality.
Relevance: low. Idea (denoise/regularize noisy teleop actions, e.g. by smoothing targets) is mildly relevant to SO-101 jittery leader-arm data, but evidence is unimodal-MLP and figure-only.
Decision impact:
 - Q13 data quality: denoising imperfect human actions toward a simpler policy helps vs plain BC (figure only) — weak support for action smoothing/denoising of teleop data — confidence L.
 - Q01 action head: entropy-minimizing unimodal approach explicitly fails on multimodal tasks (stated) — neutral/weak — confidence L.
