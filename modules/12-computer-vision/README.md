---
tags:
  - curriculum
  - module
  - computer-vision
status: stable
format: module-hub
difficulty: advanced
---

# Computer Vision

## Overview

This module covers practical computer vision from image representation and classical features through CNNs, localization tasks, modern backbones, multimodal systems, and deployment-oriented evaluation and safety. The reading path moves from core visual representations toward modern multimodal and risk-aware production systems.

## Reading Path

1. [Image Representations and Preprocessing](01-concepts/01-image-representations-and-preprocessing.md)
2. [Classical Features and Keypoints](01-concepts/02-classical-features-and-keypoints.md)
3. [Convolution and CNNs](01-concepts/03-convolution-and-cnns.md)
4. [Training and Regularization for Vision](01-concepts/04-training-and-regularization-for-vision.md)
5. [Detection and Segmentation Overview](01-concepts/05-detection-and-segmentation-overview.md)
6. [Evaluation Metrics and Error Analysis for Vision](01-concepts/06-evaluation-metrics-and-error-analysis-for-vision.md)
7. [Vision Transformers and Modern Backbones](01-concepts/07-vision-transformers-and-modern-backbones.md)
8. [Multimodal and Vision-Language Models](01-concepts/08-multimodal-and-vision-language-models.md)
9. [Safety, Bias, and Privacy for Vision](01-concepts/09-safety-bias-and-privacy-for-vision.md)

## Module Map

- Concepts: [ordered concept index](01-concepts/README.md)
- Cheat sheet: [Computer Vision cheat sheet](02-cheatsheets/cv-cheatsheet.md)
- Python implementations: [local-first CV toolkit](03-implementations/python/README.md)
- TypeScript implementations: [implementation notes](03-implementations/typescript/README.md)
- Case studies: [case study index](04-case-studies/README.md)
- Exercises: [exercise index](05-exercises/README.md)
- Notes: [further notes](06-notes/README.md)

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r modules/12-computer-vision/03-implementations/python/requirements.txt
python3 -m pytest -q modules/12-computer-vision/03-implementations/python/tests
python3 modules/12-computer-vision/03-implementations/python/src/cv/mini_project/cli.py defect-detect --seed 42
python3 modules/12-computer-vision/03-implementations/python/src/cv/mini_project/cli.py doc-ocr-lite --seed 42
python3 modules/12-computer-vision/03-implementations/python/src/cv/mini_project/cli.py shelf-availability --seed 42
python3 modules/12-computer-vision/03-implementations/python/src/cv/mini_project/cli.py evaluate
```
