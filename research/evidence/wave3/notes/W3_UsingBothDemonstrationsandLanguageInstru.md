# W3_UsingBothDemonstrationsandLanguageInstru — Using Both Demonstrations and Language Instructions to Efficiently Learn Robotic Tasks (DeL-TaCo) (2023, ICLR, arXiv 2210.04476)
Setup: SIM ONLY (Roboverse/PyBullet WidowX pick-and-place), ~300 tasks (objects x colors x shapes x bins); multi-task BC with ResNet-18 + spatial softmax policy; task conditioning on a single demo video embedding (small CNN, contrastive task-encoder loss) and/or frozen miniLM language embedding. Eval 2 trials/task x all test tasks x 3 seeds (thousands of trials). Zero-shot to novel tasks.
Claim: Conditioning on demo + language jointly disambiguates task specification and generalizes to novel objects/colors/shapes better than either alone.
Evidence (Scenario A novel objects/colors/shapes, success %): one-hot 4.9; oracle 69.3; CLIP-frozen lang-only 14.4 / demo-only 3.5 / both 15.8; miniLM lang-only 17.1; CNN demo-only 20.8; DeL-TaCo 25.8; BC-Z 6.7; MCIL 7.5. Scenario B (novel colors/shapes): lang-only 25.4, demo-only 20.0, both 31.6. Demo-only needs fine-tuning on 50 demos per new task (26.1) to match DeL-TaCo zero-shot (25.8); 100 demos → 32.9.
Ablations (Table 8, Scenario A; flattened table, mapping moderately confident):
 - Conditioning architecture: FiLM(demo)+concat(lang) 25.8 > FiLM(both) 22.4 >> concat(both) 7.9 → FiLM injection into the CNN is important for at least one modality.
 - Task-encoder loss: contrastive 25.8 vs cosine-to-language (BC-Z style) 12.5 vs none 10.0.
 - Language encoder: DistilBERT 27.1, DistilRoBERTa 25.2, miniLM 25.8 (small LMs all fine); frozen CLIP ~10.7–11.8.
 - Demo encoder: pretrained R3M + MLP 13.5 vs scratch CNN 25.8 (sim domain gap).
Failure/limitations: sim only; absolute success low (≤32%); multi-task zero-shot novel-task setting, not single-task robustness; R3M/CLIP inferiority likely due to sim-vs-real image gap (authors say so).
Conflicts: FiLM > late concat agrees with BC-Z/RT-1 practice; late concat of language as in many small VLAs is here the weaker option. Pretrained visual encoders (R3M/CLIP) underperform scratch CNN in sim — typical sim artifact; real-world papers usually show opposite.
Relevance: Only matters if we add a second object with language. Suggests: a small frozen sentence encoder (miniLM/DistilBERT) is enough; inject language via FiLM into the vision backbone rather than only concatenating to the final feature.
Decision impact:
 - Q08 language conditioning: FiLM injection >> plain concat (22.4–25.8 vs 7.9); small frozen text encoders (miniLM, DistilBERT) suffice — supports FiLM + small LM — confidence L (sim, multi-task zero-shot setting).
