# Sequential Circuits and Transition Systems

## What it is
Sequential circuits are discrete systems with memory. They can be modeled as
transition systems (TS) where each state captures latch/flip-flop values.

## Why it matters
Hardware controllers and many embedded safety logics are naturally discrete and
are verified using TS-based methods.

## Core definitions
- **State**: vector of flip-flop values.
- **Input**: external Boolean signals at each clock tick.
- **Transition function**: next_state = f(state, input).
- **Output function**: output = g(state, input) (Mealy) or g(state) (Moore).

## Worked micro-example
A 1-bit toggle flip-flop:
- State s ∈ {0,1}
- Input t ∈ {0,1}
- Next state: if t=1 then s' = 1-s else s' = s
This is a TS with two states and edges labeled by t.

## Common pitfalls
- Forgetting to include all relevant latches in the state.
- Assuming combinational logic is instantaneous across ticks.
- Omitting reset behavior in the initial state.

## Verification / debug checklist
- Can you enumerate all states for a small instance?
- Are transition labels deterministic for each input?
- Do properties hold under all input sequences?
- Is the reset state modeled explicitly?

## References
- *Logic in Computer Science* (Huth & Ryan) — https://www.cs.bham.ac.uk/~mdr/LICS/
- *Principles of Model Checking* — https://mitpress.mit.edu/9780262026499/
