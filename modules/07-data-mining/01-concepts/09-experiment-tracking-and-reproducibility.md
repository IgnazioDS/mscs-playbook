# Experiment Tracking and Reproducibility

## Key Ideas

- Experiment tracking records what data, code, parameters, and outputs produced a mining result so the team can rerun or audit it later.
- Reproducibility is not only about fixing random seeds; it also depends on dataset version, preprocessing choices, thresholds, and artifact storage.
- Mining workflows are especially vulnerable to irreproducibility because exploratory analysis often combines many manual decisions that are easy to forget.
- A tracked experiment should make it possible to explain both the result and the path that led to it.
- Reproducibility is what separates an interesting notebook from a reliable analytical workflow.

## 1. What Experiment Tracking Does

Experiment tracking captures the metadata needed to rerun or compare data mining workflows. It makes result provenance explicit.

### 1.1 Core Definitions

- An **experiment run** is one complete execution of a pipeline or mining configuration.
- **Provenance** is the record of where data, code, and outputs came from.
- A **seed** controls randomized parts of the workflow such as splitting or initialization.
- An **artifact** is a saved output such as a metric table, rule set, segmentation export, or plot.
- **Determinism** means the same inputs and configuration produce the same or materially equivalent outputs.

### 1.2 Why This Matters

Data mining often involves many threshold choices, random initializations, and manual exploration steps. If those are not recorded, a later rerun may produce a different segmentation or rule set with no clear explanation why.

## 2. What Must Be Recorded

### 2.1 Data and Code Version

The dataset snapshot, source extraction date, and code version are necessary to understand whether a later run is actually comparable.

### 2.2 Parameters and Thresholds

Support thresholds, contamination rates, selected features, and split rules all shape the output and should be logged explicitly.

### 2.3 Artifacts and Reports

Metrics alone are not enough. Many mining workflows also need saved plots, rule tables, cluster assignments, or anomaly-review exports.

## 3. Reproducibility Beyond Seeds

### 3.1 Randomness Control

Seeds matter for initialization-sensitive methods such as k-means or randomized forests.

### 3.2 Pipeline Definition

The transformation sequence must also be fixed. A run with the same seed but a different cleaning rule is not the same experiment.

### 3.3 Comparable Reporting

If runs report different metrics or use different filtering logic, comparisons become scientifically weak even when the code is similar.

## 4. Worked Example: Comparing Two Recorded Runs

Suppose two clustering runs are logged as:

```text
run_A:
    dataset_version = 2026-03-01
    seed = 42
    k = 3
    scaling = standard
    silhouette = 0.51

run_B:
    dataset_version = 2026-03-01
    seed = 42
    k = 4
    scaling = standard
    silhouette = 0.47
```

### 4.1 Identify What Changed

The dataset version, seed, and scaling are the same in both runs. The main modeled difference is:

```text
k changed from 3 to 4
```

### 4.2 Compare the Validation Signal

```text
0.51 > 0.47
```

So `run_A` is stronger under silhouette score.

### 4.3 Why Tracking Matters

Because the other key conditions are fixed, the team can reasonably attribute the score difference to the change in `k` rather than to a hidden dataset or preprocessing change.

Verification: the comparison is interpretable because both runs share the same dataset version, seed, and scaling, leaving the `k` change as the primary controlled difference.

## 5. Common Mistakes

1. **Seed-only reproducibility.** Assuming a seed alone makes the workflow reproducible ignores data and preprocessing drift; capture the whole run context.
2. **Notebook-memory dependence.** Relying on remembered exploratory steps instead of logged pipeline states makes later reruns unreliable; write decisions into the workflow record.
3. **Artifact loss.** Keeping only summary metrics but not the rule tables, assignments, or flagged cases makes validation and review hard; store task-specific artifacts too.
4. **Incomparable runs.** Comparing results produced under different filters, metrics, or dataset versions without noting it leads to false conclusions; standardize reporting before comparison.
5. **No provenance for decisions.** Presenting a final segmentation or rule set without documenting how it was produced weakens trust; retain the path from raw data to final artifact.

## 6. Practical Checklist

- [ ] Record dataset version, code version, and configuration for every run.
- [ ] Log seeds, thresholds, selected features, and preprocessing choices explicitly.
- [ ] Save artifacts that matter for later review, not only summary metrics.
- [ ] Use consistent reporting templates so runs are comparable.
- [ ] Keep experiment history alongside the implementation, not only in memory or chat.
- [ ] Reproduce at least one prior run after major pipeline changes to verify continuity.

## 7. References

- Kitzes, Justin, Daniel Turek, and Fatma Deniz, eds. 2018. *The Practice of Reproducible Research*. University of California Press. <https://www.practicereproducibility.org/>
- Pineau, Joelle, et al. 2021. Improving Reproducibility in Machine Learning Research. <https://jmlr.org/papers/v22/20-303.html>
- MLflow. 2026. *Tracking*. <https://mlflow.org/docs/latest/tracking.html>
- DVC. 2026. *Versioning Data and Pipelines*. <https://dvc.org/doc>
- Provost, Foster, and Tom Fawcett. 2013. *Data Science for Business*. O'Reilly Media.
- Han, Jiawei, Micheline Kamber, and Jian Pei. 2011. *Data Mining: Concepts and Techniques* (3rd ed.). Morgan Kaufmann.
- scikit-learn. 2026. *Common Pitfalls*. <https://scikit-learn.org/stable/common_pitfalls.html>
