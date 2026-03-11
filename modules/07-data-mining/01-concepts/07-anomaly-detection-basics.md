# Anomaly Detection Basics

## Key Ideas

- Anomaly detection searches for observations that differ meaningfully from the learned notion of normal behavior, but "different" depends on context, representation, and threshold choice.
- The most useful anomaly systems are designed around investigation cost and false-positive tolerance, not around abstract model novelty alone.
- Point anomalies, contextual anomalies, and collective anomalies are different problem types and should not be treated as interchangeable.
- Anomaly scores are rankings or signals of unusualness, not ground-truth labels, so they must be validated against domain review, holdout data, or downstream utility.
- Preprocessing and seasonality handling matter because many apparent anomalies are actually scale, drift, or context effects.

## 1. What Anomaly Detection Is

Anomaly detection identifies rare or unusual observations relative to an expected pattern of normal data. It is often used for fraud review, failure detection, abuse monitoring, or data-quality triage.

### 1.1 Core Definitions

- A **point anomaly** is an individual observation that is unusual by itself.
- A **contextual anomaly** is unusual only under certain conditions such as time, season, or region.
- A **collective anomaly** is a suspicious pattern that emerges only across multiple observations together.
- An **anomaly score** ranks observations by unusualness.
- **Contamination** is the assumed fraction of anomalous points in the data.

### 1.2 Why This Matters

Anomaly detection often sits in front of human review or automated intervention. A poor setup can overwhelm analysts with noise or miss costly rare events. The design must balance rarity detection with operational precision.

## 2. Common Approaches

### 2.1 Statistical Thresholding

Simple methods such as z-scores or robust thresholds are useful when the normal distribution is well understood and relatively stable.

### 2.2 Isolation and Density Methods

Methods such as Isolation Forest or Local Outlier Factor score points based on how isolated or sparse they are relative to the rest of the dataset.

### 2.3 Context-Aware Approaches

When seasonality or temporal context matters, anomaly scoring must consider what is normal for that time, place, or segment rather than what is globally rare.

## 3. Why Thresholding Is the Real Decision

### 3.1 Ranking Versus Action

A model can rank observations well, but the operational question is where to cut the list for alerting or review.

### 3.2 Precision-Recall Tradeoff

Lower thresholds catch more rare cases but usually increase false positives. Higher thresholds reduce noise but may miss important events.

### 3.3 Drift and Seasonality

Normal behavior changes. Thresholds that worked last month may become noisy or blind after process changes or seasonal swings.

## 4. Worked Example: Thresholding an Anomaly Score List

Suppose a model produces anomaly scores for five transactions:

```text
T1 = 0.12
T2 = 0.18
T3 = 0.74
T4 = 0.83
T5 = 0.21
```

Assume the team alerts on:

```text
score >= 0.70
```

### 4.1 Identify Flagged Transactions

Flagged items are:

```text
T3 = 0.74
T4 = 0.83
```

So the number of alerts is:

```text
alert_count = 2
```

### 4.2 Compute Alert Rate

```text
alert_rate = 2 / 5 = 0.40 = 40%
```

### 4.3 Interpret the Result

The model is not saying that `T3` and `T4` are definitely fraudulent or erroneous. It is saying they are the most unusual under the current scoring logic and threshold. Whether a `40%` alert rate is acceptable depends on review capacity and the expected rarity of real anomalies.

Verification: only `0.74` and `0.83` exceed the `0.70` threshold, so `2` out of `5` observations are correctly flagged, yielding an alert rate of `40%`.

## 5. Common Mistakes

1. **Score-as-truth thinking.** Treating anomaly scores as labels instead of as review priorities creates false certainty; validate flagged cases with domain evidence or downstream checks.
2. **Context neglect.** Ignoring time, seasonality, or segment differences causes many normal events to appear anomalous; make context part of the normality definition when needed.
3. **Threshold by intuition.** Choosing the alert threshold without reviewing workload and base-rate implications leads to operational noise; tune thresholds against review capacity and validation evidence.
4. **Rare-event cleaning.** Removing extreme points before anomaly analysis can erase the very cases the method should study; align preprocessing with the anomaly objective.
5. **Static-normal assumption.** Assuming normal behavior never drifts makes the detector stale; monitor score distribution and alert yield over time.

## 6. Practical Checklist

- [ ] Define what kind of anomaly the workflow is trying to detect.
- [ ] Choose features and context windows that reflect normal behavior realistically.
- [ ] Calibrate thresholds using review capacity, validation data, or top-k analysis.
- [ ] Track alert precision and analyst feedback when labels are available.
- [ ] Monitor drift in score distribution and false-positive volume over time.
- [ ] Treat anomaly outputs as investigation signals, not as automatic truth.

## 7. References

- Liu, Fei Tony, Kai Ming Ting, and Zhi-Hua Zhou. 2008. Isolation Forest. <https://doi.org/10.1109/ICDM.2008.17>
- Chandola, Varun, Arindam Banerjee, and Vipin Kumar. 2009. Anomaly Detection: A Survey. <https://doi.org/10.1145/1541880.1541882>
- Aggarwal, Charu C. 2017. *Outlier Analysis* (2nd ed.). Springer.
- Tan, Pang-Ning, Michael Steinbach, Anuj Karpatne, and Vipin Kumar. 2018. *Introduction to Data Mining* (2nd ed.). Pearson.
- scikit-learn. 2026. *Novelty and Outlier Detection*. <https://scikit-learn.org/stable/modules/outlier_detection.html>
- Breunig, Markus M., et al. 2000. LOF: Identifying Density-Based Local Outliers. <https://sigmodrecord.org/?smd_process_download=1&download_id=6631>
- Hawkins, Douglas M. 1980. *Identification of Outliers*. Chapman and Hall.
