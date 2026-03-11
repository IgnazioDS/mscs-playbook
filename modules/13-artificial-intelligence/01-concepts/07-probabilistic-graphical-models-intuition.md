# Probabilistic Graphical Models Intuition

## Overview
Probabilistic graphical models (PGMs) represent conditional dependencies between
random variables using graphs.

## Why it matters
PGMs provide compact representations for complex probabilistic systems and
enable structured inference.

## Key ideas
- Bayesian networks are directed acyclic graphs
- Markov random fields are undirected graphs
- Conditional independence reduces complexity
- Inference uses variable elimination or sampling

## Practical workflow
- Define variables and edges based on dependencies
- Encode conditional probability tables or factors
- Choose exact or approximate inference methods
- Validate with synthetic and real-world queries

## Failure modes
- Incorrect independence assumptions
- Large cliques causing computational blowups
- Poorly calibrated probabilities
- Intractable inference without approximation

## Checklist
- Validate conditional independencies with data
- Use sampling for large graphs
- Monitor inference runtime and memory
- Document assumptions and factorization

## References
- Bayes Nets — https://en.wikipedia.org/wiki/Bayesian_network
- PGMs overview — https://people.eecs.berkeley.edu/~jordan/prelims/graphical-models.pdf
