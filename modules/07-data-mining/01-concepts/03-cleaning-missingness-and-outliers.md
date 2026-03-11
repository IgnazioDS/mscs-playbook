# Cleaning, Missingness, and Outliers

## Key Ideas

- Cleaning is the set of transformations that correct or stabilize the dataset before mining, but every cleaning step changes what patterns can later be discovered.
- Missingness is not a single phenomenon; values may be absent for different reasons, and those reasons affect whether imputation, deletion, or explicit missing-value modeling is appropriate.
- Outliers are unusual observations, but unusual does not automatically mean erroneous; some outliers are exactly the cases the mining workflow is meant to surface.
- Cleaning should preserve traceability so that the team can distinguish source problems from intentional preprocessing decisions.
- The best cleaning strategy is task-dependent: association rules, clustering, anomaly detection, and supervised validation react differently to the same cleaning choices.

## 1. What Cleaning Tries to Achieve

Cleaning aims to make the dataset usable without silently erasing important signal. It addresses missing values, inconsistent types, duplicates, impossible values, and suspicious extremes.

### 1.1 Core Definitions

- **Imputation** replaces missing values using a rule such as mean, median, or most-frequent value.
- **Deletion** removes rows or columns that fail a chosen criterion.
- An **outlier** is an observation that is unusually far from the majority under a chosen measurement.
- **Winsorization** caps extreme values at chosen thresholds rather than removing them.
- A **missingness mechanism** is the process that causes values to be absent.

### 1.2 Why This Matters

Mining methods are sensitive to data quality. Distance-based methods can be dominated by a few extreme values, while association-rule mining can be distorted by duplicated or malformed transactions. Cleaning is therefore part of the model design, not merely housekeeping.

## 2. Handling Missingness

### 2.1 Diagnose Before Imputing

The team should ask:

- which fields are missing,
- how often they are missing,
- whether missingness is random or process-related,
- whether missingness itself carries information.

### 2.2 Common Strategies

Typical options include:

- dropping fields with extreme missingness,
- row deletion when the missing portion is small and non-critical,
- median or mode imputation,
- adding a missingness indicator feature.

### 2.3 Tradeoffs

Imputation stabilizes later methods, but it can also flatten real variation or create artificial clusters if used carelessly.

## 3. Handling Outliers

### 3.1 Detecting Outliers

Common methods include IQR thresholds, z-scores, robust scaling, or domain-specific bounds.

### 3.2 Distinguishing Error from Rare Signal

A transaction amount of `0` may be an ingestion bug, while a very large purchase may be a valuable signal. Cleaning should not erase important rare behavior without justification.

### 3.3 Task-Specific Treatment

For clustering, capping extremes may stabilize distances. For anomaly detection, removing extremes may destroy the actual object of interest.

## 4. Worked Example: IQR-Based Outlier Review

Suppose a purchase-amount field has:

```text
Q1 = 20
Q3 = 50
```

### 4.1 Compute the IQR

```text
IQR = Q3 - Q1 = 50 - 20 = 30
```

### 4.2 Compute Standard IQR Bounds

Lower bound:

```text
lower = Q1 - 1.5 * IQR
lower = 20 - 1.5 * 30
lower = 20 - 45 = -25
```

Upper bound:

```text
upper = Q3 + 1.5 * IQR
upper = 50 + 45 = 95
```

### 4.3 Classify Example Values

For the values:

```text
18, 44, 91, 130
```

- `18` is within bounds
- `44` is within bounds
- `91` is within bounds
- `130` is above `95`, so it is flagged as an outlier candidate

This does not prove that `130` is an error. It only means it deserves review.

Verification: the IQR calculation yields bounds of `-25` and `95`, so among the example values only `130` falls outside the upper bound and is correctly flagged.

## 5. Common Mistakes

1. **Blind imputation.** Filling missing values before understanding why they are missing can introduce false structure; profile the missingness pattern first.
2. **Rare-signal deletion.** Removing all outliers by default may erase the cases the analysis actually needs to explain; distinguish error correction from rare-event discovery.
3. **Unlogged cleaning.** Transforming data without recording thresholds and rules breaks reproducibility; treat cleaning as part of the formal pipeline.
4. **One-strategy-for-all-fields.** Applying the same imputation or outlier rule to every column ignores semantics and units; choose strategies field by field.
5. **Task-insensitive cleaning.** Using the same cleanup plan for clustering and anomaly detection can be self-defeating; adapt preprocessing to the mining objective.

## 6. Practical Checklist

- [ ] Quantify missingness by field before choosing deletion or imputation.
- [ ] Document whether missingness itself may be informative.
- [ ] Use domain constraints alongside statistical heuristics for outlier review.
- [ ] Record every cleaning threshold and transformation in the pipeline metadata.
- [ ] Recompare distributions before and after cleaning to detect overcorrection.
- [ ] Match the cleaning strategy to the downstream mining task.

## 7. References

- Little, Roderick J. A., and Donald B. Rubin. 2019. *Statistical Analysis with Missing Data* (3rd ed.). Wiley.
- Han, Jiawei, Micheline Kamber, and Jian Pei. 2011. *Data Mining: Concepts and Techniques* (3rd ed.). Morgan Kaufmann.
- Tan, Pang-Ning, Michael Steinbach, Anuj Karpatne, and Vipin Kumar. 2018. *Introduction to Data Mining* (2nd ed.). Pearson.
- scikit-learn. 2026. *SimpleImputer*. <https://scikit-learn.org/stable/modules/generated/sklearn.impute.SimpleImputer.html>
- pandas. 2026. *Missing Data*. <https://pandas.pydata.org/docs/user_guide/missing_data.html>
- Wilcox, Rand R. 2017. *Introduction to Robust Estimation and Hypothesis Testing* (4th ed.). Academic Press.
- Iglewicz, Boris, and David Hoaglin. 1993. *How to Detect and Handle Outliers*. ASQC Quality Press.
