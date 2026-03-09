# Verification Toolbox

## Key Ideas

- Tool choice follows model class and property class. The wrong tool can produce
  a formally correct answer to the wrong question.
- Explicit-state model checkers, symbolic model checkers, timed model checkers,
  hybrid verifiers, SMT solvers, theorem provers, and synthesizers each occupy
  different points in the expressiveness-versus-automation trade-off.
- Counterexamples are not just debugging artifacts; they are mathematical
  witnesses. Learning to read them is a core verification skill.
- Bounded methods are excellent for bug finding, but a clean bounded run is not
  a proof unless the bound is known to cover the reachable state space.
- For hybrid and continuous systems, many tools are approximate or bounded. The
  soundness direction of the approximation must be stated explicitly.

## Intuition

Formal methods is not one algorithm. In practice, a verification engineer moves
among several tool families depending on the model and the property. A finite
concurrent protocol might belong in SPIN. A real-time scheduler belongs in
UPPAAL. A hybrid aircraft model may require SpaceEx or Flow*. A nonlinear proof
obligation might need an SMT solver or an interactive theorem prover.

The key practical question is not "which tool is strongest?" but "what exactly
does this tool prove?" Some tools are complete decision procedures for a
well-defined class of models. Others are incomplete but scalable bug finders.
Others still compute sound over-approximations that are good for safety but not
for liveness. If you do not understand that boundary, it is easy to overclaim.

This page is a field guide. It does not teach every tool in full detail; it
explains when each category is appropriate, how its output should be read, and
what common interpretation mistakes to avoid.

## 1. Tool Categories

| Category | Representative tools | Primary algorithm | Handles |
|----------|----------------------|-------------------|---------|
| Explicit-state model checker | SPIN, NuSMV | BFS/DFS plus Büchi emptiness | Finite transition systems, LTL/CTL |
| Symbolic model checker | NuSMV, nuXmv | BDD, SAT, IC3/PDR | Larger finite systems |
| Timed model checker | UPPAAL, KRONOS | Zones / DBMs | Timed automata, TCTL-like queries |
| Hybrid-system verifier | SpaceEx, Flow* | Set-based reachability / flowpipes | Linear and nonlinear hybrid safety |
| SMT-based verifier | Z3, dReal | SMT over arithmetic theories | Encoded transition systems, proof obligations |
| Theorem prover | Coq, Isabelle/HOL | Interactive proof | Infinite-state and rich mathematics |
| Reactive synthesizer | TuLiP, Slugs, STRIX | Game solving / GR(1) / LTL synthesis | Controller construction |

## 2. Decision Guide

Use the following decision tree.

1. Is the state space finite and discrete?
   Then start with SPIN, NuSMV, or nuXmv.
2. Does the model have explicit deadlines or durations?
   Then use UPPAAL or another timed-automata tool.
3. Does the model combine discrete modes with continuous dynamics?
   Then use SpaceEx, Flow*, or another hybrid reachability tool, and state
   whether the result is approximate or bounded.
4. Is the model infinite-state or the property richer than the model checker can
   express?
   Then encode the obligation in SMT or move to a theorem prover.
5. Do you need a controller rather than a yes/no verdict?
   Then use a synthesis tool such as TuLiP, Slugs, or STRIX.

## 3. Representative Tools

### 3.1 SPIN

SPIN takes Promela models of concurrent systems and supports LTL checking via
`never` claims. Its main strengths are:

- explicit-state exploration;
- strong support for concurrency;
- partial-order reduction to tame interleavings;
- concrete counterexample traces.

Interpretation tip:

- a SPIN counterexample is a concrete execution sequence through the Promela
  model;
- if the property was added as a `never` claim, the trace shows a path accepted
  by that claim.

### 3.2 UPPAAL

UPPAAL models networks of timed automata with clocks, channels, and finite
integers. Common query forms are:

- `A[] p`
- `E<> p`
- `A<> p`
- `E[] p`
- `p --> q`

Diagnostic traces are symbolic timed traces. They identify locations,
synchronizations, and representative clock valuations.

### 3.3 SpaceEx

SpaceEx targets hybrid systems, especially linear dynamics. It computes
flowpipes: set over-approximations of reachable states over bounded time
horizons.

Interpretation warning:

- "no violation found up to time `T`" means bounded safety only;
- the result is sound for safety because the reachable set is over-approximated,
  but it is not a proof of unbounded correctness.

### 3.4 Z3 and SMT Solvers

SMT solvers are useful when the model or property is easier to encode as logic
than to model in a dedicated checker.

Key distinction:

- `sat` means there exists an assignment satisfying the encoding;
- `unsat` means no such assignment exists under the encoding;
- validity is usually checked by negation: `φ` is valid iff `¬φ` is unsat.

Unsat cores can help isolate which assumptions are jointly inconsistent.

### 3.5 Theorem Provers

Coq and Isabelle/HOL trade automation for expressiveness. They are appropriate
when:

- the state space is infinite;
- the proof involves arbitrary induction or rich mathematics;
- the desired claim goes beyond the logic supported by model checkers.

### 3.6 Reactive Synthesizers

TuLiP, Slugs, and STRIX solve controller-construction problems from logical
specifications. Their output is usually a strategy, automaton, or controller
implementation template rather than a simple verdict.

## 4. Counterexample Interpretation

A counterexample trace answers two questions:

1. What path falsifies the property in the model?
2. Does that path represent a real system risk or only a modeling artifact?

Diagnostic workflow:

- reproduce the trace by hand on the model;
- check whether the property or fairness assumption was written correctly;
- determine whether the trace uses unrealistic environment powers;
- if not, treat it as a real design defect.

Counterexamples are often shortest-path witnesses. That makes them useful for
debugging because they isolate the minimal prefix that leads to failure.

## 5. Bounded Model Checking

Bounded model checking (BMC) unrolls the transition relation to depth `k` and
asks a SAT or SMT solver whether a counterexample of length at most `k` exists.

**Theorem (BMC soundness and limitation).**  
If the BMC encoding of depth `k` is satisfiable, then there exists a concrete
counterexample of length at most `k`. If the encoding is unsatisfiable, then the
system has no counterexample of length at most `k`; this does not imply the
property holds unboundedly unless `k` exceeds the system diameter or another
completeness threshold.

Plain-English reading: BMC is a bug finder by default, not a proof method by
default.

*Proof sketch.* The encoding is constructed so that each satisfying assignment
corresponds to a concrete path of length `k` whose last state violates the
property or completes a lasso violating the temporal formula. Thus satisfiability
gives a real counterexample. Unsatisfiability only rules out such paths within
the chosen depth; longer bad paths may still exist. Completeness requires a
separate argument about the reachable-state diameter or loop structure.

## 6. Practical Tool Selection Matrix

| Situation | Preferred tool family | Reason |
|-----------|-----------------------|--------|
| Finite controller, safety invariant | SPIN / nuXmv | Exhaustive finite-state search |
| Finite controller, LTL liveness | SPIN / nuXmv | Büchi emptiness on product graph |
| Real-time watchdog or deadline property | UPPAAL | Native clocks and timed queries |
| Linear hybrid safety over bounded horizon | SpaceEx | Flowpipe over-approximation |
| Nonlinear arithmetic proof obligation | Z3 or dReal | SMT over reals |
| Proof over an infinite-state semantics | Coq / Isabelle | Rich logic and induction |
| Need controller automatically | TuLiP / Slugs / STRIX | Strategy synthesis |

## 7. Common Mistakes

1. Running a bounded checker and reporting "verified" instead of "no bug found
   up to bound `k`."
2. Using a timed model checker for dynamics that really require a hybrid model.
3. Ignoring whether a hybrid verification result is an over- or
   under-approximation.
4. Reading `unsat` as "the system is correct" without checking that the logical
   encoding captured the intended property.
5. Treating a counterexample as an implementation bug before checking whether it
   is an abstraction artifact.

## 8. Practical Checklist

- [ ] Match the tool to the model class before writing the input file.
- [ ] Match the property class to the algorithm: reachability, invariance,
      liveness, timed property, or synthesis.
- [ ] Check whether the tool result is exact, bounded, over-approximate, or
      under-approximate.
- [ ] Read at least one diagnostic trace manually.
- [ ] Record the fairness assumptions and bounds used in the run.
- [ ] Distinguish "counterexample found," "no counterexample up to bound,"
      "property proved," and "property proved on the model abstraction."

## 9. References

- Baier, Christel, and Joost-Pieter Katoen. 2008. *Principles of Model
  Checking*. MIT Press.
  <https://mitpress.mit.edu/9780262026499/principles-of-model-checking/>
- Biere, Armin, Alessandro Cimatti, Edmund Clarke, and Yunshan Zhu. 1999.
  Symbolic Model Checking without BDDs. *TACAS 1999*.
  <https://doi.org/10.1007/3-540-49059-0_14>
- Frehse, Goran, et al. 2011. SpaceEx: Scalable Verification of Hybrid Systems.
  *CAV 2011*.
  <https://doi.org/10.1007/978-3-642-22110-1_30>
- Holzmann, Gerard J. 2003. *The SPIN Model Checker*. Addison-Wesley.
  <https://spinroot.com/spin/Doc/Book_extras/>
- Larsen, Kim G., Paul Pettersson, and Wang Yi. 1997. UPPAAL in a Nutshell.
  *STTT* 1: 134-152.
  <https://doi.org/10.1007/s100090050010>
- Moura, Leonardo de, and Nikolaj Bjørner. 2008. Z3: An Efficient SMT Solver.
  *TACAS 2008*.
  <https://doi.org/10.1007/978-3-540-78800-3_24>
