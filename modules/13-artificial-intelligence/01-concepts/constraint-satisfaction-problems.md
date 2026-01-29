# Constraint Satisfaction Problems

## Overview
CSPs model problems as variables with domains and constraints that must be
satisfied.

## Why it matters
Scheduling, assignment, and configuration tasks map naturally to CSPs.

## Key ideas
- Variables, domains, and constraints define the problem
- Backtracking searches for consistent assignments
- Constraint propagation prunes domains
- Heuristics (MRV, LCV) improve efficiency

## Practical workflow
- Model variables and explicit constraints
- Use backtracking with forward checking
- Apply AC-3 for arc consistency
- Add variable and value ordering heuristics

## Failure modes
- Huge search trees without pruning
- Incorrect constraints eliminate valid solutions
- Overly large domains cause slow convergence
- Lack of propagation leads to wasted search

## Checklist
- Validate constraints with small known cases
- Track backtracking depth and failures
- Use MRV and LCV by default
- Log constraint propagation steps

## References
- AIMA Chapter on CSPs
- AC-3 algorithm — https://doi.org/10.1145/321892.321894
