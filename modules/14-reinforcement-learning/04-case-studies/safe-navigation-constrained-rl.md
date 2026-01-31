# Safe Navigation with Constrained RL

## Problem and constraints
- Navigate a robot to a goal while avoiding unsafe regions
- Safety constraints must never be violated
- Limited exploration in real environments

## MDP formulation (S, A, R, P, gamma)
- S: robot position, velocity, and obstacle map
- A: velocity commands
- R: negative step cost, positive goal reward
- P: stochastic dynamics with noise
- gamma: 0.9

## Algorithm choice and why
- Constrained RL with safety-aware policy updates
- Safe exploration using a constraint penalty or shield

## Training setup (env, reward, exploration)
- Simulated environment with safety constraints
- Reward shaping for safe progress
- Conservative exploration policy

## Evaluation plan
- Track constraint violations (must be zero)
- Measure success rate and path length
- Test across varied obstacle maps

## Failure modes and mitigations
- Constraint violations during training: use safety filters
- Reward conflicts with safety: prioritize constraint satisfaction
- Overfitting to sim: domain randomization

## What I would ship checklist
- [ ] Safety constraint verification
- [ ] Simulation-to-real transfer tests
- [ ] Monitoring for near-violation behavior
- [ ] Fallback safe controller
- [ ] Human override and stop controls
