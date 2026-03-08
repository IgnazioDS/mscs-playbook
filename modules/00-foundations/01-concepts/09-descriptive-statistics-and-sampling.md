# Descriptive Statistics and Sampling

## Key Ideas

- Descriptive statistics summarize a dataset through measures of center, spread, and shape, but the right summary depends on the data distribution.
- Sampling lets us estimate population quantities from a subset of observations, but every estimate includes sampling error.
- The mean is sensitive to outliers, whereas the median and interquartile range are more robust for skewed or heavy-tailed data.
- Standard deviation measures dispersion around the mean, while the standard error measures uncertainty in an estimate such as a sample mean.
- Confidence intervals quantify plausible ranges for population parameters under stated assumptions; they do not eliminate bias from bad sampling.

## 1. What It Is

Descriptive statistics provide a compact way to summarize observed data. They answer questions such as:

- Where is the data centered?
- How variable is it?
- Is the distribution symmetric, skewed, or heavy-tailed?
- How much uncertainty should we expect when a summary comes from a sample rather than a full population?

Sampling extends this toolkit from description to estimation. When we cannot measure an entire population, we measure a sample and use sample statistics to estimate population quantities such as the mean, proportion, or variance.

### 1.1 Core Definitions

- A **population** is the full set of units or observations of interest.
- A **sample** is a subset drawn from the population.
- A **parameter** is a numerical quantity describing the population, such as a population mean `mu`.
- A **statistic** is a numerical quantity computed from the sample, such as a sample mean `x_bar`.
- **Sampling error** is the difference between a sample statistic and the true population parameter caused by random sampling variation.
- **Bias** is systematic error introduced by flawed measurement, nonrepresentative sampling, or data collection problems.

### 1.2 Why This Matters

Most analytical pipelines begin with summary tables, dashboards, and quick checks. If these summaries are wrong or misleading, everything that follows is at risk.

For example, a model trained on a biased sample may look accurate on paper but fail in deployment. A business report that presents only the mean revenue can misrepresent “typical” customer value if the distribution is highly skewed. Sound descriptive statistics help detect these issues early.

## 2. Measures of Center, Spread, and Shape

### 2.1 Measures of Center

The most common measures of central tendency are:

- **Mean**: the arithmetic average.
- **Median**: the middle value after sorting.
- **Mode**: the most frequent value.

For a sample `x_1, x_2, ..., x_n`, the sample mean is:

```text
x_bar = (1/n) * sum_{i=1 to n} x_i
```

The mean uses every value, which makes it efficient for symmetric distributions without large outliers. The median is more robust because extreme values affect it less.

### 2.2 Measures of Spread

Spread describes how dispersed the data is.

Common measures include:

- **Range**: `max - min`
- **Variance**: average squared deviation from the mean
- **Standard deviation**: square root of the variance
- **Interquartile range (IQR)**: `Q3 - Q1`

For a sample, the variance is:

```text
s^2 = (1 / (n - 1)) * sum_{i=1 to n} (x_i - x_bar)^2
```

and the sample standard deviation is:

```text
s = sqrt(s^2)
```

The IQR is often preferable when the distribution is skewed or contains outliers.

### 2.3 Measures of Shape

Shape describes the geometry of the distribution.

- **Symmetric** distributions have similar left and right tails.
- **Right-skewed** distributions have a long tail to the right.
- **Left-skewed** distributions have a long tail to the left.
- **Heavy-tailed** distributions produce more extreme values than a light-tailed reference distribution such as the normal distribution.

Shape matters because it affects which summaries are stable and interpretable. In skewed data, the mean and median can differ substantially.

## 3. Sampling and Estimation

### 3.1 Sample Statistics vs Population Parameters

A population parameter is fixed but usually unknown. A sample statistic is observable but varies from sample to sample.

This distinction is essential. The sample mean is not “the truth”; it is one estimate of the population mean.

### 3.2 Standard Error

The **standard deviation** measures variability among individual observations. The **standard error** measures uncertainty in an estimator.

For the sample mean, the standard error is:

```text
SE(x_bar) = s / sqrt(n)
```

This formula shows an important tradeoff: increasing the sample size reduces estimator uncertainty, but only at the rate `1 / sqrt(n)`. Doubling the sample size does not halve the standard error.

### 3.3 Confidence Intervals

A confidence interval gives a range of plausible values for a population parameter under a statistical model.

A common large-sample interval for the population mean is:

```text
x_bar +- z * SE(x_bar)
```

where `z` is a critical value such as `1.96` for an approximate 95% confidence interval under standard normal assumptions.

A confidence interval is not a guarantee that the parameter lies in the reported range. It is a procedure that, under repeated sampling and the stated assumptions, captures the true parameter at the advertised long-run rate.

## 4. Worked Example

Suppose a sample of monthly customer revenue is:

```text
[12, 15, 18, 20, 22, 25, 30, 120]
```

This dataset has one large outlier.

### 4.1 Compute the Mean

```text
Sum = 12 + 15 + 18 + 20 + 22 + 25 + 30 + 120 = 262
n = 8
x_bar = 262 / 8 = 32.75
```

### 4.2 Compute the Median

The sorted data already appears in order:

```text
[12, 15, 18, 20, 22, 25, 30, 120]
```

With `n = 8`, the median is the average of the 4th and 5th values:

```text
Median = (20 + 22) / 2 = 21
```

### 4.3 Interpret the Difference

- Mean = `32.75`
- Median = `21`

The outlier `120` pulls the mean upward. The median better reflects the typical customer in this sample.

### 4.4 Approximate Standard Error of the Mean

Using the sample standard deviation `s` computed from the data, suppose we obtain approximately:

```text
s ≈ 35.37
```

Then the standard error of the mean is:

```text
SE(x_bar) = 35.37 / sqrt(8) ≈ 12.51
```

A rough 95% confidence interval for the population mean using `z = 1.96` is:

```text
32.75 +- 1.96 * 12.51
32.75 +- 24.52
```

So the interval is approximately:

```text
[8.23, 57.27]
```

This interval is wide because the sample is small and highly variable.

Verification: the worked example is internally consistent because the sample sum is `262`, the mean is `262 / 8 = 32.75`, the median is `21`, and the reported confidence interval is centered at the sample mean with half-width `1.96 * 12.51 ≈ 24.52`.

## 5. Practical Interpretation Guidelines

### 5.1 When to Prefer the Mean

Use the mean when:

- the distribution is roughly symmetric,
- outliers are rare or substantively meaningful,
- and downstream methods rely on arithmetic averaging.

### 5.2 When to Prefer the Median and IQR

Use the median and IQR when:

- the data is skewed,
- outliers are present,
- or the goal is to report a stable “typical” value.

### 5.3 When Uncertainty Must Be Reported

Report uncertainty when:

- summaries are estimated from samples,
- sample size is limited,
- decisions depend on small differences,
- or readers may mistake an estimate for an exact population value.

## 6. Common Mistakes

1. **Reporting only the mean.** A mean without spread or uncertainty can hide skewness, outliers, and instability; pair it with standard deviation, IQR, or a confidence interval when appropriate.
2. **Confusing standard deviation with standard error.** Standard deviation describes the data, while standard error describes estimator uncertainty; using one in place of the other misstates variability.
3. **Mixing heterogeneous groups.** Combining distinct populations such as new and returning users can produce misleading summaries that describe neither group well.
4. **Ignoring sampling bias.** A large sample does not fix a biased collection process; confidence intervals address sampling variability, not bad sampling design.
5. **Treating confidence intervals as guarantees.** A 95% confidence interval is not a 95% probability statement about a fixed parameter after observing the data.

## 7. Practical Checklist

- [ ] Define the population and sampling unit before computing summary statistics.
- [ ] Report at least one measure of center and one measure of spread.
- [ ] Check for skewness, outliers, or subgroup mixing before choosing between mean and median.
- [ ] Distinguish standard deviation from standard error in both notation and prose.
- [ ] State the sample size whenever reporting sample-based estimates.
- [ ] Include confidence intervals when inference or decision-making depends on estimated quantities.
- [ ] Document known sources of sampling bias or measurement bias.

## 8. References

- Freedman, David, Robert Pisani, and Roger Purves. 2007. *Statistics* (4th ed.). W. W. Norton.
- Illowsky, Barbara, and Susan Dean. 2023. *Introductory Statistics*. OpenStax. <https://openstax.org/details/books/introductory-statistics>
- OpenIntro. 2024. *OpenIntro Statistics* (4th ed.). OpenIntro. <https://www.openintro.org/book/os/>
- NIST/SEMATECH. 2012. *e-Handbook of Statistical Methods*. National Institute of Standards and Technology. <https://www.itl.nist.gov/div898/handbook/>
- Rice University. 2023. *Introductory Statistics*. LibreTexts. <https://stats.libretexts.org/Bookshelves/Introductory_Statistics>
- Wasserstein, Ronald L., and Nicole A. Lazar. 2016. The ASA's Statement on p-Values: Context, Process, and Purpose. *The American Statistician* 70(2): 129–133. <https://doi.org/10.1080/00031305.2016.1154108>
- Wickham, Hadley, and Garrett Grolemund. 2017. *R for Data Science*. O'Reilly Media. <https://r4ds.hadley.nz/>
