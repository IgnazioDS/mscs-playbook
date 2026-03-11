# Temporal-Difference Learning

## Overview
Temporal-difference (TD) methods learn from incomplete episodes by bootstrapping
value estimates.

## Why it matters
TD methods combine the efficiency of DP with the model-free setting of MC.

## Key ideas
- TD(0) updates using immediate reward and next value
- SARSA and Q-learning are core TD control methods
- Bootstrapping reduces variance but can introduce bias
- Eligibility traces connect TD and MC (TD(lambda))

## Practical workflow
- Choose on-policy (SARSA) or off-policy (Q-learning)
- Tune learning rate and exploration schedule
- Monitor value convergence and policy stability
- Use experience replay for stability in complex tasks

## Failure modes
- Divergence with function approximation
- Overestimation bias in Q-learning
- Poor exploration leads to suboptimal policies
- Non-stationary rewards destabilize learning

## Checklist
- Validate TD updates with small MDPs
- Track Q-value ranges and variance
- Ensure epsilon decay is well-behaved
- Compare SARSA vs Q-learning performance

## References
- Sutton & Barto Chapter on TD
- Q-learning — https://link.springer.com/article/10.1023/A:1022676722315
