# Statistical Inference Basics

## Key Ideas

- Statistical inference uses sample data to reason about unknown population parameters, so every conclusion depends on both a model and a sampling process.
- An estimator, its standard error, and its sampling distribution serve different roles, and confusing them leads to incorrect confidence intervals and tests.
- Confidence intervals quantify a procedure's long-run coverage under stated assumptions; they do not assign a posterior probability to a fixed parameter.
- Hypothesis tests compare observed data against a null model, and a p-value measures incompatibility with that model rather than the probability that the null hypothesis is true.
- Statistical significance, effect size, and practical significance are different questions, so sound decisions require checking all three rather than stopping at a threshold.

## 1. What It Is

Statistical inference is the part of statistics that moves from observed data to claims about a broader population or process. Descriptive statistics summarize what was observed. Inference asks what the sample says about quantities we did not observe directly, such as a population mean, a conversion rate, or the difference between two systems.

### 1.1 Core Definitions

- A **parameter** is a fixed but usually unknown property of the population, such as a population mean `mu` or proportion `p`.
- An **estimator** is a rule for computing a quantity from sample data, such as the sample mean `x_bar`.
- An **estimate** is the numerical value produced by the estimator on one dataset.
- A **sampling distribution** is the distribution of an estimator over repeated samples from the same process.
- The **standard error** is the standard deviation of an estimator's sampling distribution or its sample-based approximation.
- A **confidence interval** is an interval-valued procedure designed to cover the true parameter at a stated long-run rate, such as 95%.
- A **hypothesis test** compares observed data to a null hypothesis `H_0` using a test statistic and a reference distribution.

### 1.2 Why This Matters

Inference appears whenever a team decides whether an experiment worked, whether a model improved a metric, whether a sensor is drifting, or whether a production change altered latency. Without inference, small random fluctuations can be mistaken for real effects. With weak inference, noisy evidence can be overstated as certainty.

## 2. Estimators, Bias, and Standard Error

### 2.1 Point Estimation

A point estimate gives one best-guess number for a parameter. For a population proportion `p`, a common estimator is:

```text
p_hat = x / n
```

where `x` is the number of successes in `n` trials.

Point estimates are useful, but they hide uncertainty. Two samples can give the same `p_hat` with very different reliability if one sample has size `20` and the other has size `20,000`.

### 2.2 Bias and Consistency

An estimator is **biased** if its expected value differs from the parameter it targets. Bias concerns systematic deviation under repeated sampling, not one unlucky dataset.

An estimator is **consistent** if it converges to the true parameter as sample size grows. A consistent estimator can still be noisy in small samples, so consistency does not remove the need for uncertainty quantification.

### 2.3 Standard Error

The standard error measures how much an estimator would vary across repeated samples. For a sample proportion, an approximate standard error is:

```text
SE(p_hat) = sqrt(p_hat (1 - p_hat) / n)
```

This formula shows why sample size matters. If `n` increases by a factor of `4`, the standard error is roughly cut in half.

## 3. Confidence Intervals

### 3.1 Purpose

A confidence interval reports a range of plausible parameter values under a statistical model. It is meant to communicate both the estimate and the uncertainty around it.

For a large-sample proportion, an approximate 95% confidence interval is:

```text
p_hat +- 1.96 * SE(p_hat)
```

This is often called a Wald-style interval. It is easy to compute, but it can be inaccurate for small samples or proportions near `0` or `1`.

### 3.2 Interpretation

The correct frequentist interpretation is procedural: if we repeated the data-collection-and-interval-building process many times, about 95% of those intervals would contain the true parameter, assuming the model assumptions hold.

The interval does not say there is a 95% probability that the fixed parameter lies inside this specific realized interval.

## 4. Hypothesis Tests and p-Values

### 4.1 Setup

A hypothesis test starts with:

- a **null hypothesis** `H_0`, usually representing no effect or a baseline value,
- an **alternative hypothesis** `H_1`, representing the effect or deviation of interest,
- and a **test statistic** that should behave predictably if `H_0` is true.

For a proportion test against `H_0: p = p_0`, a common large-sample statistic is:

```text
z = (p_hat - p_0) / sqrt(p_0 (1 - p_0) / n)
```

### 4.2 p-Value and Error Types

A **p-value** is the probability, assuming the null model is true, of obtaining a test statistic at least as extreme as the one observed.

Two standard error concepts matter in testing:

- A **Type I error** rejects a true null hypothesis.
- A **Type II error** fails to reject a false null hypothesis.

Reducing one error type often affects the other, so testing is about tradeoffs rather than perfect certainty.

## 5. Worked Example

Suppose a product team wants to know whether a signup flow exceeds a historical baseline conversion rate of `15%`.

They observe:

```text
n = 200 visitors
x = 50 conversions
```

So the sample proportion is:

```text
p_hat = 50 / 200 = 0.25
```

### 5.1 Approximate Standard Error for the Estimate

Using the sample-based approximation:

```text
SE(p_hat) = sqrt(0.25 * 0.75 / 200)
          = sqrt(0.1875 / 200)
          = sqrt(0.0009375)
          ≈ 0.0306
```

### 5.2 Build a 95% Confidence Interval

Use `1.96` as the large-sample critical value:

```text
margin = 1.96 * 0.0306 ≈ 0.0600
```

Therefore:

```text
95% CI ≈ 0.25 +- 0.0600 = [0.1900, 0.3100]
```

This interval suggests the population conversion rate is plausibly between `19.0%` and `31.0%` under the model assumptions.

### 5.3 Test the Baseline Hypothesis

Set:

```text
H_0: p = 0.15
H_1: p > 0.15
```

Under the null hypothesis, use the null-based standard error:

```text
SE_0 = sqrt(0.15 * 0.85 / 200)
     = sqrt(0.1275 / 200)
     = sqrt(0.0006375)
     ≈ 0.0252
```

Now compute the z-statistic:

```text
z = (0.25 - 0.15) / 0.0252
  = 0.10 / 0.0252
  ≈ 3.97
```

A one-sided standard normal tail above `3.97` is very small:

```text
p_value < 0.001
```

So the data is strongly inconsistent with the baseline `15%` conversion model.

Verification: `p_hat = 0.25`, the 95% interval `[0.1900, 0.3100]` lies entirely above `0.15`, and the one-sided z-test gives `z ≈ 3.97` with `p_value < 0.001`, so the interval and the test support the same practical conclusion.

## 6. Pseudocode Pattern

```text
procedure one_sample_proportion_test(successes, trials, null_rate):
    p_hat = successes / trials
    se_est = sqrt(p_hat * (1 - p_hat) / trials)
    ci_low = p_hat - 1.96 * se_est
    ci_high = p_hat + 1.96 * se_est

    se_null = sqrt(null_rate * (1 - null_rate) / trials)
    z_stat = (p_hat - null_rate) / se_null

    return p_hat, ci_low, ci_high, z_stat
```

Time: `Theta(1)` worst case. Space: `Theta(1)` auxiliary space.

## 7. Common Mistakes

1. **Point-estimate certainty.** Treating `p_hat` or `x_bar` as the parameter ignores sampling variability; always report uncertainty alongside the estimate.
2. **Confidence-interval probability language.** Saying a 95% confidence interval gives a 95% probability that the parameter is inside misstates the frequentist interpretation; describe the long-run coverage procedure instead.
3. **p-value inversion.** Reading a p-value as the probability that the null hypothesis is true is incorrect; it is computed under the assumption that the null hypothesis is true.
4. **Significance-only thinking.** Declaring success from a small p-value without checking effect size, interval width, or business relevance can produce technically significant but practically weak conclusions.
5. **Assumption blindness.** Independence failures, biased sampling, multiple testing, or poor measurement can invalidate an otherwise correct formula; check data-collection assumptions before trusting the output.

## 8. Practical Checklist

- [ ] State the population parameter and the estimator separately.
- [ ] Report the sample size before presenting a confidence interval or hypothesis test.
- [ ] Check whether the sampling design and independence assumptions are plausible.
- [ ] Distinguish the estimate's standard error from the data's standard deviation.
- [ ] Write the null and alternative hypotheses explicitly before computing a p-value.
- [ ] Interpret statistical significance together with effect size and interval width.
- [ ] Flag small-sample settings where large-sample approximations may be unreliable.

## 9. References

- Casella, George, and Roger L. Berger. 2002. *Statistical Inference* (2nd ed.). Duxbury.
- Wasserman, Larry. 2004. *All of Statistics*. Springer. <https://link.springer.com/book/10.1007/978-0-387-21736-9>
- OpenIntro. 2024. *OpenIntro Statistics* (4th ed.). OpenIntro. <https://www.openintro.org/book/os/>
- NIST/SEMATECH. 2012. *e-Handbook of Statistical Methods*. National Institute of Standards and Technology. <https://www.itl.nist.gov/div898/handbook/>
- Illowsky, Barbara, and Susan Dean. 2023. *Introductory Statistics*. OpenStax. <https://openstax.org/details/books/introductory-statistics>
- Rice University. 2023. *Introductory Statistics*. LibreTexts. <https://stats.libretexts.org/Bookshelves/Introductory_Statistics>
- Wasserstein, Ronald L., and Nicole A. Lazar. 2016. The ASA's Statement on p-Values: Context, Process, and Purpose. *The American Statistician* 70(2): 129-133. <https://doi.org/10.1080/00031305.2016.1154108>
