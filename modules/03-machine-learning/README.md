# Machine Learning

## Status

- Concepts, cheat sheet, case study, implementations, and mini-project are complete.
- Tests and CLI run locally with pinned dependencies.

## Overview

This module covers supervised learning, feature representation, disciplined
evaluation, leakage prevention, regularization, unsupervised structure
discovery, dimensionality reduction, optimization, model selection,
calibration, intro deep learning, interpretability, and model-debugging
practice. It emphasizes reproducible iteration from baseline models to more
complex training workflows.

## Prerequisites

- Python 3.10+
- Virtual environment tooling (venv)
- Basic numpy familiarity

## How to use this module

- Read the concept pages in order.
- Keep the cheat sheet open while implementing and evaluating models.
- Use the case study as a template for your own projects.

## Recommended learning path

1. Start with supervised learning, feature representation, and how model quality is measured.
2. Learn how leakage, regularization, optimization, and tuning affect generalization.
3. Move into unsupervised learning and dimensionality reduction as structure-discovery tools.
4. Finish with deep learning, explanation methods, and a capstone page on debugging model failures.

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
- [02 Feature Engineering and Preprocessing](01-concepts/02-feature-engineering-and-preprocessing.md)
- [03 Evaluation Metrics and Validation](01-concepts/03-evaluation-metrics-and-validation.md)
- [04 Data Leakage and Reproducibility](01-concepts/04-data-leakage-and-reproducibility.md)
- [05 Regularization and Bias/Variance](01-concepts/05-regularization-and-bias-variance.md)
- [06 Unsupervised Learning Foundations](01-concepts/06-unsupervised-learning-foundations.md)
- [07 Dimensionality Reduction](01-concepts/07-dimensionality-reduction.md)
- [08 Loss Functions and Optimization for Machine Learning](01-concepts/08-loss-functions-and-optimization-for-machine-learning.md)
- [09 Model Selection and Hyperparameter Tuning](01-concepts/09-model-selection-and-hyperparameter-tuning.md)
- [10 Class Imbalance and Calibration](01-concepts/10-class-imbalance-and-calibration.md)
- [11 Deep Learning Training Loop](01-concepts/11-deep-learning-training-loop.md)
- [12 Interpretability and Model Explanation Basics](01-concepts/12-interpretability-and-model-explanation-basics.md)
- [13 Model Debugging and Error Analysis](01-concepts/13-model-debugging-and-error-analysis.md)

## Concept-to-project bridge

- Use the concept numbers as the default reading order even if you jump directly into the case study or mini-project.
- Read `01` through `05` before training baseline supervised models seriously.
- Read `06` and `07` before clustering or representation-learning explorations.
- Read `08` through `10` before comparing tuning, thresholding, or calibration changes.
- Read `11` before iterating on neural-network experiments.
- Read `12` and `13` alongside the case study and mini-project when reviewing model revisions.

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
