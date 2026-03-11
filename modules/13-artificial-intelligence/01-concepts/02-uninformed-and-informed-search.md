# Uninformed and Informed Search

## Key Ideas

- Search algorithms solve problems by exploring a state space defined by states, actions, transitions, and a goal test.
- Uninformed search uses only the problem definition, while informed search also uses heuristic estimates to guide exploration.
- Time and space behavior depend more on branching factor and depth than on code elegance, which is why search design begins with problem structure.
- Heuristics are valuable only when they provide useful guidance without violating the guarantees required by the task.
- Search instrumentation matters because node expansions, frontier size, and repeated-state handling often determine feasibility in practice.

## 1. Problem Formulation

A search problem usually specifies:

- a start state
- a goal test
- a successor function
- step costs

The algorithm’s job is to find a path from the start to a goal, often with minimum cost.

This means the real design work begins before the algorithm is chosen. Bad state representations create huge search spaces no algorithm will rescue easily.

## 2. Uninformed Search

Common uninformed methods include:

- breadth-first search
- depth-first search
- uniform-cost search

They differ in completeness, optimality, and resource use.

Breadth-first search is useful for shallow unweighted shortest paths, while uniform-cost search handles varying step costs.

## 3. Informed Search

Informed search adds a **heuristic**, a function estimating the cost or distance from a state to a goal.

The most common example is A*, which prioritizes states by:

```text
f(n) = g(n) + h(n)
```

where:

- `g(n)` is the path cost so far
- `h(n)` is the heuristic estimate to the goal

If `h(n)` is admissible, A* retains optimality under standard conditions.

## 4. Worked Example: A* Priorities

Suppose a pathfinding problem has a state `S` with two frontier successors:

```text
state A: g(A) = 4, h(A) = 3
state B: g(B) = 2, h(B) = 6
```

### 4.1 Compute Priorities

```text
f(A) = 4 + 3 = 7
f(B) = 2 + 6 = 8
```

### 4.2 Expansion Choice

A* expands `A` before `B` because:

```text
7 < 8
```

Even though `B` is cheaper so far, its estimated total path cost is worse.

Verification: A* chooses the node with lower estimated total cost, not just lower path cost so far.

## 5. Search Complexity in Practice

Theoretical complexity often depends on:

- branching factor `b`
- solution depth `d`

For example:

- breadth-first search has worst-case time `O(b^d)` and worst-case space `O(b^d)`
- depth-first search has worst-case time `O(b^m)` where `m` is maximum depth, and worst-case space `O(bm)`

These case labels matter because space, not only time, often becomes the limiting resource.

## 6. Common Mistakes

1. **Algorithm-first thinking.** Choosing BFS, UCS, or A* before formulating the state space clearly leads to weak results; define states and transitions first.
2. **Heuristic overconfidence.** Using an inaccurate heuristic without checking admissibility can break optimality; validate heuristics against known shortest paths.
3. **Repeated-state neglect.** Omitting closed sets or duplicate handling causes wasted work and cycles; track explored states in graph search.
4. **Branching-factor blindness.** Underestimating branching growth leads to infeasible searches; estimate resource usage before scaling up.
5. **Metric mismatch.** Using step count when the real objective is weighted cost gives the wrong path; align the path cost with the true objective.

## 7. Practical Checklist

- [ ] Define the state representation, goal test, and transition rules explicitly.
- [ ] Estimate branching factor and likely solution depth before picking an algorithm.
- [ ] Use graph search with explored-state tracking unless there is a reason not to.
- [ ] Validate heuristics on small known instances before relying on A*.
- [ ] Instrument node expansions and frontier size during experiments.
- [ ] Align the search cost function with the real optimization objective.

## 8. References

- Russell, Stuart, and Peter Norvig. *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson, 2020.
- Hart, Peter E., Nils J. Nilsson, and Bertram Raphael. "A Formal Basis for the Heuristic Determination of Minimum Cost Paths." 1968. <https://doi.org/10.1109/TSSC.1968.300136>
- Pearl, Judea. *Heuristics: Intelligent Search Strategies for Computer Problem Solving*. Addison-Wesley, 1984.
- Poole, David, and Alan Mackworth. *Artificial Intelligence: Foundations of Computational Agents* (2nd ed.). Cambridge University Press, 2017. <https://artint.info/2e/html/ArtInt2e.html>
- LaValle, Steven M. *Planning Algorithms*. Cambridge University Press, 2006. <https://lavalle.pl/planning/>
- Korf, Richard E. "Depth-first iterative-deepening." 1985. <https://www.sciencedirect.com/science/article/pii/0004370285900840>
- Berkeley AIMA search code resources. <https://github.com/aimacode>
