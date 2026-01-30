# Timed Automata Basics

## What it is

A timed automaton (TA) is a transition system augmented with real-valued clocks
that evolve at rate 1, enabling timing constraints on transitions and states.

## Why it matters

Many autonomy failures are timing-related (timeouts, delays, watchdogs). TAs
capture these constraints without full continuous dynamics.

## Core definitions

- **Clock**: variable x ≥ 0 increasing at rate 1.
- **Guard**: condition like x ≥ c enabling a transition.
- **Reset**: set a clock to 0 on a transition.
- **Invariant**: constraint like x ≤ c that must hold in a location.

## Worked micro-example

Watchdog with timeout 3:

- Locations: Waiting, Alarm
- Clock x starts at 0
- Invariant in Waiting: x ≤ 3
- Transition to Alarm when x ≥ 3
If no reset occurs before 3s, the system must move to Alarm.

## Common pitfalls

- Combining guards and invariants that make a location unreachable.
- Forgetting that time must progress unless blocked by invariants.
- Using zero-time cycles that cause Zeno behavior.

## Verification / debug checklist

- Do invariants allow time to progress?
- Are guards reachable given resets?
- Is there a path that forces a timeout/violation?
- Can the model deadlock in a location?

## References

- *A Theory of Timed Automata* (Alur & Dill) — <https://doi.org/10.1016/0304-3975(94)90010-8>
- UPPAAL Tutorial — <https://uppaal.org/>
