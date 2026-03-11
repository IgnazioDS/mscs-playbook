# Reward Design and Shaping

## Overview
Reward design defines the learning signal and can accelerate training through
shaping.

## Why it matters
Poor rewards lead to unintended behaviors and misaligned policies.

## Key ideas
- Sparse rewards slow learning
- Shaping adds intermediate incentives
- Potential-based shaping preserves optimal policies
- Reward scaling affects stability

## Practical workflow
- Start with a clear task objective reward
- Add shaping terms aligned to desired behavior
- Normalize rewards to stable ranges
- Monitor for reward hacking

## Failure modes
- Shaping that changes optimal policy
- Reward hacking and loopholes
- Over-penalization discouraging exploration
- Inconsistent rewards across environments

## Checklist
- Verify shaping with ablation studies
- Track reward distributions over time
- Test for unintended behavior
- Document reward components and weights

## References
- Potential-based shaping — https://dl.acm.org/doi/10.1023/A:1022676722315
- Reward design survey — https://arxiv.org/abs/2006.04830
