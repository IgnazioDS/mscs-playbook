# Data Leakage and Reproducibility

## Key Ideas

- Data leakage occurs when the training process uses information that would not be available at prediction time, so the reported performance no longer measures the real task.
- Reproducibility means that an experiment can be rerun with the same setup and produce materially consistent results, which is necessary for trustworthy comparison and debugging.
- Leakage often enters through preprocessing, splitting, temporal ordering, target-derived features, or repeated tuning on the same evaluation set rather than through obviously illegal variables.
- Reproducibility is broader than setting a random seed; it also depends on pinned data versions, pipeline definitions, feature generation, and evaluation protocol.
- A non-reproducible experiment cannot support strong conclusions because apparent improvements may be artifacts of randomness or hidden procedural changes.

## 1. What It Is

Leakage is the accidental inclusion of information from outside the legitimate training context. Reproducibility is the ability to rerun the same experiment and obtain results that are consistent enough to support the same scientific conclusion.

### 1.1 Core Definitions

- **Data leakage** is any information path that lets training benefit from knowledge unavailable at inference time.
- **Target leakage** uses variables that encode the label directly or indirectly.
- **Split leakage** occurs when train and evaluation data are not properly isolated.
- A **deterministic pipeline** is a pipeline whose outputs are stable under the same inputs and environment.
- **Experiment provenance** is the record of data version, code version, configuration, and random state used for a run.

### 1.2 Why This Matters

Leakage can make a weak model look excellent offline and then fail in production. Poor reproducibility makes it impossible to tell whether a supposed improvement came from a real design change or from random variation, data drift, or an unrecorded preprocessing change. These are not cosmetic issues. They directly determine whether model-development claims are trustworthy.

## 2. Common Leakage Paths

### 2.1 Preprocessing Before Splitting

Fitting scalers, imputers, encoders, or reducers on the full dataset before the split exposes validation or test information to training.

### 2.2 Temporal Leakage

If the task predicts the future, random shuffling can leak future observations into training. Time-aware problems require time-aware validation.

### 2.3 Entity or Group Leakage

If multiple rows come from the same user, device, patient, or session, random splitting can place near-duplicates across training and evaluation sets. That inflates performance without improving true generalization.

## 3. Reproducibility Controls

### 3.1 Randomness Control

Random seeds help stabilize operations such as:

- train/validation splitting,
- parameter initialization,
- minibatch ordering,
- and stochastic search.

### 3.2 Data and Code Versioning

Reproducibility also requires recording:

- the dataset snapshot,
- the feature-generation code,
- the package versions,
- and the exact hyperparameters.

### 3.3 Experiment Logging

A useful experiment record should make it possible to answer:

- what data was used,
- what model and preprocessing pipeline were used,
- what split was used,
- what metric was reported,
- and what configuration produced the result.

## 4. Worked Example

Suppose a binary classification dataset has `1000` rows. A team wants to standardize numeric features and evaluate a logistic-regression model.

They compare two workflows.

### 4.1 Correct Workflow

1. Split data into `800` training rows and `200` validation rows.
2. Fit the scaler on the `800` training rows only.
3. Transform both training and validation rows using that scaler.
4. Train the model on transformed training data.
5. Evaluate once on transformed validation data.

### 4.2 Leaked Workflow

1. Fit the scaler on all `1000` rows first.
2. Transform all `1000` rows.
3. Split into `800` training rows and `200` validation rows.
4. Train and evaluate.

### 4.3 Why the Second Workflow Is Wrong

The second workflow allows the validation distribution to influence the scaling parameters seen during training. Even though the labels were not leaked directly, the evaluation is no longer a clean estimate of future performance.

### 4.4 Reproducibility Extension

Now suppose the team reruns the correct workflow but changes:

- the random split,
- the package version,
- and the feature list,

without recording those changes. If the metric moves from `0.81` to `0.84`, the team cannot tell whether the improvement is real or procedural.

Verification: the leaked workflow is invalid because the scaler is fit on `1000` rows instead of only the `800` training rows, and the unreproducible rerun is scientifically ambiguous because multiple uncontrolled variables changed at once.

## 5. Pseudocode Pattern

```text
procedure run_reproducible_experiment(dataset, split_seed, config):
    train_set, validation_set = split_dataset(dataset, split_seed)
    pipeline = fit_pipeline(train_set, config)
    score = evaluate(pipeline, validation_set)
    log_run(split_seed, config, score)
    return score
```

Time: O(n d) worst case for fitting and evaluating a simple pipeline on `n` examples with `d` features, excluding the cost of more expensive model-specific training. Space: O(n d) worst case if the split datasets and transformed matrices are materialized explicitly.

## 6. Common Mistakes

1. **Seed-only reproducibility.** Treating a fixed random seed as sufficient ignores data versioning, package versions, and pipeline definition; log the full experiment context.
2. **Leakage-by-preprocessing.** Performing transformations on the full dataset before splitting is still leakage even when labels are untouched; fit preprocessing on training data only.
3. **Random-split temporal tasks.** Using shuffled validation on future-prediction problems leaks time structure; split according to chronology.
4. **Unlogged comparisons.** Declaring one run better than another without recording the exact configuration makes the comparison scientifically weak; keep experiment provenance.
5. **Entity-overlap blindness.** Allowing rows from the same entity into both training and validation can create near-duplicate leakage; check grouping assumptions explicitly.

## 7. Practical Checklist

- [ ] Fit every preprocessing step on the training split only.
- [ ] Choose grouped or temporal splits when the data-generating process requires them.
- [ ] Pin and record data version, code version, package version, and configuration.
- [ ] Control random seeds for splitting, initialization, and search procedures when applicable.
- [ ] Log every reported metric together with the exact split and pipeline used.
- [ ] Treat unexpected metric jumps as a reason to audit leakage before celebrating improvement.

## 8. References

- Kaufman, Shachar, et al. 2012. Leakage in Data Mining: Formulation, Detection, and Avoidance. *ACM TKDD* 6(4). <https://doi.org/10.1145/2382577.2382579>
- Cawley, Gavin C., and Nicola L. C. Talbot. 2010. On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation. *Journal of Machine Learning Research* 11. <https://jmlr.org/papers/v11/cawley10a.html>
- Kuhn, Max, and Kjell Johnson. 2019. *Feature Engineering and Selection*. Chapman and Hall/CRC.
- Géron, Aurelien. 2022. *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media.
- scikit-learn. 2025. *Common pitfalls and recommended practices*. <https://scikit-learn.org/stable/common_pitfalls.html>
- Pineau, Joelle, et al. 2021. Improving Reproducibility in Machine Learning Research. *Journal of Machine Learning Research* 22(164). <https://jmlr.org/papers/v22/20-303.html>
- Kapoor, Sayash, and Arvind Narayanan. 2023. *Leakage and the Reproducibility Crisis in ML-based Science*. <https://arxiv.org/abs/2207.07048>
