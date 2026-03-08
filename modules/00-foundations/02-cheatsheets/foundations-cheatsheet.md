
# Foundations Cheat Sheet

## Complexity Quick-Reference

### Core asymptotic classes

| Class | Growth | Typical use / pattern |
|---|---:|---|
| `O(1)` | constant | hash lookup, array index access |
| `O(log n)` | logarithmic | binary search, balanced tree operations |
| `O(n)` | linear | single pass over data |
| `O(n log n)` | linearithmic | efficient comparison sorting |
| `O(n^2)` | quadratic | double nested loops over the same input |
| `O(2^n)` | exponential | subset enumeration, naive recursion |
| `O(n!)` | factorial | permutation enumeration |

### Core data and math operations

| Item | Time | Space | Notes |
|---|---:|---:|---|
| Binomial coefficient `C(n, k)` via multiplicative formula | `Theta(k)` worst | `Theta(1)` | avoids large factorials |
| Subset count of an `n`-element set | `Theta(1)` to state | `Theta(1)` | exact count is `2^n` |
| Permutation count of `n` distinct items | `Theta(1)` to state | `Theta(1)` | exact count is `n!` |
| Matrix-vector multiply `(m x n)` by `(n x 1)` | `Theta(mn)` | `Theta(m)` output | shape must match |
| Binomial PMF direct evaluation | `O(k)` or better | `O(1)` | depends on combination implementation |
| Kahan summation | `Theta(n)` | `Theta(1)` | more accurate than naive summation |

### Core distributions and summaries

| Concept | Formula / summary | Notes |
|---|---|---|
| Sample mean | `x_bar = (1/n) * sum x_i` | sensitive to outliers |
| Sample variance | `s^2 = (1/(n-1)) * sum (x_i - x_bar)^2` | use centered form |
| Conditional probability | `P(A | B) = P(A intersection B) / P(B)` | requires `P(B) > 0` |
| Bayes’ rule | `P(A | B) = P(B | A) P(A) / P(B)` | easy to misuse without base rates |
| Bernoulli | `E[X] = p`, `Var(X) = p(1-p)` | one binary trial |
| Binomial | `E[X] = np`, `Var(X) = np(1-p)` | fixed number of independent trials |
| Poisson | `E[X] = lambda`, `Var(X) = lambda` | count in interval |
| Normal | `E[X] = mu`, `Var(X) = sigma^2` | symmetric continuous model |

## Decision Tree

### Which foundation tool do you need?

Top-level question: what kind of problem are you looking at?

```text
Need to summarize observed numeric data?
├─ Distribution looks symmetric and outliers are limited?     → mean + standard deviation
└─ Distribution is skewed or has outliers?                   → median + IQR

Need to reason about uncertainty or event likelihood?
├─ One binary event?                                         → Bernoulli model
├─ Count successes in n independent trials?                  → Binomial model
├─ Count arrivals/events in a fixed interval at stable rate? → Poisson model
└─ Continuous quantity with roughly symmetric noise?         → Normal model

Need to compare two vectors or embeddings?
├─ Magnitude should matter?                                  → dot product
└─ Direction matters more than scale?                        → cosine similarity

Need to count or bound a discrete search space?
├─ Choosing positions or items without order?                → combinations / binomial coefficients
├─ Arranging distinct objects in order?                      → permutations / factorial growth
└─ Exploring all subsets of an n-element set?                → `2^n` state-space warning

Need to validate a formula or data pipeline?
├─ Physical or business units involved?                      → dimensional analysis
├─ Floating-point cancellation or rounding risk?             → stable reformulation / Kahan sum
└─ Shape mismatch in vectors or matrices?                    → dimension check before algebra
```

## Compact Glossary

- **Sample space** — set of all possible outcomes.
- **Event** — subset of the sample space.
- **Random variable** — numerical mapping from outcomes to values.
- **PMF** — probability rule for a discrete random variable.
- **PDF** — density for a continuous random variable.
- **Expectation** — long-run average value of a random variable.
- **Variance** — average squared deviation from the expectation.
- **Conditional probability** — probability after restricting attention to a known event.
- **Independence** — condition where `P(A intersection B) = P(A)P(B)`.
- **Binomial coefficient** — count of unordered `k`-element subsets from `n` items.
- **Permutation** — ordered arrangement of distinct items.
- **Factorial** — product `n! = n(n-1)...1`, common in permutation counts.
- **Gradient** — vector of partial derivatives.
- **Convex function** — objective where any local minimum is global.
- **Learning rate** — step size in gradient-based optimization.
- **Dot product** — scalar measuring vector alignment.
- **Norm** — measure of vector magnitude.
- **Matrix transpose** — row/column swap operation.
- **Catastrophic cancellation** — severe precision loss from subtracting nearly equal numbers.
- **Machine epsilon** — spacing between `1` and the next larger representable float.
- **Dimension** — physical type of a quantity, such as length or time.
- **Offset unit** — unit with arbitrary zero, such as Celsius.
- **Canonical unit** — single standard internal unit used across a system.

## Key Formulas / Index Formulas

### Descriptive statistics

```text
x_bar = (1/n) * sum_{i=1 to n} x_i
s^2 = (1/(n-1)) * sum_{i=1 to n} (x_i - x_bar)^2
SE(x_bar) = s / sqrt(n)
```

### Probability

```text
P(A^c) = 1 - P(A)
P(A union B) = P(A) + P(B) - P(A intersection B)
P(A | B) = P(A intersection B) / P(B)
P(A | B) = P(B | A) P(A) / P(B)
```

### Distributions

```text
P(X = k) = C(n, k) p^k (1-p)^(n-k)        -- Binomial
P(X = k) = e^(-lambda) lambda^k / k!      -- Poisson
```

### Linear algebra

```text
x · y = sum_{i=1 to n} x_i y_i
||x||_2 = sqrt(sum_{i=1 to n} x_i^2)
cos_sim(x, y) = (x · y) / (||x|| ||y||)
(AB)_ij = sum_{k=1 to n} A_ik B_kj
```

### Optimization

```text
w_(t+1) = w_t - alpha * grad L(w_t)
```

### Units and dimensional analysis

```text
quantity = number * unit
valid addition requires matching dimensions
conversion = value * (target unit / source unit)
```

## Debugging / Diagnosis

| Symptom | Likely cause |
|---|---|
| Mean looks much larger than the “typical” value | outliers or right-skew; median may be the better summary |
| Bayes result feels implausibly high | base-rate neglect or incorrect denominator `P(B)` |
| Probability calculation is too small or too large by orders of magnitude | dependence was ignored and probabilities were multiplied incorrectly |
| Matrix multiplication code crashes or returns wrong shape | inner dimensions do not match or row/column convention is inconsistent |
| Gradient descent oscillates or diverges | learning rate too large or features poorly scaled |
| Variance becomes slightly negative | unstable one-pass computation or floating-point cancellation |
| Float equality check fails for values that “should” match | exact comparison used instead of tolerance-based comparison |
| Latency / storage / money numbers are off by a constant factor | silent unit mismatch such as ms vs s, MB vs MiB, dollars vs cents |
| Temperature calculation gives nonsense ratios | offset unit handled like a ratio unit |
| Brute-force design explodes immediately | the search space is combinatorial, such as `2^n` or `n!` |

## When NOT to Use

| Structure / Algorithm / Summary | Avoid when |
|---|---|
| Mean | distribution is highly skewed or dominated by outliers |
| Standard deviation alone | data is heavy-tailed and you have not also checked robust summaries |
| Bernoulli model | outcome is not binary |
| Binomial model | trials are not independent or success probability changes across trials |
| Poisson model | event rate is unstable or arrivals are strongly clustered |
| Normal model | variable is bounded, highly skewed, or based on very small counts |
| Cosine similarity | one or both vectors can be zero or magnitude is semantically important |
| Direct inverse-based linear solve | a stable factorization method is available and numerical reliability matters |
| One-pass variance formula `E[X^2] - (E[X])^2` | values are large relative to their spread |
| Raw unitless numeric fields | multiple systems or APIs use different unit conventions |

## References

- Blitzstein, Joseph K., and Jessica Hwang. 2019. *Introduction to Probability* (2nd ed.). Chapman and Hall/CRC. <https://projects.iq.harvard.edu/stat110/home>
- Graham, Ronald L., Donald E. Knuth, and Oren Patashnik. 1994. *Concrete Mathematics* (2nd ed.). Addison-Wesley. <https://www-cs-faculty.stanford.edu/~knuth/gkp.html>
- Goldberg, David. 1991. What Every Computer Scientist Should Know About Floating-Point Arithmetic. *ACM Computing Surveys* 23(1): 5–48. <https://doi.org/10.1145/103162.103163>
- Hefferon, Jim. 2020. *Linear Algebra*. Orthogonal Publishing. <https://hefferon.net/linearalgebra/>
- Higham, Nicholas J. 2002. *Accuracy and Stability of Numerical Algorithms* (2nd ed.). SIAM. <https://doi.org/10.1137/1.9780898718027>
- Illowsky, Barbara, and Susan Dean. 2023. *Introductory Statistics*. OpenStax. <https://openstax.org/details/books/introductory-statistics>
- NIST/SEMATECH. 2012. *e-Handbook of Statistical Methods*. National Institute of Standards and Technology. <https://www.itl.nist.gov/div898/handbook/>
- Strang, Gilbert. 2016. *Introduction to Linear Algebra* (5th ed.). Wellesley-Cambridge Press. <https://math.mit.edu/~gs/linearalgebra/>
