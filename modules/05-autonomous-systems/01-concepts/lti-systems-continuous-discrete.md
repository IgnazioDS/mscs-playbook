# LTI Systems (Continuous and Discrete)

## What it is

Linear time-invariant (LTI) systems model dynamics where state changes linearly
and do not depend explicitly on time.

## Why it matters

LTI models are the backbone of control and estimation, and they are simple
enough to analyze with proofs and fast checks.

## Core definitions

- **Continuous LTI**: ẋ = A x + B u
- **Discrete LTI**: x_{k+1} = A x_k + B u_k
- **Trajectory**: sequence of states from an initial condition and inputs.
- **Stability (intuition)**: trajectories remain bounded for bounded inputs.

## Worked micro-example

A 1D integrator with input u_k:

- A = [1], B = [1], x_0 = 0
- Inputs U = [1, 1, 1]
- Trajectory: x_1 = 1, x_2 = 2, x_3 = 3

## Common pitfalls

- Confusing continuous and discrete matrices (A_c vs A_d).
- Using large dt in discretization, hiding instability.
- Forgetting that input saturation breaks linearity.

## Verification / debug checklist

- Are units consistent (seconds, meters, etc.)?
- Did you discretize with the correct dt?
- Do trajectories match hand-computed steps on a tiny example?
- Is the safety invariant checked at each step?

## References

- *Linear Systems* (Kailath) — <https://web.stanford.edu/~boyd/ee363/>
- *Feedback Systems* (Åström & Murray) — <https://fbsbook.org/>
