# Dynamic Programming for Policy Evaluation and Control

## Key Ideas
- Dynamic programming assumes the transition model and reward model are known exactly, which makes it a planning method rather than a model-free learning method.
- Policy evaluation computes the value of a fixed policy, while policy improvement uses those values to build a better policy.
- Policy iteration alternates evaluation and improvement until the policy stops changing.
- Value iteration folds evaluation and improvement into a single Bellman optimality backup and often reaches a good solution faster.
- Dynamic programming is usually computationally feasible only for small or structured state spaces, but it defines the core equations used by later RL algorithms.

## 1. Why dynamic programming comes first

Dynamic programming (DP) matters because it exposes the structure of optimal control without the noise of sampling. When the full MDP is known, DP can compute exact values up to numerical tolerance. That makes it the cleanest place to understand Bellman updates, contraction arguments, and the relationship between values and policies.

DP is not usually the final tool used in real deployments. The state space is often too large, the transition model is unknown, or the environment is only available as a simulator. Even so, nearly every RL method is a sampled or approximate version of a DP idea.

## 2. Policy evaluation and policy iteration

For a fixed policy `pi`, iterative policy evaluation repeatedly applies the Bellman expectation backup:

`V_{k+1}(s) = sum_a pi(a | s) sum_s' P(s' | s, a) [R(s, a, s') + gamma V_k(s')]`

Because the Bellman operator for a fixed policy is a contraction when `0 <= gamma < 1`, repeated application converges to `V^pi`.

Once `V^pi` is available, policy improvement acts greedily with respect to that value:

`pi_new(s) = argmax_a sum_s' P(s' | s, a) [R(s, a, s') + gamma V^pi(s')]`

If the improved policy differs from the old one, the policy was not optimal. Repeating evaluation and improvement yields **policy iteration**.

## 3. Value iteration and computational tradeoffs

Value iteration uses the Bellman optimality backup directly:

`V_{k+1}(s) = max_a sum_s' P(s' | s, a) [R(s, a, s') + gamma V_k(s')]`

After convergence, the greedy policy with respect to `V` is optimal.

The worst-case time per full sweep is `Theta(|S|^2 |A|)` when transitions from each state-action pair may reach all states. Space is `Theta(|S|)` for the value table if the model is stored separately, or much larger if transition probabilities are stored explicitly.

Value iteration often performs fewer outer loops than policy iteration, but each method can be preferable depending on the problem structure. Modified policy iteration sits between the two by doing only partial evaluation before improving the policy.

## 4. Worked example: value iteration on a three-state chain

Consider an episodic chain with states:

- `s0` start
- `s1` middle
- `goal` terminal

Actions:

- at `s0`: `stay`, `advance`
- at `s1`: `back`, `finish`

Transitions and rewards:

1. At `s0`
   - `stay` leads to `s0` with reward `0`
   - `advance` leads to `s1` with reward `0`
2. At `s1`
   - `back` leads to `s0` with reward `0`
   - `finish` leads to `goal` with reward `10`
3. `goal` is terminal with value `0`

Discount factor: `gamma = 0.9`

Start with `V_0(s0) = 0`, `V_0(s1) = 0`.

First sweep:

- `V_1(s1) = max(0 + 0.9 V_0(s0), 10 + 0.9 * 0) = max(0, 10) = 10`
- `V_1(s0) = max(0 + 0.9 V_0(s0), 0 + 0.9 V_0(s1)) = max(0, 0) = 0`

Second sweep:

- `V_2(s1) = max(0 + 0.9 V_1(s0), 10) = max(0, 10) = 10`
- `V_2(s0) = max(0 + 0.9 * 0, 0 + 0.9 * 10) = 9`

Third sweep:

- `V_3(s1) = max(0 + 0.9 * 9, 10) = max(8.1, 10) = 10`
- `V_3(s0) = max(0 + 0.9 * 9, 0 + 0.9 * 10) = max(8.1, 9) = 9`

The values have stabilized:

- `V*(s1) = 10`
- `V*(s0) = 9`

Optimal policy:

- at `s0`, choose `advance`
- at `s1`, choose `finish`

Verification: taking `advance` then `finish` yields return `0 + 0.9 * 10 = 9`, which matches `V*(s0)`.

## 5. When dynamic programming breaks down

DP becomes impractical when the state or action space is large because every sweep must examine all relevant state-action-next-state combinations. That is the **curse of dimensionality**. If a robot state includes position, velocity, battery temperature, tool orientation, and sensor mode, a tabular model becomes enormous.

DP also depends on accurate transition probabilities and rewards. If the model is wrong, the computed policy is exactly optimal for the wrong environment. This is why sampled methods and model learning become necessary in realistic settings.

## 6. Common Mistakes

1. **Model optimism**: assuming the transition table is accurate when it is estimated or incomplete produces misleading policies; separate planning with a known model from learning with uncertainty.
2. **Loose convergence checks**: stopping after a few sweeps can freeze a visibly suboptimal policy; track the maximum value change per sweep and use a stated tolerance.
3. **Terminal-state confusion**: forgetting that terminal values should not bootstrap into future rewards causes inflated estimates; handle absorbing states explicitly.
4. **State-space explosion**: tabulating every variable combination without abstraction makes the method unusable; aggregate states or move to approximation methods when scale demands it.
5. **Policy-improvement shortcuts**: changing the policy before values are even roughly stable can produce noisy oscillation; use value iteration intentionally or complete enough evaluation before improvement.

## 7. Practical Checklist

- [ ] Confirm that the environment model is known and trusted before using dynamic programming as the main method.
- [ ] Write the Bellman backup equation for one state by hand before coding full sweeps.
- [ ] Track the maximum absolute value update `delta` at each iteration.
- [ ] Treat terminal states and absorbing transitions explicitly in the implementation.
- [ ] Compare policy iteration and value iteration on a small toy problem before scaling up.
- [ ] Use DP results as a sanity baseline for later sampled methods when possible.

## References

1. Richard S. Sutton and Andrew G. Barto, *Reinforcement Learning: An Introduction*, Chapter 4. [http://incompleteideas.net/book/the-book-2nd.html](http://incompleteideas.net/book/the-book-2nd.html)
2. Dimitri P. Bertsekas, *Dynamic Programming and Optimal Control*. [https://www.mit.edu/~dimitrib/dpbook.html](https://www.mit.edu/~dimitrib/dpbook.html)
3. David Silver, *Lecture 2: Markov Decision Processes*. [https://www.davidsilver.uk/teaching/](https://www.davidsilver.uk/teaching/)
4. Stanford CS234, *Bellman Equations and Dynamic Programming*. [https://web.stanford.edu/class/cs234/](https://web.stanford.edu/class/cs234/)
5. Ronald Bellman, *Dynamic Programming*. [https://press.princeton.edu/books/paperback/9780691651873/dynamic-programming](https://press.princeton.edu/books/paperback/9780691651873/dynamic-programming)
6. MIT Press, *Algorithms for Decision Making*. [https://algorithmsbook.com/](https://algorithmsbook.com/)
7. Csaba Szepesvari, *Algorithms for Reinforcement Learning*. [https://sites.ualberta.ca/~szepesva/rlbook.html](https://sites.ualberta.ca/~szepesva/rlbook.html)
