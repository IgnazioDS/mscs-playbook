# Constraint Satisfaction Problems

## Key Ideas

- A constraint satisfaction problem models reasoning as assigning values to variables while satisfying constraints.
- CSP structure matters because decomposition and propagation can shrink huge search spaces before brute-force enumeration begins.
- Backtracking is the core search method, but heuristics and consistency enforcement usually determine practical feasibility.
- Variables, domains, and constraints should express the problem at the right abstraction level or the solver will waste effort on avoidable symmetry or redundancy.
- CSP techniques are especially effective for scheduling, assignment, timetabling, and configuration tasks with explicit combinatorial structure.

## 1. What a CSP Is

A CSP consists of:

- a set of variables
- a domain of possible values for each variable
- constraints that define which combinations are allowed

The goal is to find a complete assignment that satisfies all constraints.

This representation is powerful because it separates problem structure from the search procedure.

## 2. Why Propagation Matters

Naive backtracking considers assignments and undoes them when they fail. Constraint propagation improves this by pruning impossible values before deeper search.

Common techniques include:

- forward checking
- arc consistency
- domain reduction after each assignment

These are crucial because CSP search trees grow rapidly when domains stay large.

## 3. Heuristics

Two especially common heuristics are:

- **MRV**: choose the variable with minimum remaining values
- **LCV**: try the value that rules out the fewest choices for neighbors

These heuristics reduce wasted search by focusing on the most constrained parts of the problem first.

## 4. Worked Example: Tiny Scheduling CSP

Suppose two classes, `A` and `B`, must be scheduled into time slots:

```text
domain(A) = {1, 2}
domain(B) = {1, 2}
constraint: A != B
```

### 4.1 Assign A

Try:

```text
A = 1
```

### 4.2 Propagate Constraint

Because `A != B`, value `1` is removed from `B`:

```text
domain(B) = {2}
```

### 4.3 Assign B

Only one choice remains:

```text
B = 2
```

This yields a complete consistent solution.

Verification: once `A = 1` is chosen, propagation reduces `B` to its only valid value, which avoids unnecessary branching.

## 5. Modeling Quality Matters

A CSP formulation can fail even with good algorithms if:

- variables are too low-level
- domains are unnecessarily large
- constraints are incomplete or inconsistent

Good modeling reduces symmetry, captures the true restrictions clearly, and exposes opportunities for propagation.

## 6. Common Mistakes

1. **Poor variable design.** Choosing variables that are too fine-grained or redundant inflates the search space; model the problem at the most useful constraint level.
2. **Propagation neglect.** Using bare backtracking without forward checking or consistency checks wastes search effort; prune domains early.
3. **Heuristic omission.** Ignoring MRV or LCV on nontrivial CSPs makes search far slower than necessary; add ordering heuristics by default.
4. **Constraint bugs.** An incorrect constraint can silently eliminate valid solutions or admit impossible ones; test constraints on small known cases first.
5. **Symmetry blindness.** Equivalent assignments can multiply the search tree; add symmetry-breaking constraints when appropriate.

## 7. Practical Checklist

- [ ] Define variables, domains, and constraints explicitly before choosing a solver strategy.
- [ ] Validate the model on tiny hand-checkable instances first.
- [ ] Add forward checking or arc consistency for nontrivial problems.
- [ ] Use MRV and LCV unless there is a reason not to.
- [ ] Watch for symmetries that create duplicate search effort.
- [ ] Instrument backtracks and domain reductions to understand runtime.

## 8. References

- Russell, Stuart, and Peter Norvig. *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson, 2020.
- Mackworth, Alan K. "Consistency in Networks of Relations." 1977. <https://doi.org/10.1016/0004-3702(77)90007-8>
- Dechter, Rina. *Constraint Processing*. Morgan Kaufmann, 2003.
- Kumar, Vipin. "Algorithms for Constraint-Satisfaction Problems: A Survey." 1992. <https://link.springer.com/article/10.1007/BF00126902>
- Poole, David, and Alan Mackworth. *Artificial Intelligence: Foundations of Computational Agents* (2nd ed.). Cambridge University Press, 2017. <https://artint.info/2e/html/ArtInt2e.html>
- Rossi, Francesca, Peter van Beek, and Toby Walsh, eds. *Handbook of Constraint Programming*. Elsevier, 2006.
- Gent, Ian P., and Barbara M. Smith. "Symmetry Breaking in Constraint Programming." 2000. <https://link.springer.com/chapter/10.1007/3-540-45193-0_24>
