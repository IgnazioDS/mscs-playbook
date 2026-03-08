# Greedy Correctness

## Key Ideas

- A greedy algorithm is correct only when a locally optimal choice can be shown to preserve access to a globally optimal solution.
- Greedy correctness is a proof obligation, not an intuition; a rule that looks reasonable can still fail badly on small counterexamples.
- Exchange arguments prove correctness by transforming an optimal solution so that it agrees with the greedy choice without making the solution worse.
- Stays-ahead arguments prove correctness by showing that after every step, the greedy partial solution is at least as good as any competing partial solution under the relevant progress measure.
- Greedy algorithms are often efficient because each step commits irrevocably, but that same commitment is what makes correctness proofs necessary.

## 1. What It Is

A greedy algorithm constructs a solution step by step by making the best-looking local choice according to some rule. Once a choice is made, the algorithm does not revisit it.

This distinguishes greedy methods from dynamic programming and backtracking. Dynamic programming explores many subproblem combinations and reuses results. Backtracking explores alternatives and may undo choices. Greedy algorithms commit immediately, which often makes them simpler and faster, but also more fragile.

A greedy algorithm is not correct merely because it is fast or intuitive. It is correct only when the problem structure guarantees that each greedy decision can be extended to an optimal full solution.

### 1.1 Core Definitions

- A **greedy algorithm** builds a solution incrementally by repeatedly choosing the locally best available option.
- A **locally optimal choice** is the best choice according to the greedy rule at the current step.
- A **globally optimal solution** is the best feasible solution over all possibilities.
- The **greedy-choice property** means that at least one optimal solution begins with the greedy choice.
- **Optimal substructure** means that after making a safe choice, the remaining problem is itself an optimal subproblem of the same form.
- An **exchange argument** proves that if an optimal solution does not use the greedy choice, it can be modified to use it without becoming worse.
- A **stays-ahead argument** proves that after each step, the greedy partial solution is never behind any competing solution under a chosen progress measure.

### 1.2 Why This Matters

Greedy algorithms appear in interval scheduling, Huffman coding, minimum spanning trees, Dijkstra’s algorithm on nonnegative graphs, and many approximation algorithms. When they work, they are often among the cleanest and most efficient solutions available.

But greedy methods also fail often. For coin systems, scheduling rules, routing choices, and covering problems, a natural local rule can produce a globally suboptimal answer. This means that in algorithm design, “greedy” is not the proof; it is the hypothesis. The real work is showing why the hypothesis is safe.

## 2. How Greedy Correctness Is Proved

### 2.1 Exchange Argument

An exchange argument starts with an arbitrary optimal solution and shows how to modify it so that it uses the greedy choice first. The modification must preserve feasibility and not worsen the objective.

This proof template usually has three steps:

1. Let `G` be the greedy choice at the current step.
2. Let `O` be an optimal solution that may or may not contain `G`.
3. Show that `O` can be transformed into another optimal solution `O'` that does contain `G`.

Once that is established, the problem reduces to the remaining subproblem after taking `G`.

This is the standard proof style for interval scheduling and many minimum spanning tree arguments.

### 2.2 Stays-Ahead Argument

A stays-ahead proof compares the greedy partial solution with any other partial solution after the same number of steps.

The goal is to show that greedy is never worse according to a quantity that matters for future feasibility or optimality. For example, in interval scheduling, one common progress measure is the finishing time of the last selected interval.

If greedy always finishes no later than any competing solution with the same number of selected intervals, then greedy preserves at least as much room for future choices.

### 2.3 Structural or Cut-Based Proofs

Some greedy algorithms rely on a structural theorem rather than a direct exchange on complete solutions.

Examples:

- Kruskal’s and Prim’s algorithms rely on the cut property for minimum spanning trees.
- Dijkstra’s algorithm relies on the invariant that once a minimum-distance unsettled vertex is extracted, its shortest-path value is final, provided all weights are nonnegative.

These are still greedy proofs, but the correctness statement is expressed through an invariant or structural lemma instead of a direct swap.

## 3. When Greedy Works and When It Fails

### 3.1 Signs That Greedy May Work

Greedy algorithms are promising when:

- a locally best choice seems to simplify the remaining problem without destroying future options,
- the problem has an ordering rule that appears dominance-preserving,
- the objective and feasibility constraints interact monotonically,
- or known structural theorems support safe local commitment.

These are hints, not guarantees.

### 3.2 Signs That Greedy May Fail

Greedy is dangerous when:

- early choices can block better combinations later,
- the objective depends on interactions among multiple future decisions,
- local gains are not aligned with global feasibility,
- or small counterexamples appear when trying simple test cases.

For example, choosing the interval with shortest duration is not a correct greedy rule for interval scheduling, even though it sounds plausible.

### 3.3 Greedy vs Dynamic Programming

A useful contrast is:

- **Greedy:** commit now, prove the commitment is always safe.
- **Dynamic programming:** delay commitment, compare many possibilities, and reuse subproblem answers.

If you cannot prove the greedy choice is safe, the problem may require DP, graph search, branch-and-bound, or approximation instead.

## 4. Worked Example

Consider the classic **interval scheduling** problem. Each job has a start and finish time, and we want the maximum number of non-overlapping jobs.

Suppose the intervals are:

```text
A = [1, 4]
B = [3, 5]
C = [0, 6]
D = [5, 7]
E = [8, 9]
F = [5, 9]
```

The standard greedy rule is:

- sort by increasing finish time,
- repeatedly take the next compatible interval that finishes earliest.

### 4.1 Sort by Finish Time

The order by finish time is:

```text
A = [1, 4]
B = [3, 5]
C = [0, 6]
D = [5, 7]
E = [8, 9]
F = [5, 9]
```

### 4.2 Greedy Trace

Start with an empty schedule.

| Step | Candidate | Compatible? | Take? | Current schedule |
|---|---|---|---|---|
| 1 | `A = [1, 4]` | yes | yes | `{A}` |
| 2 | `B = [3, 5]` | no, overlaps `A` | no | `{A}` |
| 3 | `C = [0, 6]` | no, overlaps `A` | no | `{A}` |
| 4 | `D = [5, 7]` | yes | yes | `{A, D}` |
| 5 | `E = [8, 9]` | yes | yes | `{A, D, E}` |
| 6 | `F = [5, 9]` | no, overlaps `D` and `E` | no | `{A, D, E}` |

The greedy algorithm returns:

```text
{A, D, E}
```

with `3` intervals.

### 4.3 Why the Choice Is Safe

Suppose an optimal schedule does not start with the earliest-finishing compatible interval `A`. Let its first chosen interval be some interval `X` that finishes at or after `A`. Replacing `X` with `A` cannot reduce the number of intervals that fit afterward, because `A` leaves at least as much remaining time as `X`.

So there exists an optimal solution that begins with `A`. After choosing `A`, the remaining problem is again interval scheduling on the intervals that start after time `4`.

Verification: the greedy schedule selects `A, D, E`, which is feasible and has size `3`. No schedule can contain `4` mutually non-overlapping intervals from this set, so the greedy answer is optimal. Correct.

## 5. Pseudocode Pattern

```text
procedure interval_scheduling(intervals):
    sort intervals by increasing finish time
    solution = empty_list()
    last_finish = -inf
    for each interval in intervals:
        if interval.start >= last_finish:
            append solution, interval
            last_finish = interval.finish
    return solution
```

Time: `O(n log n)` worst case because of sorting, followed by an `O(n)` scan. Space: `O(n)` if the output list is counted, or `O(1)` auxiliary space beyond the output and sort implementation details.

The correctness proof uses an exchange argument: the earliest-finishing compatible interval can always be placed first in some optimal solution.

## 6. Common Mistakes

1. **Intuition-as-proof.** Claiming a greedy rule is correct because it “seems best” or “works on examples” is not a correctness argument; a structural proof is still required.
2. **Wrong greedy key.** Sorting or prioritizing by a plausible but incorrect attribute, such as shortest interval length instead of earliest finish time, can produce suboptimal solutions.
3. **Feasibility drift.** Making a locally attractive choice without re-checking global constraints can produce an invalid partial solution that blocks completion.
4. **Tie-handling blindness.** Assuming ties do not matter can hide correctness or implementation issues when multiple equal-priority choices exist.
5. **Greedy-DP confusion.** Applying a greedy commitment in a problem that requires comparing multiple future branches can destroy optimality when the problem lacks the greedy-choice property.

## 7. Practical Checklist

- [ ] State the greedy rule in one exact sentence before implementing it.
- [ ] Identify the objective function and verify whether the problem is minimization or maximization.
- [ ] Write down the invariant that must remain true after each greedy step.
- [ ] Decide which proof style applies: exchange argument, stays-ahead argument, or structural theorem.
- [ ] Test the rule on a small counterexample search before trusting it.
- [ ] Re-check feasibility after every committed choice.
- [ ] Separate the correctness proof from the runtime analysis.

## References

- Cormen, Thomas H., Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. 2022. *Introduction to Algorithms* (4th ed.). MIT Press. <https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/>
- Kleinberg, Jon, and Eva Tardos. 2021. *Algorithm Design*. Pearson. <https://www.pearson.com/en-us/subject-catalog/p/algorithm-design/P200000003259/9780137546350>
- Erickson, Jeff. 2019. *Algorithms*. <https://jeffe.cs.illinois.edu/teaching/algorithms/>
- Dasgupta, Sanjoy, Christos Papadimitriou, and Umesh Vazirani. 2008. *Algorithms*. McGraw-Hill. <http://algorithmics.lsi.upc.edu/docs/Dasgupta-Papadimitriou-Vazirani.pdf>
- Sedgewick, Robert, and Kevin Wayne. 2011. *Algorithms* (4th ed.). Addison-Wesley. <https://algs4.cs.princeton.edu/home/>
- Mehlhorn, Kurt, and Peter Sanders. 2008. *Algorithms and Data Structures: The Basic Toolbox*. Springer. <https://doi.org/10.1007/978-3-540-77978-0>
