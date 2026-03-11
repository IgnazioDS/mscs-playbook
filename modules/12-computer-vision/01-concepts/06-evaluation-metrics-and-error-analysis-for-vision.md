# Evaluation Metrics and Error Analysis for Vision

## Key Ideas

- Vision evaluation must match the task because classification, detection, segmentation, OCR, and retrieval fail in different ways.
- Aggregate metrics can hide failures on small objects, rare classes, lighting conditions, or acquisition sources, so slice-based analysis is essential.
- Metrics such as accuracy, IoU, Dice, mAP, and recall only become meaningful when annotation quality and split design are sound.
- Qualitative review is necessary because many vision failures involve labeling ambiguity, boundary artifacts, or environmental context that summary metrics cannot explain.
- Error analysis should guide data collection, annotation cleanup, and threshold tuning rather than only reporting model quality after the fact.

## 1. Why Vision Evaluation Is Task-Specific

A classifier answering "what is in this image?" and a detector answering "where are the objects?" should not be judged by the same metric. The right metric depends on what the system must get right operationally.

Examples:

- image classification often uses accuracy, precision, recall, and F1
- object detection often uses IoU-based matching and mean average precision
- segmentation often uses IoU or Dice

Choosing the wrong metric can hide operational failure.

## 2. Core Metrics

### 2.1 Classification

Useful metrics include:

- accuracy
- precision
- recall
- F1 score

### 2.2 Detection

Detection usually depends on an **intersection over union** threshold to decide whether a predicted box matches a ground-truth box.

### 2.3 Segmentation

Segmentation often uses:

- IoU
- Dice coefficient

These capture overlap quality between predicted and true masks.

## 3. Why Slice Analysis Matters

A model may look strong overall while failing on:

- small objects
- dark scenes
- rare classes
- blurred images
- specific camera sources

Those are often the exact conditions that matter in deployment. Slice analysis therefore turns evaluation into a debugging tool rather than a scoreboard.

## 4. Worked Example: IoU for One Detection

Suppose a predicted box has:

```text
area(prediction) = 120
```

The ground-truth box has:

```text
area(ground_truth) = 100
```

Their overlap area is:

```text
intersection = 80
```

### 4.1 Union

```text
union = 120 + 100 - 80 = 140
```

### 4.2 IoU

```text
IoU = 80 / 140 ≈ 0.571
```

If the matching threshold is `0.5`, this counts as a correct detection. If the threshold is `0.75`, it does not.

Verification: the same box can be considered correct or incorrect depending on the IoU threshold, which is why evaluation definitions must be stated explicitly.

## 5. Error Analysis Workflow

A practical workflow is:

1. compute task metrics
2. slice results by class, size, and acquisition condition
3. inspect representative failures visually
4. decide whether the main problem is annotation quality, preprocessing, thresholding, or modeling

This is the step that turns metrics into engineering decisions.

## 6. Common Mistakes

1. **Metric mismatch.** Optimizing classification accuracy when the real task is localization misses the operational need; choose metrics aligned with the actual decision.
2. **Annotation complacency.** Trusting noisy or inconsistent labels makes metrics unstable; audit label quality before drawing strong conclusions.
3. **Aggregate-only reporting.** Looking only at global scores hides failures on small objects or rare classes; slice by the conditions that matter in deployment.
4. **Threshold opacity.** Reporting metrics without the thresholds or matching rules that define them makes comparisons misleading; document evaluation settings clearly.
5. **No visual review.** Numbers alone rarely explain why the model failed; inspect images from each major failure bucket.

## 7. Practical Checklist

- [ ] Use metrics that match the task’s operational goal.
- [ ] Document IoU thresholds, confidence thresholds, and matching rules.
- [ ] Review performance by class, size, source, and environment.
- [ ] Audit annotation quality before large model changes.
- [ ] Pair quantitative metrics with qualitative failure review.
- [ ] Re-run evaluation after threshold, data, or preprocessing changes.

## 8. References

- COCO. "Detection evaluation." <https://cocodataset.org/#detection-eval>
- Everingham, Mark, et al. "The Pascal Visual Object Classes Challenge." 2010. <https://link.springer.com/article/10.1007/s11263-009-0275-4>
- Rezatofighi, Hamid, et al. "Generalized Intersection over Union." 2019. <https://arxiv.org/abs/1902.09630>
- Milletari, Fausto, Nassir Navab, and Seyed-Ahmad Ahmadi. "V-Net." 2016. <https://arxiv.org/abs/1606.04797>
- Szeliski, Richard. *Computer Vision: Algorithms and Applications* (2nd ed.). Springer, 2022. <https://szeliski.org/Book/>
- Bolya, Daniel, et al. "YOLACT." 2019. <https://arxiv.org/abs/1904.02689>
- Ribeiro, Marco Tulio, et al. "Beyond Accuracy" is NLP-focused, but the slice-based evaluation discipline applies broadly. <https://aclanthology.org/2020.acl-main.442/>
