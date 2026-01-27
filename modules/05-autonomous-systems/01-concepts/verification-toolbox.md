# Verification Toolbox

## What it is
A menu of lightweight verification approaches for autonomous-system models,
from simulation to bounded checking.

## Why it matters
Full model checking can be expensive; small, targeted checks can catch many
safety issues early and guide model refinement.

## Core definitions
- **Simulation**: execute the model with inputs to produce traces.
- **Invariant checking**: prove or test a condition holds on all reachable states.
- **Reachability**: search for a path to a target (or unsafe) state.
- **Bounded model checking (BMC)**: search up to depth k.

## Worked micro-example
For a TS with states A→B→C, check reachability of C:
- BFS finds path A, B, C, so C is reachable.
- If an invariant says "never C", it is violated by that path.

## Common pitfalls
- Treating simulation coverage as proof.
- Forgetting to bound inputs or disturbances.
- Using too small a depth in BMC and concluding safety.

## Verification / debug checklist
- Is the model deterministic? If not, how do you explore branches?
- What inputs/environment assumptions are fixed?
- Do you have a minimal counterexample trace?
- Are checks fast enough to run on every change?

## References
- *Principles of Model Checking* — https://mitpress.mit.edu/9780262026499/
- *Model Checking* (Clarke, Grumberg, Peled) — https://mitpress.mit.edu/9780262032704/
