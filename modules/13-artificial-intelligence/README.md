---
tags:
  - curriculum
  - module
  - artificial-intelligence
status: stable
format: module-hub
difficulty: advanced
---

# Artificial Intelligence

## Overview

This module covers core artificial-intelligence ideas spanning agents, search, games, constraints, logic, uncertainty, graphical models, learning, and safety. The reading path moves from agent formulation and classical reasoning toward uncertain inference, learning, and system-level evaluation concerns.

## Reading Path

1. [Intelligent Agents and Rationality](01-concepts/01-intelligent-agents-and-rationality.md)
2. [Uninformed and Informed Search](01-concepts/02-uninformed-and-informed-search.md)
3. [Adversarial Search: Minimax and Alpha-Beta](01-concepts/03-adversarial-search-minimax-and-alpha-beta.md)
4. [Constraint Satisfaction Problems](01-concepts/04-constraint-satisfaction-problems.md)
5. [Knowledge Representation: Propositional and FOL](01-concepts/05-knowledge-representation-propositional-and-fol.md)
6. [Reasoning Under Uncertainty: Bayes and MDP](01-concepts/06-reasoning-under-uncertainty-bayes-and-mdp.md)
7. [Probabilistic Graphical Models Intuition](01-concepts/07-probabilistic-graphical-models-intuition.md)
8. [Learning in AI: Overview](01-concepts/08-learning-in-ai-overview.md)
9. [AI Safety, Alignment, and Evaluation](01-concepts/09-ai-safety-alignment-and-evaluation.md)

## Module Map

- Concepts: [ordered concept index](01-concepts/README.md)
- Cheat sheet: [AI cheat sheet](02-cheatsheets/ai-cheatsheet.md)
- Python implementations: [offline AI toolkit](03-implementations/python/README.md)
- TypeScript implementations: [implementation notes](03-implementations/typescript/README.md)
- Case studies: [case study index](04-case-studies/README.md)
- Exercises: [exercise index](05-exercises/README.md)
- Notes: [further notes](06-notes/README.md)

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r modules/13-artificial-intelligence/03-implementations/python/requirements.txt
python3 -m pytest -q modules/13-artificial-intelligence/03-implementations/python/tests
python3 modules/13-artificial-intelligence/03-implementations/python/src/ai13/mini_project/cli.py route-plan --seed 42
python3 modules/13-artificial-intelligence/03-implementations/python/src/ai13/mini_project/cli.py schedule --seed 42
python3 modules/13-artificial-intelligence/03-implementations/python/src/ai13/mini_project/cli.py diagnose --seed 42
python3 modules/13-artificial-intelligence/03-implementations/python/src/ai13/mini_project/cli.py evaluate --seed 42
```
