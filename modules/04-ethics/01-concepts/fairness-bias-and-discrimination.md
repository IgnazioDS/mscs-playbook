# Fairness, Bias, and Discrimination

## What it is

Systematic differences in outcomes across groups due to data, design, or model behavior.

## Why it matters

Unfair systems can amplify discrimination and cause measurable harm.

## Core concepts

- Representation bias in data collection
- Measurement bias in labels or proxies
- Group fairness metrics (e.g., parity, equalized odds)

## Common failure modes

- Using biased historical data without auditing
- Optimizing overall accuracy while harming minorities
- Ignoring intersectional groups and small sample sizes

## Engineering checklist

- Define protected groups and harm scenarios
- Compute group metrics and error rates
- Run bias audits on data and predictions

## References

- Fairness and Machine Learning (Barocas et al.)
- NIST AI Risk Management Framework
