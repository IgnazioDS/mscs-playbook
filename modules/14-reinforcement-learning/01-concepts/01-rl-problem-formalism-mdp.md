# Reinforcement Learning Problem Formalism and Markov Decision Processes

## Key Ideas
- Reinforcement learning studies how an agent improves decisions through interaction with an environment that returns rewards.
- A Markov decision process (MDP) defines states, actions, transitions, rewards, and a discount factor so the task can be analysed precisely.
- The Markov property matters because the current state must contain all information needed to predict the next-step distribution.
- A policy maps states to actions or action probabilities, and value functions measure expected long-term return under that policy.
- Clear task formalisation prevents later mistakes in reward design, evaluation, and algorithm choice.

## 1. Why reinforcement learning needs a formal model

Reinforcement learning is harder than supervised learning because the agent does not receive labelled correct actions for each state. Instead, it chooses actions, changes the future data it will see, and often receives delayed rewards. A formal model is necessary so terms like "good action" and "better policy" have precise meaning.

An MDP is the standard mathematical model. It contains:

- a **state** space `S`, where each state summarizes the current situation
- an **action** space `A`, where each action is a decision available to the agent
- a **transition model** `P(s' | s, a)`, the probability of reaching next state `s'` from state `s` after action `a`
- a **reward function** `R(s, a, s')`, the scalar feedback from that transition
- a **discount factor** `gamma`, with `0 <= gamma < 1`, which reduces the weight of far-future rewards

The **return** from time step `t` is the discounted sum of future rewards:

`G_t = R_{t+1} + gamma R_{t+2} + gamma^2 R_{t+3} + ...`

The discount factor is not only a modelling convenience. It expresses how much the task values long-term outcomes and ensures that infinite-horizon returns remain finite when rewards are bounded.

## 2. Policies, values, and optimality

A **policy** `pi` tells the agent what to do. In a deterministic policy, `pi(s)` returns one action. In a stochastic policy, `pi(a | s)` gives the probability of choosing action `a` in state `s`.

Two value functions define how good a policy is:

- the **state-value function** `V^pi(s)`, the expected return starting in state `s` and then following policy `pi`
- the **action-value function** `Q^pi(s, a)`, the expected return after taking action `a` in state `s` and then following `pi`

These values satisfy the Bellman expectation equations. For state values,

`V^pi(s) = sum_a pi(a | s) sum_s' P(s' | s, a) [R(s, a, s') + gamma V^pi(s')]`

An **optimal policy** `pi*` is one whose value is at least as high as every other policy in every state. Its value functions are `V*` and `Q*`. Much of reinforcement learning can be understood as different strategies for estimating these optimal quantities or directly searching for `pi*`.

## 3. Episodic and continuing tasks

An **episodic task** has clear terminal states, such as reaching a goal cell in gridworld or ending a game. Returns are naturally bounded by episode length. Monte Carlo methods fit well here because complete episodes are available.

A **continuing task** does not naturally terminate, such as load balancing or process control. In those settings, discounting or average-reward formulations are necessary. Continuing tasks make stability and evaluation harder because there is no single natural reset point.

This distinction matters when choosing algorithms:

- dynamic programming can handle either setting if the model is known
- Monte Carlo methods naturally fit episodic tasks
- temporal-difference methods work well for both episodic and continuing settings

## 4. Worked example: a two-state maintenance MDP

Consider a simple machine with two states:

- `Healthy`
- `Worn`

The actions are:

- `Run`
- `Repair`

Discount factor: `gamma = 0.9`

Transition and reward model:

1. From `Healthy`:
   - `Run` keeps the machine `Healthy` with probability `0.8` and reward `+5`
   - `Run` moves the machine to `Worn` with probability `0.2` and reward `+5`
   - `Repair` keeps it `Healthy` with certainty and reward `-2`
2. From `Worn`:
   - `Run` keeps it `Worn` with probability `0.7` and reward `+1`
   - `Run` breaks it to a terminal failure state with probability `0.3` and reward `-10`
   - `Repair` moves it to `Healthy` with certainty and reward `-2`

Suppose policy `pi` is:

- in `Healthy`, choose `Run`
- in `Worn`, choose `Repair`

Let `V(H)` mean `V^pi(Healthy)` and `V(W)` mean `V^pi(Worn)`.

Bellman equations:

1. For `Healthy`:

`V(H) = 0.8 * [5 + 0.9 V(H)] + 0.2 * [5 + 0.9 V(W)]`

`V(H) = 5 + 0.72 V(H) + 0.18 V(W)`

`0.28 V(H) - 0.18 V(W) = 5`

2. For `Worn`:

The policy always repairs, so:

`V(W) = -2 + 0.9 V(H)`

Substitute into the first equation:

`0.28 V(H) - 0.18(-2 + 0.9 V(H)) = 5`

`0.28 V(H) + 0.36 - 0.162 V(H) = 5`

`0.118 V(H) = 4.64`

`V(H) ≈ 39.32`

Now compute `V(W)`:

`V(W) = -2 + 0.9 * 39.32 ≈ 33.39`

Interpretation:

- the long-run value of keeping a healthy machine running under this policy is about `39.32`
- even the worn state is still valuable because the policy repairs it before catastrophic failure

Verification: substituting `V(H) ≈ 39.32` and `V(W) ≈ 33.39` back into both Bellman equations reproduces the same values up to rounding.

## 5. What goes wrong when the formalism is wrong

Many RL failures are not algorithm failures. They are modelling failures.

If the state omits important information, the process is no longer Markov from the agent's perspective. For example, if a robot state omits battery level, then the same visible location may require different actions depending on hidden charge. The agent will see inconsistent consequences and learn unstable values.

If the reward is misaligned with the real objective, optimisation amplifies the mistake. A navigation task rewarded only for speed may learn unsafe shortcuts. A recommendation system rewarded only for clicks may degrade long-term satisfaction.

If the action space is poorly defined, the agent may be unable to express desirable behaviour at all. A policy cannot learn to brake gently if the only available actions are `full_throttle` and `stop`.

## 6. Common Mistakes

1. **State aliasing**: treating different situations as the same state causes contradictory targets; add the missing task-relevant information or move to a partially observable formulation.
2. **Reward confusion**: mixing business metrics, safety penalties, and debugging signals without clear priority produces unstable optimisation; define the primary objective explicitly and document each reward term.
3. **Discount misuse**: choosing `gamma` by habit rather than task horizon distorts behaviour; tie `gamma` to how far into the future decisions should matter.
4. **Action-space mismatch**: using actions that are too coarse or too constrained prevents the agent from expressing good strategies; redesign the action set before tuning the algorithm.
5. **Evaluation leakage**: scoring a policy inside the same simulator assumptions used to define the reward hides modelling errors; test under perturbations and alternative scenarios.

## 7. Practical Checklist

- [ ] Write down `S`, `A`, `P`, `R`, and `gamma` before selecting an RL algorithm.
- [ ] Check whether the current state representation plausibly satisfies the Markov property.
- [ ] Decide whether the task is episodic or continuing and match the evaluation setup to that choice.
- [ ] Define at least one simple baseline policy for comparison.
- [ ] Compute one small Bellman-style example by hand to verify the task formalisation.
- [ ] Record how each reward component maps to the actual objective and constraints.

## References

1. Richard S. Sutton and Andrew G. Barto, *Reinforcement Learning: An Introduction*, 2nd ed. [http://incompleteideas.net/book/the-book-2nd.html](http://incompleteideas.net/book/the-book-2nd.html)
2. David Silver, *UCL Reinforcement Learning Lecture 1*. [https://www.davidsilver.uk/teaching/](https://www.davidsilver.uk/teaching/)
3. Stanford CS234, *Introduction to Reinforcement Learning*. [https://web.stanford.edu/class/cs234/](https://web.stanford.edu/class/cs234/)
4. Dimitri P. Bertsekas, *Dynamic Programming and Optimal Control*. [https://www.mit.edu/~dimitrib/dpbook.html](https://www.mit.edu/~dimitrib/dpbook.html)
5. OpenAI Spinning Up, *Key Concepts in RL*. [https://spinningup.openai.com/en/latest/spinningup/rl_intro.html](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html)
6. MIT Press, *Algorithms for Decision Making*. [https://algorithmsbook.com/](https://algorithmsbook.com/)
7. Csaba Szepesvari, *Algorithms for Reinforcement Learning*. [https://sites.ualberta.ca/~szepesva/rlbook.html](https://sites.ualberta.ca/~szepesva/rlbook.html)
