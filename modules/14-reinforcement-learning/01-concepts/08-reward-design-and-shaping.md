# Reward Design and Shaping

## Key Ideas
- Reward design defines what behavior the agent is incentivized to produce, so it is a specification problem before it is an optimization problem.
- Sparse rewards are often correct but difficult to learn from, while shaped rewards can accelerate learning if they preserve the original objective.
- Potential-based shaping is important because it changes learning speed without changing the optimal policy under standard assumptions.
- Reward hacking happens when the agent exploits loopholes in the proxy reward instead of achieving the real objective.
- Careful reward design requires ablations, behavioral inspection, and evaluation under altered conditions rather than trust in training curves alone.

## 1. Why reward design is the hardest part

An RL algorithm does exactly what the reward asks, not what the designer intended. This makes reward design unusually important. If the reward omits a safety constraint, overweights a proxy metric, or inconsistently scores similar outcomes, the agent will optimize those flaws.

This is why reward design should be treated as task specification. Before any shaping term is added, the desired outcome, prohibited behavior, and evaluation metric should be written down in plain language.

## 2. Sparse rewards, shaping, and policy preservation

A **sparse reward** is one that appears only at rare events, such as reaching a goal. Sparse rewards are often semantically clean but can make credit assignment extremely slow.

**Reward shaping** adds intermediate signals to guide learning. For example, in navigation one might add a term for reducing distance to the goal. The danger is that the shaped reward can change the objective.

**Potential-based shaping** avoids that by adding:

`F(s, s') = gamma Phi(s') - Phi(s)`

for some potential function `Phi`. Under standard conditions, this changes transient rewards but preserves the optimal policy.

## 3. Typical failure modes

Common reward failures include:

- **proxy mismatch**: the reward tracks a measurable proxy rather than the real goal
- **loophole exploitation**: the agent finds a way to score highly without doing the intended task
- **inconsistent scaling**: one reward term numerically dominates everything else
- **nonstationary semantics**: the same action is rewarded differently across contexts in ways not captured by the state

These are not rare corner cases. They are the default risk whenever the environment is rich and the reward is handcrafted.

## 4. Worked example: potential-based shaping in grid navigation

Suppose an agent moves on a line toward a goal at position `4`. The sparse task reward is:

- `+10` for entering the goal
- `0` otherwise

Discount factor: `gamma = 0.9`

Choose potential:

`Phi(s) = - distance_to_goal(s)`

Then:

- at position `1`, distance is `3`, so `Phi(1) = -3`
- at position `2`, distance is `2`, so `Phi(2) = -2`

Shaping reward from moving `1 -> 2`:

`F(1, 2) = 0.9 * Phi(2) - Phi(1)`

`F(1, 2) = 0.9 * (-2) - (-3) = -1.8 + 3 = 1.2`

Now consider moving `2 -> 3`:

- `Phi(3) = -1`

`F(2, 3) = 0.9 * (-1) - (-2) = -0.9 + 2 = 1.1`

Final move `3 -> 4` reaches the goal:

- sparse reward `= 10`
- `Phi(4) = 0`

Shaping term:

`F(3, 4) = 0.9 * 0 - (-1) = 1`

Total shaped reward on the final move:

`10 + 1 = 11`

The agent receives dense progress feedback on each step, but the shaping term is constructed so the optimal policy is preserved.

Verification: each shaping term equals `gamma Phi(s') - Phi(s)` using the stated potential values.

## 5. How to validate a reward

Reward design should be validated like an interface contract. Useful checks include:

- ablate each shaping term and compare behavior
- inspect trajectories, not only total return
- perturb the environment and see whether the policy keeps doing the intended task
- compare the proxy reward with a separate evaluation metric that reflects the real objective

If the policy improves reward while worsening the real objective, the problem is not training instability. It is a broken specification.

## 6. Common Mistakes

1. **Proxy overreach**: optimizing an easy-to-measure proxy instead of the real objective invites reward hacking; keep a separate evaluation metric for the true goal.
2. **Policy-changing shaping**: adding dense bonuses without checking whether they alter the optimal solution can train the wrong behavior; prefer potential-based shaping when possible.
3. **Scale imbalance**: one large penalty or bonus can dominate every other term numerically; inspect the empirical magnitude of each reward component.
4. **Behavior-free evaluation**: trusting scalar return without looking at trajectories hides exploitative shortcuts; review actual policy behavior under representative scenarios.
5. **Frozen reward assumptions**: leaving the reward untouched after obvious failure cases are observed slows iteration; treat reward design as part of system design, not a one-time constant.

## 7. Practical Checklist

- [ ] Write the intended task outcome in plain language before defining the numeric reward.
- [ ] Separate sparse objective reward from any shaping terms in the implementation.
- [ ] Measure the magnitude distribution of each reward component during training.
- [ ] Review trajectories for loopholes and unintended shortcuts.
- [ ] Use ablation tests to verify whether shaping improves learning speed without changing the goal.
- [ ] Maintain an external evaluation metric that the agent is not directly optimizing.

## References

1. Richard S. Sutton and Andrew G. Barto, *Reinforcement Learning: An Introduction*. [http://incompleteideas.net/book/the-book-2nd.html](http://incompleteideas.net/book/the-book-2nd.html)
2. Andrew Y. Ng, Daishi Harada, and Stuart Russell, *Policy Invariance Under Reward Transformations*. [https://www.andrewng.org/publications/policy-invariance-under-reward-transformations-theory-and-application-to-reward-shaping/](https://www.andrewng.org/publications/policy-invariance-under-reward-transformations-theory-and-application-to-reward-shaping/)
3. OpenAI, *Faulty Reward Functions in the Wild*. [https://openai.com/research/faulty-reward-functions](https://openai.com/research/faulty-reward-functions)
4. Dylan Hadfield-Menell et al., *The Off-Switch Game*. [https://arxiv.org/abs/1611.08219](https://arxiv.org/abs/1611.08219)
5. DeepMind, *Specification Gaming Examples in AI*. [https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/](https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/)
6. Stanford CS234, *Reward Design and Inverse RL Context*. [https://web.stanford.edu/class/cs234/](https://web.stanford.edu/class/cs234/)
7. David Silver, *Advanced RL Lecture Materials*. [https://www.davidsilver.uk/teaching/](https://www.davidsilver.uk/teaching/)
