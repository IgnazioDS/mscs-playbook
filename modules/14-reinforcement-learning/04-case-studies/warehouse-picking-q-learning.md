# Warehouse Picking with Q-Learning

## Problem and constraints
- Optimize robot picking routes to minimize travel time
- Avoid collisions and dead ends
- Limited compute on edge devices

## MDP formulation (S, A, R, P, gamma)
- S: robot position and remaining pick list
- A: move directions and pick action
- R: negative step cost, positive pick reward
- P: stochastic transitions due to slippage
- gamma: 0.9 for long-term planning

## Algorithm choice and why
- Q-learning for model-free control in discrete grids
- Suitable for sparse reward and small state spaces

## Training setup (env, reward, exploration)
- Simulated warehouse grid environment
- Reward shaping for approaching targets
- Epsilon-greedy exploration with decay

## Evaluation plan
- Measure average steps per episode
- Track success rate and collision count
- Compare to shortest-path baseline

## Failure modes and mitigations
- Reward hacking: cap shaping rewards
- Overfitting to map layout: randomize obstacles
- Slow convergence: increase exploration or learning rate

## What I would ship checklist
- [ ] Safety constraints for collisions
- [ ] Regression tests on fixed maps
- [ ] Monitoring for drift in layout
- [ ] Latency benchmarks on target hardware
- [ ] Rollback plan for policy updates
