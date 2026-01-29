# Retail Shelf Availability and Pricing

## Problem and constraints
- Detect out-of-stock items and pricing discrepancies
- Work across multiple stores and lighting conditions
- Must be accurate enough for operational decisions

## Data strategy and labeling plan
- Capture shelf images at consistent angles
- Label products with bounding boxes and SKU IDs
- Label price tags and link them to products
- Use semi-automated labeling with human verification

## Architecture (components and data flow)
- Image capture and preprocessing service
- Product detection and classification model
- Price tag detection and OCR
- Matching logic for product-price association

## Evaluation plan and metrics
- Metrics: detection mAP, SKU accuracy, price OCR accuracy
- Track per-store performance and drift
- Evaluate on seasonal and promotional changes

## Failure modes and mitigations
- Occluded products: add multi-angle captures
- Misread price tags: improve OCR preprocessing
- Domain shift across stores: fine-tune on new store data

## Security and privacy considerations
- Avoid capturing customer faces when possible
- Blur sensitive content in logs and dashboards
- Restrict image access to authorized users

## Cost and latency levers
- Reduce capture frequency during low-traffic hours
- Use edge inference to avoid upload costs
- Batch OCR for price tags

## What I would ship checklist
- [ ] Store-level accuracy dashboard
- [ ] SKU coverage and drift monitoring
- [ ] OCR confidence thresholds with fallback
- [ ] Privacy review for in-store capture
- [ ] Operational playbook for retraining
