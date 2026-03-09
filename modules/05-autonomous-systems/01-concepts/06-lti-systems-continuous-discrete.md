# LTI Systems: Continuous and Discrete

## Key Ideas

- An LTI state-space model captures continuous or sampled linear dynamics in a
  compact matrix form; it models superposition and time invariance, but it does
  not capture saturation, mode switching, or nonlinear effects unless those are
  abstracted away.
- The continuous-time solution `x(t) = e^{At} x(0) + ∫_0^t e^{A(t-τ)} B u(τ) dτ`
  is load-bearing: stability, discretization, and controllability arguments all
  flow from it.
- For autonomous continuous-time LTI systems, asymptotic stability is
  equivalent to every eigenvalue of `A` having strictly negative real part; for
  discrete-time LTI systems, the corresponding condition is `|λ_i(A_d)| < 1`.
- Exact zero-order-hold discretization preserves the sampled dynamics; Euler
  discretization is only an approximation and can distort or even destabilize a
  controller when the sample time is too large.
- Continuous LTI dynamics often appear as one mode inside a hybrid automaton,
  so control-theoretic analysis and formal-methods analysis meet at the mode
  boundary.

## Intuition

Control theory often begins by linearizing the world. Around an operating
point, many physical systems behave approximately like "current state times a
matrix plus input times a matrix." That approximation is not universally true,
but it is powerful because linear algebra gives exact formulas for trajectories,
stability, controllability, and observability.

The state-space form packages those ideas cleanly. Instead of writing one high
order differential equation for each output, we track a vector of internal
variables that evolve together. That view is especially useful for autonomous
systems, because the controller rarely cares about one scalar alone; it cares
about position, velocity, attitude, error states, and actuator commands as a
coupled dynamical system.

Digital control introduces a second layer. The plant may evolve continuously,
but the controller samples sensors and updates commands at discrete times. That
means a continuous-time model and its sampled discrete-time implementation are
not interchangeable. If the discretization is wrong, the implemented controller
may behave very differently from the design on paper.

## 1. State-Space Representation

**Definition (Continuous-time LTI system).**  
A continuous-time LTI system is a tuple `(A, B, C, D)` together with the
equations

`ẋ(t) = A x(t) + B u(t)`  
`y(t) = C x(t) + D u(t)`

where:

- `x(t) ∈ R^n` is the state vector;
- `u(t) ∈ R^m` is the input vector;
- `y(t) ∈ R^p` is the output vector;
- `A ∈ R^{n×n}`, `B ∈ R^{n×m}`, `C ∈ R^{p×n}`, `D ∈ R^{p×m}` are constant
  matrices.

Gloss:

- `A` governs autonomous state evolution.
- `B` tells inputs how to push the state.
- `C` selects what part of the state is measured as output.
- `D` is the direct feedthrough term.

Constraint note:

- Time invariance means the matrices are constant, not functions of `t`.

Minimal reusable example:

- `A = [[0, 1], [0, 0]]`, `B = [[0], [1]]`, `C = [[1, 0]]`, `D = [[0]]`.

**Definition (Discrete-time LTI system).**  
A discrete-time LTI system is a tuple `(A_d, B_d, C, D)` together with the
equations

`x[k+1] = A_d x[k] + B_d u[k]`  
`y[k] = C x[k] + D u[k]`

where the symbols have the analogous meanings in sampled time.

## 2. Solving the Continuous-Time State Equation

We derive the solution for

`ẋ(t) = A x(t) + B u(t)`, `x(0) = x_0`.

First consider the homogeneous system `ẋ = A x`. Define the matrix exponential

`e^{At} = Σ_{k=0}^∞ (A^k t^k) / k!`.

It satisfies `(d/dt)e^{At} = A e^{At}` and `e^{A0} = I`, so

`x_h(t) = e^{At} x_0`

solves the homogeneous equation.

For the forced system, use variation of constants by writing `x(t) = e^{At} z(t)`.
Differentiating gives

`ẋ(t) = A e^{At} z(t) + e^{At} ż(t)`.

Substituting into the state equation and canceling `A e^{At} z(t)` yields

`e^{At} ż(t) = B u(t)`,

so

`ż(t) = e^{-At} B u(t)`.

Integrating from `0` to `t`,

`z(t) = x_0 + ∫_0^t e^{-Aτ} B u(τ) dτ`.

Multiplying by `e^{At}` gives the full solution:

`x(t) = e^{At} x_0 + ∫_0^t e^{A(t-τ)} B u(τ) dτ`.

This formula is the continuous-time analogue of unrolling a recurrence.

## 3. Stability

For the autonomous system `ẋ = A x`, asymptotic stability means

`lim_{t->∞} x(t) = 0`

for every initial state `x_0`.

**Theorem (Continuous-time eigenvalue test).**  
The autonomous continuous-time LTI system `ẋ = A x` is asymptotically stable if
and only if every eigenvalue of `A` satisfies `Re(λ_i(A)) < 0`.

Plain-English reading: every dynamical mode of the matrix must decay
exponentially rather than persist or grow.

*Proof sketch.* Write the solution as `x(t) = e^{At} x_0`. In Jordan normal
form, `e^{At}` decomposes into terms of the form `t^k e^{λ t}`. If every
`Re(λ) < 0`, then the exponential decay dominates any polynomial factor and each
term tends to zero, so `e^{At} -> 0`. Conversely, if some eigenvalue has
non-negative real part, then the corresponding modal component does not decay to
zero, so there exists an initial condition whose trajectory fails to converge to
the origin. Full proofs appear in standard control texts such as Ogata or
Kailath.

The discrete-time analogue is:

**Corollary (Discrete-time eigenvalue test).**  
The autonomous discrete-time system `x[k+1] = A_d x[k]` is asymptotically
stable if and only if `|λ_i(A_d)| < 1` for every eigenvalue of `A_d`.

## 4. Exact Discretization and Euler Approximation

Suppose the input is held constant over each sample interval of length `T_s`
(zero-order hold). Then the exact sampled model is

`x[k+1] = A_d x[k] + B_d u[k]`

with

`A_d = e^{A T_s}`  
`B_d = ∫_0^{T_s} e^{Aτ} B dτ`.

If `A` is invertible, the integral simplifies to

`B_d = A^{-1}(A_d - I) B`.

Euler discretization replaces the continuous dynamics by a first-order finite
difference:

`x[k+1] ≈ (I + A T_s) x[k] + T_s B u[k]`.

This is computationally cheap but approximate.

**Warning.** The Euler discretization `A_d ≈ I + A T_s` can destabilize a
controller numerically when the sample period is too large or when the
continuous-time system is only marginally stable. Exact discretization should
be the default for design and analysis.

## 5. Controllability and Observability

**Definition (Controllability).**  
The discrete-time pair `(A_d, B_d)` is controllable if the controllability
matrix

`Ctrb = [B_d, A_d B_d, A_d^2 B_d, ..., A_d^{n-1} B_d]`

has rank `n`.

Interpretation: every state dimension can be influenced by some input sequence.

**Definition (Observability).**  
The pair `(A_d, C)` is observable if the observability matrix

`Obs = [C; C A_d; C A_d^2; ...; C A_d^{n-1}]`

has rank `n`.

Interpretation: the internal state can be reconstructed from output
measurements over time.

Minimal contrast:

- Controllable example: the double integrator below has
  `rank([B, AB]) = 2`.
- Uncontrollable example: `A = [[1, 0], [0, 1]]`, `B = [[1], [0]]` has
  controllability rank `1`, so the second state cannot be actuated.

## 6. Worked Example: Double Integrator

Consider the double-integrator system

`ẋ(t) = A x(t) + B u(t)`, with  
`A = [[0, 1], [0, 0]]`, `B = [[0], [1]]`.

Choose `C = [[1, 0]]`, `D = [[0]]`.

### 6.1 Stability and eigenvalues

The characteristic polynomial of `A` is `λ^2`, so the eigenvalues are
`λ_1 = 0`, `λ_2 = 0`. Because the real parts are not strictly negative, the
continuous-time system is not asymptotically stable.

In fact, with `u(t) = 0`,

`x_2(t) = x_2(0)`,  
`x_1(t) = x_1(0) + t x_2(0)`,

so position can drift linearly.

### 6.2 Exact discretization for `T_s = 0.1 s`

Because `A^2 = 0`, the matrix exponential truncates:

`A_d = e^{A T_s} = I + A T_s = [[1, 0.1], [0, 1]]`.

Also,

`B_d = ∫_0^{0.1} e^{Aτ} B dτ = [[0.005], [0.1]]`.

Euler gives the same `A_d` here only because `A^2 = 0`; in general it would be
an approximation, not an equality.

### 6.3 Controllability and observability

The continuous-time controllability matrix is

`[B, AB] = [[0, 1], [1, 0]]`,

which has rank `2`, so the system is controllable.

The observability matrix for `C = [[1, 0]]` is

`[C; C A] = [[1, 0], [0, 1]]`,

which also has rank `2`, so the state is observable from position
measurements over time.

### 6.4 State-feedback pole placement

Let `u = -K x` with `K = [k_1, k_2]`. Then

`A - B K = [[0, 1], [-k_1, -k_2]]`.

Its characteristic polynomial is

`λ^2 + k_2 λ + k_1`.

To place the closed-loop poles at `-1` and `-2`, match to

`(λ + 1)(λ + 2) = λ^2 + 3 λ + 2`,

so choose `K = [2, 3]`.

### 6.5 Executable sampled trace

Use the discrete-time closed-loop model with `u[k] = -K x[k]`,
`x[0] = [1, 0]^T`, and `T_s = 0.1`.

| Step | `x[k]` | `u[k] = -K x[k]` | Update | `x[k+1]` |
|------|--------|-------------------|--------|-----------|
| 0 | `[1, 0]^T` | `-2.00` | `A_d x[0] + B_d u[0]` | `[0.99, -0.20]^T` |
| 1 | `[0.99, -0.20]^T` | `-1.38` | `A_d x[1] + B_d u[1]` | `[0.9631, -0.338]^T` |
| 2 | `[0.9631, -0.338]^T` | `-0.9122` | `A_d x[2] + B_d u[2]` | `[0.92484, -0.42922]^T` |

The state norm is decreasing, consistent with the chosen stable closed-loop
poles.

### 6.6 Property check

The property is "the closed-loop sampled system moves toward the origin." The
trace is not a proof by itself, but it is consistent with the eigenvalue test:
the continuous-time closed-loop matrix

`A - B K = [[0, 1], [-2, -3]]`

has eigenvalues `-1` and `-2`, so the equilibrium is asymptotically stable.

## 7. Connection Forward

In a hybrid automaton, one mode may have flow `ẋ = A_i x + B_i u` while another
mode uses a different pair `(A_j, B_j)`. The LTI analysis here therefore
provides the local dynamics inside each mode, while the hybrid model handles
switching between them; see
[08-hybrid-systems-intuition.md](08-hybrid-systems-intuition.md).

## 8. Common Mistakes

1. Mixing up continuous-time `A` and discrete-time `A_d` as if they were the
   same object.
2. Using Euler discretization in a controller implementation without checking
   whether the sample time is small enough.
3. Declaring a system stable because all eigenvalues are non-positive; strict
   negativity of the real parts is required for asymptotic stability.
4. Checking controllability on the wrong pair, such as using the continuous-time
   rank test on a discretized design without recomputing the matrices.
5. Forgetting that saturation, switching, and dead zones invalidate the linear
   model outside its operating range.

## 9. Practical Checklist

- [ ] Write the full continuous-time and, if implemented digitally, the sampled
      discrete-time model.
- [ ] Derive or compute `A_d` and `B_d` using exact discretization before using
      Euler as an approximation.
- [ ] Check eigenvalues against the correct stability condition for the time
      domain you are in.
- [ ] Verify controllability before attempting pole placement.
- [ ] Verify observability before designing a state estimator.
- [ ] Validate the model numerically on a small hand-computable trace.

## 10. References

- Kailath, Thomas. 1980. *Linear Systems*. Prentice Hall.
- Lee, Edward A., and Sanjit A. Seshia. 2017. *Introduction to Embedded
  Systems*. 2nd ed.
  <https://ptolemy.berkeley.edu/books/leeseshia/>
- Ogata, Katsuhiko. 2010. *Modern Control Engineering*. 5th ed. Pearson.
- Rugh, Wilson J. 1996. *Linear System Theory*. 2nd ed. Prentice Hall.
- Sontag, Eduardo D. 1998. *Mathematical Control Theory*. 2nd ed. Springer.
- Zhou, Kemin, John C. Doyle, and Keith Glover. 1996. *Robust and Optimal
  Control*. Prentice Hall.
