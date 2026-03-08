# Approximation Intro

## Key Ideas

- Approximation algorithms target optimization problems where exact polynomial-time solutions are unlikely, and they trade optimality for provable performance guarantees.
- An approximation ratio is a worst-case guarantee relative to the optimal solution, not an empirical average over easy instances.
- The guarantee depends on whether the problem is a minimization or maximization problem, so the ratio must be stated with the objective direction.
- Many approximation algorithms work by exploiting structure such as submodularity, LP relaxations, primal-dual relationships, or metric inequalities.
- A useful approximation algorithm is not just fast; it must also preserve a rigorous link between the returned solution and the optimum.

## 1. What It Is

Approximation algorithms are polynomial-time algorithms for optimization problems that are believed to be hard to solve exactly. Instead of guaranteeing the optimal answer, they guarantee a solution that is within a known factor of optimal.

This is most relevant for NP-hard optimization problems such as vertex cover, set cover, metric traveling salesman, and facility location. For these problems, exact algorithms may be exponential in the worst case, while approximation algorithms provide predictable solution quality at practical running times.

### 1.1 Core Definitions

- An **optimization problem** asks for the best feasible solution under an objective, such as minimum cost or maximum value.
- A **feasible solution** satisfies all problem constraints.
- The **optimal solution** is the feasible solution with the best objective value.
- A **polynomial-time approximation algorithm** runs in polynomial time and returns a feasible solution with a provable quality guarantee.
- For a **minimization** problem, an algorithm is an `r`-approximation if for every instance it returns a solution of cost at most `r * OPT`, where `OPT` is the optimal cost.
- For a **maximization** problem, an algorithm is an `r`-approximation if for every instance it returns a solution of value at least `OPT / r`. Equivalent formulations sometimes use a factor `alpha` in `(0, 1]`; the convention must be stated explicitly.

### 1.2 Why This Matters

Approximation algorithms are a practical response to computational hardness. When exact optimization is too slow, the question becomes: how much quality can we retain while still solving large instances efficiently?

This matters in routing, scheduling, resource allocation, clustering, network design, and covering problems. A guarantee such as “within 2 times optimal” or “within `1 + ln n` times optimal” provides something stronger than heuristic performance claims: it states what happens even on adversarial instances.

## 2. Approximation Ratios and Guarantees

### 2.1 Minimization vs Maximization

The approximation guarantee must match the optimization direction.

For minimization:

```text
cost(alg) <= r * OPT
```

For maximization:

```text
value(alg) >= OPT / r
```

This distinction matters because the same sentence can become wrong when the objective flips. A smaller cost is better, but a larger value is better.

### 2.2 Worst-Case Guarantee

The approximation ratio is a worst-case statement over all instances, not a claim about typical or average behavior on one benchmark set.

For example, if a 2-approximation algorithm for vertex cover returns a solution twice the optimum on a carefully constructed instance, it is still performing within its guarantee. If it performs much better on most inputs, that is useful empirically, but it is not the formal meaning of the ratio.

### 2.3 What a Guarantee Does Not Say

An approximation guarantee does not imply:

- that the returned solution is usually close to the ratio bound,
- that the algorithm is always better than a heuristic in practice,
- or that the bound is tight for every input.

It only says that the solution quality never crosses the proven worst-case threshold.

## 3. Main Design Patterns

### 3.1 Greedy Approximation

Some approximation algorithms repeatedly make a locally attractive choice and then prove that the local loss is globally bounded.

Examples include:

- set cover using a greedy cost-per-uncovered-element rule,
- load balancing via sorted or unsorted greedy assignment,
- some clustering and covering routines.

Greedy methods are attractive because they are often simple to implement and analyze, but the proof usually depends on a structural inequality rather than the greedy rule alone.

### 3.2 LP Relaxation and Rounding

For many NP-hard problems, an integer program is relaxed into a linear program by allowing variables to take fractional values. The fractional solution is then rounded into an integral feasible solution.

The key proof idea is:

1. the LP optimum is a lower bound for the integer optimum in minimization problems,
2. the rounding step increases the objective by a controlled factor.

This approach is standard for vertex cover, facility location variants, and many covering or packing problems.

### 3.3 Primal-Dual Methods

Primal-dual approximation algorithms construct a feasible primal solution and a dual certificate simultaneously. The dual objective provides a lower bound, and the analysis shows that the primal solution is within a bounded factor of that lower bound.

This method is especially important for covering problems because it often produces direct and combinatorial algorithms without solving the LP exactly.

### 3.4 Problem-Specific Structure

Some approximation algorithms rely on properties specific to the problem class.

Examples:

- triangle inequality in metric TSP,
- submodularity in coverage-like maximization,
- tree embeddings or metric decompositions in network design,
- local-exchange arguments in clustering or packing.

**Why this matters:** approximation is not one generic trick. The guarantee comes from exploiting structure that the exact-hardness result does not remove.

## 4. Worked Example

Consider the **vertex cover** problem on the graph with edges:

```text
(1, 2), (1, 3), (2, 3), (3, 4)
```

A vertex cover is a set of vertices that touches every edge.

### 4.1 A Standard 2-Approximation Strategy

A classic approximation algorithm works as follows:

1. pick any uncovered edge,
2. add both endpoints to the cover,
3. remove all edges incident to those endpoints,
4. repeat until no edges remain.

### 4.2 Step-by-Step Trace

Start with:

```text
E = {(1, 2), (1, 3), (2, 3), (3, 4)}
cover = {}
```

Pick edge `(1, 2)`.

Add both endpoints:

```text
cover = {1, 2}
```

Remove all edges incident to `1` or `2`:

- `(1, 2)` removed
- `(1, 3)` removed
- `(2, 3)` removed

Remaining edges:

```text
E = {(3, 4)}
```

Pick edge `(3, 4)`.

Add both endpoints:

```text
cover = {1, 2, 3, 4}
```

Remove all edges incident to `3` or `4`:

```text
E = {}
```

The algorithm returns:

```text
{1, 2, 3, 4}
```

### 4.3 Compare with the Optimum

An optimal cover for this graph is:

```text
{1, 3}
```

Check:

- `(1, 2)` covered by `1`
- `(1, 3)` covered by `1` or `3`
- `(2, 3)` covered by `3`
- `(3, 4)` covered by `3`

So:

```text
ALG = 4
OPT = 2
ALG / OPT = 2
```

Verification: the returned solution has size `4`, the optimal cover has size `2`, and the ratio is exactly `2`, matching the guarantee of the algorithm. Correct.

## 5. Pseudocode Pattern

```text
procedure edge_pair_vertex_cover(G):
    cover = empty_set()
    while G has an uncovered edge (u, v):
        add u to cover
        add v to cover
        remove from G every edge incident to u or v
    return cover
```

Time: `O(m + n)` to `O(mn)` depending on the graph representation and how uncovered edges are maintained. Approximation ratio: `2` for vertex cover.

The proof idea is that each chosen edge in the loop is disjoint from the others after incident edges are removed. Therefore, any valid vertex cover must contain at least one endpoint from each chosen edge, while the algorithm takes both endpoints. This gives the factor `2`.

## 6. Common Mistakes

1. **Empirical-ratio confusion.** Measuring `ALG / OPT` on a few instances and calling that “the approximation ratio” confuses observed performance with the formal worst-case guarantee.
2. **Objective-direction mismatch.** Using the minimization definition for a maximization problem, or the reverse, makes the stated guarantee mathematically wrong.
3. **Feasibility loss during rounding.** Rounding an LP solution without re-checking constraints can produce an integral solution that is not actually feasible.
4. **Hardness-blind optimism.** Expecting a constant-factor approximation for every NP-hard problem ignores known inapproximability barriers; the achievable ratio depends strongly on the problem.
5. **Proof-free greediness.** Calling a greedy algorithm an approximation algorithm without proving a bound turns it into a heuristic, not a guaranteed approximation method.

## 7. Practical Checklist

- [ ] State clearly whether the problem is a minimization or maximization problem before writing the ratio guarantee.
- [ ] Verify that the algorithm always returns a feasible solution, not just a numerically attractive one.
- [ ] Separate the running-time analysis from the approximation-ratio proof.
- [ ] Identify the lower bound or comparison object used in the proof, such as `OPT`, an LP relaxation, or a dual solution.
- [ ] Check whether the guarantee is worst case, expected, or depends on a special property such as metricity.
- [ ] Distinguish a heuristic from a true approximation algorithm unless a proof is present.
- [ ] Test the algorithm on at least one instance where the ratio is not trivially `1`.

## References

- Williamson, David P., and David B. Shmoys. 2011. *The Design of Approximation Algorithms*. Cambridge University Press. <https://www.designofapproxalgs.com/>
- Vazirani, Vijay V. 2003. *Approximation Algorithms*. Springer. <https://link.springer.com/book/10.1007/978-3-662-04565-7>
- Cormen, Thomas H., Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. 2022. *Introduction to Algorithms* (4th ed.). MIT Press. <https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/>
- Hochbaum, Dorit S., ed. 1997. *Approximation Algorithms for NP-Hard Problems*. PWS Publishing.
- Shmoys, David B. Approximation Algorithms lecture notes. Cornell University. <https://people.orie.cornell.edu/shmoys/or630/approx.pdf>
- Trevisan, Luca. CS261: Approximation Algorithms lecture notes. Bocconi University. <https://lucatrevisan.wordpress.com/teaching/cs261-approximation-algorithms/>
