# Dynamic Programming: Policy Evaluation and Control

## Overview
Dynamic programming solves MDPs with full model knowledge using Bellman
equations.

## Why it matters
DP provides ground-truth baselines and clarifies value and policy relationships.

## Key ideas
- Policy evaluation computes V^pi
- Policy improvement yields better policies
- Value iteration alternates evaluation and improvement
- Requires full transition dynamics

## Practical workflow
- Define transition model and rewards
- Implement iterative policy evaluation
- Use value iteration for control
- Track convergence with delta thresholds

## Failure modes
- Large state spaces make DP intractable
- Incorrect transition models lead to wrong values
- Poor convergence criteria cause oscillations
- Discount factor too high slows convergence

## Checklist
- Validate Bellman backups with small MDPs
- Monitor max value changes per iteration
- Use small gamma for unstable dynamics
- Compare to known analytical solutions

## References
- Sutton & Barto Chapter on DP
- Bellman equations — https://web.stanford.edu/class/cs234/lecture2.pdf
