# Hybrid Systems Intuition

## What it is
Hybrid systems combine continuous dynamics (flows) with discrete transitions
(jumps) between modes.

## Why it matters
Robots, vehicles, and safety controllers often switch between modes such as
cruise, brake, or emergency stop with different dynamics.

## Core definitions
- **Mode**: discrete state with its own continuous dynamics.
- **Flow**: continuous evolution within a mode (e.g., ẋ = f(x)).
- **Jump**: discrete transition, possibly resetting variables.
- **Guard**: condition that enables a jump.

## Worked micro-example
A simple thermostat:
- Mode Heat: temperature increases by +0.5 per minute
- Mode Cool: temperature decreases by -0.2 per minute
- Switch to Cool when T ≥ 22, to Heat when T ≤ 20
This is a two-mode hybrid system with threshold guards.

## Common pitfalls
- Ignoring mode-dependent constraints (e.g., maximum braking).
- Discretizing continuous dynamics too coarsely.
- Missing reset behavior on mode switches.

## Verification / debug checklist
- Are mode guards mutually consistent (no gaps or overlaps)?
- Do flows respect invariants in each mode?
- Do resets preserve safety constraints?
- Is the model robust to small perturbations?

## References
- *Hybrid Systems: Computation and Control* — https://link.springer.com/conference/hscc
- *Hybrid Dynamical Systems* (Goebel, Sanfelice, Teel) — https://hybrid.soe.ucsc.edu/book
