# Autonomous Systems Cheat Sheet

## Model types and when to use them
- **Discrete TS**: finite controller logic, protocols, and mode switching.
- **LTI (continuous)**: linearized physics and control design.
- **LTI (discrete)**: sampled dynamics, digital control, simulation checks.
- **Timed automata**: timing constraints, watchdogs, schedulers.
- **Hybrid systems**: mode-dependent dynamics (brake/accelerate, heat/cool).

## LTL operators and meanings
- **X p**: p holds in the next step.
- **G p**: p holds always.
- **F p**: p holds eventually.
- **p U q**: p holds until q holds.
- **!p, p && q, p || q**: negation, and, or.

## Common spec patterns
- **Always avoid**: G !bad
- **Eventually reach**: F goal
- **Respond**: G (request -> F grant)
- **Until**: safe U goal

## Verification options
- **Simulation**: execute with scenarios, check invariants on traces.
- **Invariant checking**: prove/test that a condition holds for all reachable states.
- **Bounded checking**: search counterexamples up to depth k.
- **Reachability search**: BFS/DFS to unsafe/goal states.

## Debugging checklist
- Are AP labels defined for every state?
- Are time steps small enough for timing constraints?
- Do tests include edge cases near guards/invariants?
- Do counterexamples map back to model assumptions?
