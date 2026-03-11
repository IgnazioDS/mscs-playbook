# Intelligent Agents and Rationality

## Key Ideas

- An intelligent agent maps percept history to actions in order to achieve a defined performance objective.
- Rationality is about choosing actions that maximize expected performance given the available information, not about perfect knowledge or omniscience.
- The environment type determines what kinds of agent architecture are appropriate, because fully observable, deterministic worlds are easier than partially observable, stochastic ones.
- Agent design starts from the performance measure and task environment, not from a favored algorithm.
- A system can be highly capable yet irrational for its task if its objective, assumptions, or action model are misaligned with the environment.

## 1. What an Agent Is

An **agent** is an entity that perceives its environment through sensors and acts on that environment through actuators. The behavior of the agent can be viewed as a function from percept history to action.

This framing matters because it ties intelligence to action under uncertainty rather than to abstract reasoning alone.

### 1.1 Core Terms

- A **percept** is one observation received from the environment.
- A **percept sequence** is the history of observations seen so far.
- A **performance measure** defines what success means for the task.
- The **task environment** specifies the world, sensors, actions, and success criteria.

## 2. What Rationality Means

A rational agent does not always pick the objectively best action in hindsight. It picks the action expected to perform best according to:

- what it has observed
- what it knows about the environment
- what actions are available
- how success is measured

This is why rationality depends on the performance measure. A route-planning agent optimized only for distance may be irrational if the real objective includes safety or toll cost.

## 3. Agent Types

Common agent patterns include:

- simple reflex agents
- model-based agents
- goal-based agents
- utility-based agents
- learning agents

These are not status levels. They are design responses to different environment constraints.

## 4. Worked Example: Vacuum Agent Rationality

Suppose a vacuum agent operates in two rooms, `A` and `B`.

Performance measure:

- `+10` for each clean room at the end
- `-1` for each move
- `-2` for each unnecessary suction action

Current percept:

```text
location = A
room A = dirty
room B = unknown
```

### 4.1 Candidate Actions

- `suck`
- `move_to_B`

### 4.2 Immediate Reasoning

If the agent chooses `suck`, it cleans room `A` immediately and avoids a move cost. If it chooses `move_to_B` first, it pays a move penalty while leaving a known dirty room unchanged.

Under the current percept history, `suck` dominates `move_to_B`.

### 4.3 Rational Choice

The rational action is:

```text
action = suck
```

Verification: given a known dirty room and a cost for moving, cleaning the current room first gives higher expected performance than moving away.

## 5. Why Task Environments Matter

Agent behavior cannot be judged in isolation. The same agent may be rational in one environment and irrational in another.

Important environment dimensions include:

- fully versus partially observable
- deterministic versus stochastic
- episodic versus sequential
- static versus dynamic

These properties determine how much memory, uncertainty handling, and planning the agent needs.

## 6. Common Mistakes

1. **Capability-rationality confusion.** Treating rationality as raw intelligence level misses the task definition; judge actions against the performance measure instead.
2. **Objective vagueness.** Building an agent without a precise success criterion makes evaluation incoherent; define the performance measure first.
3. **Environment denial.** Assuming full observability or determinism when the real world is noisy produces brittle behavior; model the environment honestly.
4. **Architecture cargo cult.** Choosing a learning or utility agent because it sounds advanced can add unnecessary complexity; pick the lightest architecture that matches the task.
5. **Single-scenario validation.** Testing only one friendly environment hides irrational behavior in edge cases; evaluate across diverse scenarios.

## 7. Practical Checklist

- [ ] Write down the performance measure before designing behavior.
- [ ] Specify sensors, actions, and environment assumptions explicitly.
- [ ] Match the agent architecture to observability and uncertainty conditions.
- [ ] Test rationality on diverse scenarios rather than one nominal path.
- [ ] Revisit the objective if the agent exploits loopholes in the metric.
- [ ] Separate what the agent knows from what the environment actually contains.

## 8. References

- Russell, Stuart, and Peter Norvig. *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson, 2020.
- Poole, David, and Alan Mackworth. *Artificial Intelligence: Foundations of Computational Agents* (2nd ed.). Cambridge University Press, 2017. <https://artint.info/2e/html/ArtInt2e.html>
- Wooldridge, Michael. *An Introduction to MultiAgent Systems* (2nd ed.). Wiley, 2009.
- Russell, Stuart. *Human Compatible*. Viking, 2019.
- Berkeley AIMA resources. <https://aima.cs.berkeley.edu/>
- Sutton, Richard S., and Andrew G. Barto. *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press, 2018. <http://incompleteideas.net/book/the-book-2nd.html>
- Simon, Herbert A. "A Behavioral Model of Rational Choice." 1955. <https://www.jstor.org/stable/1826929>
