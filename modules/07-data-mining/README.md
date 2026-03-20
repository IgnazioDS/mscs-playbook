---
tags:
  - curriculum
  - module
  - data-mining
status: stable
format: module-hub
difficulty: intermediate
---

# Data Mining

## Status

- Concepts, cheat sheet, implementations, case studies, and mini-project materials are present.
- The concept sequence now follows a numbered pipeline-oriented reading path.
- Python implementations and CLI exercises provide reproducible reference workflows for the core mining tasks.

## Overview

This module covers practical data mining from end to end: pipeline framing,
profiling, cleaning, feature construction, validation, clustering, anomaly
detection, association-rule mining, and reproducible experimentation. The
emphasis is on stable workflows that turn exploratory analysis into auditable
artifacts and defensible decisions.

## Recommended learning path

1. Start with the pipeline overview, profiling, cleaning, and feature construction to build a reliable preparation workflow.
2. Learn validation discipline before trusting any discovered structure or mining result.
3. Move into clustering and anomaly detection for structure discovery and rare-event triage.
4. Finish with association rules and experiment tracking so findings can be interpreted, compared, and reproduced.

## Prerequisites

- Python 3.10+
- Virtual environment tooling (`venv`)
- Basic familiarity with pandas and scikit-learn

## Quickstart

- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `python3 -m pip install -r modules/07-data-mining/03-implementations/python/requirements.txt`
- `python3 -m pytest -q modules/07-data-mining/03-implementations/python/tests`
- `python3 modules/07-data-mining/03-implementations/python/src/cli.py cluster --dataset iris --k 3 --seed 42`

## Concepts (reading order)

- [01 Data Mining Pipeline Overview](01-concepts/01-data-mining-pipeline-overview.md)
- [02 Data Understanding and Profiling](01-concepts/02-data-understanding-and-profiling.md)
- [03 Cleaning, Missingness, and Outliers](01-concepts/03-cleaning-missingness-and-outliers.md)
- [04 Feature Engineering and Encoding](01-concepts/04-feature-engineering-and-encoding.md)
- [05 Model Selection and Validation](01-concepts/05-model-selection-and-validation.md)
- [06 Clustering and Evaluation](01-concepts/06-clustering-and-evaluation.md)
- [07 Anomaly Detection Basics](01-concepts/07-anomaly-detection-basics.md)
- [08 Association Rules: Apriori and FP-Growth](01-concepts/08-association-rules-apriori-and-fp-growth.md)
- [09 Experiment Tracking and Reproducibility](01-concepts/09-experiment-tracking-and-reproducibility.md)

## Concept-to-project bridge

- Read `01` through `05` before treating any mined result as stable or comparable.
- Read `06` and `07` before running the clustering or anomaly CLI flows.
- Read `08` before interpreting market-basket outputs or writing rule-based business recommendations.
- Read `09` alongside the case studies and CLI mini-project so the outputs stay reproducible.

## Cheat sheet

- [Data Mining Cheat Sheet](02-cheatsheets/data-mining-cheatsheet.md)

## Case studies

- [Retail Basket Analysis](04-case-studies/retail-basket-analysis.md)
- [Churn Proxy Segmentation](04-case-studies/churn-proxy-segmentation.md)
- [Fraud Anomaly Triage](04-case-studies/fraud-anomaly-triage.md)

## Implementations

- [Python reference implementations](03-implementations/python/README.md)

## Mini-project

- [Data Mining Mini-Project](05-exercises/data-mining-mini-project.md)
