# LTL Basics and Trace Semantics

## What it is

Linear Temporal Logic (LTL) expresses properties over sequences of states using
temporal operators like "always" and "eventually".

## Why it matters

LTL is a standard way to specify and check temporal requirements for autonomous
systems and controllers.

## Core definitions

- **Atomic proposition (AP)**: Boolean label on a state.
- **X p**: p holds in the next state.
- **G p**: p holds globally (always).
- **F p**: p holds eventually.
- **p U q**: p holds until q holds.
- **Trace**: sequence of AP valuations over time.

## Worked micro-example

Trace over AP {safe}:

- Trace: [safe, safe, safe]
- Property: G safe
- Result: true (safe holds at every step)

## Common pitfalls

- Mixing up "eventually" with "always eventually".
- Forgetting that finite traces need a convention for X/G/F/U.
- Using LTL without defining AP labeling.

## Verification / debug checklist

- Are APs defined for every state in the model?
- Is the trace finite or infinite? Which semantics are you using?
- Can you produce a counterexample trace by hand?
- Are properties decomposed into smaller, checkable parts?

## References

- *Principles of Model Checking* — <https://mitpress.mit.edu/9780262026499/>
- *Linear Temporal Logic and Büchi Automata* (Vardi) — <https://dl.acm.org/doi/10.1145/70730.70733>
