# 13-artificial-intelligence

## Status
- Docs: complete
- Python implementations: complete
- Mini-project: complete

## Overview
This module covers foundational AI: agents, search, games, constraints,
knowledge representation, uncertainty, and learning. It is written as an
engineering playbook with actionable checklists.

## Prerequisites
- Python 3.10+
- Discrete math, probability, and basic algorithms

## Quickstart
Run from the repo root:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r modules/13-artificial-intelligence/03-implementations/python/requirements.txt
python -m pytest -q modules/13-artificial-intelligence/03-implementations/python/tests
python modules/13-artificial-intelligence/03-implementations/python/src/ai/mini_project/cli.py route-plan --seed 42
python modules/13-artificial-intelligence/03-implementations/python/src/ai/mini_project/cli.py schedule --seed 42
python modules/13-artificial-intelligence/03-implementations/python/src/ai/mini_project/cli.py diagnose --seed 42
python modules/13-artificial-intelligence/03-implementations/python/src/ai/mini_project/cli.py evaluate
```

## Reproducibility notes
- All workflows are offline and deterministic (no external APIs).
- Toy problems use fixed seeds and small state spaces for repeatable results.

## Concepts
- [Intelligent Agents and Rationality](01-concepts/intelligent-agents-and-rationality.md)
- [Uninformed and Informed Search](01-concepts/uninformed-and-informed-search.md)
- [Adversarial Search: Minimax and Alpha-Beta](01-concepts/adversarial-search-minimax-alpha-beta.md)
- [Constraint Satisfaction Problems](01-concepts/constraint-satisfaction-problems.md)
- [Knowledge Representation: Propositional and FOL](01-concepts/knowledge-representation-propositional-and-fol.md)
- [Reasoning Under Uncertainty: Bayes and MDP](01-concepts/reasoning-under-uncertainty-bayes-and-mdp.md)
- [Probabilistic Graphical Models Intuition](01-concepts/probabilistic-graphical-models-intuition.md)
- [Learning in AI: Overview](01-concepts/learning-in-ai-overview.md)
- [AI Safety, Alignment, and Evaluation](01-concepts/ai-safety-alignment-and-evaluation.md)

## Cheat sheet
- [AI Cheat Sheet](02-cheatsheets/ai-cheatsheet.md)

## Case studies
- [Route Planning with A*](04-case-studies/route-planning-with-a-star.md)
- [Scheduling with CSP and Constraints](04-case-studies/scheduling-with-csp-and-constraints.md)
- [Diagnosis with Bayes Net](04-case-studies/diagnosis-with-bayes-net.md)

## Implementations
- [Python implementations](03-implementations/python/README.md)
- [TypeScript implementations](03-implementations/typescript/README.md)

## Mini-project
- [Mini-project writeup](05-exercises/mini-project-ai-toolkit.md)
