---
tags:
  - archive
  - 04-case-studies
status: stable
---

# Case Study: Experiment Sizing and Sanity Checks

## Overview
A product team wants to run an A/B test on a checkout flow. The goal is to
estimate conversion lift while controlling risk and compute cost.

## Requirements
- Detect a 2% relative lift with 80% power
- Control false positives at 5%
- Daily traffic: 200k users

## Approach
1. Define baseline conversion (p0) from historical data.
2. Set minimum detectable effect (MDE) to 2% relative.
3. Use a two-proportion sample size estimate.
4. Validate with a short "A/A" test for instrumentation sanity.

## Key Decisions
- Use daily randomization by user ID to avoid spillover.
- Track primary metric (conversion) and guardrails (latency, error rate).
- Pre-register stopping rules.

## Implementation Notes
- Store raw events and aggregate daily counts.
- Use consistent time windows and exclude partial days.
- Verify unit consistency (percentage vs fraction).

## Outcomes
- Sample size per variant: ~1.5M users (about 7.5 days at 200k/day).
- A/A test shows no significant difference, indicating clean instrumentation.

## Pitfalls
- Peeking and early stopping without correction
- Multiple comparisons without adjustments
- Mixing cohorts with different traffic sources

## References
- Kohavi et al., *Trustworthy Online Controlled Experiments*
- OpenIntro Statistics (sample size for proportions)


## Related Concepts

- [Discrete Mathematics Basics](../01-concepts/01-discrete-mathematics-basics.md)
- [Proof Techniques for Computer Science](../01-concepts/02-proof-techniques-for-computer-science.md)
- [Counting and Combinatorics Basics](../01-concepts/03-counting-and-combinatorics-basics.md)
