# 12-computer-vision

## Status
- Docs: complete
- Python implementations: complete
- Mini-project: complete

## Overview
This module covers practical computer vision: image representations, classical
features, CNNs and transformers, detection/segmentation, evaluation, and
production tradeoffs. It is written as an engineering playbook with actionable
checklists.

## Prerequisites
- Python 3.10+
- Basic linear algebra and probability
- Familiarity with training ML models

## Quickstart
Run from the repo root:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r modules/12-computer-vision/03-implementations/python/requirements.txt
python -m pytest -q modules/12-computer-vision/03-implementations/python/tests
python modules/12-computer-vision/03-implementations/python/src/cv/mini_project/cli.py defect-detect --seed 42
python modules/12-computer-vision/03-implementations/python/src/cv/mini_project/cli.py doc-ocr-lite --seed 42
python modules/12-computer-vision/03-implementations/python/src/cv/mini_project/cli.py shelf-availability --seed 42
python modules/12-computer-vision/03-implementations/python/src/cv/mini_project/cli.py evaluate
```

## Reproducibility notes
- All workflows are offline and deterministic (no external APIs).
- Toy pipelines use synthetic data generation with fixed seeds.
- Metrics are computed using simple rule-based pipelines for stability.

## Concepts
- [Image Representations and Preprocessing](01-concepts/image-representations-and-preprocessing.md)
- [Classical Features and Keypoints](01-concepts/classical-features-and-keypoints.md)
- [Convolution and CNNs](01-concepts/convolution-and-cnns.md)
- [Training and Regularization for Vision](01-concepts/training-and-regularization-for-vision.md)
- [Detection and Segmentation Overview](01-concepts/detection-and-segmentation-overview.md)
- [Vision Transformers and Modern Backbones](01-concepts/vision-transformers-and-modern-backbones.md)
- [Multimodal and Vision-Language Models](01-concepts/multimodal-and-vision-language-models.md)
- [Evaluation Metrics and Error Analysis for Vision](01-concepts/evaluation-metrics-and-error-analysis-vision.md)
- [Safety, Bias, and Privacy for Vision](01-concepts/safety-bias-privacy-for-vision.md)

## Cheat sheet
- [Computer Vision Cheat Sheet](02-cheatsheets/cv-cheatsheet.md)

## Case studies
- [Defect Detection on a Production Line](04-case-studies/defect-detection-on-production-line.md)
- [Document OCR and Layout Understanding](04-case-studies/document-ocr-and-layout-understanding.md)
- [Retail Shelf Availability and Pricing](04-case-studies/retail-shelf-availability-and-pricing.md)

## Implementations
- [Python implementations](03-implementations/python/README.md)
- [TypeScript implementations](03-implementations/typescript/README.md)

## Mini-project
- [Mini-project writeup](05-exercises/mini-project-cv-toolkit.md)
- [Mini-project CLI entry](03-implementations/python/src/cv/mini_project/cli.py)
