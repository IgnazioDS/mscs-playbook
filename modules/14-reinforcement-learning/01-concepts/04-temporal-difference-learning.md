# Temporal-Difference Learning

## Key Ideas
- Temporal-difference learning updates value estimates from one-step or multi-step targets before the episode ends.
- TD methods bootstrap, meaning they use current estimates to improve future estimates.
- TD prediction reduces variance relative to Monte Carlo methods, but it introduces bias through the bootstrap target.
- SARSA and Q-learning are the canonical control algorithms that show the difference between on-policy and off-policy learning.
- Temporal-difference methods are the practical bridge from tabular RL to large-scale approximate RL.

## 1. Why temporal-difference learning is central

Temporal-difference (TD) learning matters because it combines two useful properties:

- like Monte Carlo, it learns from raw experience without a model
- like dynamic programming, it updates from bootstrapped estimates rather than waiting for full returns

That combination makes TD methods sample efficient and online. An agent can improve after each transition instead of after each episode. This is why TD ideas sit at the center of modern RL systems.

## 2. Prediction with TD(0)

For a transition `S_t -> S_{t+1}` with reward `R_{t+1}`, TD(0) updates:

`V(S_t) = V(S_t) + alpha [R_{t+1} + gamma V(S_{t+1}) - V(S_t)]`

The bracketed term is the **TD error**:

`delta_t = R_{t+1} + gamma V(S_{t+1}) - V(S_t)`

This error measures surprise relative to the current estimate. A positive TD error means the state was better than expected. A negative error means it was worse.

The worst-case time per transition update is `Theta(1)` for tabular TD(0), and space is `Theta(|S|)` for the value table.

## 3. SARSA, Q-learning, and the meaning of on-policy

For control, TD methods usually learn action values.

**SARSA** updates from the action actually taken next:

`Q(S_t, A_t) = Q(S_t, A_t) + alpha [R_{t+1} + gamma Q(S_{t+1}, A_{t+1}) - Q(S_t, A_t)]`

Because the next action comes from the current behavior policy, SARSA is **on-policy**.

**Q-learning** updates toward the greedy next action:

`Q(S_t, A_t) = Q(S_t, A_t) + alpha [R_{t+1} + gamma max_a Q(S_{t+1}, a) - Q(S_t, A_t)]`

Because its target assumes greedy control regardless of the behavior policy, Q-learning is **off-policy**.

This distinction matters in risky settings. SARSA often learns safer behavior under persistent exploration because its updates account for the possibility of exploratory mistakes. Q-learning often pursues more aggressive optimal values.

## 4. Worked example: one-step Q-learning updates

Suppose `gamma = 0.9` and learning rate `alpha = 0.5`.

Current action values:

- `Q(s0, left) = 2`
- `Q(s0, right) = 4`
- `Q(s1, left) = 3`
- `Q(s1, right) = 5`

Observed transition:

- start in `s0`
- take action `left`
- receive reward `1`
- arrive in `s1`

Q-learning target:

`target = 1 + 0.9 * max(Q(s1, left), Q(s1, right))`

`target = 1 + 0.9 * max(3, 5) = 1 + 4.5 = 5.5`

TD error:

`delta = 5.5 - Q(s0, left) = 5.5 - 2 = 3.5`

Updated value:

`Q_new(s0, left) = 2 + 0.5 * 3.5 = 2 + 1.75 = 3.75`

Now suppose a second transition from `s1`:

- take action `right`
- receive reward `2`
- move to terminal

Terminal next-state value is `0`, so:

`target = 2`

`delta = 2 - 5 = -3`

`Q_new(s1, right) = 5 + 0.5 * (-3) = 3.5`

Verification: each update equals old estimate plus `alpha` times the corresponding TD error.

## 5. Eligibility traces and multi-step targets

One-step TD is not the only choice. Multi-step returns blend immediate samples with future estimates over several steps. **Eligibility traces** distribute TD error backward across recently visited states or state-action pairs. TD(`lambda`) interpolates between:

- Monte Carlo at `lambda = 1`
- one-step TD at `lambda = 0`

This matters because different tasks benefit from different bias-variance tradeoffs. Short horizons often tolerate one-step backups well. Sparse delayed rewards often benefit from multi-step propagation.

## 6. Common Mistakes

1. **Learning-rate instability**: using a large `alpha` can make values oscillate or diverge; start conservatively and monitor value ranges over time.
2. **Terminal bootstrap leakage**: bootstrapping from terminal states adds nonexistent future reward; set the next-state value to zero at termination.
3. **On-policy/off-policy confusion**: mixing SARSA logic with Q-learning targets changes the algorithm unintentionally; define the update target before coding.
4. **Exploration neglect**: evaluating TD control with almost no exploration locks in bad early estimates; maintain a stated exploration schedule.
5. **Overinterpreting single runs**: TD learning is stochastic and seed-sensitive; compare multiple runs before drawing conclusions about performance.

## 7. Practical Checklist

- [ ] Write the exact TD target formula for the algorithm you intend to use.
- [ ] Handle terminal transitions with explicit no-bootstrap logic.
- [ ] Track TD error statistics alongside rewards and returns.
- [ ] Log the exploration parameter, such as `epsilon`, for every training run.
- [ ] Compare SARSA and Q-learning on at least one environment where risky exploration matters.
- [ ] Use multiple random seeds before judging convergence or sample efficiency.

## References

1. Richard S. Sutton and Andrew G. Barto, *Reinforcement Learning: An Introduction*, Chapters 6 and 7. [http://incompleteideas.net/book/the-book-2nd.html](http://incompleteideas.net/book/the-book-2nd.html)
2. Christopher J. C. H. Watkins and Peter Dayan, *Q-learning*. [https://link.springer.com/article/10.1007/BF00992698](https://link.springer.com/article/10.1007/BF00992698)
3. David Silver, *Lecture 4: Model-Free Prediction and Control*. [https://www.davidsilver.uk/teaching/](https://www.davidsilver.uk/teaching/)
4. Stanford CS234, *Temporal-Difference Learning*. [https://web.stanford.edu/class/cs234/](https://web.stanford.edu/class/cs234/)
5. OpenAI Spinning Up, *Key Concepts and Algorithms*. [https://spinningup.openai.com/](https://spinningup.openai.com/)
6. Ronald J. Williams and Leemon C. Baird, *Tight Performance Bounds on Greedy Policies*. [https://proceedings.neurips.cc/paper/1993](https://proceedings.neurips.cc/paper/1993)
7. Csaba Szepesvari, *Algorithms for Reinforcement Learning*. [https://sites.ualberta.ca/~szepesva/rlbook.html](https://sites.ualberta.ca/~szepesva/rlbook.html)
