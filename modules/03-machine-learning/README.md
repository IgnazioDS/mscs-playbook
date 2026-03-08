# Machine Learning

## Status

- Concepts, cheat sheet, case study, implementations, and mini-project are complete.
- Tests and CLI run locally with pinned dependencies.

## Overview

This module covers supervised learning, evaluation, leakage prevention,
regularization, unsupervised structure discovery, dimensionality reduction,
intro deep learning, and model-debugging practice. It emphasizes disciplined
validation, reproducibility, and iteration from baseline models to more complex
training workflows.

## Prerequisites

- Python 3.10+
- Virtual environment tooling (venv)
- Basic numpy familiarity

## How to use this module

- Read the concept pages in order.
- Keep the cheat sheet open while implementing and evaluating models.
- Use the case study as a template for your own projects.

## Recommended learning path

1. Start with the supervised-learning problem setup and how model quality is measured.
2. Learn how leakage, reproducibility, and regularization affect generalization.
3. Move into unsupervised learning and dimensionality reduction as structure-discovery tools.
4. Finish with the deep-learning training loop and a capstone page on debugging model failures.

## Quickstart

- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `python3 -m pip install -r modules/03-machine-learning/03-implementations/python/requirements.txt`
- `python3 -m pytest -q modules/03-machine-learning/03-implementations/python/tests`
- `python3 modules/03-machine-learning/03-implementations/python/src/cli.py train-classifier --dataset iris --seed 42`
- `python3 modules/03-machine-learning/03-implementations/python/src/cli.py train-regressor --dataset california_housing --seed 42`
- `python3 modules/03-machine-learning/03-implementations/python/src/cli.py cluster --dataset iris --k 3 --seed 42`

## Concepts (reading order)

- [01 Supervised Learning Foundations](01-concepts/01-supervised-learning-foundations.md)
- [02 Evaluation Metrics and Validation](01-concepts/02-evaluation-metrics-and-validation.md)
- [03 Data Leakage and Reproducibility](01-concepts/03-data-leakage-and-reproducibility.md)
- [04 Regularization and Bias/Variance](01-concepts/04-regularization-and-bias-variance.md)
- [05 Unsupervised Learning Foundations](01-concepts/05-unsupervised-learning-foundations.md)
- [06 Dimensionality Reduction](01-concepts/06-dimensionality-reduction.md)
- [07 Deep Learning Training Loop](01-concepts/07-deep-learning-training-loop.md)
- [08 Model Debugging and Error Analysis](01-concepts/08-model-debugging-and-error-analysis.md)

## Concept-to-project bridge

- Use the concept numbers as the default reading order even if you jump directly into the case study or mini-project.
- Read `01` through `04` before training baseline supervised models.
- Read `05` and `06` before clustering or representation-learning explorations.
- Read `07` before iterating on neural-network experiments.
- Read `08` alongside the case study and mini-project when comparing model revisions.

## Cheat sheet

- [ML Cheat Sheet](02-cheatsheets/ml-cheatsheet.md)

## Case study

- [From Baseline to Deployable Model](04-case-studies/from-baseline-to-deployable-model.md)

## Mini-project

- [ML Baseline to Iteration](05-exercises/mini-project-ml-baseline-to-iteration.md)

## Implementations

- [Python reference implementations](03-implementations/python/README.md)

## CLI examples

- `python3 modules/03-machine-learning/03-implementations/python/src/cli.py train-classifier --dataset iris --seed 42`
- `python3 modules/03-machine-learning/03-implementations/python/src/cli.py train-regressor --dataset california_housing --seed 42`
- `python3 modules/03-machine-learning/03-implementations/python/src/cli.py cluster --dataset iris --k 3 --seed 42`

## Tests

- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `python3 -m pip install -r modules/03-machine-learning/03-implementations/python/requirements.txt`
- `python3 -m pytest -q modules/03-machine-learning/03-implementations/python/tests`
