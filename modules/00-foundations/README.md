# 00-foundations

## Status
- Foundations Toolkit CLI and tests are complete.
- Core module documentation is complete.

## Overview
This module covers foundational math and CS skills needed throughout the playbook.
It ships a deterministic CLI mini-project to validate core statistics, number theory,
and matrix operations.

## Prerequisites
- Python 3.10+
- Virtual environment tooling (venv)

## Quickstart
From the repo root:
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r modules/00-foundations/03-implementations/python/requirements.txt
python3 -m pytest -q modules/00-foundations/03-implementations/python/tests
python3 modules/00-foundations/03-implementations/python/src/foundations/mini_project/cli.py stats --nums "1 2 3"
```

## Implementations
- [Python implementations](03-implementations/python/README.md)

## Mini-project
- [Foundations Toolkit CLI](05-exercises/foundations-toolkit-cli.md)

## Contents
- [Concepts](01-concepts/README.md)
- [Cheat sheets](02-cheatsheets/README.md)
- [Implementations](03-implementations/)
- [Case studies](04-case-studies/README.md)
- [Exercises](05-exercises/README.md)
- [Notes](06-notes/README.md)

## Concepts (quick links)
- [Descriptive Statistics and Sampling](01-concepts/descriptive-statistics-and-sampling.md)
- [Probability and Distributions Basics](01-concepts/probability-and-distributions-basics.md)
- [Linear Algebra: Vectors and Matrices](01-concepts/linear-algebra-vectors-and-matrices.md)
- [Calculus and Optimization Basics](01-concepts/calculus-and-optimization-basics.md)
- [Data Structures and Complexity Basics](01-concepts/data-structures-and-complexity-basics.md)
- [Numerical Stability and Precision](01-concepts/numerical-stability-and-precision.md)
- [Units and Dimensional Analysis](01-concepts/units-and-dimensional-analysis.md)

## Cheat sheet
- [Foundations Cheat Sheet](02-cheatsheets/foundations-cheatsheet.md)

## Case study
- [Experiment Sizing and Sanity Checks](04-case-studies/experiment-sizing-and-sanity-checks.md)
