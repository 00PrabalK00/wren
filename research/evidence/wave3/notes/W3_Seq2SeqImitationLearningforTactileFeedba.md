# W3_Seq2SeqImitationLearningforTactileFeedba — Seq2Seq Imitation Learning for Tactile Feedback-based Manipulation (2023, arXiv 2303.02646)
Setup: NO VISION. Force/wrench + pose inputs only; POMDP where the target pose (rail / door) is hidden and must be inferred by exploratory contacts. Transformer encoder aggregates an interaction history → decoder outputs a pose sequence (skill trajectory); DAgger-style collection. Sim door-open (expert = SAC oracle) and real snap-on insertion (human expert), 50 demos; 100 test runs per method (Table I); real robustness 102 random poses.
Claim: a transformer seq2seq over the contact-interaction history infers hidden state and solves tactile POMDP tasks from 50 demos where RL/BC fail.
Evidence (Table I, success door-open sim / snap-on real): expert 95/100; SQIL 20/–(failed); BC-LSTM 11/5; Seq2Seq-LSTM 56/0; Seq2Seq (transformer) 76/84; Seq2Seq-Oracle (supervised hidden-state) 89/88. Real robustness: 84/102 random rail poses; fixed poses 20/20, 20/20, 18/20.
Ablations: LSTM vs transformer encoder of history (above); demos 5 → 200 (real, 45 tests): improves rapidly and converges after ~50 demos (figure only); hidden-pose estimate converges after ~4 exploration steps.
Failure/limitations: tactile-only, pose-control skill primitives, DAgger; not a visuomotor policy.
Relevance: low. Our tasks are vision-driven pick-place; no force sensing on SO-101. Only generic points: history helps when state is truly unobservable from the current observation (contacts), and ~50 demos saturation for a narrow task.
Decision impact:
 - Q07 observation history: history via transformer helps in a genuinely partially-observable (tactile) task; transformer ≫ LSTM for history (84 vs 0 real) — confidence L (no vision; not our failure mode).
 - Q13 data quantity: performance converges ~50 demos for a narrow real insertion task (figure only) — confidence L.
