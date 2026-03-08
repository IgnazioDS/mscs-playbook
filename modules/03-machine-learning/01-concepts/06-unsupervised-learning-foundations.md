# Unsupervised Learning Foundations

## Key Ideas

- Unsupervised learning studies data without target labels, so the central question is not "what is the correct answer?" but "what structure is stable enough to be worth modeling?"
- The main unsupervised goals are clustering, density estimation, and representation discovery, and each goal implies a different notion of similarity or usefulness.
- Distance, scaling, and feature representation matter more in unsupervised settings because there is no label signal to correct a poor geometry automatically.
- Unsupervised outputs are hypotheses about structure, not ground truth, so interpretation requires domain validation and downstream usefulness checks.
- A method can optimize its internal objective well and still produce misleading clusters or components if the objective does not match the real problem.

## 1. What Unsupervised Learning Is

Unsupervised learning is the study of methods that analyze observations without labeled outcomes. Instead of predicting a known target, the model tries to discover regularities such as groups, low-dimensional structure, or regions of high probability.

### 1.1 Core Definitions

- An **unlabeled dataset** contains observations without task-specific target values.
- A **cluster** is a set of observations judged to be similar under a chosen representation and similarity rule.
- A **density model** estimates which regions of the feature space are common or rare.
- A **representation** is a transformed version of the original data intended to preserve important structure.
- A **similarity measure** or **distance measure** defines how closeness between observations is computed.

### 1.2 Why This Matters

Many real datasets arrive before a target is defined. Teams use unsupervised methods to segment users, detect atypical behavior, compress high-dimensional measurements, initialize downstream models, and explore whether a problem even has coherent substructure. The value comes from discovering useful organization in data, not from achieving an evaluation score against labels.

## 2. Main Problem Types

### 2.1 Clustering

Clustering tries to partition observations into groups whose members are more similar to each other than to members of other groups. Common examples include customer segmentation and document grouping.

### 2.2 Density Estimation and Anomaly Detection

Density estimation models which regions of the input space are typical. Low-density observations can then be treated as unusual, which is useful for anomaly detection and novelty detection.

### 2.3 Representation Learning

Representation learning maps data into a new space that preserves important structure with fewer dimensions or more useful features. Principal component analysis, autoencoders, and embeddings are examples.

## 3. Why Geometry and Preprocessing Dominate

### 3.1 Distance Depends on Scale

If one feature ranges from `0` to `10,000` and another ranges from `0` to `1`, Euclidean distance will mostly reflect the first feature unless scaling is applied. This can make clusters appear to exist only because one measurement dominates the geometry.

### 3.2 Feature Design Changes the Meaning of Similarity

Similarity in raw pixel space, bag-of-words space, and learned embedding space can produce very different clusters for the same objects. Unsupervised results are therefore inseparable from the representation used to produce them.

### 3.3 Internal Objectives Are Not Universal Truth

For example, minimizing within-cluster squared distance is useful when compact spherical groups are plausible. It is a poor objective for elongated, nested, or density-based patterns. A model can succeed at its optimization target and still fail at the real interpretive task.

## 4. Worked Example: One Iteration of k-Means

Suppose four customers are represented by two features:

- `monthly_orders`
- `average_order_value`

Data points:

```text
x_1 = (1, 2)
x_2 = (2, 1)
x_3 = (8, 9)
x_4 = (9, 8)
```

We choose `k = 2` clusters and initialize centroids as:

```text
c_1 = (1, 2)
c_2 = (8, 9)
```

### 4.1 Assign Each Point to Its Nearest Centroid

Using Euclidean distance:

- For `x_1 = (1, 2)`:
  - distance to `c_1` = `0`
  - distance to `c_2` = sqrt((1 - 8)^2 + (2 - 9)^2) = sqrt(49 + 49) = sqrt(98)
  - assign `x_1` to cluster `1`

- For `x_2 = (2, 1)`:
  - distance to `c_1` = sqrt((2 - 1)^2 + (1 - 2)^2) = sqrt(1 + 1) = sqrt(2)
  - distance to `c_2` = sqrt((2 - 8)^2 + (1 - 9)^2) = sqrt(36 + 64) = sqrt(100) = 10
  - assign `x_2` to cluster `1`

- For `x_3 = (8, 9)`:
  - distance to `c_1` = sqrt(98)
  - distance to `c_2` = `0`
  - assign `x_3` to cluster `2`

- For `x_4 = (9, 8)`:
  - distance to `c_1` = sqrt((9 - 1)^2 + (8 - 2)^2) = sqrt(64 + 36) = sqrt(100) = 10
  - distance to `c_2` = sqrt((9 - 8)^2 + (8 - 9)^2) = sqrt(1 + 1) = sqrt(2)
  - assign `x_4` to cluster `2`

### 4.2 Recompute the Centroids

Cluster `1` contains `x_1` and `x_2`, so:

```text
new_c_1 = ((1 + 2) / 2, (2 + 1) / 2) = (1.5, 1.5)
```

Cluster `2` contains `x_3` and `x_4`, so:

```text
new_c_2 = ((8 + 9) / 2, (9 + 8) / 2) = (8.5, 8.5)
```

### 4.3 Interpret the Result

The first update identifies two compact groups: low-order customers and high-order customers. This is a useful segmentation only if these two features and Euclidean distance capture the business notion of similarity.

Verification: after one assignment step, `x_1` and `x_2` are closest to the first centroid and `x_3` and `x_4` are closest to the second, so the updated centroids `(1.5, 1.5)` and `(8.5, 8.5)` are consistent with the cluster memberships.

## 5. Practical Evaluation of Unsupervised Results

### 5.1 Internal Diagnostics

Internal diagnostics such as inertia or silhouette score summarize cluster compactness or separation, but they only evaluate the chosen geometry and objective.

### 5.2 Stability Checks

If small changes in preprocessing, initialization, or random seeds produce very different outputs, the discovered structure may not be robust enough to trust.

### 5.3 Domain and Downstream Validation

The strongest evaluation often asks whether the result helps a real task:

- does a clustering support a useful intervention,
- does a representation improve a downstream predictor,
- does anomaly scoring surface genuinely interesting cases?

## 6. Common Mistakes

1. **Cluster realism assumption.** Treating every cluster output as a real natural category confuses an algorithmic partition with a validated phenomenon; confirm that the grouping is meaningful in the application domain.
2. **Scale blindness.** Running distance-based methods on unscaled features lets large-range variables dominate similarity; standardize or otherwise normalize when the method assumes comparable feature scales.
3. **Objective overinterpretation.** Believing that a low clustering objective automatically means useful segmentation ignores mismatch between the optimization target and the real task; inspect whether the objective is appropriate.
4. **Label-style evaluation.** Expecting unsupervised methods to have one obviously correct answer leads to false confidence or false disappointment; evaluate stability, interpretation, and downstream utility instead.
5. **Representation neglect.** Applying clustering on a poor feature space and blaming the algorithm misses a major design decision; revisit the data representation before discarding the method.

## 7. Practical Checklist

- [ ] Define whether the goal is clustering, density estimation, or representation learning before choosing a method.
- [ ] Inspect feature scales and similarity assumptions before using any distance-based algorithm.
- [ ] Compare outputs under multiple seeds or initializations when the method is non-deterministic.
- [ ] Use internal diagnostics as supporting evidence rather than as the sole proof of quality.
- [ ] Validate discovered structure with domain interpretation or downstream task performance.
- [ ] Record preprocessing, distance choice, and hyperparameters so the analysis can be reproduced.

## 8. References

- Hastie, Trevor, Robert Tibshirani, and Jerome Friedman. 2009. *The Elements of Statistical Learning* (2nd ed.). Springer. <https://hastie.su.domains/ElemStatLearn/>
- Murphy, Kevin P. 2022. *Probabilistic Machine Learning: An Introduction*. MIT Press.
- Bishop, Christopher M. 2006. *Pattern Recognition and Machine Learning*. Springer.
- James, Gareth, et al. 2021. *An Introduction to Statistical Learning* (2nd ed.). Springer. <https://www.statlearning.com/>
- Tan, Pang-Ning, Michael Steinbach, Anuj Karpatne, and Vipin Kumar. 2018. *Introduction to Data Mining* (2nd ed.). Pearson.
- scikit-learn. 2025. *Clustering*. <https://scikit-learn.org/stable/modules/clustering.html>
- scikit-learn. 2025. *Unsupervised dimensionality reduction*. <https://scikit-learn.org/stable/modules/unsupervised_reduction.html>
