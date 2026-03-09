# Requirements: Safety, Liveness, Reachability

## Key Ideas

- Requirement class determines verification method: safety reduces to bad-state
  reachability, while liveness requires reasoning about infinite behaviors and
  accepting cycles.
- Reachability, invariance, persistence, and response are related but not
  interchangeable. A system can reach a goal once without guaranteeing eventual
  service on all paths.
- Every `omega`-regular property can be decomposed into a safety part and a
  liveness part; this is a structural theorem, not a slogan.
- Fairness assumptions are sometimes necessary for liveness proofs, but adding
  them changes the claim being made about the system.
- Many real requirements fail not because the logic is too weak, but because
  the English statement was underspecified or vacuous.

## Intuition

When engineers say "the system is correct," they usually mean several different
things at once. Some requirements say that something bad must never happen: two
trains must never occupy the same block, both lanes must never show green, the
pacemaker must never pace faster than its safety limit. Other requirements say
that something good must eventually happen: a request is eventually served, the
elevator eventually reaches the requested floor, the robot eventually docks.

Those are not the same kind of claim. A safety violation has a finite witness:
once the bad thing happens, the requirement is already broken. A liveness
violation has no finite witness, because any finite execution prefix can still
be extended by doing the right thing later. That difference is why model
checkers use different algorithms for the two cases.

Formal specification patterns help translate English requirements into LTL
without reinventing the logic every time. They do not remove the need for
judgment, but they do prevent many common mistakes, especially in recurring
structures such as response, absence, and precedence.

## 1. Formal Definitions

A property `P ⊆ (2^AP)^ω` is a set of infinite traces.

**Definition (Safety property).**  
A property `P` is a safety property iff every violating trace has a finite bad
prefix:

for every `σ ∉ P`, there exists a finite prefix `u` of `σ` such that every
infinite extension of `u` is also outside `P`.

Gloss: once a safety property is violated, the violation can be detected after a
finite amount of behavior.

**Definition (Liveness property).**  
A property `P` is a liveness property iff every finite trace prefix can be
extended to some infinite trace in `P`.

Gloss: no finite observation is enough to refute liveness.

**Definition (Reachability and invariance).**  
For a transition system `TS` and state predicates `goal` and `safe`:

- reachability is expressed by `F goal`;
- invariance is expressed by `G safe`.

Their duality is immediate:

`TS ⊨ G ¬bad` iff no reachable state satisfies `bad`.

## 2. Safety, Liveness, and the Alpern-Schneider Decomposition

Let `cl(P)` denote the topological closure of `P` in the prefix topology over
infinite traces.

**Theorem (Alpern-Schneider decomposition).**  
Every `omega`-regular property `P` can be written as

`P = S ∩ L`

where `S` is a safety property and `L` is a liveness property.

Plain-English reading: every temporal requirement has a "nothing bad ever
happens" part and a "something good eventually happens" part.

*Proof sketch.* Take `S = cl(P)`, the closure of `P`. This is a safety property
because closure exactly captures the idea that violating traces expose a finite
bad prefix. Then define `L = P ∪ complement(cl(P))`. This `L` is liveness
because any finite prefix can be extended either into `P` or into a trace that
escapes the closure of `P`; intuitively, liveness is the dense component left
after safety has captured all finitely refutable behavior. By construction,
`P = cl(P) ∩ (P ∪ complement(cl(P))) = S ∩ L`. Full proof in Alpern and
Schneider 1985.

## 3. Verification Consequences

For safety, verification reduces to bad-state reachability:

- define `bad` as the undesirable predicate;
- search for a reachable state satisfying `bad`;
- if one exists, the path to it is a counterexample.

For liveness, reachability is not enough. A liveness counterexample is an
infinite path that fails to make progress, which is why Büchi acceptance or
fair-cycle detection is needed.

Canonical LTL forms:

- safety: `G ¬bad`
- reachability: `F goal`
- recurrence / liveness: `G F p`
- persistence: `F G p`
- response: `G (p -> F q)`

## 4. Fairness

Fairness constrains which infinite paths count as admissible behaviors.

- **Weak fairness (justice):** if an action is continuously enabled from some
  point onward, it must eventually occur.
- **Strong fairness (compassion):** if an action is enabled infinitely often, it
  must eventually occur.

Fairness matters because many liveness claims are false in the raw transition
system but true under an assumption that the scheduler or environment will not
starve a continuously enabled component forever.

You should state fairness explicitly. Adding fairness changes the theorem from
"the system guarantees liveness" to "the system guarantees liveness under the
fairness assumption."

## 5. Specification Patterns Catalogue

The table below uses:

- `p` as the main triggering proposition;
- `s` as the response or constrained proposition;
- `t` as the second response in the chain-response pattern;
- `q` and `r` as scope delimiters.

Here "before `r`" means before the first occurrence of `r`; "after `q`" means
from each occurrence of `q` onward; "between `q` and `r`" means on every
segment that starts with `q` and ends with the next `r`.

| Pattern | Globally | Before `r` | After `q` | Between `q` and `r` |
|---------|----------|------------|-----------|----------------------|
| Universality of `p` | `G p` | `F r -> (p U r)` | `G(q -> G p)` | `G((q ∧ ¬r ∧ F r) -> (p U r))` |
| Absence of `p` | `G ¬p` | `F r -> (¬p U r)` | `G(q -> G ¬p)` | `G((q ∧ ¬r ∧ F r) -> (¬p U r))` |
| Existence of `p` | `F p` | `¬r U (p ∧ ¬r)` | `G(q -> F p)` | `G((q ∧ ¬r ∧ F r) -> F(p ∧ ¬r))` |
| Response `p` leads to `s` | `G(p -> F s)` | `G((p ∧ ¬r) -> (¬r U s))` | `G(q -> G(p -> F s))` | `G((q ∧ ¬r ∧ F r) -> G((p ∧ ¬r) -> (¬r U s)))` |
| Precedence `p` before `s` | `¬s W p` | `F r -> ((¬s ∧ ¬r) W (p ∨ r))` | `G(q -> (¬s W p))` | `G((q ∧ ¬r ∧ F r) -> ((¬s ∧ ¬r) W (p ∨ r)))` |
| Chain response `p` leads to `s` then `t` | `G(p -> F(s ∧ F t))` | `G((p ∧ ¬r) -> (¬r U (s ∧ F t)))` | `G(q -> G(p -> F(s ∧ F t)))` | `G((q ∧ ¬r ∧ F r) -> G((p ∧ ¬r) -> F(s ∧ F t)))` |

These formulas are not the only encodings, but they make the scope explicit and
are suitable for turning structured English requirements into LTL.

## 6. Worked Example: Elevator Controller

Assume an elevator model with atomic propositions:

- `door_open`
- `moving`
- `at_f1`, `at_f2`, `at_f3`
- `call_f2`
- `overload`
- `service_done`

### 6.1 Requirements table

| ID | English requirement | LTL formula | Class | Fairness needed? |
|----|---------------------|-------------|-------|------------------|
| R1 | The elevator must never move while the door is open. | `G ¬(moving ∧ door_open)` | Safety | No |
| R2 | Every call to floor 2 is eventually served. | `G(call_f2 -> F at_f2)` | Liveness / response | Yes, if scheduler may starve the request forever |
| R3 | The elevator can eventually reach floor 3 from startup. | `F at_f3` | Reachability | No |
| R4 | Once overload is detected, the elevator does not move until overload clears. | `G(overload -> (¬moving W ¬overload))` | Safety | No |
| R5 | After service completes, the system eventually returns to floor 1. | `G(service_done -> F at_f1)` | Liveness | Usually yes, if the environment can keep injecting higher-priority calls forever |

### 6.2 Executable trace fragment

| Step | State labels | Interpretation |
|------|--------------|----------------|
| 0 | `{at_f1, door_open}` | idle at floor 1 |
| 1 | `{at_f1, call_f2}` | request issued |
| 2 | `{moving}` | doors closed, elevator moving |
| 3 | `{at_f2, door_open}` | request served |

Property check:

- `R1` holds on the trace because there is no step with `moving ∧ door_open`.
- `R2` holds on the trace because the `call_f2` at step 1 is followed by
  `at_f2` at step 3.

The trace is not a proof of the system-wide property, but it validates that the
formalization matches the intended English meaning on one concrete execution.

## 7. Common Mistakes

1. Calling `F goal` a liveness proof when only one path to `goal` has been
   shown. Reachability is existential; liveness is universal over paths.
2. Forgetting that safety violations have finite bad prefixes and therefore can
   be checked by reachability.
3. Adding fairness assumptions silently, thereby strengthening the model until
   the property becomes true.
4. Writing implication-heavy formulas whose antecedent never holds.
5. Confusing `G F p` with `F G p`.

## 8. Practical Checklist

- [ ] Classify each requirement as safety, liveness, reachability, or a
      combination before selecting a verification algorithm.
- [ ] Define the bad states and goal states explicitly.
- [ ] Check whether any liveness claim depends on a scheduler or environment
      fairness assumption.
- [ ] Validate each formalized requirement on one positive and one negative
      trace.
- [ ] Look for vacuity, especially when the English requirement begins with
      "if" or "when."
- [ ] Keep the English statement next to the LTL formula so the translation can
      be audited.

## 9. References

- Alpern, Bowen, and Fred B. Schneider. 1985. Defining Liveness.
  *Information Processing Letters* 21 (4): 181-185.
  <https://doi.org/10.1016/0020-0190(85)90056-0>
- Baier, Christel, and Joost-Pieter Katoen. 2008. *Principles of Model
  Checking*. MIT Press.
  <https://mitpress.mit.edu/9780262026499/principles-of-model-checking/>
- Dwyer, Matthew B., George S. Avrunin, and James C. Corbett. 1999. Patterns in
  Property Specifications for Finite-State Verification. *ICSE 1999*: 411-420.
  <https://doi.org/10.1145/302405.302672>
- Lamport, Leslie. 2002. *Specifying Systems*. Addison-Wesley.
  <https://lamport.azurewebsites.net/tla/book.html>
- Manna, Zohar, and Amir Pnueli. 1992. *The Temporal Logic of Reactive and
  Concurrent Systems*. Springer.
- Pnueli, Amir. 1977. The Temporal Logic of Programs. *FOCS 1977*: 46-57.
  <https://doi.org/10.1109/SFCS.1977.32>
