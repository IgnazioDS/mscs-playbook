# Reinforcement Learning Cheat Sheet

## MDP notation and Bellman equations
- States: S, Actions: A, Rewards: R, Transition: P, Discount: gamma
- Bellman expectation: V^pi(s) = E[R + gamma V^pi(s')]
- Bellman optimality: V*(s) = max_a E[R + gamma V*(s')]

## Algorithm selection
- DP: full model, small MDPs
- MC: episodic, model-free
- TD: continuing tasks, faster learning
- PG: continuous actions, stochastic policies
- AC: PG + value baseline

## Hyperparameter checklist
- gamma: long-term vs short-term
- alpha: learning rate
- epsilon: exploration rate
- entropy bonus: exploration for PG
- clip range: PPO stability

## Common bugs
- Leaky environment reset
- Off-by-one in episode termination
- Reward scaling too large/small
- Incorrect discounting or bootstrapping

## Evaluation
- Run multiple seeds
- Track learning curves and variance
- Use success metrics and episode length
- Compare to baselines

## Reward shaping do/don't
- Do keep shaping aligned with objectives
- Do test for reward hacking
- Don't change optimal policies unintentionally
- Don't over-penalize exploration

## Safety notes
- Add constraints for risky actions
- Watch for distribution shift
- Use conservative methods for offline RL
