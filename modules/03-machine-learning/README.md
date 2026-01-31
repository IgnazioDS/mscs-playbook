# 03-machine-learning

## Status

- Concepts, cheat sheet, case study, implementations, and mini-project are complete.
- Tests and CLI run locally with pinned dependencies.

## Overview

This module covers supervised, unsupervised, and intro deep learning concepts
with a focus on evaluation discipline and reproducibility. You will build and
assess baseline models, reason about bias/variance, and apply practical
troubleshooting workflows.

## Prerequisites

- Python 3.10+
- Virtual environment tooling (venv)
- Basic numpy familiarity

## How to use this module

- Read the concept pages in order.
- Keep the cheat sheet open while implementing and evaluating models.
- Use the case study as a template for your own projects.

## Quickstart

- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r modules/03-machine-learning/03-implementations/python/requirements.txt`
- `python -m pytest -q modules/03-machine-learning/03-implementations/python/tests`
- `python modules/03-machine-learning/03-implementations/python/src/cli.py train-classifier --dataset iris --seed 42`
- `python modules/03-machine-learning/03-implementations/python/src/cli.py train-regressor --dataset california_housing --seed 42`
- `python modules/03-machine-learning/03-implementations/python/src/cli.py cluster --dataset iris --k 3 --seed 42`

## Concepts

- [Supervised Learning Foundations](01-concepts/supervised-learning-foundations.md)
- [Evaluation Metrics and Validation](01-concepts/evaluation-metrics-and-validation.md)
- [Regularization and Bias/Variance](01-concepts/regularization-and-bias-variance.md)
- [Unsupervised Learning Toolkit](01-concepts/unsupervised-learning-toolkit.md)
- [Dimensionality Reduction](01-concepts/dimensionality-reduction.md)
- [Deep Learning Training Loop](01-concepts/deep-learning-training-loop.md)
- [Model Debugging and Error Analysis](01-concepts/model-debugging-and-error-analysis.md)
- [Data Leakage and Reproducibility](01-concepts/data-leakage-and-reproducibility.md)

## Cheat sheet

- [ML Cheat Sheet](02-cheatsheets/ml-cheatsheet.md)

## Case study

- [From Baseline to Deployable Model](04-case-studies/from-baseline-to-deployable-model.md)

## Mini-project

- [ML Baseline to Iteration](05-exercises/mini-project-ml-baseline-to-iteration.md)

## Implementations

- [Python reference implementations](03-implementations/python/README.md)

## CLI examples

- `python modules/03-machine-learning/03-implementations/python/src/cli.py train-classifier --dataset iris --seed 42`
- `python modules/03-machine-learning/03-implementations/python/src/cli.py train-regressor --dataset california_housing --seed 42`
- `python modules/03-machine-learning/03-implementations/python/src/cli.py cluster --dataset iris --k 3 --seed 42`

## Tests

- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r modules/03-machine-learning/03-implementations/python/requirements.txt`
- `python -m pytest -q modules/03-machine-learning/03-implementations/python/tests`
