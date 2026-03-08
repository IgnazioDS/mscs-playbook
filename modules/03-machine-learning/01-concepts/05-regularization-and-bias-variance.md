# Regularization and Bias/Variance

## Key Ideas

- Regularization changes the effective complexity of a model so that it fits repeatable structure rather than noise in the training data.
- Bias and variance describe two different ways a model can generalize poorly: one through systematic underfitting and the other through instability across datasets.
- The useful question is not whether a model is simple or complex in the abstract, but whether its capacity is appropriate for the data, representation, and evaluation regime.
- Regularization can act through explicit penalties, early stopping, architecture constraints, data augmentation, or search-space restrictions.
- Learning curves are often more informative than single summary scores when diagnosing whether bias or variance is the dominant problem.

## 1. What It Is

Regularization is any method that constrains or stabilizes learning in order to improve generalization. The bias/variance framework is a conceptual tool for understanding why a model may perform poorly even when the implementation is correct.

### 1.1 Core Definitions

- **Bias** is the error from systematic inability to represent the true signal well.
- **Variance** is the error from sensitivity to sampling fluctuations in the training data.
- **Underfitting** means the model is too inflexible or too constrained to capture the relevant structure.
- **Overfitting** means the model fits noise or idiosyncrasies that do not generalize.
- An **L2 penalty** discourages large parameter magnitudes by adding a squared penalty term.
- An **L1 penalty** encourages sparsity by adding an absolute-value penalty term.

### 1.2 Why This Matters

Most practical model iteration is a search for an acceptable bias/variance tradeoff. A model that is too rigid misses important signal. A model that is too flexible learns patterns that vanish outside the training sample. Regularization provides the mechanisms used to control that tradeoff.

## 2. Bias and Variance Intuition

### 2.1 High Bias

High-bias models are typically too simple for the task. They often show:

- poor training performance,
- poor validation performance,
- similar errors on both datasets.

### 2.2 High Variance

High-variance models often show:

- strong training performance,
- weaker validation performance,
- large sensitivity to data split or hyperparameters.

### 2.3 Why the Tradeoff Exists

Increasing capacity can reduce bias but increase variance. Increasing regularization can reduce variance but increase bias. The right choice depends on data size, label quality, feature design, and model family.

## 3. Main Regularization Tools

### 3.1 Explicit Penalties

An objective with regularization often looks like:

```text
objective = empirical_loss + lambda * penalty
```

where `lambda` sets the regularization strength.

### 3.2 Implicit Regularization

Not all regularization appears as a penalty term. Examples include:

- early stopping,
- limited model depth,
- dropout,
- data augmentation,
- and constrained search spaces.

### 3.3 Learning-Curve Diagnosis

Learning curves compare training and validation error as the training set grows. They are useful because they reveal whether the current problem is primarily lack of capacity, lack of data, or excessive variance.

## 4. Worked Example

Suppose two models are trained on the same classification task.

Model A:

```text
training error = 0.22
validation error = 0.25
```

Model B:

```text
training error = 0.03
validation error = 0.21
```

### 4.1 Diagnose Model A

Model A has relatively high training error and only a small train/validation gap:

```text
gap_A = 0.25 - 0.22 = 0.03
```

This suggests high bias or underfitting.

### 4.2 Diagnose Model B

Model B has very low training error but a much larger validation gap:

```text
gap_B = 0.21 - 0.03 = 0.18
```

This suggests high variance or overfitting.

### 4.3 Choose an Intervention

Reasonable next steps are:

- for Model A: increase capacity, improve features, or reduce regularization,
- for Model B: increase regularization, simplify the model, add data, or improve validation discipline.

Verification: Model A's small gap with high training error is consistent with underfitting, while Model B's large gap with near-perfect training fit is consistent with overfitting.

## 5. Pseudocode Pattern

```text
procedure train_validation_gap(training_error, validation_error):
    return validation_error - training_error
```

Time: Theta(1) worst case. Space: Theta(1) auxiliary space.

## 6. Common Mistakes

1. **Complexity panic.** Assuming every complex model is automatically overfitting ignores the role of data size, regularization, and representation; diagnose with evidence, not intuition alone.
2. **Gap-only diagnosis.** Looking only at the train/validation gap without checking the absolute training error can misclassify underfitting as success; consider both fit quality and gap size.
3. **Penalty-only view.** Treating regularization as only L1 or L2 misses important implicit mechanisms such as early stopping or architecture constraints; account for all capacity controls.
4. **Data-free interpretation.** Declaring a variance problem without checking whether the dataset is simply too small or noisy skips a key cause of instability; connect diagnosis to data regime.
5. **One-score tuning.** Picking regularization strength from one convenient split can produce unstable conclusions; use a sound validation protocol when the choice matters.

## 7. Practical Checklist

- [ ] Inspect both training and validation performance before diagnosing bias or variance.
- [ ] Use learning curves when a single summary metric is not enough to explain failure.
- [ ] Tune regularization strength with validation data rather than by default values alone.
- [ ] Consider feature quality and data quantity before blaming the model family.
- [ ] Remember that early stopping and architecture choices also regularize learning.
- [ ] Re-evaluate bias/variance conclusions after any major representation change.

## 8. References

- Hastie, Trevor, Robert Tibshirani, and Jerome Friedman. 2009. *The Elements of Statistical Learning* (2nd ed.). Springer. <https://hastie.su.domains/ElemStatLearn/>
- Bishop, Christopher M. 2006. *Pattern Recognition and Machine Learning*. Springer.
- Goodfellow, Ian, Yoshua Bengio, and Aaron Courville. 2016. *Deep Learning*. MIT Press. <https://www.deeplearningbook.org/>
- Murphy, Kevin P. 2022. *Probabilistic Machine Learning: An Introduction*. MIT Press.
- James, Gareth, et al. 2021. *An Introduction to Statistical Learning* (2nd ed.). Springer. <https://www.statlearning.com/>
- Géron, Aurelien. 2022. *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media.
- Ng, Andrew. 2018. *Machine Learning Yearning*. <https://www.mlyearning.org/>
