# Detection and Segmentation Overview

## Key Ideas

- Detection localizes objects with bounding boxes, while segmentation localizes them at pixel level.
- The right task formulation depends on the operational decision: sometimes coarse localization is enough, and sometimes exact boundaries are required.
- Detection and segmentation performance depend heavily on resolution, annotation quality, and object scale distribution.
- Two-stage, one-stage, semantic, instance, and panoptic approaches make different tradeoffs between speed, precision, and output granularity.
- Post-processing and thresholding are part of the model system because duplicate boxes, weak masks, and confidence calibration affect the final result.

## 1. Why Localization Tasks Matter

Many vision problems require more than whole-image classification. If the system must know where a defect is, where text appears, or which shelf region is empty, then localization becomes central.

This leads to several task types:

- **object detection** for boxes
- **semantic segmentation** for per-pixel class labels
- **instance segmentation** for separate object masks
- **panoptic segmentation** for combined stuff-and-thing understanding

## 2. Detection vs Segmentation

Detection is often enough when a box around the object supports the downstream action. Segmentation is necessary when exact shape, area, or boundary matters.

Examples:

- a retail shelf audit may work with boxes
- a medical lesion outline may require masks
- document layout often benefits from region-level segmentation

Task selection should therefore follow the business need, not only model availability.

## 3. Model Families

### 3.1 Two-Stage Detection

Two-stage detectors generate proposals first and classify/refine them later. They are often accurate but slower.

### 3.2 One-Stage Detection

One-stage detectors predict objects directly over dense locations. They are often faster and easier to deploy.

### 3.3 Segmentation Models

Segmentation systems predict masks rather than just boxes and must preserve stronger spatial detail.

## 4. Worked Example: Precision and Recall from Detections

Suppose an image contains `4` true objects.

A detector outputs `5` boxes:

- `3` are correct matches
- `2` are false positives

### 4.1 Precision

```text
precision = true_positives / predicted_positives
          = 3 / 5
          = 0.60
```

### 4.2 Recall

```text
recall = true_positives / actual_positives
       = 3 / 4
       = 0.75
```

### 4.3 Interpretation

The detector finds most objects but produces too many extra boxes. That suggests threshold or NMS tuning may improve precision.

Verification: the example separates missed detections from duplicate or incorrect detections, which is exactly the balance detection tuning must manage.

## 5. Practical Design Tradeoffs

Detection and segmentation pipelines must balance:

- resolution versus latency
- small-object recall versus noise
- annotation cost versus output quality
- threshold strictness versus operational tolerance

This is why post-processing choices such as confidence thresholds and non-maximum suppression are not afterthoughts. They directly change what users see.

## 6. Common Mistakes

1. **Task mismatch.** Using detection when exact boundaries matter, or segmentation when boxes are sufficient, wastes effort or loses critical detail; define the operational output precisely first.
2. **Annotation complacency.** Poor boxes or masks cap model quality early; audit label consistency before blaming the architecture.
3. **Small-object neglect.** Training and evaluating at too low a resolution hides weak recall on small targets; inspect performance by size bucket.
4. **Threshold blindness.** Reporting one metric without studying precision-recall tradeoffs misses deployment tuning; select thresholds against real operating costs.
5. **Post-processing neglect.** Treating NMS or mask cleanup as secondary can leave duplicate or noisy outputs in production; validate the full inference stack.

## 7. Practical Checklist

- [ ] Choose detection or segmentation based on the downstream decision.
- [ ] Audit annotation quality before large training runs.
- [ ] Measure performance by object size and crowding level.
- [ ] Tune confidence and suppression thresholds against operational costs.
- [ ] Visualize qualitative outputs alongside summary metrics.
- [ ] Benchmark full-pipeline latency, not just model forward time.

## 8. References

- Ren, Shaoqing, et al. "Faster R-CNN." 2015. <https://arxiv.org/abs/1506.01497>
- Redmon, Joseph, et al. "You Only Look Once." 2016. <https://arxiv.org/abs/1506.02640>
- Lin, Tsung-Yi, et al. "Focal Loss for Dense Object Detection." 2018. <https://arxiv.org/abs/1708.02002>
- He, Kaiming, et al. "Mask R-CNN." 2017. <https://arxiv.org/abs/1703.06870>
- Kirillov, Alexander, et al. "Panoptic Segmentation." 2019. <https://arxiv.org/abs/1801.00868>
- Szeliski, Richard. *Computer Vision: Algorithms and Applications* (2nd ed.). Springer, 2022. <https://szeliski.org/Book/>
- COCO. "Detection evaluation." <https://cocodataset.org/#detection-eval>
