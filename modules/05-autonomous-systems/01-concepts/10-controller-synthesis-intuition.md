# Controller Synthesis Intuition

## Key Ideas

- Verification asks whether a controller is correct; synthesis asks how to
  construct one automatically from a plant model and a formal specification.
- Synthesis is naturally formulated as a two-player game between the controller
  and an adversarial environment.
- Safety and reachability games admit fixed-point algorithms on finite graphs;
  richer winning conditions such as Büchi or GR(1) extend the same idea with
  nested fixed points.
- The GR(1) fragment is important because it captures many practical reactive
  requirements while retaining polynomial-time symbolic synthesis.
- A synthesized strategy is mathematically a feedback policy. The conceptual
  link to control theory is strong, even when the objective is logical rather
  than numeric.

## Intuition

Formal verification is a pass-fail test. You design a controller, build a
model, and ask whether the design satisfies the specification. Reactive
synthesis flips that workflow around. Instead of checking a finished design, you
start with the plant and the requirement and ask the algorithm to construct a
controller that is correct by construction.

The adversarial viewpoint is essential. A controller does not get to choose
everything. The environment may issue requests, schedule other agents, block a
path, or inject disturbances. Synthesis therefore models the problem as a game:
the environment chooses what it can control, the system chooses how to respond,
and the objective is to guarantee the specification no matter how the
environment behaves within its assumptions.

This perspective connects formal methods to control. In both settings, a
controller is a rule that maps observations or states to actions. The main
difference is the objective. Classical control often optimizes a numeric cost,
while reactive synthesis enforces a temporal-logic specification such as "avoid
unsafe states forever and visit the goal infinitely often."

## 1. Formal Problem Statement

**Definition (Turn-based game arena).**  
A finite turn-based game arena is a tuple

`G = (S_env, S_sys, Act_env, Act_sys, δ, Init, Bad, Goal)`

where:

- `S_env` is the set of environment states;
- `S_sys` is the set of system states;
- `Act_env` is the environment action set;
- `Act_sys` is the system action set;
- `δ` is the transition function;
- `Init ⊆ S_env ∪ S_sys` is the set of initial states;
- `Bad ⊆ S_env ∪ S_sys` is the unsafe set;
- `Goal ⊆ S_env ∪ S_sys` is the target set.

Gloss:

- The current player is determined by whether the state lies in `S_env` or
  `S_sys`.
- A strategy for the controller chooses a system action whenever the play is in
  `S_sys`.
- A winning strategy ensures the specification against all environment moves.

Constraint note:

- The environment assumptions are part of the arena. If the arena gives the
  environment impossible powers, synthesis may fail for the wrong reason.

**Definition (Strategy).**  
A strategy for the controller is a function

`σ : S^* S_sys -> Act_sys`

that maps every finite play ending in a system state to a legal system action.

For many finite-state safety games, memoryless strategies are sufficient, but
response and recurrence objectives may require memory or a product construction.

## 2. Winning Conditions

Common objectives:

- **Safety:** stay out of `Bad` forever.
- **Reachability:** eventually enter `Goal`.
- **Büchi:** visit `Goal` infinitely often.
- **GR(1):** if the environment satisfies its recurrence assumptions, then the
  system satisfies its recurrence guarantees.

The canonical GR(1) shape is:

`G F a_1 ∧ ... ∧ G F a_n -> G F g_1 ∧ ... ∧ G F g_m`

where the `a_i` are environment assumptions and the `g_j` are system
guarantees.

Why GR(1) matters:

- it covers many robotics and embedded-control mission specs;
- it admits symbolic synthesis algorithms with polynomial complexity in the
  state graph size;
- tools such as TuLiP and Slugs are built around it.

## 3. Fixed-Point Algorithm for Safety Games

For a turn-based safety game, the controller's winning region is the greatest
fixed point of the predecessor operator restricted to safe states.

Define:

- `W_0 = S \ Bad`
- `W_{i+1} = Pre(W_i) ∩ W_i`

where `Pre(W_i)` contains:

- every system state from which the controller has some action whose successors
  all stay in `W_i`;
- every environment state whose all legal successors stay in `W_i`.

The iteration stops when `W_{i+1} = W_i`.

**Theorem (Safety-game fixed point).**  
For a finite turn-based safety game, the limit `W` of the descending sequence
above is exactly the set of states from which the controller has a winning
strategy for avoiding `Bad` forever.

Plain-English reading: repeatedly delete states that cannot be kept safe, and
what remains is precisely the controller's safe operating envelope.

*Proof sketch.* If a state remains in the fixed point, then by construction the
controller can choose actions that keep the play inside the fixed point at every
system turn, while the environment cannot force escape at its turns. This yields
an invariant strategy. Conversely, if a state is removed at some iteration, then
at that stage either the controller has no action keeping all successors safe or
the environment has a move forcing escape, so the controller cannot have a
winning safety strategy from that state. This is the standard greatest
fixed-point characterization of safety games.

## 4. Connection to Control Theory

A synthesized strategy is a feedback law:

- it observes the current abstract state;
- it chooses an input action;
- the closed-loop system follows the resulting successor relation.

The difference from classical control is primarily the objective:

- LQR optimizes a quadratic cost over trajectories;
- reactive synthesis enforces a temporal property over all admissible
  environment behaviors.

These viewpoints are complementary, not competing. Hybrid and symbolic control
often combine them by discretizing a plant into an abstract game for logical
planning and then refining the strategy into a low-level controller.

## 5. Worked Example: 3x3 Robot Game

Consider a robot on a `3 x 3` grid.

- Start: `(1, 1)`
- Goal: `(3, 3)`
- Obstacle: `(2, 2)`
- Service cell: `(1, 3)`
- State also includes a bit `pending ∈ {0, 1}` indicating whether a service
  request is outstanding.

Environment behavior:

- at the initial environment state, it chooses whether `pending = 0` or
  `pending = 1`;
- on later environment turns, it may either allow the chosen move or stall the
  robot for one step.

System objective:

- safety: never enter `(2, 2)`;
- reachability: eventually reach `(3, 3)`;
- response: `G(pending -> F at_service)`.

The robot clears `pending` when it enters the service cell `(1, 3)`.

### 5.1 Safety winning region

For safety alone, the obstacle cell is removed immediately:

- `W_0 =` all nine grid cells except `(2, 2)`.

Because the controller can always choose a move that keeps the robot in the
free cells and the environment can only stall, not redirect into the obstacle,
the fixed point stabilizes at the same set:

- `W_1 = W_0`
- `W = W_0`

So every non-obstacle cell is winning for safety.

### 5.2 Strategy for the response objective

Use a simple memory-based strategy:

- if `pending = 1`, move toward `(1, 3)` by going north until service is
  delivered;
- if `pending = 0`, move toward `(3, 3)` along the safe corridor
  `(1, 1) -> (2, 1) -> (3, 1) -> (3, 2) -> (3, 3)`.

### 5.3 Executable trace

Suppose the environment initially sets `pending = 1` and stalls once.

| Step | State `(cell, pending)` | Player / move | Next state | Property status |
|------|--------------------------|---------------|------------|-----------------|
| 0 | `((1,1), 1)` | env chooses `pending = 1` | `((1,1), 1)` | request active |
| 1 | `((1,1), 1)` | sys chooses `North` | `((1,2), 1)` | safe |
| 2 | `((1,2), 1)` | env chooses `stall` | `((1,2), 1)` | still safe |
| 3 | `((1,2), 1)` | sys chooses `North` | `((1,3), 0)` | response discharged |
| 4 | `((1,3), 0)` | sys chooses `East` | `((2,3), 0)` | safe |
| 5 | `((2,3), 0)` | sys chooses `East` | `((3,3), 0)` | goal reached |

### 5.4 Strategy table

| State | Chosen action |
|-------|---------------|
| `((1,1), 1)` | `North` |
| `((1,2), 1)` | `North` |
| `((1,3), 0)` | `East` |
| `((2,3), 0)` | `East` |
| `((1,1), 0)` | `East` |
| `((2,1), 0)` | `East` |
| `((3,1), 0)` | `North` |
| `((3,2), 0)` | `North` |

Property check:

- Safety holds because the strategy never selects `(2, 2)`.
- The response requirement holds because whenever `pending = 1`, the strategy
  eventually reaches `(1, 3)` and clears it.
- Reachability holds because after service is discharged, the strategy reaches
  `(3, 3)`.

## 6. Limitations

- State explosion is inherited from model checking because synthesis works on
  the product of plant, environment, and specification memory.
- Infinite-state games are undecidable in general.
- A synthesized symbolic policy may still require refinement before it becomes
  an implementable embedded controller.

## 7. Common Mistakes

1. Treating the plant as if the controller controls every transition.
2. Omitting environment assumptions, which usually makes the synthesis problem
   unrealizable for artificial reasons.
3. Using a safety-game algorithm for a liveness or Büchi objective.
4. Assuming a synthesized strategy is directly implementable without checking
   timing, sensing, and actuator limits.
5. Ignoring the gap between an abstract winning region and a concrete plant.

## 8. Practical Checklist

- [ ] Separate system-controlled and environment-controlled transitions.
- [ ] Write the specification before attempting synthesis.
- [ ] Check whether the objective is safety, reachability, Büchi, or GR(1).
- [ ] Compute the winning region before trying to extract a strategy.
- [ ] Validate the extracted strategy on hand-executable traces.
- [ ] Record which plant assumptions are required for realizability.

## 9. References

- Bloem, Roderick, Krishnendu Chatterjee, Karin Greimel, Thomas A. Henzinger,
  and Barbara Jobstmann. 2012. Synthesis of Reactive(1) Designs. *Journal of
  Computer and System Sciences* 78 (3): 911-938.
  <https://doi.org/10.1016/j.jcss.2011.08.007>
- Kress-Gazit, Hadas, Georgios E. Fainekos, and George J. Pappas. 2009.
  Temporal-Logic-Based Reactive Mission and Motion Planning. *IEEE TRO* 25 (6):
  1370-1381.
  <https://doi.org/10.1109/TRO.2009.2030225>
- Piterman, Nir, Amir Pnueli, and Yaniv Sa'ar. 2006. Synthesis of Reactive(1)
  Designs. *VMCAI 2006*.
  <https://doi.org/10.1007/11609773_16>
- TuLiP: Temporal Logic Planning Toolbox.
  <https://tulip-control.readthedocs.io/>
- Bloem, Roderick, et al. 2014. *Handbook of Model Checking*, chapter on
  reactive synthesis.
- Slugs reactive synthesis tool. <https://github.com/VerifiableRobotics/slugs>
