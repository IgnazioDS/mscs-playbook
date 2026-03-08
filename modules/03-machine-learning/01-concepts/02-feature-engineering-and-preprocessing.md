# Feature Engineering and Preprocessing

## Key Ideas

- Feature engineering turns raw observations into model-ready variables, so it directly controls what structure a learning algorithm can and cannot use.
- Preprocessing steps such as scaling, encoding, imputation, and transformation must be fit on training data only, or the pipeline leaks information and inflates evaluation metrics.
- A representation is not neutral: the same raw data can produce very different model behavior depending on how missing values, categories, nonlinearities, and outliers are encoded.
- Good preprocessing reduces avoidable variance and optimization instability, but aggressive or poorly justified transformations can erase signal or break interpretability.
- A sound machine-learning workflow treats preprocessing as part of the model pipeline rather than as an informal cleanup step performed outside validation.

## 1. What It Is

Feature engineering is the process of constructing or selecting input variables that make a prediction problem easier to learn. Preprocessing is the set of transformations that convert raw features into a form suitable for modeling, such as normalized numeric inputs, encoded categories, or imputed missing values.

### 1.1 Core Definitions

- A **feature** is a measurable input variable used by a model.
- A **representation** is the full way the raw data is encoded for learning.
- **Imputation** replaces missing values with estimated or reserved values.
- **Scaling** changes the numerical range of features, often by standardization or normalization.
- **Encoding** converts non-numeric variables such as categories or text tokens into numeric forms.
- A **pipeline** is an ordered sequence of transformations and model steps treated as one training and inference unit.

### 1.2 Why This Matters

Many model failures are not caused by choosing the wrong algorithm. They are caused by feeding the algorithm a poor representation of the problem. Linear models behave differently if one feature is unscaled and dominates the objective. Tree models react differently to missing-value handling than distance-based methods do. Leakage often enters the system through preprocessing rather than through the estimator itself.

## 2. Main Preprocessing Decisions

### 2.1 Numeric Features

Numeric features may need:

- missing-value imputation,
- scaling,
- clipping or winsorization for outliers,
- or transformations such as `log(x)` for strongly skewed values.

These decisions depend on the model family. Gradient-based and distance-based models are often sensitive to scale. Tree-based methods are usually less sensitive to monotonic rescaling, but they still depend on meaningful missing-value handling and feature definitions.

### 2.2 Categorical Features

Categorical variables can be encoded in several ways:

- **one-hot encoding** for low-cardinality nominal categories,
- **ordinal encoding** only when order is semantically meaningful,
- **frequency or target-aware schemes** when cardinality is high and leakage is controlled carefully.

The encoding choice changes model capacity and risk of spurious structure.

### 2.3 Derived Features

Derived features can capture structure the raw variables hide, such as:

- ratios,
- interaction terms,
- bucketed time features,
- rolling aggregates,
- or domain-specific indicators.

Derived features can improve simple models substantially, but they should still be justified by mechanism or repeated empirical benefit rather than by random experimentation alone.

## 3. Pipelines and Leakage Control

Preprocessing must be part of the train/validation procedure, not a step performed once on the full dataset before splitting.

If scaling, imputation, or dimensionality reduction is fit on all data first, the training process has already seen information from the validation or test distribution. The model may appear more accurate than it really is.

The safe rule is:

1. split the data,
2. fit preprocessing on training data only,
3. apply the learned transformation to validation or test data,
4. evaluate the full pipeline.

## 4. Worked Example

Suppose a training set has one numeric feature `income_k` measured in thousands of dollars:

```text
[40, 50, 60, 100]
```

and one validation example:

```text
[80]
```

Assume we want to standardize the feature using:

```text
z = (x - mean) / std
```

using population standard deviation for this worked example.

### 4.1 Correct Training-Only Standardization

Compute the training mean:

```text
mean_train = (40 + 50 + 60 + 100) / 4 = 62.5
```

Compute squared deviations:

```text
(40 - 62.5)^2 = 506.25
(50 - 62.5)^2 = 156.25
(60 - 62.5)^2 = 6.25
(100 - 62.5)^2 = 1406.25
```

Sum:

```text
506.25 + 156.25 + 6.25 + 1406.25 = 2075
```

Population variance:

```text
var_train = 2075 / 4 = 518.75
```

Standard deviation:

```text
std_train = sqrt(518.75) ≈ 22.78
```

Now transform the validation example `80`:

```text
z_valid = (80 - 62.5) / 22.78 ≈ 0.77
```

### 4.2 Incorrect Leakage-Prone Standardization

If we wrongly compute the mean using both training and validation values:

```text
mean_all = (40 + 50 + 60 + 100 + 80) / 5 = 66
```

The validation point has now influenced the transformation applied back to itself and to the training set. That is information leakage.

### 4.3 Why the Difference Matters

The leaked pipeline changes the representation seen during evaluation. Even if the numeric difference seems small here, the principle scales to PCA, target encoding, imputation, and learned embeddings, where the damage can be much larger.

Verification: the correct training-only standardization gives `mean_train = 62.5`, `std_train ≈ 22.78`, and `z_valid ≈ 0.77`, while the leaked transformation changes the statistics by incorporating the validation point.

## 5. Pseudocode Pattern

```text
procedure fit_transform_pipeline(train_rows, validation_rows):
    transformer = fit_preprocessor(train_rows)
    train_features = transform(transformer, train_rows)
    validation_features = transform(transformer, validation_rows)
    return train_features, validation_features
```

Time: `O(n d)` worst case for fitting simple column-wise preprocessing on `n` rows and `d` features, excluding any downstream estimator training. Space: `O(n d)` worst case if transformed matrices are materialized explicitly.

## 6. Common Mistakes

1. **Split-after-preprocessing.** Fitting scalers, imputers, or reducers on the full dataset before splitting leaks future information; fit transformations on training data only.
2. **Ordinal-encoding fiction.** Assigning integer order to nominal categories such as colors or cities can create false distance structure; use an encoding that matches the semantics.
3. **One-size-fits-all scaling.** Assuming every model needs the same scaling pipeline ignores model-family differences; choose preprocessing based on the estimator and feature behavior.
4. **Derived-feature sprawl.** Adding many weak interaction terms without validation increases variance and maintenance cost; keep engineered features tied to mechanism or repeated benefit.
5. **Inference-pipeline mismatch.** Training with one preprocessing path and serving with another breaks reproducibility; version and deploy the full pipeline, not just the model weights.

## 7. Practical Checklist

- [ ] Identify numeric, categorical, missing, and high-cardinality features before choosing transformations.
- [ ] Fit every preprocessing step on training data only.
- [ ] Keep preprocessing and model fitting inside one explicit pipeline.
- [ ] Check whether the estimator is sensitive to scale, sparsity, or missing-value representation.
- [ ] Validate engineered features against both offline metrics and interpretability constraints.
- [ ] Ensure the same preprocessing logic is available at inference time.

## 8. References

- Kuhn, Max, and Kjell Johnson. 2019. *Feature Engineering and Selection*. Chapman and Hall/CRC.
- Géron, Aurélien. 2022. *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media.
- Murphy, Kevin P. 2022. *Probabilistic Machine Learning: An Introduction*. MIT Press.
- Bishop, Christopher M. 2006. *Pattern Recognition and Machine Learning*. Springer.
- scikit-learn. 2025. *Preprocessing data*. <https://scikit-learn.org/stable/modules/preprocessing.html>
- scikit-learn. 2025. *Common pitfalls and recommended practices*. <https://scikit-learn.org/stable/common_pitfalls.html>
- Molnar, Christoph. 2024. *Interpretable Machine Learning* (2nd ed.).
