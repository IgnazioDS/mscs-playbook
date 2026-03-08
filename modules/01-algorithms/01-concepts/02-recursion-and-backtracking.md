# Recursion and Backtracking

## Key Ideas

- Recursion solves a problem by defining it in terms of smaller instances of the same problem.
- Backtracking is a search strategy that builds partial solutions incrementally and abandons them as soon as they violate feasibility or cannot lead to a valid full solution.
- A recursive formulation is useful only when the base cases, state transitions, and termination conditions are explicit.
- Backtracking performance depends heavily on pruning, ordering, and feasibility checks, because the naive search tree is often exponential in the worst case.
- Correctness comes from showing that the recursion explores exactly the intended search space and that pruning removes only branches that cannot succeed.

## 1. What It Is

A recursive algorithm calls itself on smaller inputs. This is natural when the problem structure is self-similar, such as trees, divide-and-conquer algorithms, or recursive enumeration.

Backtracking is a specific recursive pattern for search problems. It chooses a partial decision, recurses, and then undoes that decision if the branch fails. Typical uses include permutation generation, constraint satisfaction, subset search, and path enumeration.

### 1.1 Core definitions

- A **base case** is an input small enough to solve directly.
- A **recursive case** reduces the problem to smaller subproblems.
- A **partial solution** is an incomplete candidate being extended during search.
- **Pruning** means stopping exploration of a branch early because it cannot lead to a valid answer.
- A **search tree** is the tree of recursive choices explored by the backtracking procedure.

## 2. Why It Matters

Recursion is the clearest way to express many algorithms. Trees are traversed recursively because each subtree is itself a tree. Divide-and-conquer algorithms recurse because each subarray is a smaller instance of the original problem. Enumeration procedures recurse because a length-`k` prefix can be extended to a length-`k+1` prefix by the same rule.

Backtracking matters because many exact algorithms for combinatorial search rely on it before more advanced ideas such as memoization or branch-and-bound are introduced.

## 3. Backtracking Structure

### 3.1 General design pattern

A backtracking solver typically does three things:

1. check whether the current partial solution is complete,
2. generate legal next choices,
3. recurse on each choice and undo it afterward.

### 3.2 Complexity perspective

Backtracking often has exponential worst-case time because the search tree branches repeatedly. Pruning reduces the explored tree, but unless a stronger structural result is available, the worst-case bound may remain exponential.

This is why careful feasibility checks matter: they do not change the abstract search space, but they can dramatically shrink the explored portion.

## 4. Worked Example

Generate all subsets of `{1, 2, 3}` by recursively deciding for each element whether to include it.

### 4.1 Recursive state

At index `i`, we have processed the first `i` elements and built some current subset.

### 4.2 Trace

Start with `i = 0`, `current = {}`.

- Exclude `1` -> recurse with `i = 1`, `current = {}`
  - Exclude `2` -> recurse with `i = 2`, `current = {}`
    - Exclude `3` -> output `{}`
    - Include `3` -> output `{3}`
  - Include `2` -> recurse with `i = 2`, `current = {2}`
    - Exclude `3` -> output `{2}`
    - Include `3` -> output `{2, 3}`
- Include `1` -> recurse with `i = 1`, `current = {1}`
  - Exclude `2` -> recurse with `i = 2`, `current = {1}`
    - Exclude `3` -> output `{1}`
    - Include `3` -> output `{1, 3}`
  - Include `2` -> recurse with `i = 2`, `current = {1, 2}`
    - Exclude `3` -> output `{1, 2}`
    - Include `3` -> output `{1, 2, 3}`

The outputs are:

```text
{}
{3}
{2}
{2, 3}
{1}
{1, 3}
{1, 2}
{1, 2, 3}
```

Verification: exactly `2^3 = 8` subsets are generated, and every subset of `{1, 2, 3}` appears once.

## 5. Pseudocode Pattern

```text
procedure enumerate_subsets(items, index, current, output):
    if index == length(items):
        append(output, copy(current))
        return

    enumerate_subsets(items, index + 1, current, output)

    append(current, items[index])
    enumerate_subsets(items, index + 1, current, output)
    remove_last(current)
```

Time: `Theta(2^n * n)` worst case if copying each subset of up to length `n` is counted. Space: `Theta(n)` auxiliary recursion depth, excluding stored output.

## 6. Common Mistakes

1. **Missing base case.** A recursive procedure without a precise stopping condition risks nontermination or invalid calls; define the smallest directly solvable inputs first.
2. **State-leak mutation.** Forgetting to undo a choice after recursion corrupts sibling branches; backtracking requires restoring the partial state before returning.
3. **Pruning without proof.** Cutting off a branch because it “looks bad” can remove valid solutions; justify every pruning rule with a feasibility argument.
4. **Work-space confusion.** Treating the recursion stack as free hides real memory usage; count recursion depth separately from output storage.
5. **Enumeration-value collapse.** Using backtracking when the task only needs a count or optimum can waste exponential work; check whether dynamic programming or greedy structure exists instead.

## 7. Practical Checklist

- [ ] State the recursive input and the smaller subproblem relation explicitly.
- [ ] Prove that each recursive call makes measurable progress toward a base case.
- [ ] Keep the partial solution representation minimal.
- [ ] Undo every state mutation before exploring the next branch.
- [ ] Add pruning only when you can explain why the pruned branch cannot succeed.
- [ ] Estimate the branching factor and depth before committing to backtracking.

## 8. References

- Cormen, Thomas H., Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. 2022. *Introduction to Algorithms* (4th ed.). MIT Press. <https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/>
- Kleinberg, Jon, and Eva Tardos. 2005. *Algorithm Design*. Pearson. <https://www.pearson.com/en-us/subject-catalog/p/algorithm-design/P200000003815>
- Erickson, Jeff. 2023. *Algorithms*. University of Illinois Urbana-Champaign. <https://jeffe.cs.illinois.edu/teaching/algorithms/>
- Skiena, Steven S. 2020. *The Algorithm Design Manual* (3rd ed.). Springer. <https://www.algorist.com/>
- Knuth, Donald E. 2011. *The Art of Computer Programming, Volume 4A*. Addison-Wesley. <https://www-cs-faculty.stanford.edu/~knuth/taocp.html>
- Lehman, Eric, F. Thomson Leighton, and Albert R. Meyer. 2018. *Mathematics for Computer Science*. MIT. <https://courses.csail.mit.edu/6.042/spring18/mcs.pdf>
