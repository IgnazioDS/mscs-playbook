# Defect Detection on a Production Line

## Problem and constraints
- Detect surface defects on products in real time
- High throughput and low latency requirements
- Limited labeled defect examples

## Data strategy and labeling plan
- Capture images at multiple stations and lighting conditions
- Use active learning to prioritize uncertain samples
- Label defects with bounding boxes and defect categories
- Maintain a defect taxonomy with clear labeling rules

## Architecture (components and data flow)
- Camera ingestion and preprocessing pipeline
- Detection model with lightweight backbone
- Post-processing for NMS and confidence thresholds
- Quality dashboard and alerting system

## Evaluation plan and metrics
- Metrics: mAP, recall at fixed precision, latency
- Track false negatives for critical defect types
- Run weekly regression tests on a fixed validation set

## Failure modes and mitigations
- Missed small defects: increase resolution or add zoomed views
- False positives from glare: add lighting calibration
- Domain shift across lines: fine-tune per line

## Security and privacy considerations
- Restrict camera access to production network
- Store only defect crops when possible
- Maintain audit logs for model decisions

## Cost and latency levers
- Reduce input resolution for non-critical lines
- Batch inference during low-volume periods
- Use edge accelerators for faster inference

## What I would ship checklist
- [ ] Labeling guide and QA checks
- [ ] Latency benchmark on target hardware
- [ ] Defect recall targets by category
- [ ] Monitoring for drift and false positives
- [ ] Rollback plan for model updates
