# Evaluation for LLMs and Guardrails

## Overview
Evaluation measures quality, safety, and reliability while guardrails enforce
policies at runtime.

## Why it matters
LLM outputs are probabilistic, so continuous evaluation and enforcement prevent
silent regressions and unsafe behavior.

## Key ideas
- Offline evals use golden datasets and rubric-based scoring
- Online evals monitor live traffic and user feedback
- Guardrails include input filtering, output validation, and tool gating
- Regression testing prevents prompt and model drift

## Practical workflow
- Build a small, high-quality eval set per task
- Add automated checks for format, citations, and safety
- Run A/B tests or shadow evals for model changes
- Track failure categories and close the loop

## Failure modes
- Overfitting to the eval set
- Metrics that miss factuality or hallucinations
- Guardrails that are too strict and harm usability
- Unmonitored model updates causing regressions

## Checklist
- Define quality, safety, and latency targets
- Log and label failures for root-cause analysis
- Add schema validation and rejection handling
- Re-run evals for every prompt or model update

## References
- HELM: Holistic Evaluation of Language Models — https://arxiv.org/abs/2211.09110
- LM Evaluation Harness — https://github.com/EleutherAI/lm-evaluation-harness
