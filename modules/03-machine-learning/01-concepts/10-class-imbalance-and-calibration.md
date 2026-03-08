# Class Imbalance and Calibration

## Key Ideas

- Class imbalance changes what a “good” classifier should optimize, so accuracy alone can become misleading even when a model is operationally useless.
- Calibration asks whether predicted probabilities match observed frequencies, which is a different question from ranking quality or thresholded classification accuracy.
- Threshold selection, resampling, class weighting, and calibration should be treated as separate decisions because each changes model behavior in a different way.
- A classifier can rank examples well but still produce poorly calibrated probabilities, which matters when decisions depend on risk scores rather than hard labels.
- Evaluation under imbalance must connect the metric, threshold, and probability quality to the real decision costs rather than to a default library setting.

## 1. What It Is

Class imbalance occurs when one class appears much less often than another, such as fraud detection, equipment failure prediction, or rare disease screening. Calibration studies whether a model's stated probabilities are numerically trustworthy.

### 1.1 Core Definitions

- A **positive class** is the outcome of special interest, often the rarer one.
- A **decision threshold** converts a predicted score or probability into a class label.
- **Precision** is the fraction of predicted positives that are correct.
- **Recall** is the fraction of true positives that are found.
- **Calibration** means that predictions near probability `p` occur with frequency approximately `p`.
- A **reliability diagram** compares predicted probabilities with observed outcome frequencies.

### 1.2 Why This Matters

A model can achieve high accuracy by predicting the majority class almost always, yet fail completely at the task people actually care about. Similarly, a model can have strong ranking performance but poor probability estimates, making it unreliable for triage, prioritization, or cost-sensitive decisions.

## 2. Imbalance Changes Evaluation

### 2.1 Accuracy Can Mislead

If only `1%` of examples are positive, a classifier that predicts every example as negative achieves `99%` accuracy but zero recall on the positive class.

### 2.2 Better Metrics

Under imbalance, common alternatives include:

- precision,
- recall,
- F1,
- precision-recall curves,
- ROC-AUC,
- and cost-aware expected utility.

The right choice depends on the downstream decision. Precision and recall are not universally “better”; they are better only when they reflect the actual stakes.

## 3. Calibration and Thresholding

### 3.1 Calibration

Suppose a model outputs a probability `0.8`. A well-calibrated model means predictions around `0.8` should be correct about `80%` of the time over many similar cases.

### 3.2 Threshold Choice

The default threshold `0.5` is rarely sacred. If missed positives are very expensive, a lower threshold may be better. If false alarms are expensive, a higher threshold may be better.

### 3.3 Rebalancing Techniques

Common ways to respond to imbalance include:

- class weighting,
- oversampling,
- undersampling,
- threshold adjustment,
- or explicitly calibrated post-processing.

These are different interventions and should not be conflated.

## 4. Worked Example

Suppose a dataset has `100` cases:

```text
10 positives
90 negatives
```

A classifier predicts `12` positives. Among those predicted positives:

```text
8 are true positives
4 are false positives
```

That means:

```text
false negatives = 10 - 8 = 2
true negatives = 90 - 4 = 86
```

### 4.1 Compute Accuracy

```text
accuracy = (true_positives + true_negatives) / total
accuracy = (8 + 86) / 100 = 94 / 100 = 0.94
```

### 4.2 Compute Precision and Recall

```text
precision = true_positives / predicted_positives = 8 / 12 ≈ 0.667
recall = true_positives / actual_positives = 8 / 10 = 0.8
```

### 4.3 Interpret the Result

An accuracy of `94%` sounds excellent, but it hides the fact that one-third of predicted positives are wrong and two real positives were missed. Precision and recall reveal the tradeoff more clearly.

### 4.4 Calibration Illustration

Now suppose the model produced five probability predictions near `0.8`, but only three of those five cases were actually positive.

Observed positive rate in that bin is:

```text
3 / 5 = 0.6
```

So the model is overconfident in that probability region because it predicts `0.8` while reality is closer to `0.6`.

Verification: the confusion counts produce `accuracy = 0.94`, `precision ≈ 0.667`, and `recall = 0.8`, and the `0.8` probability bin with `3/5` positives shows overconfidence because `0.6 < 0.8`.

## 5. Pseudocode Pattern

```text
procedure precision_recall(true_positives, false_positives, false_negatives):
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)
    return precision, recall
```

Time: `Theta(1)` worst case once the confusion counts are known. Space: `Theta(1)` auxiliary space.

## 6. Common Mistakes

1. **Accuracy-only evaluation.** Reporting only accuracy on highly imbalanced data can hide total failure on the minority class; include metrics that expose the positive-class tradeoff.
2. **Threshold-default worship.** Treating `0.5` as the natural threshold ignores cost asymmetry and prevalence; choose thresholds using the decision objective, not convention alone.
3. **Ranking-calibration confusion.** Assuming a model with good ROC-AUC must also have reliable probabilities conflates two different properties; evaluate calibration separately.
4. **Resampling-equivalence claims.** Treating class weights, oversampling, and threshold shifts as interchangeable hides their different effects on optimization and decision behavior; test them separately.
5. **Probability-overtrust.** Using raw model scores as probabilities without checking reliability can produce bad operational decisions; calibrate or at least audit probability quality first.

## 7. Practical Checklist

- [ ] Measure class prevalence before choosing any metric or threshold.
- [ ] Report at least one threshold-free and one thresholded metric on imbalanced tasks.
- [ ] Tune the decision threshold using validation data and decision costs.
- [ ] Check reliability diagrams or calibration curves when probabilities drive action.
- [ ] Compare class weighting and resampling as separate interventions.
- [ ] Keep the final test set untouched while choosing thresholds and calibration methods.

## 8. References

- Niculescu-Mizil, Alexandru, and Rich Caruana. 2005. Predicting Good Probabilities with Supervised Learning. *ICML 2005*. <https://www.cs.cornell.edu/~alexn/papers/calibration.icml05.crc.rev3.pdf>
- Saito, Takaya, and Marc Rehmsmeier. 2015. The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets. *PLOS ONE* 10(3). <https://doi.org/10.1371/journal.pone.0118432>
- Provost, Foster, and Tom Fawcett. 2013. *Data Science for Business*. O'Reilly Media.
- scikit-learn. 2025. *Probability calibration*. <https://scikit-learn.org/stable/modules/calibration.html>
- scikit-learn. 2025. *Classification metrics*. <https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics>
- imbalanced-learn. 2025. *User Guide*. <https://imbalanced-learn.org/stable/user_guide.html>
- Kuhn, Max, and Kjell Johnson. 2013. *Applied Predictive Modeling*. Springer.
