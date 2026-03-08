# Model Selection and Hyperparameter Tuning

## Key Ideas

- Model selection is the process of choosing among competing model families or configurations using evidence that approximates future performance rather than training error alone.
- Hyperparameters control training behavior or model capacity, so they must be chosen through a validation procedure that is separate from the final test evaluation.
- A search strategy is only as good as its evaluation design, which is why nested tuning, correct validation splits, and reproducible search spaces matter more than blind parameter sweeps.
- Simple baselines and constrained search ranges often outperform large undisciplined searches because they reduce variance and make results easier to interpret.
- The goal of tuning is not merely to maximize one validation score but to choose a model that is robust, reproducible, and appropriate for the deployment constraints.

## 1. What It Is

Model selection is the decision process used to choose which estimator, architecture, or training configuration should be kept after comparing alternatives. Hyperparameter tuning is the search over settings such as regularization strength, tree depth, learning rate, or batch size that are not learned directly from the data by the estimator itself.

### 1.1 Core Definitions

- A **hyperparameter** is a configuration value set before training, such as `k` in k-nearest neighbors or `lambda` in regularization.
- A **search space** is the set or range of hyperparameter values considered.
- A **validation set** is data used to compare model configurations during development.
- A **test set** is held out until the final evaluation and should not drive tuning decisions.
- **Cross-validation** repeatedly partitions the training data to estimate generalization more stably.
- **Nested validation** separates outer evaluation from inner tuning to reduce selection bias.

### 1.2 Why This Matters

Most model improvements are not discovered by inventing a new algorithm. They come from choosing the right model family, regularization level, search range, and evaluation protocol. If tuning repeatedly looks at the test set or explores an uncontrolled number of alternatives, apparent improvements can be statistical noise rather than real progress.

## 2. Search Strategies

### 2.1 Grid Search

Grid search evaluates every combination from a predefined finite set of hyperparameter values.

- It is easy to reason about.
- It becomes expensive when many parameters are varied.

### 2.2 Random Search

Random search samples configurations from distributions over the search space.

- It often covers important dimensions more efficiently than dense grids.
- It is especially useful when only a few hyperparameters strongly affect performance.

### 2.3 Guided Search

More advanced methods such as Bayesian optimization or bandit-style search use prior evaluations to choose promising next trials. These methods can reduce evaluation cost, but they still depend on a sound validation protocol.

## 3. Validation Design

### 3.1 Holdout vs Cross-Validation

A single holdout split is simple and cheap, but its estimate may vary substantially on small datasets. Cross-validation trades more computation for a more stable comparison signal.

### 3.2 Avoiding Selection Bias

If the same validation set is used for many rounds of tuning, the search can overfit the validation process itself. That is why the final test set should remain untouched until the end, and why nested evaluation is preferred when selection pressure is high.

### 3.3 Practical Constraints

The best validation scheme depends on:

- dataset size,
- class imbalance,
- temporal structure,
- group dependencies,
- and compute budget.

There is no universally best tuner without regard to these constraints.

## 4. Worked Example

Suppose we compare logistic regression with three regularization settings using 3-fold cross-validation.

Validation scores:

```text
C = 0.1  -> [0.78, 0.80, 0.79]
C = 1.0  -> [0.82, 0.81, 0.83]
C = 10.0 -> [0.79, 0.84, 0.76]
```

Assume the metric is validation F1.

### 4.1 Compute Mean Validation Score

For `C = 0.1`:

```text
mean = (0.78 + 0.80 + 0.79) / 3 = 2.37 / 3 = 0.79
```

For `C = 1.0`:

```text
mean = (0.82 + 0.81 + 0.83) / 3 = 2.46 / 3 = 0.82
```

For `C = 10.0`:

```text
mean = (0.79 + 0.84 + 0.76) / 3 = 2.39 / 3 ≈ 0.797
```

### 4.2 Compare Stability

`C = 10.0` has one strong fold but also one noticeably weaker fold. `C = 1.0` has the highest mean and the most stable fold pattern among the three.

### 4.3 Choose the Configuration

Under this evidence, the best choice is:

```text
C = 1.0
```

Then retrain the model on the full training set with `C = 1.0` and evaluate once on the untouched test set.

Verification: the mean validation scores are `0.79`, `0.82`, and about `0.797`, so `C = 1.0` is the best configuration under the observed cross-validation evidence.

## 5. Pseudocode Pattern

```text
procedure select_best_config(configs, validation_scores):
    best_config = nil
    best_score = -infinity

    for config in configs:
        score = mean(validation_scores[config])
        if score > best_score:
            best_score = score
            best_config = config

    return best_config, best_score
```

Time: `Theta(m k)` worst case for `m` configurations with `k` recorded fold scores each. Space: `Theta(1)` auxiliary space beyond the stored score table.

## 6. Common Mistakes

1. **Test-set tuning.** Using test performance to choose hyperparameters destroys the purpose of the test set; tune on validation data and reserve test data for the final estimate only.
2. **Search-space sprawl.** Exploring many arbitrary ranges without prior reasoning increases variance and compute waste; define a compact, justified search space first.
3. **Mean-only selection.** Picking the highest mean score without checking fold variability can favor unstable configurations; inspect both central tendency and spread.
4. **Cross-validation mismatch.** Using random folds on grouped or temporal data breaks the deployment assumptions; choose a split strategy that matches the data-generating process.
5. **Baseline neglect.** Running complex searches before establishing a simple baseline makes improvement claims hard to interpret; compare every tuned model against a transparent reference.

## 7. Practical Checklist

- [ ] Define the metric and split strategy before starting any search.
- [ ] Keep the test set untouched until the final selected model is ready.
- [ ] Start from a simple baseline and a small, defensible search space.
- [ ] Prefer cross-validation when the dataset is small or noisy enough that one holdout is unstable.
- [ ] Record every tried configuration and score so the search is reproducible.
- [ ] Check whether the winning configuration is stable across folds, not just highest on average.

## 8. References

- Cawley, Gavin C., and Nicola L. C. Talbot. 2010. On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation. *Journal of Machine Learning Research* 11. <https://jmlr.org/papers/v11/cawley10a.html>
- Bergstra, James, and Yoshua Bengio. 2012. Random Search for Hyper-Parameter Optimization. *Journal of Machine Learning Research* 13. <https://jmlr.org/beta/papers/v13/bergstra12a.html>
- Kuhn, Max, and Kjell Johnson. 2013. *Applied Predictive Modeling*. Springer.
- Géron, Aurélien. 2022. *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media.
- scikit-learn. 2025. *Tuning the hyper-parameters of an estimator*. <https://scikit-learn.org/stable/modules/grid_search.html>
- Hastie, Trevor, Robert Tibshirani, and Jerome Friedman. 2009. *The Elements of Statistical Learning* (2nd ed.). Springer. <https://hastie.su.domains/ElemStatLearn/>
- Murphy, Kevin P. 2022. *Probabilistic Machine Learning: An Introduction*. MIT Press.
