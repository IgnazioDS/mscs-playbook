# Probability and Distributions Basics

## Key Ideas

- Probability assigns numerical values to uncertain events, but those values must satisfy the probability axioms to remain coherent.
- Conditional probability updates beliefs using additional information, and Bayes’ rule makes that update explicit.
- Independence is a structural assumption, not a default; treating dependent events as independent produces systematically wrong calculations.
- Distributions such as Bernoulli, Binomial, Poisson, and Normal encode different data-generating mechanisms, so choosing the wrong one leads to incorrect modeling and inference.
- Expectation and variance summarize center and spread, but their interpretation depends on the random variable and the assumptions behind the distribution.

## 1. What It Is

Probability provides a mathematical language for reasoning about uncertainty. It formalizes statements such as “the service fails 1% of the time,” “the next request arrives within one second,” or “the A/B test conversion rate is likely higher for variant B.”

A **probability distribution** describes how probability is allocated across the possible values of a random variable. In practice, distributions are not just abstract objects. They encode assumptions about how data is generated, how often rare events occur, and how much variability to expect.

This page introduces the core ideas needed for later work:

- probability rules,
- conditional probability and Bayes’ rule,
- independence,
- common discrete and continuous distributions,
- and expectation and variance.

### 1.1 Core Definitions

- A **sample space** is the set of all possible outcomes of an experiment.
- An **event** is a subset of the sample space.
- A **probability measure** assigns each event a number in `[0, 1]` such that probability of the whole sample space is `1` and disjoint events add.
- A **random variable** is a function that maps outcomes to numerical values.
- A **probability mass function (pmf)** gives probabilities for discrete random variables.
- A **probability density function (pdf)** describes continuous distributions, where probabilities over intervals are obtained by integration.
- The **expectation** of a random variable is its long-run average value.
- The **variance** measures the average squared deviation from the expectation.

### 1.2 Why This Matters

Many engineering and data decisions are probabilistic even when they are presented as deterministic outputs. Reliability analysis depends on failure probabilities. Ranking and recommendation systems depend on uncertain outcomes. Statistical inference depends on sampling distributions. Machine learning models often optimize expected loss rather than exact future outcomes.

If the probability model is wrong, downstream reasoning is wrong. A Poisson assumption for bursty traffic, a Normal approximation for heavily skewed data, or an independence assumption for correlated failures can all lead to misleading conclusions.

## 2. Probability Rules

### 2.1 Probability Axioms

A valid probability model must satisfy three foundational rules:

1. `P(A) >= 0` for every event `A`.
2. `P(S) = 1`, where `S` is the sample space.
3. If `A` and `B` are disjoint, then `P(A union B) = P(A) + P(B)`.

These rules imply many common identities. For example:

```text
P(A^c) = 1 - P(A)
```

and

```text
P(A union B) = P(A) + P(B) - P(A intersection B)
```

### 2.2 Conditional Probability

Conditional probability answers the question: what is the probability of `A` given that `B` has already occurred?

```text
P(A | B) = P(A intersection B) / P(B)
```

provided `P(B) > 0`.

This formula is not just mechanical. It changes the reference universe from the full sample space to the event `B`.

### 2.3 Bayes’ Rule

Bayes’ rule rewrites conditional probability in a way that separates prior beliefs from evidence:

```text
P(A | B) = P(B | A) P(A) / P(B)
```

This is essential when reasoning from observed evidence back to an underlying cause, such as disease testing, spam filtering, or anomaly detection.

### 2.4 Independence

Two events `A` and `B` are independent if:

```text
P(A intersection B) = P(A) P(B)
```

Equivalently, if `P(B) > 0`, then independence implies:

```text
P(A | B) = P(A)
```

Independence is a strong modeling assumption. It must be justified by the process, not assumed because it simplifies the arithmetic.

## 3. Common Distributions

### 3.1 Bernoulli Distribution

A Bernoulli random variable models a single trial with two outcomes, usually coded as `1` for success and `0` for failure.

If `X ~ Bernoulli(p)`, then:

```text
P(X = 1) = p
P(X = 0) = 1 - p
E[X] = p
Var(X) = p(1 - p)
```

**Use it when:** you model one binary event, such as whether a request fails, a user clicks, or a packet is dropped.

### 3.2 Binomial Distribution

A Binomial random variable counts the number of successes in `n` independent Bernoulli trials with success probability `p`.

If `X ~ Binomial(n, p)`, then:

```text
P(X = k) = C(n, k) p^k (1 - p)^(n-k)
```

for `k = 0, 1, ..., n`.

Also:

```text
E[X] = np
Var(X) = np(1 - p)
```

**Use it when:** you count successes in a fixed number of repeated independent trials.

### 3.3 Poisson Distribution

A Poisson random variable models the count of events in a fixed interval when events occur independently at a constant average rate `lambda`.

If `X ~ Poisson(lambda)`, then:

```text
P(X = k) = e^(-lambda) lambda^k / k!
```

for `k = 0, 1, 2, ...`.

Also:

```text
E[X] = lambda
Var(X) = lambda
```

**Use it when:** modeling counts such as arrivals, failures, or rare events in time or space, provided the constant-rate and independence assumptions are reasonable.

### 3.4 Normal Distribution

A Normal random variable is continuous and described by mean `mu` and variance `sigma^2`.

If `X ~ Normal(mu, sigma^2)`, then its density is bell-shaped and symmetric around `mu`.

Also:

```text
E[X] = mu
Var(X) = sigma^2
```

**Use it when:** the quantity is approximately symmetric and influenced by many small additive effects, or when justified by theory such as the central limit theorem.

## 4. Expectation and Variance

### 4.1 Expectation

For a discrete random variable `X` with pmf `p(x)`, expectation is:

```text
E[X] = sum_x x p(x)
```

For a continuous random variable with density `f(x)`, expectation is:

```text
E[X] = integral x f(x) dx
```

Expectation is linear, which means:

```text
E[aX + b] = aE[X] + b
```

and more generally:

```text
E[X + Y] = E[X] + E[Y]
```

whether or not `X` and `Y` are independent.

### 4.2 Variance

Variance measures spread around the expectation:

```text
Var(X) = E[(X - E[X])^2]
```

An equivalent computational identity is:

```text
Var(X) = E[X^2] - (E[X])^2
```

Variance is not linear in the same way expectation is. However:

```text
Var(aX + b) = a^2 Var(X)
```

and if `X` and `Y` are independent:

```text
Var(X + Y) = Var(X) + Var(Y)
```

## 5. Worked Example

Suppose a service request fails with probability `p = 0.02`, independently from one request to the next.

### 5.1 Bernoulli Model for One Request

Let `X` be `1` if a request fails and `0` otherwise.

Then:

```text
X ~ Bernoulli(0.02)
```

So:

```text
P(X = 1) = 0.02
P(X = 0) = 0.98
E[X] = 0.02
Var(X) = 0.02 * 0.98 = 0.0196
```

### 5.2 Binomial Model for 100 Requests

Let `Y` be the number of failed requests in the next `100` requests.

Then:

```text
Y ~ Binomial(100, 0.02)
```

The expected number of failures is:

```text
E[Y] = np = 100 * 0.02 = 2
```

The variance is:

```text
Var(Y) = np(1-p) = 100 * 0.02 * 0.98 = 1.96
```

The probability of exactly `3` failures is:

```text
P(Y = 3) = C(100, 3) (0.02)^3 (0.98)^97
```

Compute step by step:

```text
C(100, 3) = 161700
(0.02)^3 = 0.000008
(0.98)^97 ≈ 0.1400
```

Now multiply:

```text
P(Y = 3) ≈ 161700 * 0.000008 * 0.1400
         ≈ 1.2936 * 0.1400
         ≈ 0.1811
```

So the probability of exactly `3` failures is about `0.181`.

Verification: the model uses a binary event, a fixed number of trials, and an independence assumption, so the Binomial choice is appropriate. The expected failure count is `2`, and getting exactly `3` failures has probability about `18.1%`. Correct.

## 6. Pseudocode Pattern

```text
procedure binomial_pmf(n, k, p):
    -- returns P(X = k) for X ~ Binomial(n, p)
    if k < 0 or k > n:
        return 0
    coeff = combination(n, k)
    return coeff * (p ^ k) * ((1 - p) ^ (n - k))
```

Time: `O(k)` or better, depending on how `combination(n, k)` is implemented. Space: `O(1)` auxiliary space if the combination is computed iteratively without storing intermediate arrays.

## 7. Common Mistakes

1. **Assumed independence.** Treating events as independent without justification underestimates or overestimates probabilities when failures, arrivals, or decisions are correlated.
2. **Base-rate neglect.** Applying Bayes’ rule without accounting for the prior probability of the underlying event leads to badly distorted posterior conclusions.
3. **Wrong distribution choice.** Using a Normal model for highly skewed counts or using a Poisson model when the rate is not stable produces poor approximations and misleading uncertainty estimates.
4. **Expectation-probability confusion.** Interpreting expectation as the most likely outcome is incorrect; the expected value is a weighted average, not necessarily the mode or even an attainable value.
5. **Variance additivity without conditions.** Writing `Var(X + Y) = Var(X) + Var(Y)` without independence or covariance conditions is false in general.

## 8. Practical Checklist

- [ ] Define the sample space and event of interest before assigning probabilities.
- [ ] Check whether dependence is plausible before multiplying probabilities or using Binomial formulas.
- [ ] Match the distribution to the data-generating mechanism, not just the output type.
- [ ] State the assumptions behind every distributional model explicitly.
- [ ] Compute both expectation and variance when summarizing a random variable.
- [ ] Use Bayes’ rule only after writing out the prior, likelihood, and evidence terms.
- [ ] Verify whether a Normal approximation is justified before using it for skewed or low-count data.

## 9. References

- Blitzstein, Joseph K., and Jessica Hwang. 2019. *Introduction to Probability* (2nd ed.). Chapman and Hall/CRC. <https://projects.iq.harvard.edu/stat110/home>
- Wasserman, Larry. 2004. *All of Statistics: A Concise Course in Statistical Inference*. Springer. <https://link.springer.com/book/10.1007/978-0-387-21736-9>
- OpenIntro. 2024. *OpenIntro Statistics*. OpenIntro. <https://www.openintro.org/book/os/>
- NIST/SEMATECH. 2012. *e-Handbook of Statistical Methods*. National Institute of Standards and Technology. <https://www.itl.nist.gov/div898/handbook/>
- NIST/SEMATECH. 2012. *Probability Distributions*. National Institute of Standards and Technology. <https://www.itl.nist.gov/div898/handbook/eda/section3/eda36.htm>
- Ross, Sheldon M. 2014. *Introduction to Probability Models* (11th ed.). Academic Press. <https://shop.elsevier.com/books/introduction-to-probability-models/ross/978-0-12-407948-9>
- Grinstead, Charles M., and J. Laurie Snell. 1997. *Introduction to Probability*. American Mathematical Society. <https://math.dartmouth.edu/~prob/prob/prob.pdf>
