
# Numerical Stability and Precision

## Key Ideas

- Finite-precision arithmetic does not obey real-number algebra exactly, so mathematically equivalent formulas can produce very different numerical errors.
- A numerically stable algorithm limits the amplification of rounding error, while an unstable algorithm can turn small floating-point perturbations into large output errors.
- Catastrophic cancellation occurs when subtracting nearly equal numbers, because leading digits cancel and the remaining result has much lower relative accuracy.
- Conditioning and stability are different: conditioning measures the sensitivity of the mathematical problem, while stability measures the quality of the algorithm used to solve it.
- Scaling, compensated summation, and stable reformulations are practical tools for reducing numerical error in statistics, optimization, and simulation code.

## 1. What It Is

Numerical stability studies how finite-precision arithmetic affects computation. Real machines do not compute with exact real numbers. They use floating-point representations with limited precision, finite exponent range, and rounding rules. As a result, every arithmetic operation may introduce a small error.

These small errors are often harmless, but they do not always stay small. In poorly designed computations, rounding error can accumulate, cancellation can destroy significant digits, and overflow or underflow can make a result unusable. Numerical analysis therefore asks two related questions:

- Is the underlying mathematical problem sensitive to small perturbations?
- Does the chosen algorithm control or amplify the errors introduced by finite precision?

### 1.1 Core Definitions

- A **floating-point number** is a finite-precision approximation of a real number, typically represented by sign, exponent, and significand.
- **Rounding error** is the difference between the exact real result of an operation and its floating-point representation.
- A problem is **well-conditioned** if small input perturbations produce only small output perturbations.
- A problem is **ill-conditioned** if small input perturbations can cause large output changes.
- An algorithm is **numerically stable** if it does not amplify rounding errors excessively during computation.
- **Machine epsilon** is the gap between `1` and the next larger representable floating-point number in a given format.
- **Catastrophic cancellation** is the loss of significant digits when subtracting nearly equal quantities.

### 1.2 Why This Matters

Numerical instability appears in many places that look unrelated at first:

- computing variance or covariance from large values,
- summing gradients in optimization,
- solving linear systems,
- estimating probabilities close to `0` or `1`,
- and comparing floating-point outputs in tests.

A pipeline can be logically correct and still produce unreliable results if its arithmetic is unstable. In machine learning, this can lead to exploding or vanishing intermediate values. In statistics, it can produce negative variances from formulas that should never be negative. In simulation, it can make a trajectory drift purely because of arithmetic error.

## 2. Floating-Point Arithmetic

### 2.1 Finite Representation

Most real numbers cannot be represented exactly in binary floating point. Even simple decimal values such as `0.1` usually become nearby approximations. This means that expressions like

```text
0.1 + 0.2 == 0.3
```

may evaluate to false in a programming language that uses IEEE 754 floating point.

The key consequence is that floating-point arithmetic approximates real arithmetic, but it is not identical to it.

### 2.2 Rounding and Error Accumulation

Suppose a floating-point operation returns

```text
fl(x op y) = (x op y)(1 + delta)
```

where `|delta|` is small. A single rounding error may be tiny, but long chains of operations can accumulate many such perturbations.

Some computations are relatively tolerant of this accumulation. Others are not. For example, adding many positive numbers of similar scale is usually more stable than alternating additions and subtractions of very different magnitudes.

### 2.3 Overflow, Underflow, and Loss of Significance

Finite exponent range creates two additional hazards:

- **Overflow** occurs when a magnitude is too large to represent.
- **Underflow** occurs when a magnitude is too small to represent normally.

Loss of significance is different: it happens even when the result is representable, but many meaningful digits are destroyed by arithmetic structure, especially subtraction of nearly equal terms.

## 3. Stability, Conditioning, and Cancellation

### 3.1 Conditioning vs Stability

It is essential to separate the problem from the algorithm.

- **Conditioning** is about the mathematical problem itself.
- **Stability** is about the algorithm used to solve that problem.

A well-conditioned problem can still be solved poorly by an unstable algorithm. An ill-conditioned problem can still be handled as carefully as possible by a stable algorithm, though the output may still be sensitive because the problem itself is sensitive.

### 3.2 Catastrophic Cancellation

Catastrophic cancellation occurs when subtracting nearly equal values:

```text
a - b
```

If `a` and `b` agree in many leading digits, those digits cancel, and the result may retain only a small number of accurate digits. The subtraction is not wrong, but the relative error of the result can become very large.

This often appears in formulas such as:

- quadratic roots,
- variance formulas based on `E[X^2] - (E[X])^2`,
- finite differences,
- and log-probability transformations.

### 3.3 Backward Error Intuition

A useful mental model is **backward stability**. An algorithm is backward stable if its computed answer is exactly correct for a slightly perturbed input. This is often the strongest practical notion of stability in numerical linear algebra and scientific computing.

**Why this matters:** Backward stability gives a concrete error story. Instead of asking whether every intermediate step is exact, ask whether the final result is what you would get from solving a nearby problem.

## 4. Worked Example

Consider the sample values

```text
x = [100000001, 100000002, 100000003]
```

We will compare two ways to compute the sample variance.

### 4.1 Unstable One-Pass Formula

A common formula is

```text
variance = (1/n) * sum(x_i^2) - ((1/n) * sum(x_i))^2
```

Compute the pieces:

```text
n = 3
sum(x_i) = 100000001 + 100000002 + 100000003 = 300000006
mean = 300000006 / 3 = 100000002
```

Now square and sum:

```text
100000001^2 = 10000000200000001
100000002^2 = 10000000400000004
100000003^2 = 10000000600000009
```

So

```text
sum(x_i^2) = 30000001200000014
(1/n) * sum(x_i^2) = 10000000400000004.666...
```

Also:

```text
mean^2 = 100000002^2 = 10000000400000004
```

Subtract:

```text
variance = 10000000400000004.666... - 10000000400000004
         = 0.666...
```

In exact arithmetic this is fine. But in floating-point arithmetic, the two large terms can be rounded before subtraction. Because they are extremely close relative to their size, cancellation can remove most meaningful digits. On real machines this formula can lose accuracy badly and may even produce a tiny negative value for data that should yield a nonnegative variance.

### 4.2 Stable Two-Pass Computation

Now compute the variance using centered values.

First pass: compute the mean.

```text
mean = 100000002
```

Second pass: compute squared deviations.

```text
100000001 - 100000002 = -1
100000002 - 100000002 =  0
100000003 - 100000002 =  1
```

Square and sum:

```text
(-1)^2 + 0^2 + 1^2 = 1 + 0 + 1 = 2
```

Population variance:

```text
variance = 2 / 3 = 0.666...
```

The stable version works with small centered numbers rather than subtracting two huge nearly equal quantities.

Verification: the centered deviations are `[-1, 0, 1]`, their squared sum is `2`, and the population variance is `2/3`. This matches the exact variance. Correct.

## 5. Stable Patterns and Practical Techniques

### 5.1 Prefer Stable Reformulations

Many unstable formulas have stable alternatives.

Examples:

- Use centered formulas for variance and covariance.
- Use numerically stable quadratic root formulas to avoid subtractive cancellation.
- Use `logsumexp` instead of exponentiating large-magnitude logits directly.
- Solve linear systems with factorization methods instead of explicitly computing matrix inverses when possible.

### 5.2 Summation Order Matters

Summing from smallest magnitude to largest can reduce error relative to arbitrary order when numbers differ substantially in scale. Compensated summation methods such as Kahan summation go further by tracking lost low-order bits.

### 5.3 Scaling Before Optimization

Poor feature scaling can worsen numerical behavior in optimization and linear algebra. Scaling does not just help convergence rates; it can also reduce loss of precision by keeping magnitudes in a numerically reasonable range.

## 6. Pseudocode Pattern

```text
procedure kahan_sum(values):
    -- compensated summation for improved floating-point accuracy
    total = 0.0
    c = 0.0
    for i = 0 to length(values) - 1:
        y = values[i] - c
        t = total + y
        c = (t - total) - y
        total = t
    return total
```

Time: `Theta(n)` in all cases. Space: `Theta(1)` auxiliary space.

This algorithm adds a compensation term `c` that captures the low-order bits lost in previous additions.

## 7. Common Mistakes

1. **Exact float equality.** Comparing floating-point values with exact equality often fails because representable numbers are approximations; use a tolerance-based comparison when the task is numeric equivalence rather than bitwise identity.
2. **One-pass variance subtraction.** Computing variance as `E[X^2] - (E[X])^2` can trigger catastrophic cancellation for large values with small spread; prefer a stable two-pass method or Welford’s online algorithm.
3. **Uncompensated mixed-scale summation.** Summing very large and very small numbers in arbitrary order can lose the smaller contributions almost entirely; use sorted accumulation or compensated summation when precision matters.
4. **Ignored conditioning.** Blaming the algorithm alone when outputs are unstable can miss the deeper issue that the mathematical problem is ill-conditioned; check both the formulation and the method.
5. **Unscaled optimization inputs.** Feeding wildly different magnitudes into optimization or matrix computations can magnify rounding and conditioning problems; rescale inputs before solving or training.

## 8. Practical Checklist

- [ ] Check whether the formula being implemented subtracts nearly equal quantities.
- [ ] Use tolerance-based comparisons for floating-point assertions unless exact representation is required.
- [ ] Prefer stable reformulations over algebraically equivalent but cancellation-prone formulas.
- [ ] Track whether the problem is ill-conditioned separately from whether the algorithm is unstable.
- [ ] Use compensated summation when aggregating many values with mixed magnitudes.
- [ ] Rescale features, coefficients, or units when magnitudes differ by several orders.
- [ ] Verify worked examples or tests with inputs that include both large values and small gaps.

## 9. References

- Goldberg, David. 1991. What Every Computer Scientist Should Know About Floating-Point Arithmetic. *ACM Computing Surveys* 23(1): 5–48. <https://doi.org/10.1145/103162.103163>
- Higham, Nicholas J. 2002. *Accuracy and Stability of Numerical Algorithms* (2nd ed.). SIAM. <https://doi.org/10.1137/1.9780898718027>
- IEEE Standards Association. 2019. *IEEE Standard for Floating-Point Arithmetic (IEEE 754-2019)*. <https://ieeexplore.ieee.org/document/8766229>
- NIST/SEMATECH. 2012. *e-Handbook of Statistical Methods*. National Institute of Standards and Technology. <https://www.itl.nist.gov/div898/handbook/>
- Trefethen, Lloyd N., and David Bau III. 1997. *Numerical Linear Algebra*. SIAM. <https://epubs.siam.org/doi/book/10.1137/1.9781611971484>
- Wilkinson, James H. 1994. *Rounding Errors in Algebraic Processes*. Dover Publications. <https://store.doverpublications.com/products/9780486797052>
- Welford, B. P. 1962. Note on a Method for Calculating Corrected Sums of Squares and Products. *Technometrics* 4(3): 419–420. <https://doi.org/10.1080/00401706.1962.10490022>
