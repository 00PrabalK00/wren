# W3_ObjectVLAEndtoEndOpenWorldObjectManipula — ObjectVLA: End-to-End Open-World Object Manipulation Without Demonstration (2025, arXiv 2502.19250)
Setup: Franka, 2 external ZED cams + RealSense D435i wrist cam. DiVLA (2B diffusion-VLA) co-trained on robot demos + image-text pairs with bounding boxes (robot-to-VL ratio 10:1). The robot data carries a localization "reasoning" string mirroring the VL data. Tasks: "move to object" (4 trials/object, success only if all 4 correct), push/rotate (40 demos per skill-object, 400 total; 5 ID + 20 OOD objects x 3 trials), instruction-driven bin picking (600 demos; 11 ID + 50 OOD objects x 3 trials). Smartphone-photo continual fine-tuning for 2 new objects (10 trials each, figure).
Claim: co-training with box-grounded image-text data about objects lets a VLA manipulate objects never seen in robot demos.
Evidence:
 - Move-to (Fig. 5): all variants 100% ID. OOD objects: DiVLA robot-only 8% (~chance), co-train without bbox/reasoning 19%, ObjectVLA 64%.
 - Bin picking (Table 2): OpenVLA ID 14/33, OOD 17/150; ObjectVLA ID 21/33, OOD 87/150.
 - Push/rotate: OOD ~two-thirds of trials succeed. Most OOD failures are skill execution (insecure grasp), not wrong-object selection.
Ablations: bbox grounding + mirrored reasoning format: 19% -> 64% OOD. More robot data than 10:1 lowered in-domain success (stated; the authors attribute this to the 2B model's limited capacity).
Failure/limitations: authors say the method "struggles to generalize to novel backgrounds and lighting conditions". The image-text data was captured by the robot cameras or a phone in the same scene. The strict 4/4 criterion makes numbers look lower than raw trial rates.
Conflicts: supports the view that fine-tuning a VLM-based policy on narrow robot data overwrites pretrained visual concepts (robot-only fine-tune ~8% on OOD objects, even for objects the VLM surely knew, like Pikachu). This matches our observation that the SmolVLA fine-tune breaks on a different-looking pumpkin. It contrasts with claims that VLA pretraining alone gives object generalization.
Relevance: medium for diagnosis, low for adoption (2B model; our GPU and latency budget rule it out). Practical transfer: if we keep a VLM-based policy, co-train on (image, "pumpkin" bbox) pairs of many pumpkin-like objects photographed in our scene, or freeze more of the VLM. For a small policy, the equivalent is object-appearance diversity in demos/augmentation or an open-vocabulary detector front-end.
Decision impact:
 - Q14 novel objects: + co-training with grounded image-text pairs (8% -> 64% OOD object selection); robot-only fine-tuning of a VLA ~chance on OOD objects — confidence M (real, many objects, but 2B model)
 - Q03 encoder: - full fine-tuning of a pretrained VLM backbone on narrow robot data (catastrophic forgetting of visual concepts) — confidence M
 - Q08 language: ~ language helps object selection only when grounded (bbox) data is mixed in — confidence L-M
 - Q14 lighting/background: - no gain; authors report failure on novel backgrounds/lighting — confidence L
