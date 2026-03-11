# Image Representations and Preprocessing

## Overview
Images are arrays of pixels with spatial structure and channel semantics that
must be normalized and standardized before model training or inference.

## Why it matters
Input representation choices affect model accuracy, stability, and deployment
latency.

## Key ideas
- Color spaces (RGB, BGR, HSV) encode different information
- Resolution trades off detail vs compute
- Normalization aligns image statistics to model expectations
- Data augmentation improves generalization

## Practical workflow
- Define target resolution and aspect ratio policy
- Convert to a consistent color space
- Normalize using dataset or model-specific statistics
- Add augmentations aligned with real-world variability

## Failure modes
- Channel order mismatches (RGB vs BGR)
- Over-aggressive resizing that removes small objects
- Augmentations that change labels (e.g., flip text)
- Train/infer preprocessing drift

## Checklist
- Document image size, color space, and normalization
- Verify augmentations with visual spot checks
- Keep preprocessing identical in training and inference
- Log preprocessing parameters with model artifacts

## References
- OpenCV Color Spaces — https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html
- Data Augmentation Survey — https://arxiv.org/abs/1712.04621
