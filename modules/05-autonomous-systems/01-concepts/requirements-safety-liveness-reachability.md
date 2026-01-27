# Requirements: Safety, Liveness, Reachability

## What it is
Property types that express what an autonomous system must always avoid
(safety), must eventually do (liveness), or can reach (reachability).

## Why it matters
Clear requirement classes let you pick the right verification technique and
avoid ambiguous or untestable specs.

## Core definitions
- **Safety**: "something bad never happens" (e.g., never enter unsafe state).
- **Liveness**: "something good eventually happens" (e.g., eventually dock).
- **Reachability**: can a state be reached from the initial set?
- **Invariant**: a condition that holds in all reachable states.

## Worked micro-example
A drone must never enter a no-fly zone (NFZ) and must eventually land:
- Safety: G ¬NFZ
- Liveness: F Landed
- Reachability: can it reach Landed from Start?

## Common pitfalls
- Writing liveness where safety is needed (or vice versa).
- Forgetting to define the "bad" or "goal" state precisely.
- Assuming reachability implies liveness (it does not).

## Verification / debug checklist
- Is the property safety, liveness, or both?
- Is the bad state explicitly labeled and reachable?
- Are assumptions about the environment stated?
- Can you falsify the property with a short counterexample trace?

## References
- *Principles of Model Checking* — https://mitpress.mit.edu/9780262026499/
- *Specifying Systems* (Lamport) — https://lamport.azurewebsites.net/tla/book.html
