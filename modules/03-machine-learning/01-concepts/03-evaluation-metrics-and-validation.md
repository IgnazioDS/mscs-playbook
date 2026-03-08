# Evaluation Metrics and Validation

## Key Ideas

- Model evaluation is about estimating future task performance, so the metric and the validation design must match the decision setting rather than default library choices.
- Different metrics answer different questions: accuracy, log loss, F1, ROC-AUC, and mean squared error are not interchangeable summaries of quality.
- Validation is not a decorative final step; it is the procedure that separates genuine generalization from optimistic self-measurement on training data.
- A poor split strategy can invalidate an otherwise correct metric, especially with temporal data, grouped entities, or class imbalance.
- The test set should be treated as a final audit, not as a convenient extra validation set for repeated tuning.

## 1. What It Is

Evaluation metrics quantify how well a model performs on labeled data, while validation procedures estimate how that performance is likely to transfer to new data. Together they define the evidence used to decide whether a model is acceptable.

### 1.1 Core Definitions

- A **metric** is a numerical summary of model performance, such as accuracy or mean absolute error.
- A **validation split** is the partitioning of data used to estimate generalization during development.
- A **holdout set** is a subset reserved for evaluation rather than training.
- **Cross-validation** repeatedly reuses different held-out folds to estimate performance more stably.
- A **test set** is the final untouched evaluation set used once the modeling decisions are complete.

### 1.2 Why This Matters

If the metric does not reflect the real decision objective, the model may optimize the wrong behavior. If the validation design does not reflect the deployment setting, the reported score may be systematically optimistic. Evaluation is therefore part of the model definition, not an afterthought.

## 2. Choosing Metrics

### 2.1 Classification Metrics

Common classification metrics include:

- **accuracy** for overall label agreement,
- **precision** and **recall** for positive-class tradeoffs,
- **F1** for balancing precision and recall,
- **ROC-AUC** for ranking quality across thresholds,
- **log loss** for probability quality.

Each metric emphasizes a different failure mode.

### 2.2 Regression Metrics

Common regression metrics include:

- **mean squared error (MSE)**, which penalizes larger errors more heavily,
- **root mean squared error (RMSE)**, which restores the original unit scale,
- **mean absolute error (MAE)**, which is less sensitive to large outliers,
- **R-squared**, which summarizes variance explained under a specific baseline comparison.

### 2.3 Metric-Objective Alignment

The correct metric depends on the operational cost structure. A rare-event classifier may care more about recall at an acceptable precision than about overall accuracy. A forecast used for budgeting may care more about MAE than about RMSE if large errors are not disproportionately costly.

## 3. Validation Design

### 3.1 Holdout Validation

A simple train/validation split is easy to implement and interpret, but it can be noisy when the dataset is small.

### 3.2 Cross-Validation

Cross-validation evaluates the model across multiple held-out folds:

- it reduces dependence on one lucky or unlucky split,
- it costs more computation,
- it is often preferable when data is limited.

### 3.3 Specialized Splits

Some data requires non-random splitting:

- **time-based splits** for temporal prediction,
- **grouped splits** when multiple rows belong to one entity,
- **stratified splits** when class balance must be preserved approximately.

The split strategy should match the deployment condition the model will actually face.

## 4. Worked Example

Suppose a binary classifier makes predictions on `10` validation examples.

Confusion counts:

```text
true_positives = 3
false_positives = 1
true_negatives = 5
false_negatives = 1
```

### 4.1 Compute Accuracy

```text
accuracy = (true_positives + true_negatives) / total
accuracy = (3 + 5) / 10 = 8 / 10 = 0.8
```

### 4.2 Compute Precision

```text
precision = true_positives / (true_positives + false_positives)
precision = 3 / (3 + 1) = 3 / 4 = 0.75
```

### 4.3 Compute Recall

```text
recall = true_positives / (true_positives + false_negatives)
recall = 3 / (3 + 1) = 3 / 4 = 0.75
```

### 4.4 Interpret the Result

The model is `80%` accurate overall, but the positive-class precision and recall are both `0.75`. Whether that is acceptable depends on the application. Accuracy alone is not enough to answer that question.

Verification: the confusion counts sum to `10`, and they yield `accuracy = 0.8`, `precision = 0.75`, and `recall = 0.75`, so the metric calculations are internally consistent.

## 5. Pseudocode Pattern

```text
procedure accuracy_precision_recall(tp, fp, tn, fn):
    total = tp + fp + tn + fn
    accuracy = (tp + tn) / total
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    return accuracy, precision, recall
```

Time: Theta(1) worst case once confusion counts are known. Space: Theta(1) auxiliary space.

## 6. Common Mistakes

1. **Accuracy defaulting.** Reporting accuracy by default even when the class distribution or decision cost makes it uninformative leads to bad model selection; choose metrics that reflect the real task.
2. **Random-split misuse.** Using random splits on temporal or grouped data can leak future or related information into validation; match the split design to the data structure.
3. **Metric blending without meaning.** Presenting many metrics without explaining which one drives the decision creates ambiguity; identify the primary decision metric explicitly.
4. **Test-set reuse.** Repeatedly inspecting test performance during development causes hidden overfitting to the test set; keep it untouched until the end.
5. **Point-estimate overconfidence.** Treating one validation score as a precise truth hides sampling variability; use cross-validation or repeated evaluation when instability matters.

## 7. Practical Checklist

- [ ] Write down the decision objective before selecting the metric.
- [ ] Choose a split strategy that matches temporal, grouped, or class-balance constraints.
- [ ] Reserve the test set for the final evaluation only.
- [ ] Use cross-validation when one holdout split is too unstable for the dataset size.
- [ ] Report the primary metric and supporting diagnostics separately.
- [ ] Check whether the chosen metric is sensitive to class imbalance or calibration quality.

## 8. References

- Kuhn, Max, and Kjell Johnson. 2013. *Applied Predictive Modeling*. Springer.
- Géron, Aurelien. 2022. *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media.
- Hastie, Trevor, Robert Tibshirani, and Jerome Friedman. 2009. *The Elements of Statistical Learning* (2nd ed.). Springer. <https://hastie.su.domains/ElemStatLearn/>
- Murphy, Kevin P. 2022. *Probabilistic Machine Learning: An Introduction*. MIT Press.
- scikit-learn. 2025. *Metrics and scoring*. <https://scikit-learn.org/stable/modules/model_evaluation.html>
- Saito, Takaya, and Marc Rehmsmeier. 2015. The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets. *PLOS ONE* 10(3). <https://doi.org/10.1371/journal.pone.0118432>
- Kohavi, Ron. 1995. A Study of Cross-Validation and Bootstrap for Accuracy Estimation and Model Selection. *IJCAI 1995*. <https://www.ijcai.org/Proceedings/95-2/Papers/016.pdf>
