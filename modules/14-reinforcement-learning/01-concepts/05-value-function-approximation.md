# Value Function Approximation

## Key Ideas
- Tabular methods fail in large or continuous state spaces, so value functions must often be approximated with parameterized models.
- Linear approximation is the simplest scalable baseline because its behaviour is easier to analyse than deep networks.
- Bootstrapping, off-policy learning, and function approximation can interact badly and cause divergence.
- Feature design, normalization, and target construction often matter as much as model size.
- Approximation methods make generalization possible, but they also introduce optimisation error and representation error.

## 1. Why approximation is unavoidable

Tabular RL assumes a separate memory slot for every state or state-action pair. That assumption collapses in realistic problems. A robot with continuous position and velocity already has infinitely many possible states. A recommender system may have millions of user-item contexts.

Function approximation solves this by learning parameters `w` so that:

- `V(s) ≈ v_hat(s, w)` for state values
- `Q(s, a) ≈ q_hat(s, a, w)` for action values

The goal is not only compression. Approximation also allows **generalization**, meaning experience in one part of the state space influences predictions in similar parts of the state space.

## 2. Linear approximation and supervised-style updates

In linear value approximation, features `x(s)` represent the state and:

`v_hat(s, w) = w^T x(s)`

If a target `y` is available, a common update is stochastic gradient descent on squared error:

`w = w + alpha [y - v_hat(s, w)] x(s)`

With Monte Carlo targets, this resembles standard regression. With TD targets, the target itself depends on current estimates. That dependency is what makes RL optimisation less stable than ordinary supervised learning.

Worst-case time per update for dense linear features of dimension `d` is `Theta(d)`, and space is `Theta(d)`.

## 3. The deadly triad

Three ingredients are individually useful:

- **function approximation**
- **bootstrapping**
- **off-policy learning**

Together, they can produce divergence. This interaction is often called the **deadly triad**. Q-learning with nonlinear approximation can push estimates upward in parts of the state-action space that are poorly supported by data. Experience replay, target networks, conservative objectives, and careful evaluation all exist partly to reduce this instability.

## 4. Worked example: one linear TD update

Suppose a state is represented by two features:

`x(s) = [1, 2]`

Current weight vector:

`w = [0.5, 1.0]`

Estimated value:

`v_hat(s, w) = 0.5 * 1 + 1.0 * 2 = 2.5`

Observed transition:

- reward `R_{t+1} = 3`
- next state features `x(s') = [1, 1]`
- current estimate at next state:

`v_hat(s', w) = 0.5 * 1 + 1.0 * 1 = 1.5`

Let `gamma = 0.9` and `alpha = 0.1`.

TD target:

`y = 3 + 0.9 * 1.5 = 4.35`

TD error:

`y - v_hat(s, w) = 4.35 - 2.5 = 1.85`

Weight update:

`w_new = w + 0.1 * 1.85 * [1, 2]`

`w_new = [0.5, 1.0] + [0.185, 0.37] = [0.685, 1.37]`

New estimate for the original state:

`v_hat(s, w_new) = 0.685 * 1 + 1.37 * 2 = 3.425`

The estimate moved toward the TD target `4.35`, but not all the way because the learning rate is less than `1`.

Verification: the change in each weight equals `alpha * TD_error * feature_value`.

## 5. Deep value approximation

Deep neural networks extend the same idea with learned nonlinear features. This enables performance on high-dimensional observations such as images, but it introduces fragile optimisation. DQN became influential because it combined several stabilizers:

- experience replay to decorrelate updates
- a target network to slow target drift
- reward clipping and careful preprocessing

Those ideas did not remove approximation risk. They made it manageable enough for some benchmarks.

## 6. Common Mistakes

1. **Feature neglect**: assuming approximation will fix a poor state representation leads to brittle learning; inspect whether important task structure is even representable.
2. **Unscaled inputs**: feeding features with wildly different magnitudes into the approximator causes unstable optimisation; normalize or standardize inputs deliberately.
3. **Off-policy overconfidence**: trusting Q estimates in regions rarely seen in data creates severe extrapolation error; monitor coverage and use conservative evaluation.
4. **Tabular-baseline omission**: jumping directly to neural approximation hides whether the task or the optimiser is failing; solve a reduced tabular version first when possible.
5. **Loss-only monitoring**: a decreasing training loss does not guarantee better policy quality; track returns, value ranges, and policy behaviour together.

## 7. Practical Checklist

- [ ] State clearly what is being approximated: `V`, `Q`, or an advantage-like quantity.
- [ ] Normalize features or observations before tuning the optimiser.
- [ ] Start with a linear or otherwise interpretable baseline when the state representation allows it.
- [ ] Monitor value magnitudes, target magnitudes, and return distributions together.
- [ ] Compare on-policy and off-policy training stability if the design allows either.
- [ ] Use a small benchmark problem to sanity-check approximation updates before scaling.

## References

1. Richard S. Sutton and Andrew G. Barto, *Reinforcement Learning: An Introduction*, Chapter 9. [http://incompleteideas.net/book/the-book-2nd.html](http://incompleteideas.net/book/the-book-2nd.html)
2. Volodymyr Mnih et al., *Human-level control through deep reinforcement learning*. [https://www.nature.com/articles/nature14236](https://www.nature.com/articles/nature14236)
3. David Silver, *Lecture 6: Value Function Approximation*. [https://www.davidsilver.uk/teaching/](https://www.davidsilver.uk/teaching/)
4. Stanford CS234, *Function Approximation and Deep RL*. [https://web.stanford.edu/class/cs234/](https://web.stanford.edu/class/cs234/)
5. OpenAI Spinning Up, *Deep RL Intro*. [https://spinningup.openai.com/en/latest/spinningup/rl_intro2.html](https://spinningup.openai.com/en/latest/spinningup/rl_intro2.html)
6. Hado van Hasselt, Arthur Guez, and David Silver, *Deep Reinforcement Learning with Double Q-learning*. [https://ojs.aaai.org/index.php/AAAI/article/view/10295](https://ojs.aaai.org/index.php/AAAI/article/view/10295)
7. Csaba Szepesvari, *Algorithms for Reinforcement Learning*. [https://sites.ualberta.ca/~szepesva/rlbook.html](https://sites.ualberta.ca/~szepesva/rlbook.html)
