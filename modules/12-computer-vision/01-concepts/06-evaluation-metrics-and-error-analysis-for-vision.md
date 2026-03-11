# Evaluation Metrics and Error Analysis for Vision

## Overview
Vision evaluation uses task-specific metrics to quantify detection, segmentation,
and classification performance.

## Why it matters
Accurate metrics and error analysis reveal model weaknesses and guide data
collection.

## Key ideas
- Classification uses accuracy, precision, recall, F1
- Detection uses mAP and IoU thresholds
- Segmentation uses IoU and Dice
- Error analysis groups failures by class, size, and conditions

## Practical workflow
- Define metrics aligned to business impact
- Track per-class and per-size performance
- Inspect confusion matrices and qualitative failures
- Re-label or collect targeted data to close gaps

## Failure modes
- Optimizing for the wrong metric
- Hidden performance drops on rare classes
- Inconsistent annotation standards
- Dataset leakage that inflates metrics

## Checklist
- Use stratified evaluation sets
- Report confidence intervals or bootstrap metrics
- Review qualitative samples for each failure bucket
- Re-run evals after data or model updates

## References
- COCO Metrics — https://cocodataset.org/#detection-eval
- IoU and Dice — https://arxiv.org/abs/1606.04797
