# Controller Synthesis Intuition

## What it is
Controller synthesis constructs a policy that chooses actions to guarantee a
property (usually safety) under model assumptions.

## Why it matters
Instead of merely verifying a design, synthesis can produce a correct-by-
construction controller for a simplified model.

## Core definitions
- **Policy**: function from state (and maybe history) to action.
- **Safety game**: adversarial setting where the environment picks disturbances.
- **Winning set**: states from which a controller can enforce safety.
- **Fixed point**: iterative computation of safe states.

## Worked micro-example
A robot can move Left or Right on a line with unsafe state U:
- If from state S, either action can avoid U in one step, S is safe.
- If all actions lead to U, S is unsafe.
- The policy chooses the action that stays in the safe set.

## Common pitfalls
- Assuming synthesis without modeling the environment.
- Ignoring controllability (some transitions are not choices).
- Using overly coarse abstractions that hide unsafe states.

## Verification / debug checklist
- Is the controller choice distinguished from environment moves?
- Are safe states closed under the chosen actions?
- Does the policy handle all reachable states?
- Are assumptions about disturbances explicit?

## References
- *Principles of Model Checking* — https://mitpress.mit.edu/9780262026499/
- *Reactive Synthesis Lectures* (Bloem et al.) — https://link.springer.com/book/10.1007/978-3-319-77264-3
