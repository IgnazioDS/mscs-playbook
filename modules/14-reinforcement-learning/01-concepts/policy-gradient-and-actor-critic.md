# Policy Gradient and Actor-Critic

## Overview
Policy gradient methods optimize policies directly, while actor-critic combines
policy learning with value estimation.

## Why it matters
Policy-based methods handle continuous actions and stochastic policies well.

## Key ideas
- REINFORCE uses Monte Carlo returns
- Actor-critic uses a critic for variance reduction
- Entropy regularization encourages exploration
- PPO and TRPO stabilize policy updates

## Practical workflow
- Choose policy parameterization and action distribution
- Train with advantage estimates and baselines
- Tune learning rates, clip ranges, and entropy
- Monitor policy stability and KL divergence

## Failure modes
- High variance gradients in REINFORCE
- Policy collapse without entropy bonus
- Instability from large policy updates
- Sample inefficiency in complex environments

## Checklist
- Track entropy and KL to detect collapse
- Use advantage normalization
- Compare against value-based baselines
- Run multiple seeds for reliability

## References
- Policy Gradient Theorem — https://proceedings.neurips.cc/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html
- PPO — https://arxiv.org/abs/1707.06347
