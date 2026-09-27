# W3_WhenShouldWePreferOfflineReinforcementLe — When Should We Prefer Offline Reinforcement Learning Over Behavioral Cloning? (2022, ICLR, arXiv 2204.05618)
Setup: Theory + SIM only (gridworlds, AntMaze, Adroit from state, scripted image-based pick/place/open/grasp from Singh et al. COG, 7 Atari games); CQL (offline RL with reward labels) vs BC (old-style single-step BC, no chunking/generative head), 3 seeds; no real robot.
Claim: With sparse rewards, "critical states" and long horizons, offline RL (tuned offline) beats BC even on expert data, and offline RL on noisy-expert data beats BC on the same amount of expert data.
Evidence: image manipulation, BC(expert) vs tuned CQL(expert): pick-place-open-grasp 14.5 vs 23.5; close-open-grasp 17.4 vs 49.7; open-grasp 33.2 vs 51.9. CQL on noisy-expert data: 85.7 / 90.3 / 92.4. Adroit human: BC 71.0/86.3/73.0 vs tuned CQL 78.1/79.1/74.1 (mixed). Naive (untuned) CQL often ≤ BC.
Ablations: data noisiness sweep in gridworld (figure only, qualitative: RL advantage grows with noise); gap grows with horizon H.
Failure/limitations / critical read: baselines are weak BC (success 14–33% on scripted tasks) with no action chunking, no generative heads, no pretrained encoders; requires reward labels and careful offline tuning; entirely sim. Not a design guide for a 50–100-demo teleop pumpkin task.
Relevance: Low. Only a qualitative hint for Q13: noisy/perturbed demonstrations that cover recovery states are valuable if some return/advantage signal is used; for pure BC, recovery coverage is what matters.
Decision impact:
 - Q13 data: noisy-expert data + offline RL 86–92% vs BC on equal expert data 15–33% (sim, weak BC) — weak support for collecting perturbed/recovery data and using success-weighting — confidence L.
