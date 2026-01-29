# AI Cheat Sheet

## Search algorithm selection
- BFS: shortest path in unweighted graphs
- DFS: low memory, not optimal
- UCS: optimal with nonnegative costs
- A*: optimal with admissible heuristics
- IDA*: memory-efficient A* variant

## Heuristics checklist
- Admissible: never overestimates cost
- Consistent: triangle inequality for A*
- Validate on small known instances
- Prefer informative heuristics to reduce expansions

## Minimax and alpha-beta tips
- Use depth limits with evaluation functions
- Add move ordering for better pruning
- Cache repeated states with transposition tables
- Guard against horizon effects

## CSP toolbox
- MRV: choose smallest domain variable
- Degree heuristic: choose most constrained variable
- LCV: try least-constraining values first
- AC-3 for arc consistency

## Bayes rule and distributions
- Bayes: P(A|B) = P(B|A)P(A) / P(B)
- Common distributions: Bernoulli, Binomial, Gaussian, Poisson
- Use priors and likelihoods explicitly

## MDP basics
- Policy: mapping from states to actions
- Value: expected return under a policy
- Bellman equations define optimality
- Solve with value or policy iteration

## Debugging and evaluation
- Check state representation and transitions
- Verify goal tests and terminal conditions
- Track node expansions and frontier size
- Add regression tests for heuristics
