# Foundations

## Status
- Foundations Toolkit CLI and tests are complete.
- Core module documentation is expanding and covers the main prerequisite topics.

## Overview
This module covers the mathematical and computational foundations needed across the playbook. It emphasizes discrete reasoning, proof techniques, counting, asymptotic analysis, linear algebra, probability, statistical inference, numerical reasoning, information measures, and representation-level basics.

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

## Concepts (reading order)
- [Discrete Mathematics Basics](01-concepts/01-discrete-mathematics-basics.md)
- [Proof Techniques for Computer Science](01-concepts/02-proof-techniques-for-computer-science.md)
- [Counting and Combinatorics Basics](01-concepts/03-counting-and-combinatorics-basics.md)
- [Recurrences and Asymptotic Analysis](01-concepts/04-recurrences-and-asymptotic-analysis.md)
- [Linear Algebra: Vectors and Matrices](01-concepts/05-linear-algebra-vectors-and-matrices.md)
- [Linear Algebra: Rank, Independence, Eigenvalues, and Least Squares](01-concepts/06-linear-algebra-rank-eigenvalues-and-least-squares.md)
- [Calculus and Optimization Basics](01-concepts/07-calculus-and-optimization-basics.md)
- [Probability and Distributions Basics](01-concepts/08-probability-and-distributions-basics.md)
- [Descriptive Statistics and Sampling](01-concepts/09-descriptive-statistics-and-sampling.md)
- [Numerical Stability and Precision](01-concepts/10-numerical-stability-and-precision.md)
- [Units and Dimensional Analysis](01-concepts/11-units-and-dimensional-analysis.md)
- [Boolean Algebra and Bit Operations](01-concepts/12-boolean-algebra-and-bit-operations.md)
- [Complexity Theory Intro](01-concepts/13-complexity-theory-intro.md)

## Cheat sheet
- [Foundations Cheat Sheet](02-cheatsheets/foundations-cheatsheet.md)

## Case study
- [Experiment Sizing and Sanity Checks](04-case-studies/experiment-sizing-and-sanity-checks.md)
