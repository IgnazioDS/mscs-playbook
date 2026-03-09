# Unified Modeling Overview

## Key Ideas

- No single formalism is right for every autonomous-system problem; the choice is a three-way trade-off between expressiveness, decidability, and tool support.
- The module's formalisms form an abstraction lattice: transition systems forget time and continuous state, timed automata add dense clocks, and hybrid automata add mode-dependent continuous dynamics.
- Expressiveness usually increases faster than algorithmic tractability: finite transition systems admit exhaustive search, timed automata retain decidable reachability, and general hybrid automata do not.
- Sound abstraction depends on the property of interest: over-approximations are sound for proving safety, while under-approximations are sound only for finding bugs.
- Verification is a pipeline, not a button press. Errors can enter at the requirements, formalization, modeling, algorithm, or interpretation stage.

## Intuition

Autonomous systems sit at the boundary between software and physics. A robot,
vehicle, or medical device does not merely execute instructions once; it keeps
interacting with an environment while its internal state, clocks, and physical
variables evolve over time. That means there is no single mathematical model
that captures everything conveniently.

The practical question is therefore not "what is the most realistic model?" but
"what is the simplest model that preserves the property I care about?" If the
property is a pure sequencing rule such as "never open both valves at once," a
finite transition system may be enough. If the rule is time-bounded, such as
"send an acknowledgement within 100 ms," clocks must be modeled explicitly. If
the plant's velocity, temperature, or voltage matters, continuous dynamics enter
the picture and a control-theoretic or hybrid model becomes necessary.

This page is the map for the rest of the module. It tells you what each
formalism can represent, what it deliberately ignores, and what that buys you
algorithmically. The aim is not to memorize a taxonomy but to learn how to move
between levels of abstraction without invalidating the conclusion you want to
draw.

## 1. Formalism Lattices

### 1.1 System-model lattice

```text
Finite automata
      |
      v
Labelled transition systems / Kripke structures
      |
      v
Timed automata
      |
      v
Hybrid automata
      |
      v
General dynamical systems
```

Moving downward adds modeling power:

- Finite automata capture finite-state control flow.
- Transition systems add state labels and general transition structure.
- Timed automata add dense-time clocks.
- Hybrid automata add real-valued state with continuous evolution.
- General dynamical systems drop the finite-control restrictions entirely.

### 1.2 Logic lattice

```text
Propositional logic
      |
      v
LTL
     / \
    v   v
  CTL   (incomparable fragments)
     \ /
      v
    CTL*
      |
      v
  mu-calculus
```

The logic lattice matters because a model and a property language must match.
LTL is interpreted over single paths, while CTL and CTL* reason over branching
trees of paths. This module uses LTL as the default temporal logic and mentions
TCTL for timed-model queries in tools such as UPPAAL.

## 2. Comparison Table

| Formalism | State space | Time model | Decidable reachability? | Primary tool | Primary use |
|-----------|-------------|------------|--------------------------|--------------|-------------|
| Finite automaton | Finite discrete | None | Yes, linear in graph size | Lexer / parser generators | Parsing, simple protocols |
| Labelled transition system | Finite discrete | Implicit discrete steps | Yes, `O(|S| + |→|)` | SPIN, NuSMV | Software and controller logic |
| Timed automaton | `Loc x R^n` | Dense real time | Yes, PSPACE-complete | UPPAAL, KRONOS | Real-time protocols and schedulers |
| Initialised rectangular hybrid automaton | Finite modes x `R^n` | Dense real time | Yes | PHAVer | Restricted cyber-physical safety |
| Linear hybrid automaton | Finite modes x `R^n` | Dense real time | Undecidable in general | SpaceEx (approximate) | CPS reachability over-approximation |
| LTI system | `R^n` | Continuous or sampled | Stability decidable; arbitrary specs need more structure | MATLAB, Python control, JuliaControl | Control design and analysis |

The pattern is consistent: each row adds modeling detail, but only some rows
retain complete decision procedures. When a tool appears to "verify" an
undecidable class, read the guarantee carefully. It is usually computing an
over-approximation, a bounded result, or an incomplete search.

## 3. Abstraction and Refinement

An **abstraction** discards distinctions that are irrelevant to a property. A
continuous vehicle model may abstract to modes `{cruise, brake, stop}` if the
only question is whether stopping eventually occurs. A **refinement** adds
detail back in when the abstract model is too coarse to decide the property or
produces a spurious counterexample.

Formally, let `C` be a concrete transition system and `A` an abstract one. An
abstraction map `alpha : S_C -> S_A` groups concrete states into abstract
states. The abstraction is an **over-approximation** if every concrete
transition maps to an abstract transition, possibly along with extra abstract
transitions that do not correspond to any concrete behavior.

**Proposition (Safety preservation under over-approximation).**  
Let `C` be a concrete model and `A` an over-approximation of `C`. If every path
of `A` satisfies the safety property `G safe`, then every path of `C` satisfies
`G safe`.

*Proof sketch.* Safety properties are violated by finite bad prefixes. If `C`
violated `G safe`, there would be a concrete bad prefix. Because `A`
over-approximates `C`, the abstract image of that prefix would also be a path
of `A`, contradicting `A ⊨ G safe`. The argument fails for liveness because an
over-approximation can add unfair or non-progressing behaviors. Full proofs of
abstraction soundness appear in standard model-checking texts such as Baier and
Katoen.

The dual warning is important: an under-approximation may be useful for bug
hunting, but proving safety on an under-approximation proves almost nothing
about the original system.

## 4. Verification Pipeline

| Stage | Question | Typical artifact | Common failure mode |
|-------|----------|------------------|---------------------|
| Requirements | What must the system do or avoid? | Structured English requirement | Ambiguous or conflicting requirement |
| Formal specification | How is the requirement written mathematically? | `G safe`, `F goal`, TCTL query | Wrong logic or vacuous formula |
| Model construction | What state variables and dynamics are kept? | TS, TA, hybrid automaton, LTI model | Abstraction drops the critical behavior |
| Verification | What algorithm or tool is appropriate? | BFS, Büchi emptiness, zones, SMT | Using an incomplete or bounded method as if complete |
| Interpretation | What does the result actually prove? | Counterexample trace or proof obligation | Confusing model correctness with system correctness |

The pipeline is iterative. Counterexamples often reveal a requirement bug or a
modeling omission rather than a defect in the real system. Formal methods are
most effective when verification and model refinement are treated as a loop.

## 5. Worked Example: One System, Four Abstractions

Consider an obstacle-response controller for a mobile robot:

- The concrete plant tracks speed `v(t)` continuously.
- On obstacle detection, the controller must enter braking within `0.5 s`.
- Once braking starts, the robot must stop.

We can view the same behavior at four levels:

| Formalism | State description | What it keeps | What it omits |
|-----------|-------------------|---------------|---------------|
| LTI | `v(t)` with `dv/dt = -2v` in braking mode | Speed profile | Mode-switch logic |
| Hybrid automaton | `(mode, v)` with modes `cruise`, `brake`, `stop` | Continuous deceleration and switching | Low-level software states |
| Timed automaton | `(location, x)` where clock `x` measures time since obstacle | The `0.5 s` deadline | Continuous speed magnitude |
| Transition system | `{cruise, brake, stop}` | Ordering of modes | Real time and real-valued speed |

### 5.1 Concrete trace

Assume the obstacle is detected at `t = 0`, initial speed is `v(0) = 4 m/s`,
and the controller switches to `brake` at `t = 0.3 s`.

| Step | Time / mode | State | Transition | Conclusion |
|------|-------------|-------|------------|------------|
| 0 | `t = 0`, cruise | `v = 4` | obstacle detected | deadline clock starts |
| 1 | `t = 0.3`, brake | `v = 4` | discrete mode switch | deadline met (`0.3 <= 0.5`) |
| 2 | `t = 1.0`, brake | `v = 4e^{-2(0.7)} ≈ 0.99` | continuous evolution | slowing but not yet stopped |
| 3 | `t = 3.0`, stop abstraction | `v ≈ 0.018` | thresholded to `stop` | effectively stopped |

### 5.2 Property check

The timed requirement is "within `0.5 s` of obstacle detection, braking must
occur." A transition system cannot even state this because it has no metric
time. A timed automaton can express it with a clock guard; a hybrid automaton
can express both the deadline and the speed trajectory; an LTI model can
analyze the braking dynamics but not the discrete switching policy by itself.

The trace therefore demonstrates the central modeling lesson of the module:
choose the weakest formalism that still expresses the property of interest.

## 6. Common Mistakes

1. Treating higher expressiveness as automatically better. It often just makes
   the verification problem harder without adding information relevant to the
   requirement.
2. Using a time-free transition system for a deadline property, then claiming
   the deadline has been verified.
3. Proving safety on an under-approximate model and presenting the result as a
   system-level guarantee.
4. Ignoring the distinction between "tool says reachable" and "property fails
   in the physical system." The counterexample may exploit an abstraction
   artifact.
5. Moving between LTL and CTL notation as if they were interchangeable.

## 7. Practical Checklist

- [ ] Identify whether the system is purely discrete, real-time, continuous, or
      genuinely hybrid before choosing a model.
- [ ] State the property first; model choice should follow the property, not the
      other way around.
- [ ] Record which behaviors the abstraction deliberately omits and why they are
      irrelevant to the current property.
- [ ] Use over-approximations for safety proofs and be explicit when a result is
      bounded or approximate.
- [ ] Validate the model against at least one known-correct and one
      known-incorrect trace before trusting tool output.
- [ ] Check whether the logic used by the tool matches the logic of the
      requirement.

## 8. References

- Alur, Rajeev, and David L. Dill. 1994. A Theory of Timed Automata.
  *Theoretical Computer Science* 126 (2): 183-235.
  <https://doi.org/10.1016/0304-3975(94)90010-8>
- Baier, Christel, and Joost-Pieter Katoen. 2008. *Principles of Model
  Checking*. MIT Press.
  <https://mitpress.mit.edu/9780262026499/principles-of-model-checking/>
- Clarke, Edmund M., E. Allen Emerson, and A. Prasad Sistla. 1986. Automatic
  Verification of Finite-State Concurrent Systems Using Temporal Logic
  Specifications. *ACM TOPLAS* 8 (2): 244-263.
  <https://doi.org/10.1145/5397.5399>
- Henzinger, Thomas A., Peter W. Kopke, Anuj Puri, and Pravin Varaiya. 1995.
  What's Decidable about Hybrid Automata? *STOC 1995*.
  <https://doi.org/10.1145/225058.225162>
- Lee, Edward A., and Sanjit A. Seshia. 2017. *Introduction to Embedded
  Systems*. 2nd ed.
  <https://ptolemy.berkeley.edu/books/leeseshia/>
- Pnueli, Amir. 1977. The Temporal Logic of Programs. *FOCS 1977*: 46-57.
  <https://doi.org/10.1109/SFCS.1977.32>
