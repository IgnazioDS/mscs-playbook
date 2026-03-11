# Policy Gradient and Actor-Critic Methods

## Key Ideas
- Policy gradient methods optimize policy parameters directly instead of deriving a policy from a value table.
- Direct policy optimization is especially useful when the action space is continuous or stochastic actions are part of the task.
- The policy gradient theorem expresses the gradient of expected return without differentiating through the environment dynamics.
- Actor-critic methods reduce gradient variance by pairing a policy learner with a value-based critic.
- Stable policy optimization depends heavily on trust-region-like constraints, advantage estimation, and careful monitoring.

## 1. Why direct policy optimization matters

Value-based methods work well in discrete action settings, but they become awkward when the action space is continuous or high dimensional. A robot torque controller cannot realistically enumerate every possible action and take a `max` over them at each step. Policy methods solve this by parameterizing the policy itself.

If a policy is written as `pi_theta(a | s)`, then the objective is typically the expected discounted return `J(theta)`. Instead of estimating optimal action values and extracting a greedy policy, policy gradient methods move `theta` in a direction that increases `J(theta)`.

## 2. The policy gradient theorem and REINFORCE

The policy gradient theorem gives:

`grad J(theta) proportional to E[grad log pi_theta(A_t | S_t) * Q^pi(S_t, A_t)]`

This matters because it avoids differentiating through the state distribution in full detail. In practice, REINFORCE estimates the gradient with sampled returns:

`grad estimate = sum_t grad log pi_theta(A_t | S_t) * G_t`

REINFORCE is conceptually clean but high variance. The gradient direction is correct in expectation, yet single trajectories can produce noisy updates.

## 3. Actor-critic and variance reduction

A **baseline** subtracts a state-dependent quantity from returns without biasing the expected gradient. Using the state value `V(s)` as the baseline leads to the **advantage**:

`A(s, a) = Q(s, a) - V(s)`

An **actor-critic** method has:

- an **actor**, which updates the policy
- a **critic**, which estimates value information used to reduce variance

This architecture usually learns faster than plain REINFORCE because the actor no longer relies only on complete returns. Modern variants often use generalized advantage estimation, clipped objectives, or KL penalties to keep updates from moving too far in one step.

## 4. Worked example: a simple softmax policy update

Suppose a policy in state `s` chooses between actions `left` and `right` with a softmax over preferences:

- `h(left) = 0.2`
- `h(right) = -0.2`

Then:

- `pi(left | s) = e^{0.2} / (e^{0.2} + e^{-0.2}) ≈ 1.221 / (1.221 + 0.819) ≈ 0.599`
- `pi(right | s) ≈ 0.401`

Assume the agent sampled `left` and the estimated advantage for that action was `A = 3`.

For a softmax policy with two actions, the log-policy gradient for the selected action's preference is:

`grad log pi(left | s) = 1 - pi(left | s) ≈ 1 - 0.599 = 0.401`

Let learning rate `alpha = 0.1`.

Preference update for `left`:

`delta h(left) = alpha * A * grad log pi(left | s)`

`delta h(left) = 0.1 * 3 * 0.401 = 0.1203`

New preference:

`h_new(left) = 0.2 + 0.1203 = 0.3203`

The probability of choosing `left` increases because the sampled action had positive advantage. Using the same two-action normalization:

- `e^{0.3203} ≈ 1.378`
- `e^{-0.2} ≈ 0.819`

New probability:

`pi_new(left | s) ≈ 1.378 / (1.378 + 0.819) ≈ 0.627`

Verification: the policy's probability for `left` increased from about `0.599` to about `0.627`, which is consistent with a positive-advantage update.

## 5. Stability concerns in practice

Policy methods can collapse if updates are too large. The policy may become nearly deterministic too early, which destroys exploration and traps training in poor local behavior. This is why implementations track:

- entropy, to measure action diversity
- KL divergence, to measure how far the new policy moved from the old one
- advantage statistics, to detect unstable scaling

Proximal Policy Optimization (PPO) became widely used because clipping the objective limits how aggressively the policy can change on one batch.

## 6. Common Mistakes

1. **Variance blindness**: using raw returns without a baseline makes gradients noisy and slow; add a critic or at least a state-dependent baseline.
2. **Entropy collapse**: allowing the policy to become deterministic too early kills exploration; monitor entropy and use explicit regularization when needed.
3. **Advantage mis-scaling**: very large or poorly normalized advantages produce unstable steps; inspect advantage distributions and normalize deliberately.
4. **Critic overtrust**: treating a poorly trained critic as ground truth biases the actor update quality; debug critic loss and value calibration separately.
5. **Single-batch conclusions**: policy learning is high variance across seeds and batches; compare multiple runs before declaring improvement.

## 7. Practical Checklist

- [ ] Use policy methods only when direct action optimization is genuinely useful for the task.
- [ ] Track entropy, KL divergence, and return curves together during training.
- [ ] Verify that the critic is learning meaningful values before relying on actor-critic speedups.
- [ ] Normalize or otherwise stabilize advantages before large-batch updates.
- [ ] Compare a policy-gradient baseline against a simpler value-based baseline on reduced tasks.
- [ ] Run several seeds and report variability, not only the best run.

## References

1. Richard S. Sutton and Andrew G. Barto, *Reinforcement Learning: An Introduction*, Chapter 13. [http://incompleteideas.net/book/the-book-2nd.html](http://incompleteideas.net/book/the-book-2nd.html)
2. Ronald J. Williams, *Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning*. [https://link.springer.com/article/10.1007/BF00992696](https://link.springer.com/article/10.1007/BF00992696)
3. John Schulman et al., *High-Dimensional Continuous Control Using Generalized Advantage Estimation*. [https://arxiv.org/abs/1506.02438](https://arxiv.org/abs/1506.02438)
4. John Schulman et al., *Proximal Policy Optimization Algorithms*. [https://arxiv.org/abs/1707.06347](https://arxiv.org/abs/1707.06347)
5. David Silver, *Lecture 7: Policy Gradient Methods*. [https://www.davidsilver.uk/teaching/](https://www.davidsilver.uk/teaching/)
6. OpenAI Spinning Up, *Policy Optimization*. [https://spinningup.openai.com/en/latest/](https://spinningup.openai.com/en/latest/)
7. Stanford CS234, *Policy Gradient and Actor-Critic*. [https://web.stanford.edu/class/cs234/](https://web.stanford.edu/class/cs234/)
