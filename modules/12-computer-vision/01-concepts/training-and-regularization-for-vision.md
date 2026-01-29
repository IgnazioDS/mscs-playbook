# Training and Regularization for Vision

## Overview
Training vision models requires careful regularization, learning-rate schedules,
and augmentation to generalize well.

## Why it matters
Vision datasets can be noisy or imbalanced, and training stability affects
accuracy and deployment readiness.

## Key ideas
- Data augmentation is a primary regularizer
- Weight decay and dropout reduce overfitting
- Learning-rate schedules improve convergence
- Class imbalance requires reweighting or sampling

## Practical workflow
- Start with baseline augmentations and expand gradually
- Use cosine or step decay for learning rates
- Apply label smoothing for classification tasks
- Track per-class metrics for imbalance

## Failure modes
- Train/val leakage through near-duplicate images
- Over-augmentation that changes class semantics
- Underfitting from too-strong regularization
- Instability from high learning rates

## Checklist
- Run a small overfit test on a tiny subset
- Verify dataset splits by source or time
- Check per-class precision/recall
- Log augmentation parameters in training runs

## References
- MixUp — https://arxiv.org/abs/1710.09412
- CutMix — https://arxiv.org/abs/1905.04899
