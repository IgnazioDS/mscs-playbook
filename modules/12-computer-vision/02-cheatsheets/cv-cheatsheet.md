# Computer Vision Cheat Sheet

## Preprocessing pipeline
- Resize with aspect-ratio policy (pad or crop)
- Convert to consistent color space (RGB/BGR)
- Normalize using dataset or pretrained stats
- Add augmentations aligned with real-world variation

## Dataset splits and leakage checks
- Split by source, time, or device to avoid leakage
- Remove near-duplicate images across splits
- Keep class balance consistent across splits
- Track dataset version and labeling rules

## Loss/metrics mapping
- Classification: cross-entropy, accuracy, precision/recall/F1
- Detection: focal loss or BCE + mAP @ IoU thresholds
- Segmentation: dice or cross-entropy + IoU/Dice metrics

## Debugging checklist
- Overfit a tiny subset to validate pipeline
- Spot-check labels and class mappings
- Verify augmentations do not flip labels
- Inspect failure cases by class and size

## Deployment notes
- Measure latency on target hardware
- Use batching for throughput and amortized overhead
- Quantize or prune for edge deployment
- Monitor memory footprint and warm-up time

## Safety and privacy checklist
- Mask or blur sensitive regions when needed
- Enforce access controls and retention policies
- Audit for bias across environments and groups
- Test robustness to lighting and occlusions
