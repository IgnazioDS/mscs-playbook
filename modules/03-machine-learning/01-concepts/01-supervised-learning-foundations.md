# Supervised Learning Foundations

## Key Ideas

- Supervised learning uses labeled examples to learn a mapping from inputs to targets, so the quality of the labels and the data distribution matters as much as the model class.
- A model should be understood as a parameterized prediction rule, while the objective function defines what kinds of errors training will try hardest to reduce.
- Generalization is the central goal: a model that fits the training set well but fails on new data has not solved the problem in a useful way.
- Classification and regression are different supervised tasks, and they require different targets, losses, and evaluation choices.
- Baselines are part of the scientific method of machine learning because they tell you whether a more complex model is actually earning its complexity.

## 1. What It Is

Supervised learning is the study of how to learn from examples where each input is paired with a desired output. The learner receives a dataset of input-target pairs and tries to infer a rule that predicts the correct target for new inputs drawn from the same or a similar process.

### 1.1 Core Definitions

- An **input** or **feature vector** is the observed information used to make a prediction.
- A **target** or **label** is the output the model is supposed to predict.
- A **training set** is the collection of labeled examples used to fit the model.
- A **model** is a parameterized function that maps inputs to predictions.
- A **loss function** measures how wrong a prediction is relative to the target.
- **Generalization** is the ability of the learned model to perform well on unseen data.

### 1.2 Why This Matters

Many production machine-learning systems are supervised systems: fraud detection, demand forecasting, content moderation, medical triage, price estimation, and churn prediction all fit this pattern. The central engineering problem is not merely fitting the historical data. It is learning a rule that remains useful when the model encounters new cases.

## 2. Task Types and Learning Setup

### 2.1 Classification

In classification, the target is a category such as:

- spam or not spam,
- benign or malignant,
- churn or retain.

The model may output a class label directly or a score or probability that is later thresholded.

### 2.2 Regression

In regression, the target is numeric, such as:

- house price,
- sales volume,
- delivery time.

The model predicts a real value rather than a discrete class.

### 2.3 The Learning Pipeline

A supervised-learning workflow usually includes:

1. defining the prediction target,
2. choosing the input representation,
3. splitting data into training and evaluation sets,
4. fitting the model by minimizing an objective,
5. evaluating generalization,
6. iterating based on errors and constraints.

## 3. Empirical Risk and Generalization

### 3.1 Training Objective

Training usually minimizes an average loss over the training data:

```text
empirical_risk = (1 / n) * sum_i loss(y_hat_i, y_i)
```

This quantity is useful because it gives a concrete optimization target. It is not the same thing as future performance.

### 3.2 Why Training Error Is Not Enough

A model can memorize the training set or exploit quirks that do not repeat outside the sample. That is why evaluation on held-out data is necessary. Supervised learning should be treated as estimation under uncertainty, not as pure curve fitting.

### 3.3 Baselines

A baseline is a simple reference model, such as:

- majority-class prediction for classification,
- mean prediction for regression,
- or a linear model before trying a deep network.

Baselines protect against self-deception. If a complex model does not beat a simple baseline under the correct metric, the extra complexity is not justified yet.

## 4. Worked Example

Suppose a team wants to predict whether a user will churn in the next month.

Training data:

```text
user_1: sessions = 2, support_tickets = 3, churn = 1
user_2: sessions = 12, support_tickets = 0, churn = 0
user_3: sessions = 5, support_tickets = 1, churn = 0
user_4: sessions = 1, support_tickets = 4, churn = 1
```

Consider a very simple rule-based baseline:

```text
predict churn = 1 if sessions <= 2
predict churn = 0 otherwise
```

### 4.1 Apply the Baseline

- `user_1`: sessions `2`, predict `1`, true target `1`
- `user_2`: sessions `12`, predict `0`, true target `0`
- `user_3`: sessions `5`, predict `0`, true target `0`
- `user_4`: sessions `1`, predict `1`, true target `1`

### 4.2 Compute Accuracy

All four predictions are correct, so:

```text
accuracy = 4 / 4 = 1.0
```

### 4.3 Interpret the Result Carefully

This does not prove the rule is generally good. It only shows that on this tiny sample the feature `sessions` separates the labels perfectly. A real evaluation would require more data and a proper validation split.

Verification: the baseline predicts `[1, 0, 0, 1]`, which matches the true churn labels exactly on the four given examples, so the computed accuracy of `1.0` is internally consistent.

## 5. Pseudocode Pattern

```text
procedure evaluate_classifier(predictions, targets):
    correct = 0

    for i from 1 to length(targets):
        if predictions[i] == targets[i]:
            correct = correct + 1

    return correct / length(targets)
```

Time: Theta(n) worst case for `n` labeled examples. Space: Theta(1) auxiliary space.

## 6. Common Mistakes

1. **Curve-fitting mindset.** Treating supervised learning as merely matching historical examples ignores the real objective of generalization; always ask how the model will behave on unseen data.
2. **Task-type confusion.** Using classification assumptions for regression problems, or the reverse, leads to the wrong losses and metrics; define the target type before choosing methods.
3. **No-baseline development.** Comparing only complex models against each other hides whether any of them are meaningfully useful; establish a simple reference first.
4. **Label-trust assumption.** Assuming labels are always correct can turn annotation noise into model noise; inspect target quality before over-optimizing the algorithm.
5. **Objective-metric blur.** Training loss and business success are not automatically the same quantity; connect the optimization target to the evaluation target explicitly.

## 7. Practical Checklist

- [ ] Define whether the task is classification or regression before choosing the model family.
- [ ] Inspect the label distribution and obvious data-quality issues before training.
- [ ] Start from a simple baseline that is easy to explain and reproduce.
- [ ] Separate training and evaluation data before drawing any performance conclusion.
- [ ] Write down the loss function and the reporting metric as two distinct objects.
- [ ] Treat a strong training score as preliminary evidence, not as proof of generalization.

## 8. References

- James, Gareth, et al. 2021. *An Introduction to Statistical Learning* (2nd ed.). Springer. <https://www.statlearning.com/>
- Bishop, Christopher M. 2006. *Pattern Recognition and Machine Learning*. Springer.
- Murphy, Kevin P. 2022. *Probabilistic Machine Learning: An Introduction*. MIT Press.
- Hastie, Trevor, Robert Tibshirani, and Jerome Friedman. 2009. *The Elements of Statistical Learning* (2nd ed.). Springer. <https://hastie.su.domains/ElemStatLearn/>
- Géron, Aurelien. 2022. *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media.
- scikit-learn. 2025. *Supervised learning*. <https://scikit-learn.org/stable/supervised_learning.html>
- Russell, Stuart, and Peter Norvig. 2021. *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
