# Ethics in the ML Lifecycle

## What it is

Integrating ethics and safety checks across data, training, deployment, and monitoring.

## Why it matters

Most harms occur during handoffs and deployment, not just training.

## Core concepts

- Data sourcing and consent checks
- Model evaluation with fairness and robustness
- Monitoring for drift and harm signals

## Common failure modes

- No monitoring for post-deployment regressions
- Evaluation only on average metrics
- Unclear rollback criteria

## Engineering checklist

- Define pre-launch go/no-go criteria
- Track drift and outcome metrics post-launch
- Run incident drills and retrospectives

## References

- Google Model Card Toolkit docs
- Responsible AI practices (major provider docs)
