# Feature Engineering and Encoding

## Key Ideas

- Feature engineering transforms raw fields into representations that make meaningful structure easier for mining algorithms to detect.
- Encoding and scaling are not cosmetic preprocessing steps; they define the geometry of the problem for distance-based methods and the sparsity pattern for frequency-based methods.
- The same raw variable can support very different mining behaviors depending on whether it is bucketed, normalized, one-hot encoded, aggregated, or dropped.
- Good feature engineering preserves semantics while making the representation computationally stable and operationally reproducible.
- Encoding choices should be driven by data distribution, task objective, and downstream interpretability rather than by default library pipelines alone.

## 1. What Feature Engineering Does

Feature engineering converts raw columns into a representation more suitable for mining, clustering, anomaly scoring, or downstream modeling.

### 1.1 Core Definitions

- A **feature** is a derived or original variable used by the algorithm.
- **Encoding** is the transformation of nonnumeric values into machine-usable form.
- **One-hot encoding** creates a binary indicator for each category level.
- **Scaling** transforms feature magnitudes so they are comparable or better conditioned.
- **Sparsity** means most entries in the feature matrix are zero.

### 1.2 Why This Matters

Many mining methods operate on similarity, distance, frequency, or count structure. Feature design controls all of those. A poor representation can create artificial clusters, inflate item frequencies, or hide anomalies.

## 2. Common Feature Construction Choices

### 2.1 Numeric Features

Numeric variables may need scaling, clipping, log transforms, or bucketing depending on skew and downstream sensitivity.

### 2.2 Categorical Features

Categorical variables may be handled with one-hot encoding, ordinal encoding, frequency encoding, or grouping rare levels into broader categories.

### 2.3 Aggregated and Domain Features

Raw event logs are often converted into summary features such as counts per user, average basket value, or time-since-last-activity.

## 3. Why Encoding Changes the Mining Result

### 3.1 Distance Sensitivity

In clustering, one unscaled variable can dominate the geometry. In sparse binary spaces, similarity may look very different from Euclidean intuition.

### 3.2 High-Cardinality Risk

Very large categorical vocabularies can create sparse explosions that add cost and reduce interpretability.

### 3.3 Leakage and Semantic Drift

Feature construction must not sneak in target information or unstable future-dependent values. Even in exploratory mining, implicit leakage can distort the structure being reported.

## 4. Worked Example: One-Hot Encoding a Small Category Field

Suppose a transaction dataset has a `payment_type` field with values:

```text
row_1 = card
row_2 = cash
row_3 = card
row_4 = wallet
```

Distinct categories:

```text
card, cash, wallet
```

### 4.1 Define the Encoded Columns

Create three binary features:

```text
payment_card
payment_cash
payment_wallet
```

### 4.2 Encode Each Row

```text
row_1 -> (1, 0, 0)
row_2 -> (0, 1, 0)
row_3 -> (1, 0, 0)
row_4 -> (0, 0, 1)
```

### 4.3 Interpret the Result

The encoding preserves category membership without imposing a false numeric order. If the team had encoded `card = 1`, `cash = 2`, and `wallet = 3`, distance-based methods might wrongly treat `cash` as lying between `card` and `wallet`.

Verification: the one-hot representation is internally consistent because each row has exactly one active category indicator corresponding to its original `payment_type` value.

## 5. Common Mistakes

1. **Ordinal illusion.** Encoding nominal categories as integers for convenience can create fake ordering relationships; use encodings that match the variable semantics.
2. **Scale inconsistency.** Mixing scaled and unscaled numeric features distorts distance-based mining; standardize when magnitude comparability matters.
3. **Cardinality explosion.** One-hot encoding extremely high-cardinality fields without reduction can produce sparse, unstable representations; group, hash, or drop when justified.
4. **Feature leakage.** Creating features from future information or from post-outcome fields contaminates the mining result; audit feature provenance carefully.
5. **Representation amnesia.** Forgetting that the representation defines what the algorithm can see leads to misplaced blame on the model; revisit the feature space before changing algorithms.

## 6. Practical Checklist

- [ ] Separate numeric, categorical, ordinal, and identifier-like fields before encoding.
- [ ] Use encoding schemes that match the semantics of each feature.
- [ ] Scale numeric features when the mining method depends on distances or magnitudes.
- [ ] Review high-cardinality fields for sparsity and interpretability cost.
- [ ] Log the exact feature-generation pipeline so later runs are comparable.
- [ ] Reassess the representation when mined patterns look unstable or uninterpretable.

## 7. References

- Zheng, Alice, and Amanda Casari. 2018. *Feature Engineering for Machine Learning*. O'Reilly Media.
- Tan, Pang-Ning, Michael Steinbach, Anuj Karpatne, and Vipin Kumar. 2018. *Introduction to Data Mining* (2nd ed.). Pearson.
- Han, Jiawei, Micheline Kamber, and Jian Pei. 2011. *Data Mining: Concepts and Techniques* (3rd ed.). Morgan Kaufmann.
- scikit-learn. 2026. *OneHotEncoder*. <https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html>
- scikit-learn. 2026. *StandardScaler*. <https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html>
- pandas. 2026. *get_dummies*. <https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html>
- Kuhn, Max, and Kjell Johnson. 2019. *Feature Engineering and Selection*. CRC Press.
