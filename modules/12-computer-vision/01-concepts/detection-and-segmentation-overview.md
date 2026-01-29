# Detection and Segmentation Overview

## Overview
Detection finds objects with bounding boxes, while segmentation assigns labels to
pixels for precise localization.

## Why it matters
Many real-world applications require exact localization, not just classification.

## Key ideas
- Two-stage detectors trade speed for accuracy
- One-stage detectors offer faster inference
- Segmentation can be semantic, instance, or panoptic
- Post-processing (NMS) improves detection quality

## Practical workflow
- Select detection vs segmentation based on task needs
- Use pretrained backbones and fine-tune on domain data
- Tune confidence and NMS thresholds
- Evaluate on small/occluded objects separately

## Failure modes
- Missed small objects due to low resolution
- Overlapping detections from poor NMS tuning
- Class confusion in crowded scenes
- Segmentation artifacts at object boundaries

## Checklist
- Inspect precision/recall tradeoffs by confidence
- Track metrics by object size bins
- Validate annotation quality for boxes/masks
- Benchmark throughput on target hardware

## References
- Faster R-CNN — https://arxiv.org/abs/1506.01497
- Mask R-CNN — https://arxiv.org/abs/1703.06870
