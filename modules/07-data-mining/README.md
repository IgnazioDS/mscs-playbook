# 07-data-mining

## Status
- Docs complete (concepts + cheat sheet)
- Case studies pending
- Implementations pending
- Mini-project pending

## Overview
This module covers data mining foundations and practice: profiling, cleaning,
feature engineering, association rules, clustering, anomaly detection, and
reproducible pipelines. It emphasizes deterministic workflows and clear
reporting.

## Prerequisites
- Python 3.10+
- Virtual environment tooling (venv)
- Basic pandas and scikit-learn familiarity

## Quickstart
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r modules/07-data-mining/03-implementations/python/requirements.txt`
- `python -m pytest -q modules/07-data-mining/03-implementations/python/tests`
- `python modules/07-data-mining/03-implementations/python/src/cli.py cluster --dataset iris --k 3 --seed 42`

## Concepts
- [Data Mining Pipeline Overview](01-concepts/data-mining-pipeline-overview.md)
- [Data Understanding and Profiling](01-concepts/data-understanding-and-profiling.md)
- [Cleaning, Missingness, and Outliers](01-concepts/cleaning-missingness-and-outliers.md)
- [Feature Engineering and Encoding](01-concepts/feature-engineering-and-encoding.md)
- [Association Rules: Apriori and FP-Growth](01-concepts/association-rules-apriori-fpgrowth.md)
- [Clustering and Evaluation](01-concepts/clustering-and-evaluation.md)
- [Anomaly Detection Basics](01-concepts/anomaly-detection-basics.md)
- [Model Selection and Validation](01-concepts/model-selection-and-validation.md)
- [Experiment Tracking and Reproducibility](01-concepts/experiment-tracking-and-reproducibility.md)

## Cheat sheet
- [Data Mining Cheat Sheet](02-cheatsheets/data-mining-cheatsheet.md)

## Case studies
- [Retail Basket Analysis](04-case-studies/retail-basket-analysis.md)
- [Churn Proxy Segmentation](04-case-studies/churn-proxy-segmentation.md)
- [Fraud Anomaly Triage](04-case-studies/fraud-anomaly-triage.md)

## Implementations
- [Python reference implementations](03-implementations/python/README.md)

## Mini-project
- [Data mining mini-project CLI](03-implementations/python/README.md)
