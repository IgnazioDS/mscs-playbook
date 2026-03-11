# Reasoning Under Uncertainty: Bayes and MDP

## Key Ideas

- Many AI systems must act under uncertainty because observations are noisy, knowledge is incomplete, and actions can have stochastic outcomes.
- Bayes' rule updates beliefs when new evidence arrives, while Markov decision processes model sequential decision-making with probabilistic transitions and rewards.
- Probabilistic reasoning is valuable because it preserves uncertainty explicitly rather than hiding it behind brittle yes-no rules.
- MDPs connect uncertainty to action choice by optimizing expected long-run value instead of myopic immediate reward.
- The quality of uncertain reasoning depends heavily on the realism of the probability model and state representation.

## 1. Why Uncertainty Matters

Real environments rarely provide complete, error-free information. Sensors can be noisy, diagnoses can be ambiguous, and actions can fail or have uncertain effects.

An AI system that ignores uncertainty may behave overconfidently. A system that models uncertainty can compare alternatives based on expected outcomes instead of pretending certainty where none exists.

## 2. Bayes' Rule

Bayes' rule updates a prior belief after observing evidence:

```text
P(H | E) = P(E | H) * P(H) / P(E)
```

where:

- `H` is a hypothesis
- `E` is observed evidence

This allows the system to revise beliefs as information arrives.

## 3. Markov Decision Processes

An MDP typically includes:

- states
- actions
- transition probabilities
- rewards
- a discount factor

The objective is to find a policy that maximizes expected cumulative reward.

This differs from simple search because outcomes are probabilistic, not deterministic.

## 4. Worked Example: Bayes Update

Suppose a disease has prior probability:

```text
P(D) = 0.01
```

A test has:

```text
P(positive | D) = 0.95
P(positive | not D) = 0.10
```

### 4.1 Compute Evidence Probability

```text
P(positive) = P(positive | D)P(D) + P(positive | not D)P(not D)
            = 0.95*0.01 + 0.10*0.99
            = 0.0095 + 0.099
            = 0.1085
```

### 4.2 Posterior

```text
P(D | positive) = 0.95*0.01 / 0.1085
                = 0.0095 / 0.1085
                ≈ 0.0876
```

Even with a positive test, the posterior disease probability is about `8.76%`, not 95%.

Verification: Bayes' rule shows how a rare condition can still have a low posterior probability even after a strong positive test because false positives matter when the base rate is low.

## 5. MDP Intuition

In an MDP, the best action is determined not only by immediate reward but by expected future value. This is captured by Bellman-style reasoning:

```text
value(state) = max over actions of expected immediate reward plus discounted future value
```

That makes MDPs a core model for sequential planning under uncertainty.

## 6. Common Mistakes

1. **Base-rate neglect.** Ignoring priors leads to wildly incorrect posterior beliefs; always include the prior when applying Bayes' rule.
2. **Deterministic thinking.** Treating uncertain transitions as fixed outcomes makes policies brittle; encode stochastic effects explicitly when they matter.
3. **State oversimplification.** Leaving out key state variables breaks the Markov assumption and distorts planning; define states to capture decision-relevant memory.
4. **Probability guesswork.** Using arbitrary probabilities without validation makes the model look formal but not trustworthy; ground probabilities in data or defensible assumptions.
5. **Short-term reward fixation.** Choosing actions only by immediate payoff misses long-run consequences; evaluate policies by cumulative expected return.

## 7. Practical Checklist

- [ ] Write down priors, likelihoods, and evidence terms explicitly before computing posteriors.
- [ ] Validate probability assumptions with data or expert justification.
- [ ] Define MDP states so future decisions depend only on the current state and action.
- [ ] Compare immediate-reward and long-run-value reasoning on sample decisions.
- [ ] Use approximate methods when exact state enumeration is infeasible.
- [ ] Revisit the model when observed outcomes diverge from predicted uncertainty.

## 8. References

- Russell, Stuart, and Peter Norvig. *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson, 2020.
- Pearl, Judea. *Probabilistic Reasoning in Intelligent Systems*. Morgan Kaufmann, 1988.
- Sutton, Richard S., and Andrew G. Barto. *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press, 2018. <http://incompleteideas.net/book/the-book-2nd.html>
- Puterman, Martin L. *Markov Decision Processes*. Wiley, 1994.
- Poole, David, and Alan Mackworth. *Artificial Intelligence: Foundations of Computational Agents* (2nd ed.). Cambridge University Press, 2017. <https://artint.info/2e/html/ArtInt2e.html>
- Berkeley MDP lecture notes. <https://people.eecs.berkeley.edu/~pabbeel/cs287-fa09/lecture-notes/mdps.pdf>
- Bayes' theorem overview. <https://en.wikipedia.org/wiki/Bayes%27_theorem>
