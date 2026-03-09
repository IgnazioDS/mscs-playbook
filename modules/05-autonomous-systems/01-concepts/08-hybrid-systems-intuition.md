# Hybrid Systems Intuition

## Key Ideas

- A hybrid automaton models systems whose behavior combines discrete switching
  with continuous evolution; it keeps both control modes and physical state, but
  it usually omits stochastic effects and low-level implementation detail.
- Hybrid automata sit strictly above timed automata in expressive power because
  clocks are just a special case of continuous variables with derivative `1`.
- The price of that expressiveness is severe: reachability is undecidable for
  general linear hybrid automata, so practical tools rely on restricted classes
  or sound approximations.
- Invariants, guards, and resets are the load-bearing modeling elements. If any
  of them are wrong, the reachable set can change qualitatively.
- Zeno behavior is a modeling warning sign: infinitely many discrete jumps in
  finite time are mathematically possible in some hybrid models but physically
  meaningless for most engineered systems.

## Intuition

Many autonomous systems are not purely digital and not purely continuous. A
thermostat switches between heating and cooling modes while temperature evolves
continuously. A vehicle controller switches between cruise, brake, and emergency
stop while velocity and position follow differential equations. An aircraft
autopilot changes control laws when its mode changes, but the aircraft state
still moves through real space the whole time.

Neither a plain transition system nor a plain LTI model is enough for such
systems. A transition system can say that mode changes occur, but it cannot say
how temperature or velocity evolves between them. An LTI model can describe one
continuous regime, but it cannot represent guarded switching between different
dynamics. Hybrid automata were invented to combine both kinds of evolution in a
single formal object.

This combination makes the model far more realistic, but it also makes the
analysis much harder. Reachability is no longer just graph search over a finite
state space. The state now includes real-valued variables and continuous
trajectories between jumps. Much of hybrid-systems verification is therefore a
careful balance between modeling fidelity and algorithmic tractability.

## 1. Formal Definition

**Definition (Hybrid Automaton).**  
A hybrid automaton is a tuple

`H = (Loc, X, Init, Flow, Inv, E)`

where:

- `Loc` is a finite set of locations;
- `X = {x_1, ..., x_n}` is a finite set of continuous variables;
- `Init ⊆ Loc × R^n` is the set of initial states;
- `Flow` assigns to each location `ℓ ∈ Loc` a continuous dynamics law, typically
  an ODE `ẋ = f_ℓ(x)`;
- `Inv` assigns to each location `ℓ ∈ Loc` an invariant `Inv(ℓ) ⊆ R^n`;
- `E ⊆ Loc × Guard(X) × Reset(X) × Loc` is the set of discrete edges.

Gloss:

- A location is the current discrete mode.
- The variables in `X` evolve continuously while the automaton remains in a
  location.
- `Init` specifies valid starting mode-state pairs.
- `Flow` tells each mode how the continuous state evolves.
- `Inv` constrains how long the system may remain in a location.
- Each edge contains a guard that enables a jump and a reset map that updates
  the continuous variables on that jump.

Constraint note:

- If an invariant is violated and no outgoing guard is enabled, the model
  deadlocks.
- Resets need not be total assignments; they may leave some variables
  unchanged.

Minimal reusable example:

- `Loc = {heating, cooling}`
- `X = {x}` where `x` is temperature
- `Flow(heating): ẋ = -x + H`
- `Flow(cooling): ẋ = -x`
- `Inv(heating): x <= T_high`
- `Inv(cooling): x >= T_low`
- `E` contains
  `(heating, x >= T_high, x := x, cooling)` and
  `(cooling, x <= T_low, x := x, heating)`.

## 2. Semantics: Executions

The semantics of a hybrid automaton is a set of **executions**. An execution is
an alternating sequence of continuous flows and discrete jumps:

`(ℓ_0, ξ_0), e_0, (ℓ_1, ξ_1), e_1, (ℓ_2, ξ_2), ...`

such that:

- `(ℓ_0, ξ_0(0)) ∈ Init`;
- each `ξ_i : [0, τ_i] -> R^n` is a differentiable trajectory satisfying
  `Flow(ℓ_i)` and remaining in `Inv(ℓ_i)`;
- the endpoint `ξ_i(τ_i)` satisfies the guard of edge `e_i`;
- applying the reset of `e_i` to `ξ_i(τ_i)` yields the start point
  `ξ_{i+1}(0)`.

This is the hybrid analogue of a path in a transition system. The difference is
that each segment carries an entire continuous trajectory, not just a source and
target state.

## 3. Decidability Landscape

Timed automata are a restricted hybrid model where every continuous variable is
a clock with derivative `1` and resets to `0`. That restriction is strong
enough to recover decidable reachability.

General hybrid models are much harder.

**Theorem (Undecidability of reachability for linear hybrid automata).**  
Reachability is undecidable for general linear hybrid automata.

Plain-English reading: there is no algorithm that always decides whether an
arbitrary target set is reachable for every linear hybrid automaton.

*Proof sketch.* The classical strategy reduces the halting problem for a
two-counter Minsky machine to reachability in a linear hybrid automaton. The
counters are encoded in continuous variables and the machine instructions are
encoded as locations, guards, and resets. If reachability were decidable for
all such automata, the halting problem for two-counter machines would be
decidable as well, which is impossible. Full proof details appear in Henzinger
et al. 1995.

Important subclasses:

- **Timed automata:** decidable reachability.
- **Initialised rectangular automata:** decidable reachability.
- **General linear hybrid automata:** undecidable; tools use
  over-approximations.

## 4. Zeno Behavior

A hybrid execution is **Zeno** if it contains infinitely many discrete
transitions while the sum of elapsed times remains finite.

Why Zeno behavior arises:

- guards may allow immediate repeated switching;
- resets may return the state to another immediately enabled guard;
- invariants may force urgent transitions with no minimum dwell time.

Why it is a problem:

- most physical systems cannot switch infinitely often in finite time;
- numerical simulators become unreliable near a Zeno accumulation point;
- liveness claims may become misleading if "progress" is only discrete
  switching, not elapsed physical time.

Typical prevention strategies:

- add hysteresis, so each mode requires positive time before the next switch;
- enforce minimum dwell times with clocks;
- model actuator limits or reset maps more realistically.

## 5. Simulation and Bisimulation

A hybrid automaton `H_1` **simulates** `H_2` if every execution of `H_2` can be
matched by an execution of `H_1` after applying an observation map. If both
simulate each other, they are **bisimilar** with respect to that observation.

The concept matters operationally:

- a coarse abstraction that simulates the concrete plant can still support
  safety reasoning;
- bisimulation is stronger and preserves richer behavioral equivalences.

For hybrid models, exact bisimulation is rare. Approximate simulation and
reachability enclosure are more common in practice.

## 6. Worked Example: Thermostat Hybrid Automaton

Consider a thermostat with thresholds `T_low = 18`, `T_high = 22`, and heater
temperature parameter `H = 25`.

**Definition (Thermostat automaton).**  
Let `H_T = (Loc, X, Init, Flow, Inv, E)` where:

- `Loc = {heating, cooling}`;
- `X = {x}`;
- `Init = {(heating, 18)}`;
- `Flow(heating): ẋ = -x + 25`;
- `Flow(cooling): ẋ = -x`;
- `Inv(heating): x <= 22`;
- `Inv(cooling): x >= 18`;
- `E` contains:
  `(heating, x >= 22, identity, cooling)` and
  `(cooling, x <= 18, identity, heating)`.

### 6.1 One heating-cooling cycle

In `heating`, the solution of `ẋ = -x + 25` with `x(0) = 18` is

`x(t) = 25 - 7 e^{-t}`.

The guard `x >= 22` fires when

`25 - 7 e^{-t_h} = 22`, so `e^{-t_h} = 3/7`, hence

`t_h = ln(7/3) ≈ 0.8473`.

In `cooling`, the solution of `ẋ = -x` with starting temperature `22` is

`x(t) = 22 e^{-t}`.

The guard `x <= 18` fires when

`22 e^{-t_c} = 18`, so

`t_c = ln(22/18) ≈ 0.2007`.

### 6.2 Executable trace

| Step | Location | Continuous state | Type | Guard / invariant check | Action / delay |
|------|----------|------------------|------|-------------------------|----------------|
| 0 | `heating` | `x = 18` | initial | `x <= 22` holds | start |
| 1 | `heating` | `x = 25 - 7e^{-0.5} ≈ 20.75` | flow | `x <= 22` holds | delay `0.5` |
| 2 | `cooling` | `x = 22` | jump | guard `x >= 22` enabled at `t = 0.8473` | switch to cooling |
| 3 | `cooling` | `x = 22e^{-0.1} ≈ 19.91` | flow | `x >= 18` holds | delay `0.1` |
| 4 | `heating` | `x = 18` | jump | guard `x <= 18` enabled at `t = 0.2007` | switch to heating |

### 6.3 Property check

The safety property is "temperature remains in the comfort band
`18 <= x <= 22`." The trace satisfies it:

- in `heating`, the invariant enforces `x <= 22`;
- in `cooling`, the invariant enforces `x >= 18`;
- the jump guards switch exactly at the thresholds.

The trace also shows why the model is non-Zeno: each mode requires a positive
dwell time before the next threshold is reached.

## 7. Common Mistakes

1. Omitting invariants, which can allow physically meaningless lingering in a
   mode long after a guard should have forced a switch.
2. Forgetting to specify reset behavior on jumps, leaving ambiguity about the
   post-transition continuous state.
3. Treating a tool's approximate reachable set as an exact decision procedure
   for an undecidable model class.
4. Ignoring Zeno behavior because "the simulator still produced a plot."
5. Using a hybrid automaton where a timed automaton would have sufficed,
   needlessly leaving the decidable fragment.

## 8. Practical Checklist

- [ ] List the locations, continuous variables, invariants, guards, and resets
      explicitly before discussing behavior.
- [ ] Verify that every forced invariant violation has a corresponding enabled
      outgoing edge.
- [ ] Check whether clocks alone are sufficient; if so, use a timed automaton
      instead of a general hybrid model.
- [ ] Look for minimum dwell times or hysteresis to exclude Zeno runs.
- [ ] Interpret tool output in the correct soundness direction
      (over-approximation for safety, under-approximation for bug finding).
- [ ] Validate the model on one known-safe and one known-unsafe execution.

## 9. References

- Frehse, Goran, et al. 2011. SpaceEx: Scalable Verification of Hybrid Systems.
  *CAV 2011*.
  <https://doi.org/10.1007/978-3-642-22110-1_30>
- Goebel, Rafal, Ricardo G. Sanfelice, and Andrew R. Teel. 2012. *Hybrid
  Dynamical Systems*. Princeton University Press.
- Henzinger, Thomas A., Peter W. Kopke, Anuj Puri, and Pravin Varaiya. 1995.
  What's Decidable about Hybrid Automata? *STOC 1995*.
  <https://doi.org/10.1145/225058.225162>
- Henzinger, Thomas A. 1996. The Theory of Hybrid Automata. *LICS 1996*.
  <https://doi.org/10.1109/LICS.1996.561342>
- Lee, Edward A., and Sanjit A. Seshia. 2017. *Introduction to Embedded
  Systems*. 2nd ed.
  <https://ptolemy.berkeley.edu/books/leeseshia/>
- Tomlin, Claire, George J. Pappas, and Shankar Sastry. 2000. Conflict
  Resolution for Air Traffic Management: A Study in Multiagent Hybrid Systems.
  *IEEE TAC* 43 (4): 509-521.
