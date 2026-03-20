---
summary: Portfolio project for local-first computer-vision inference scenarios and reproducible evaluation.
tags:
  - project
  - portfolio
  - computer-vision
status: stable
format: project-brief
difficulty: intermediate
---

# p6-cv-inference-pipeline

## Purpose
Provide a local-first CV inference baseline covering toy defect detection, OCR-lite, and shelf-availability scenarios.

## Scope
- Execute deterministic CV mini-project commands.
- Validate output consistency through test coverage.
- Keep project runnable offline without external APIs.

## Modules Used
- [Machine Learning](../../modules/03-machine-learning/README.md)
- [Computer Vision](../../modules/12-computer-vision/README.md)

## How to Run
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r modules/12-computer-vision/03-implementations/python/requirements.txt
python3 modules/12-computer-vision/03-implementations/python/src/cv/mini_project/cli.py defect-detect --seed 42
python3 modules/12-computer-vision/03-implementations/python/src/cv/mini_project/cli.py doc-ocr-lite --seed 42
python3 modules/12-computer-vision/03-implementations/python/src/cv/mini_project/cli.py shelf-availability --seed 42
python3 modules/12-computer-vision/03-implementations/python/src/cv/mini_project/cli.py evaluate
```

## How to Test
```bash
python3 -m pytest -q modules/12-computer-vision/03-implementations/python/tests
```

## Expected Output
- Each CLI command prints deterministic task summaries.
- Evaluation and test suite pass on the local synthetic dataset workflow.
