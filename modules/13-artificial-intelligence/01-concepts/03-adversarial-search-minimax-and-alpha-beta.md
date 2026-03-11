# Adversarial Search: Minimax and Alpha-Beta

## Key Ideas

- Adversarial search models decision-making in competitive environments where another agent actively tries to reduce your outcome.
- Minimax assumes optimal play from both sides and chooses the action that maximizes the guaranteed value of the position.
- Alpha-beta pruning improves minimax efficiency by avoiding branches that cannot affect the final decision.
- Evaluation functions are essential when search cannot reach terminal states, but weak heuristics can dominate the final move quality.
- Competitive search quality depends on move ordering, depth control, and state evaluation, not just on implementing the recursive formula correctly.

## 1. Why Adversarial Search Is Different

Standard path search assumes the environment does not oppose the agent strategically. In games and competitive planning, that assumption fails. Every move can trigger a deliberate counter-move.

This requires reasoning about:

- your actions
- the opponent’s best response
- the downstream consequences of both

## 2. Minimax Intuition

Minimax alternates between:

- **max nodes**, where the agent chooses the highest-value action
- **min nodes**, where the opponent chooses the lowest-value action for the agent

Terminal states have known utilities such as win, draw, or loss. Nonterminal states often rely on heuristic evaluation when the search depth is limited.

## 3. Alpha-Beta Pruning

Alpha-beta pruning maintains two bounds:

- `alpha`: the best guaranteed value found so far for the maximizing player
- `beta`: the best guaranteed value found so far for the minimizing player

If a branch cannot improve the outcome under those bounds, it can be pruned safely.

This preserves the final decision while reducing search work, especially when move ordering is strong.

## 4. Worked Example: Simple Minimax Choice

Suppose a maximizing player has two actions:

- `Left`
- `Right`

Each leads to a minimizing node.

Leaf utilities:

```text
Left subtree leaves: 3, 5
Right subtree leaves: 2, 9
```

### 4.1 Min Node Values

The minimizing player chooses the smaller child value in each subtree:

```text
value(Left) = min(3, 5) = 3
value(Right) = min(2, 9) = 2
```

### 4.2 Root Decision

The maximizing player chooses:

```text
max(3, 2) = 3
```

So the agent selects:

```text
Left
```

Verification: the maximizing player prefers the subtree whose worst-case opponent response still yields the larger value.

## 5. Why Search Depth and Evaluation Matter

Real games often have large branching factors and deep trees, so full minimax is infeasible. That forces truncated search with heuristic evaluation.

Two common consequences:

- **horizon effects**, where the search misses an important future event just beyond the depth limit
- **evaluation bias**, where a fast heuristic prefers superficially good but strategically weak positions

This is why adversarial search is as much about evaluation design as about tree recursion.

## 6. Common Mistakes

1. **Tree-only thinking.** Implementing minimax without a clear game-state model or legal-move generator leads to brittle search; validate the game representation first.
2. **Evaluation neglect.** A shallow search with a weak heuristic still makes poor decisions; treat the evaluation function as part of the algorithm, not an afterthought.
3. **No move ordering.** Alpha-beta pruning is much weaker when strong moves are explored late; sort promising moves first when possible.
4. **Depth-confidence illusion.** Increasing depth without measuring node growth or horizon effects can waste compute while preserving bad heuristics; profile and validate the tradeoff.
5. **Nondeterministic debugging.** Missing tie-break rules makes search output unstable across runs; keep move ordering and tie resolution deterministic for testing.

## 7. Practical Checklist

- [ ] Validate legal move generation and terminal-state detection first.
- [ ] Start with plain minimax on tiny states before adding pruning.
- [ ] Add deterministic move ordering and tie-breaking.
- [ ] Profile node expansions with and without alpha-beta pruning.
- [ ] Evaluate heuristic quality on positions with known good moves.
- [ ] Tune depth limits against runtime and tactical failure cases.

## 8. References

- Russell, Stuart, and Peter Norvig. *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson, 2020.
- Knuth, Donald E., and Ronald W. Moore. "An Analysis of Alpha-Beta Pruning." 1975. <https://charlesames.net/references/DonaldKnuth/alpha-beta.html>
- Pearl, Judea. *Heuristics: Intelligent Search Strategies for Computer Problem Solving*. Addison-Wesley, 1984.
- Schaeffer, Jonathan. "The History Heuristic." 1989. <https://dl.acm.org/doi/10.1145/79973.79980>
- Marsland, T. A. "Computer Chess and Search." 1986. <https://www.sciencedirect.com/science/article/pii/S0004370286800217>
- Russell, Stuart. "Search in games." Berkeley AIMA materials. <https://aima.cs.berkeley.edu/>
- Silver, David, et al. "Mastering the game of Go with deep neural networks and tree search." 2016. <https://www.nature.com/articles/nature16961>
