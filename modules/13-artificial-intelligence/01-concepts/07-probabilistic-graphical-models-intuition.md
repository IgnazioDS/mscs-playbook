# Probabilistic Graphical Models Intuition

## Key Ideas

- Probabilistic graphical models represent joint distributions by exploiting conditional independence structure.
- Bayesian networks use directed graphs for causal or generative structure, while Markov random fields use undirected graphs for symmetric dependencies.
- Graph structure matters because it determines which factorization assumptions make inference tractable.
- PGMs are useful when uncertainty is structured and interpretable, not just because they provide another notation for probabilities.
- Inference difficulty is driven by graph connectivity and factor size, so model design and inference cost cannot be separated.

## 1. Why PGMs Matter

A full joint distribution over many variables grows exponentially. Graphical models reduce that complexity by expressing which variables depend directly on which others.

That provides two benefits:

- a compact representation
- a clearer picture of conditional independence

This is why PGMs are useful for diagnosis, reasoning, and structured prediction problems.

## 2. Bayesian Networks

A **Bayesian network** is a directed acyclic graph where each node has a conditional probability table given its parents.

The joint distribution factorizes as:

```text
P(X1, ..., Xn) = product over i of P(Xi | Parents(Xi))
```

This is compact when each variable depends on only a few others.

## 3. Markov Random Fields

An **MRF** uses an undirected graph and factors over cliques. It is often useful when dependencies are symmetric and do not have a natural parent-child direction.

The common theme is the same: graph structure tells us what probabilistic interactions must be represented explicitly.

## 4. Worked Example: Small Bayes Net Factorization

Suppose a three-variable Bayes net is:

```text
Cloudy -> Rain
Cloudy -> Sprinkler
Rain, Sprinkler -> WetGrass
```

The joint factorization is:

```text
P(Cloudy, Rain, Sprinkler, WetGrass)
= P(Cloudy)
  P(Rain | Cloudy)
  P(Sprinkler | Cloudy)
  P(WetGrass | Rain, Sprinkler)
```

This is much smaller than storing every joint combination directly.

### 4.1 Independence Intuition

Given `Cloudy`, `Rain` and `Sprinkler` are conditionally independent in this graph. That is the kind of structural simplification PGMs make explicit.

Verification: the graph defines a factorization that separates the joint distribution into local conditional terms, which is the main computational advantage of a Bayes net.

## 5. Inference and Complexity

Inference may involve:

- variable elimination
- belief propagation
- sampling methods

Exact inference can become infeasible when the graph induces large cliques or dense dependencies. This is why even a well-structured model can become expensive if the graph is poorly chosen.

## 6. Common Mistakes

1. **Graph-as-decoration thinking.** Drawing a graph without defending the conditional independence assumptions makes the model untrustworthy; justify edges and non-edges explicitly.
2. **Dense-graph drift.** Adding too many dependencies destroys the compactness advantage; include only dependencies the model genuinely needs.
3. **Causal overclaiming.** A directed edge in a Bayes net does not automatically prove causal truth; distinguish modeling convenience from causal claims.
4. **Inference-cost denial.** Ignoring clique growth or factor size can make exact inference infeasible; analyze runtime implications when designing the graph.
5. **Parameter neglect.** Good graph structure still needs sensible probabilities or factors; audit both the topology and the numerical parameters.

## 7. Practical Checklist

- [ ] State the variables and their dependency assumptions clearly before drawing the graph.
- [ ] Justify each edge in terms of information flow or dependency.
- [ ] Use conditional independence to simplify the model, not to oversimplify reality.
- [ ] Choose inference methods that match graph size and structure.
- [ ] Test the model on small known queries before scaling up.
- [ ] Revisit edges and factors when inference cost or prediction quality is poor.

## 8. References

- Koller, Daphne, and Nir Friedman. *Probabilistic Graphical Models: Principles and Techniques*. MIT Press, 2009.
- Pearl, Judea. *Probabilistic Reasoning in Intelligent Systems*. Morgan Kaufmann, 1988.
- Murphy, Kevin P. *Machine Learning: A Probabilistic Perspective*. MIT Press, 2012.
- Jordan, Michael I. "Graphical Models." <https://people.eecs.berkeley.edu/~jordan/prelims/graphical-models.pdf>
- Russell, Stuart, and Peter Norvig. *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson, 2020.
- Bishop, Christopher M. *Pattern Recognition and Machine Learning*. Springer, 2006.
- Poole, David, and Alan Mackworth. *Artificial Intelligence: Foundations of Computational Agents* (2nd ed.). Cambridge University Press, 2017. <https://artint.info/2e/html/ArtInt2e.html>
