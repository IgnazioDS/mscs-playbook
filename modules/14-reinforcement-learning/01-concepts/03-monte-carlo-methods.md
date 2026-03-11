# Monte Carlo Methods in Reinforcement Learning

## Key Ideas
- Monte Carlo methods estimate values from complete sampled returns, so they do not need a transition model.
- Because updates wait for episode completion, Monte Carlo methods fit naturally in episodic tasks.
- First-visit and every-visit estimators differ in how many times a state contributes within one episode.
- Monte Carlo control improves a policy by making it more greedy with respect to sampled action values while preserving exploration.
- Off-policy Monte Carlo requires importance sampling, which is unbiased in theory but often high variance in practice.

## 1. Why Monte Carlo methods matter

Dynamic programming assumes access to the model, but many environments provide only sampled experience. Monte Carlo (MC) methods show how to estimate values directly from those samples without bootstrapping. They are conceptually simple: observe what happened after visiting a state, compute the return, and average those returns over many episodes.

This simplicity matters pedagogically. MC methods make the distinction between **sampled returns** and **bootstrapped targets** explicit. They also expose the variance problem that later temporal-difference methods try to reduce.

## 2. Prediction from complete returns

For a state visited at time `t`, the return is:

`G_t = R_{t+1} + gamma R_{t+2} + ... + gamma^{T-t-1} R_T`

In **first-visit MC**, a state contributes only the first time it appears in an episode. In **every-visit MC**, every occurrence contributes a return sample. Both estimators converge under standard assumptions, though their finite-sample behavior differs.

The expected worst-case time to process one episode return table is `O(T)` where `T` is the episode length, and the worst-case space to store that episode is also `O(T)` if all rewards and states are retained before updates.

## 3. On-policy and off-policy control

For control, MC methods usually estimate action values `Q(s, a)` and then improve the policy. A purely greedy policy can stop exploring too soon, so MC control often uses **epsilon-greedy** improvement:

- with probability `1 - epsilon`, choose the current best action
- with probability `epsilon`, choose a random action

This ensures continued exploration.

In **off-policy MC**, the policy that generates data, called the **behavior policy**, differs from the target policy being evaluated. Importance sampling corrects this mismatch using a weight:

`rho = product over k of pi(A_k | S_k) / b(A_k | S_k)`

These ratios can explode when the target and behavior policies differ strongly, which is why off-policy MC is statistically delicate.

## 4. Worked example: first-visit Monte Carlo evaluation

Suppose an episodic environment has discount factor `gamma = 1` and we want `V(start)` under a fixed policy.

Observed episodes:

1. Episode 1:
   - `start -> mid -> terminal`
   - rewards: `+2`, `+3`
2. Episode 2:
   - `start -> terminal`
   - reward: `+4`
3. Episode 3:
   - `start -> mid -> terminal`
   - rewards: `+1`, `+5`

First-visit returns for `start`:

- Episode 1: `G = 2 + 3 = 5`
- Episode 2: `G = 4`
- Episode 3: `G = 1 + 5 = 6`

Monte Carlo estimate:

`V(start) = (5 + 4 + 6) / 3 = 15 / 3 = 5`

Now estimate `V(mid)` using first visits:

- Episode 1: `G = 3`
- Episode 3: `G = 5`

`V(mid) = (3 + 5) / 2 = 4`

Interpretation:

- `start` has estimated value `5`
- `mid` has estimated value `4`

Verification: the computed values equal the arithmetic mean of the observed complete returns for each state's first visit.

## 5. Strengths and limitations

Monte Carlo methods are unbiased with respect to sampled returns because they do not bootstrap from current estimates. That can make them easier to reason about than TD methods. They also work well when episodes are natural, such as games and finite-horizon tasks.

Their weakness is variance. When rewards arrive far in the future or episodes are long, return estimates fluctuate heavily. MC methods also cannot update until an episode finishes, which slows learning in continuing problems or tasks with rare termination.

## 6. Common Mistakes

1. **Episode-truncation confusion**: treating an interrupted rollout as a terminal episode biases returns; distinguish genuine termination from logging or time-limit truncation.
2. **Exploration collapse**: switching to a greedy policy too early prevents new action values from being estimated; keep an explicit exploration mechanism during control.
3. **Importance-weight explosion**: using plain importance sampling with mismatched behavior and target policies creates unstable estimates; prefer weighted variants or reduce policy mismatch.
4. **State-visit double counting**: mixing first-visit and every-visit updates without intention changes the estimator; choose one definition and implement it consistently.
5. **Continuing-task misuse**: applying plain episodic MC to continuing control problems without resets or truncation logic leaves targets undefined; use TD methods or a carefully designed episodic surrogate.

## 7. Practical Checklist

- [ ] Confirm that the task is episodic or that episodes are defined in a principled way.
- [ ] Decide explicitly between first-visit and every-visit estimation.
- [ ] Log complete trajectories so returns can be reproduced during debugging.
- [ ] Keep an exploration policy such as epsilon-greedy during control.
- [ ] Plot return variance across episodes before concluding that learning is unstable.
- [ ] Treat off-policy importance weights as a stability risk and monitor their magnitude.

## References

1. Richard S. Sutton and Andrew G. Barto, *Reinforcement Learning: An Introduction*, Chapter 5. [http://incompleteideas.net/book/the-book-2nd.html](http://incompleteideas.net/book/the-book-2nd.html)
2. David Silver, *Lecture 4: Model-Free Prediction and Control*. [https://www.davidsilver.uk/teaching/](https://www.davidsilver.uk/teaching/)
3. Stanford CS234, *Monte Carlo and Temporal-Difference Learning*. [https://web.stanford.edu/class/cs234/](https://web.stanford.edu/class/cs234/)
4. OpenAI Spinning Up, *Intro to RL*. [https://spinningup.openai.com/en/latest/spinningup/rl_intro.html](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html)
5. Andras Lazaric, *Reinforcement Learning Lecture Notes*. [https://rltheorybook.github.io/](https://rltheorybook.github.io/)
6. Csaba Szepesvari, *Algorithms for Reinforcement Learning*. [https://sites.ualberta.ca/~szepesva/rlbook.html](https://sites.ualberta.ca/~szepesva/rlbook.html)
7. Warren B. Powell, *Reinforcement Learning and Stochastic Optimization*. [https://castlelab.princeton.edu/RLSO/](https://castlelab.princeton.edu/RLSO/)
