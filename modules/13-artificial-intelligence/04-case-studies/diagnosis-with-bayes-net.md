# Diagnosis with Bayes Net

## Problem and constraints
- Diagnose system faults from noisy sensor readings
- Require probabilistic explanations and confidence
- Support incomplete observations

## Modeling choices
- Bayesian network with causal dependencies
- Conditional probability tables from data or experts
- Evidence nodes for observed symptoms

## Algorithm choice and why
- Bayesian inference to compute posterior probabilities
- Variable elimination for efficient queries

## Evaluation plan
- Compare posterior accuracy against labeled cases
- Measure calibration and confidence intervals
- Stress-test with missing or noisy inputs

## Failure modes and mitigations
- Incorrect dependencies: validate structure with experts
- Uncalibrated probabilities: apply calibration methods
- Computational blowups: use approximate inference

## Operational considerations
- Log evidence and diagnosis for audits
- Provide explainable outputs for operators
- Update CPTs as new data arrives

## What I would ship checklist
- [ ] Validated network structure and CPTs
- [ ] Calibration checks for probabilities
- [ ] Fallback to approximate inference
- [ ] Operator-facing explanations
- [ ] Monitoring for data drift
