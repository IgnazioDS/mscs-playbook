# Safety, Offline Reinforcement Learning, and Evaluation

## Key Ideas
- Safety in reinforcement learning means constraining or evaluating behavior so improvement does not depend on unacceptable failures.
- Offline reinforcement learning learns only from logged interaction data, which avoids online exploration risk but introduces severe distribution-shift problems.
- Evaluation is unusually difficult in RL because policy quality depends on long-horizon interaction, stochasticity, and environment assumptions.
- A high return on the training benchmark is not sufficient evidence that a policy is reliable, robust, or safe.
- Reliable RL systems require conservative learning, stress testing, multiple seeds, and explicit deployment rollback plans.

## 1. Why deployment concerns must be part of the curriculum

Reinforcement learning is often introduced through games and simulators, but real systems face hard constraints. An exploratory mistake in a warehouse, traffic system, or clinical workflow can be expensive or dangerous. That means the final stage of RL understanding is not only "how to improve reward" but also "when should a learned policy be trusted at all."

Two areas dominate that discussion:

- **safe RL**, which restricts or penalizes dangerous behavior during learning and deployment
- **offline RL**, which avoids online experimentation by learning from previously collected trajectories

Both areas exist because naive trial-and-error learning is often unacceptable in practice.

## 2. Offline RL and distribution shift

In offline RL, the algorithm receives a fixed dataset of trajectories from a behavior policy. It cannot collect new data during training. This avoids risky exploration, but it creates a major problem: the learned policy may choose actions not well represented in the logged dataset.

When a value function estimates those unseen actions optimistically, the error compounds through bootstrapping. This is often called **extrapolation error** or **distribution shift**. Conservative objectives, uncertainty penalties, and explicit behavior-regularized methods are used to reduce that risk.

## 3. Safety and constrained optimisation

A common safe RL idea is to optimize reward while satisfying a cost constraint. For example:

- maximize task reward
- keep expected collision cost below a threshold

This leads to **constrained MDP** formulations. In practice, safety may also be handled with action filters, human overrides, shielded policies, simulation gates, or staged deployment.

The important lesson is that safety should not be treated as one more weak penalty term when violations are unacceptable. Hard constraints and operational controls are usually necessary.

## 4. Worked example: offline policy comparison with importance weights

Suppose a logged dataset contains four one-step episodes from behavior policy `b`.

Behavior policy at the only state `s`:

- `b(a1 | s) = 0.8`
- `b(a2 | s) = 0.2`

Target policy `pi`:

- `pi(a1 | s) = 0.5`
- `pi(a2 | s) = 0.5`

Observed logged episodes:

1. action `a1`, reward `4`
2. action `a1`, reward `2`
3. action `a2`, reward `7`
4. action `a1`, reward `3`

Importance weights:

- for `a1`: `pi / b = 0.5 / 0.8 = 0.625`
- for `a2`: `pi / b = 0.5 / 0.2 = 2.5`

Weighted returns:

1. `0.625 * 4 = 2.5`
2. `0.625 * 2 = 1.25`
3. `2.5 * 7 = 17.5`
4. `0.625 * 3 = 1.875`

Ordinary importance-sampling estimate:

`(2.5 + 1.25 + 17.5 + 1.875) / 4 = 23.125 / 4 = 5.78125`

The large contribution from the single `a2` sample shows the central problem: even a small amount of mismatch between target and behavior policies can create very high-variance evaluation estimates.

Verification: the estimate equals the arithmetic mean of the four weighted returns.

## 5. What credible evaluation looks like

A credible RL evaluation stack usually includes:

- multiple random seeds
- held-out environments or perturbation tests
- sensitivity to reward weights and hyperparameters
- safety metrics separate from return
- ablations against simpler baselines
- when possible, off-policy evaluation or simulation-to-real transfer checks

Single-number leaderboard performance is not enough. A policy can be high reward, brittle, and unsafe at the same time.

## 6. Common Mistakes

1. **Benchmark overtrust**: assuming a policy that performs well in one simulator will generalize to deployment ignores environment mismatch; test under perturbations and alternate settings.
2. **Offline extrapolation optimism**: trusting high Q-values for poorly covered actions leads to dangerous overestimation; inspect dataset coverage and prefer conservative methods.
3. **Safety-as-penalty thinking**: treating critical constraints as small reward penalties invites violations when the reward tradeoff is favorable; use explicit constraints or shields for unacceptable failures.
4. **Single-seed reporting**: one lucky run hides instability and brittleness; report distributions across seeds and scenarios.
5. **No rollback path**: deploying a learned policy without intervention or rollback procedures turns evaluation mistakes into operational incidents; define operational safeguards before rollout.

## 7. Practical Checklist

- [ ] Separate task reward from safety costs and operational constraints in the problem statement.
- [ ] Measure dataset coverage before trusting offline RL training or evaluation.
- [ ] Run multiple seeds and perturbation tests before comparing policies.
- [ ] Report at least one safety or robustness metric alongside return.
- [ ] Use conservative baselines and simpler heuristics as deployment references.
- [ ] Define monitoring, rollback, and human-override procedures before real-world rollout.

## References

1. Richard S. Sutton and Andrew G. Barto, *Reinforcement Learning: An Introduction*. [http://incompleteideas.net/book/the-book-2nd.html](http://incompleteideas.net/book/the-book-2nd.html)
2. Sergey Levine et al., *Offline Reinforcement Learning: Tutorial, Review, and Perspectives on Open Problems*. [https://arxiv.org/abs/2005.01643](https://arxiv.org/abs/2005.01643)
3. Philip J. Thomas and Emma Brunskill, *Data-Efficient Off-Policy Policy Evaluation for Reinforcement Learning*. [https://proceedings.mlr.press/v48/thomasa16.html](https://proceedings.mlr.press/v48/thomasa16.html)
4. Javier Garcia and Fernando Fernandez, *A Comprehensive Survey on Safe Reinforcement Learning*. [https://jmlr.org/papers/v16/garcia15a.html](https://jmlr.org/papers/v16/garcia15a.html)
5. Aviral Kumar et al., *Conservative Q-Learning for Offline Reinforcement Learning*. [https://proceedings.neurips.cc/paper/2020/hash/0d2b2061826a66f3c60bd9b47b8f7f6a-Abstract.html](https://proceedings.neurips.cc/paper/2020/hash/0d2b2061826a66f3c60bd9b47b8f7f6a-Abstract.html)
6. Stanford CS234, *Offline RL and Safe RL Topics*. [https://web.stanford.edu/class/cs234/](https://web.stanford.edu/class/cs234/)
7. OpenAI Spinning Up, *RL Research Topics and Practical Concerns*. [https://spinningup.openai.com/](https://spinningup.openai.com/)
