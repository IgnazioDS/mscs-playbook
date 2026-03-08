# Calculus and Optimization Basics

## Key Ideas

- Calculus provides local information about change, and optimization uses that information to choose parameters that improve an objective.
- The derivative measures one-dimensional sensitivity, while the gradient generalizes that idea to multivariate functions.
- Gradient-based optimization updates parameters in the direction of decreasing objective value, typically using `w = w - alpha * grad_L(w)`.
- Convex objectives are easier to optimize because every local minimum is also a global minimum.
- The learning rate controls the tradeoff between convergence speed and numerical stability.

## 1. What It Is

Calculus studies how quantities change. In optimization, the most useful objects are derivatives, partial derivatives, and gradients because they describe how an objective responds to small parameter changes.

For a scalar function `f(x)`, the derivative `f'(x)` measures the instantaneous rate of change at `x`. For a multivariate function `f(x_1, ..., x_n)`, the gradient `grad f(x)` is the vector of partial derivatives:

```text
grad f(x) = [df/dx_1, df/dx_2, ..., df/dx_n]
```

Optimization studies how to choose inputs that minimize or maximize an objective. In engineering and machine learning, the objective is often a loss, cost, energy, or error function. A typical goal is to solve:

```text
minimize_w L(w)
```

where `w` is a parameter vector and `L(w)` is the loss.

### 1.1 Core definitions

- A **derivative** is the local slope of a one-variable function.
- A **partial derivative** measures how a multivariate function changes when one variable changes and the others are held fixed.
- A **gradient** is the vector of all partial derivatives.
- A **critical point** is a point where the gradient is zero or undefined.
- A **minimum** is a point whose objective value is smaller than nearby points; a **global minimum** is smaller than every feasible point.

### 1.2 Why this matters

These ideas appear everywhere in technical work. Model training minimizes prediction loss. Control systems tune gains to reduce error. Systems engineering chooses thresholds that trade latency against throughput or cost. Without calculus, these tasks become guesswork. Without optimization, the derivative is only descriptive and not operational.

## 2. Why It Matters in Practice

Optimization is not just a mathematical abstraction. It determines whether a model trains reliably, whether a system remains stable under load, and whether a design process converges in a reasonable amount of time.

### 2.1 Engineering tradeoffs

A small learning rate often produces stable but slow updates. A large learning rate can reduce the objective quickly at first, but it can also overshoot the minimum and diverge. This is a direct engineering tradeoff between runtime and stability.

Feature scaling creates another tradeoff. If one feature ranges in thousands and another in fractions, the objective can become badly conditioned. Gradient descent then zig-zags instead of moving efficiently toward the minimum. Preprocessing is therefore part of optimization, not a separate concern.

### 2.2 Convex and non-convex objectives

A function `f` is convex if, for any `x` and `y` and any `lambda` in `[0, 1]`,

```text
f(lambda x + (1 - lambda) y) <= lambda f(x) + (1 - lambda) f(y)
```

For convex objectives, any local minimum is also a global minimum. This gives strong guarantees and simplifies reasoning.

For non-convex objectives, local minima, saddle points, and flat regions can all appear. In that setting, initialization, step size, and optimizer choice matter much more.

## 3. Core Ideas

### 3.1 Derivatives as local sensitivity

If `f(x)` is differentiable at `x`, then `f'(x)` tells us how much `f(x)` changes for a small change in `x`. A first-order approximation is:

```text
f(x + h) ≈ f(x) + f'(x) h
```

This approximation explains why derivatives are useful in optimization: they tell us which direction locally increases or decreases the objective.

### 3.2 Gradients for multivariate functions

For `f(x, y)`, the gradient is:

```text
grad f(x, y) = [df/dx, df/dy]
```

The gradient points in the direction of steepest increase. Therefore, `-grad f(x, y)` points in the direction of steepest local decrease. Gradient descent uses that fact directly.

### 3.3 Learning rate and convergence

The standard gradient descent update is:

```text
w_(t+1) = w_t - alpha * grad L(w_t)
```

where `alpha > 0` is the learning rate.

- If `alpha` is too small, progress is slow.
- If `alpha` is too large, updates can oscillate or diverge.
- If `alpha` is chosen reasonably and the objective is well-behaved, the loss usually decreases over time.

### 3.4 Complexity and cost intuition

A single gradient descent step is not free. Its cost depends on how expensive it is to evaluate the gradient.

| Quantity | Typical interpretation |
|---|---|
| Objective evaluation | Compute `L(w)` for current parameters |
| Gradient evaluation | Compute all partial derivatives |
| Iteration count | Number of updates until stopping criterion is met |
| Total optimization cost | Cost per step times number of steps |

For many practical systems, reducing iterations is as important as reducing asymptotic complexity, because each step can involve large matrix operations or full-batch data passes.

## 4. Worked Example

Consider the one-dimensional objective `L(w) = (w - 3)^2`. This is a convex quadratic with global minimum at `w = 3`.

Its derivative is:

```text
L'(w) = 2(w - 3)
```

We run gradient descent with:

- initial value `w_0 = 0`
- learning rate `alpha = 0.25`

The update rule is:

```text
w_(t+1) = w_t - 0.25 * 2(w_t - 3)
```

**Worked example:**

| Step | `w_t` | `L(w_t)` | `L'(w_t)` | Update | `w_(t+1)` |
|---|---:|---:|---:|---|---:|
| 0 | 0.00 | 9.00 | -6.00 | `w = 0 - 0.25 * (-6)` | 1.50 |
| 1 | 1.50 | 2.25 | -3.00 | `w = 1.5 - 0.25 * (-3)` | 2.25 |
| 2 | 2.25 | 0.5625 | -1.50 | `w = 2.25 - 0.25 * (-1.5)` | 2.625 |
| 3 | 2.625 | 0.140625 | -0.75 | `w = 2.625 - 0.25 * (-0.75)` | 2.8125 |
| 4 | 2.8125 | 0.03515625 | -0.375 | `w = 2.8125 - 0.25 * (-0.375)` | 2.90625 |

The parameter moves toward `3`, and the loss decreases at every step. Because the objective is convex and the learning rate is moderate, the process is stable.

### 4.1 Comparison with a bad learning rate

Now keep the same objective but choose `alpha = 1.5`.

| Step | `w_t` | `L'(w_t)` | `w_(t+1)` |
|---|---:|---:|---:|
| 0 | 0.0 | -6.0 | 9.0 |
| 1 | 9.0 | 12.0 | -9.0 |
| 2 | -9.0 | -24.0 | 27.0 |

This sequence diverges. The example shows that the update rule alone is not enough; the step size determines whether optimization is useful.

## 5. Pseudocode Pattern

```text
procedure gradient_descent(objective, gradient, w0, alpha, max_steps, tolerance):
    w = w0
    for step = 0 to max_steps - 1:
        g = gradient(w)
        if norm(g) <= tolerance:
            return w
        w = w - alpha * g
    return w
```

### 5.1 Reading the pseudocode

- `objective` computes the current loss.
- `gradient` computes the derivative or gradient at the current point.
- `norm(g)` checks whether the gradient is close to zero.
- `tolerance` is a stopping threshold.
- `max_steps` prevents infinite loops when convergence is slow or absent.

### 5.2 Why this matters

A correct optimization routine must define both an update rule and a stopping rule. Many failures come from implementing one but not the other.

## 6. Common Mistakes

1. **Oversized learning rate.** Using a step size that is too large causes oscillation or divergence even on simple objectives; reduce `alpha` or use a schedule when the loss jumps instead of decreases.
2. **Unscaled features.** Feeding features with very different magnitudes into gradient-based methods slows convergence and can make the path unstable; standardize or normalize inputs before training.
3. **Confusing derivative and gradient.** Treating a multivariate objective as if it had a single scalar derivative leads to incomplete updates; use the full gradient vector when the parameter has multiple components.
4. **Assuming every minimum is global.** Local minima and saddle points are common in non-convex objectives; do not claim global optimality unless the problem structure justifies it.
5. **Stopping without a criterion.** Running for a fixed number of steps without checking gradient size, loss improvement, or validation behavior can waste compute or stop too early.

## 7. Practical Checklist

- [ ] State the objective function explicitly before discussing how to optimize it.
- [ ] Define whether the page is using a derivative, a partial derivative, or a full gradient.
- [ ] Specify the update rule in symbols, including the learning rate.
- [ ] Say whether each optimization claim assumes a convex or non-convex objective.
- [ ] Show at least one fully traced numerical example with intermediate values.
- [ ] Distinguish convergence speed from per-iteration computational cost.
- [ ] Include a concrete stopping condition in every optimization pseudocode block.

## References

- Boyd, Stephen, and Lieven Vandenberghe. 2004. *Convex Optimization*. Cambridge University Press. <https://web.stanford.edu/~boyd/cvxbook/>
- Goodfellow, Ian, Yoshua Bengio, and Aaron Courville. 2016. *Deep Learning*. MIT Press. <https://www.deeplearningbook.org/>
- OpenStax. 2025. *Calculus Volume 1*. OpenStax. <https://openstax.org/details/books/calculus-volume-1>
- PyTorch Contributors. 2026. *torch.optim*. PyTorch Documentation. <https://docs.pytorch.org/docs/stable/optim.html>
- NumPy Developers. 2026. *numpy.gradient*. NumPy Reference. <https://numpy.org/doc/stable/reference/generated/numpy.gradient.html>
- Wikipedia Contributors. 2026. *Gradient Descent*. Wikipedia. <https://en.wikipedia.org/wiki/Gradient_descent>
