# Sequential Circuits and Transition Systems

## Key Ideas

- A labelled transition system (LTS) is the foundational discrete model for the
  module: it captures possible behaviors as paths but intentionally omits
  metric time, probability, and real-valued dynamics.
- Kripke structures are the state-labelled variant used most often in model
  checking; LTL is interpreted over their infinite paths.
- Reachability in a finite transition system is algorithmically simple:
  breadth-first or depth-first search runs in `O(|S| + |→|)`.
- Non-determinism is not probability. It models multiple possible successors,
  often due to concurrency or underspecification.
- A synchronous sequential circuit with `n` bits of memory induces a finite
  transition system with at most `2^n` states, which is why state explosion
  appears so quickly in hardware-style models.

## Intuition

A transition system is the simplest serious model of computation for reactive
systems. Instead of asking what output a program produces and then halting, it
asks what states a system can move through forever. That matches how controllers,
protocols, schedulers, and digital circuits actually behave: they do not return
one answer and stop, they continue interacting with inputs.

The model is deliberately austere. A state records whatever information is
needed to predict the next step. A transition says the system may move from one
state to another, optionally with an action label that explains why. There is
no stopwatch, no differential equation, and no probability distribution. Those
omissions are not defects. They are what make exhaustive graph search possible.

Sequential circuits fit naturally into this view. At each clock tick, the
combinational logic computes the next values of the flip-flops from the current
values and inputs. If you treat the vector of stored bits as the state, the
circuit becomes a finite transition system. Model checking then reduces to
graph exploration over those states.

## 1. Formal Definitions

**Definition (Labelled Transition System).**  
A labelled transition system is a tuple `TS = (S, Act, →, I, AP, L)` where:

- `S` is a finite or countable set of states;
- `Act` is a set of actions;
- `→ ⊆ S × Act × S` is the transition relation;
- `I ⊆ S` is the set of initial states;
- `AP` is a set of atomic propositions;
- `L : S -> 2^AP` is the state-labelling function.

Informal gloss:

- `S` says what configurations the system can be in.
- `Act` names the externally visible or modeling-relevant steps.
- `→` describes which next states are possible.
- `I` tells us where executions may start.
- `AP` provides the vocabulary used in temporal formulas.
- `L` tells us which propositions hold in each state.

Constraints not captured by the type:

- Usually `I != ∅`; otherwise the model has no executions.
- For reactive systems, deadlock states are often undesirable even though the
  definition permits them.

Minimal reusable example:

- `S = {red_NS, green_NS, yellow_NS, green_EW, yellow_EW}`
- `Act = {tick}`
- `I = {red_NS}`
- `AP = {green_NS, yellow_NS, green_EW, yellow_EW}`
- `L(red_NS) = ∅`, `L(green_NS) = {green_NS}`, and so on.

**Definition (Kripke Structure).**  
A Kripke structure is a tuple `K = (S, I, R, AP, L)` where:

- `S` is a set of states;
- `I ⊆ S` is the set of initial states;
- `R ⊆ S × S` is the transition relation;
- `AP` is a set of atomic propositions;
- `L : S -> 2^AP` is the state-labelling function.

Informal gloss:

- A Kripke structure drops explicit action labels.
- It is the standard input model for LTL and CTL model checking.

Constraint note:

- Many textbooks require `R` to be total so that every path can be extended to
  an infinite path. If a model contains deadlocks, one common repair is to add a
  self-loop at each deadlock state before interpreting LTL.

## 2. Paths, Traces, Reachability, and Deadlock

A **path** in `TS` is a sequence `π = s_0, s_1, s_2, ...` such that for every
`i >= 0` there exists an action `a_i` with `s_i --a_i--> s_{i+1}`. A path is
**finite** if it ends in a state with no chosen successor and **infinite**
otherwise. The notation `π[i]` denotes the `i`th state, and `π^i` the suffix
starting at position `i`.

A state `t` is **reachable** if there exists a finite path from some `s_0 ∈ I`
to `t`. The set of reachable states is:

`Reach(TS) = { t ∈ S | exists s_0 ∈ I and path s_0 ->* t }`.

A state `s` is a **deadlock** if it has no outgoing transition:

`deadlock(s) iff not exists a ∈ Act, s' ∈ S : s --a--> s'`.

Deadlock matters because a reactive controller that deadlocks has stopped
responding to its environment, even if no explicit safety property has yet been
violated.

**Theorem (Graph search decides reachability).**  
For a finite transition system `TS = (S, Act, →, I, AP, L)`, reachability of a
target set `T ⊆ S` is decidable by BFS or DFS in time `O(|S| + |→|)`.

*Proof sketch.* Treat the transition system as a directed graph whose vertices
are states and whose edges are the pairs `(s, s')` for which some action yields
`s --a--> s'`. BFS and DFS each visit every reachable vertex at most once and
inspect every outgoing edge at most once, hence the linear bound. Soundness is
immediate because any discovered target state lies on a concrete path from an
initial state; completeness follows because every reachable state is eventually
explored. Full proof details appear in standard graph algorithm texts and in
Baier and Katoen's model-checking treatment.

## 3. Determinism and Non-Determinism

An LTS is **deterministic** if, for every state `s` and action `a`, there is at
most one successor `s'` such that `s --a--> s'`. It is **non-deterministic**
when multiple successors are possible.

Non-determinism is useful for two distinct reasons:

- **Concurrency.** Different schedulings of concurrent components induce
  different successors.
- **Underspecification.** The model leaves implementation choices open.

The same mathematics covers both cases, but the interpretation differs. In a
correctness proof, a non-deterministic environment is usually adversarial: the
property must hold for every possible successor, not just a likely one.

## 4. Sequential Circuits as Transition Systems

A synchronous sequential circuit has:

- a vector `q ∈ {0,1}^n` of stored bits;
- an input vector `u ∈ {0,1}^m`;
- a next-state function `f : {0,1}^n × {0,1}^m -> {0,1}^n`;
- an output function `g`.

At each clock tick, the circuit updates `q` to `f(q, u)`. This induces an LTS:

- states are the bit vectors `q`;
- actions can be the input valuations `u`;
- transitions are `q --u--> f(q, u)`;
- initial states are reset configurations.

If the circuit has `n` state bits, then the induced state space has at most
`2^n` states. This simple counting fact explains why even small synchronous
controllers can become difficult to explore exhaustively.

## 5. Worked Example: Traffic-Light Controller

We model a four-phase traffic light that alternates between north-south and
east-west traffic. The safety requirement is that both directions are never
green simultaneously.

**Definition (Traffic-light transition system).**  
Let

`TS_TL = (S, Act, →, I, AP, L)`

where:

- `S = {NS_G, NS_Y, ALL_R_1, EW_G, EW_Y, ALL_R_2}`;
- `Act = {tick}`;
- `I = {ALL_R_1}`;
- `AP = {green_NS, yellow_NS, green_EW, yellow_EW}`;
- `L(ALL_R_1) = ∅`, `L(NS_G) = {green_NS}`, `L(NS_Y) = {yellow_NS}`,
  `L(EW_G) = {green_EW}`, `L(EW_Y) = {yellow_EW}`, `L(ALL_R_2) = ∅`;
- `→` contains exactly the transitions:
  `ALL_R_1 --tick--> NS_G`,
  `NS_G --tick--> NS_Y`,
  `NS_Y --tick--> ALL_R_2`,
  `ALL_R_2 --tick--> EW_G`,
  `EW_G --tick--> EW_Y`,
  `EW_Y --tick--> ALL_R_1`.

All six states are reachable from the initial state, because the controller is a
single directed cycle.

### 5.1 Executable trace

| Step | State | Enabled actions | Action taken | Next state |
|------|-------|-----------------|--------------|------------|
| 0 | `ALL_R_1` | `{tick}` | `tick` | `NS_G` |
| 1 | `NS_G` | `{tick}` | `tick` | `NS_Y` |
| 2 | `NS_Y` | `{tick}` | `tick` | `ALL_R_2` |
| 3 | `ALL_R_2` | `{tick}` | `tick` | `EW_G` |
| 4 | `EW_G` | `{tick}` | `tick` | `EW_Y` |
| 5 | `EW_Y` | `{tick}` | `tick` | `ALL_R_1` |

### 5.2 Property check

The safety property is:

`TS_TL ⊨ G ¬(green_NS ∧ green_EW)`.

Inspection of the labelling function shows that no state carries both
`green_NS` and `green_EW`. Because every reachable state is one of the six
listed above, the bad condition is unreachable. Equivalently, if we define
`bad = green_NS ∧ green_EW`, then `Reach(TS_TL)` contains no state labelled
with `bad`.

The example also illustrates deadlock freedom: every state has exactly one
outgoing transition, so every maximal path is infinite.

## 6. Connection to Other Formalisms

- LTL formulas are interpreted over the infinite paths of Kripke structures; see
  [04-ltl-basics-trace-semantics.md](04-ltl-basics-trace-semantics.md).
- Timed automata extend transition systems with real-valued clocks and delay
  transitions; see [07-timed-automata-basics.md](07-timed-automata-basics.md).
- A sequential circuit is often the finite-state controller inside a larger
  hybrid or continuous plant model.

## 7. Common Mistakes

1. Omitting state variables that are needed to predict the future, which makes
   the model non-Markovian.
2. Treating a deadlock as harmless because "the bad state was never reached."
   A reactive controller that stops responding is usually itself a fault.
3. Reading non-determinism as probability. A possible bad branch is enough to
   falsify universal correctness.
4. Forgetting to totalize a Kripke structure before interpreting LTL on it.
5. Using reachability on the full syntactic state space rather than the
   reachable subgraph.

## 8. Practical Checklist

- [ ] Write the full tuple `TS = (S, Act, →, I, AP, L)` before stating any
      property.
- [ ] Confirm that each atomic proposition in the property appears in `AP` and
      is labelled by `L`.
- [ ] Enumerate or algorithmically compute the reachable states, not just the
      syntactic state set.
- [ ] Check explicitly for deadlocks.
- [ ] Decide whether non-determinism represents concurrency or
      underspecification.
- [ ] If the model comes from a circuit, ensure the reset behavior is included
      in `I`.

## 9. References

- Baier, Christel, and Joost-Pieter Katoen. 2008. *Principles of Model
  Checking*. MIT Press.
  <https://mitpress.mit.edu/9780262026499/principles-of-model-checking/>
- Clarke, Edmund M., Orna Grumberg, and Doron Peled. 1999. *Model Checking*.
  MIT Press.
  <https://mitpress.mit.edu/9780262032704/model-checking/>
- Huth, Michael, and Mark Ryan. 2004. *Logic in Computer Science*. 2nd ed.
  Cambridge University Press.
- Holzmann, Gerard J. 2003. *The SPIN Model Checker*. Addison-Wesley.
  <https://spinroot.com/spin/Doc/Book_extras/>
- Lee, Edward A., and Sanjit A. Seshia. 2017. *Introduction to Embedded
  Systems*. 2nd ed.
  <https://ptolemy.berkeley.edu/books/leeseshia/>
- Wakerly, John F. 2005. *Digital Design: Principles and Practices*. 4th ed.
  Pearson.
