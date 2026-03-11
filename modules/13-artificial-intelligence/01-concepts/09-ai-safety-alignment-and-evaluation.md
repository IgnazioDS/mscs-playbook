# AI Safety, Alignment, and Evaluation

## Overview
AI safety focuses on aligning system behavior with human goals and preventing
harmful outcomes through robust evaluation.

## Why it matters
Misaligned or unsafe AI systems can cause real-world harm, especially when
scaled.

## Key ideas
- Alignment ensures objectives reflect human intent
- Safety evaluates robustness and edge cases
- Monitoring catches drift and unexpected behavior
- Evaluation should include adversarial scenarios

## Practical workflow
- Define safety constraints and guardrails
- Build evaluation sets for failure modes
- Stress-test with red-team scenarios
- Establish monitoring and rollback plans

## Failure modes
- Reward hacking or specification gaming
- Overreliance on narrow benchmarks
- Safety regressions after updates
- Lack of oversight and auditability

## Checklist
- Document safety requirements and risks
- Maintain a regression suite for critical tasks
- Implement human-in-the-loop controls
- Log decisions for post-incident analysis

## References
- NIST AI Risk Management Framework — https://www.nist.gov/itl/ai-risk-management-framework
- Alignment overview — https://arxiv.org/abs/2209.00626
