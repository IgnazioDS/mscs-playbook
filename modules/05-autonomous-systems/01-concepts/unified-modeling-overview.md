# Unified Modeling Overview

## What it is

A compact view of how common autonomous-system models relate: continuous dynamics,
discrete transitions, timing constraints, and hybrid combinations.

## Why it matters

Choosing the right model class determines what properties you can verify and what
assumptions your results rely on.

## Core definitions

- **State**: minimal variables describing the system at an instant.
- **Dynamics**: how state evolves (continuous, discrete, or both).
- **Transition system (TS)**: discrete states with labeled edges.
- **LTI system**: linear dynamics, continuous or discrete time.
- **Timed automaton (TA)**: TS with real-valued clocks and timing guards.
- **Hybrid system**: mixed continuous flows and discrete jumps.

## Worked micro-example

A robot alternates between "move" and "stop".

- TS: states {Move, Stop}, edges Move→Stop, Stop→Move.
- Add a clock x with invariant in Move: x ≤ 5 (must stop within 5s).
- The same behavior can be approximated by a discrete LTI position update
  x_{k+1} = x_k + v·dt with mode-dependent velocity.

## Common pitfalls

- Modeling continuous dynamics with too-large time steps.
- Ignoring timing constraints by collapsing to a plain TS.
- Mixing units or forgetting to reset clocks on mode switches.

## Verification / debug checklist

- Are the state variables sufficient to explain future behavior?
- Do you need time explicitly, or are discrete steps enough?
- Are invariants and guards consistent (not contradictory)?
- Do discretization steps preserve safety-relevant behavior?

## References

- *Principles of Model Checking* — <https://mitpress.mit.edu/9780262026499/>
- *Hybrid Systems: Computation and Control* — <https://link.springer.com/conference/hscc>
