# FAILDetect — Can We Detect Failures Without Failure Data? Uncertainty-Aware Runtime Failure Detection for IL Policies (RSS 2025, arXiv 2503.08558, TRI)
Setup: DP and flow-matching policies. Sim Robomimic Square, Transport, Can, Toolhang (2000 test rollouts; OOD = third-person camera bumped 10 cm up mid-rollout at t=50). Hardware: bimanual Franka, FoldRedTowel (human disturbance mid-task; OOD crumpled towel + unseen distractor) and CleanUpSpill; 50 hardware rollouts. Two stages: (1) train a scalar score from SUCCESSFUL data only on policy inputs/outputs (obs embeddings O_t with 2 obs steps, optionally actions); (2) time-varying conformal-prediction band calibrated on successful rollouts; alarm when score exits band.
Scores compared: learned logpZO (flow density — norm of the noise obtained by integrating a CNF from the observation embedding), logpO, RND, NatPN, DER, CFM; post-hoc STAC, PCA-kmeans, SPARC.
Evidence:
 - Sim (16 cases): logpZO top-1 combined accuracy in 10/16 and top-3 in 14/16; RND top-1 5/16, top-3 9/16; STAC top-3 8/16, PCA-kmeans 3/16. Learned methods detect fastest; STAC slowest, often after the average success time ("not practical").
 - Hardware (12 cases): logpZO top-1 8/12, top-3 11/12; RND always top-3 but never top-1; PCA-kmeans top-1 4/12. Score spikes align with physical events (towel pulled, bad fold).
 - STAC with 256 samples/step was too slow to run in real time on hardware → omitted.
Ablations: many score families; setting-dependent vs ID-only CP band.
Failure/limitations: detection only, no recovery; learned score network is an extra model; 50 real rollouts; per-step thresholding criticized by FIPER as producing false alarms (its w=1 variant had very low TNR in FIPER's tests).
Conflicts: STAC (Sentinel) practical cost issue here vs Sentinel's positive results; FIPER shows adding action entropy and windowing improves over logpZO-style obs-only single-step scores.
Relevance to SO-101: supports observation-embedding density/novelty as the cheapest reliable failure score; catches camera bumps (a failure we have observed: slightly moved camera). The CNF/RND score on the policy's own embedding costs a small MLP per step.
Decision impact:
 - Monitor on policy observation embedding (RND or flow density), calibrated with conformal bands from ~successful rollouts — SUPPORTED — M.
 - Avoid heavy multi-sample (B=256) consistency monitors at control rate — SUPPORTED — M.
