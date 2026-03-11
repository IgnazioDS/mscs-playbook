# Path Planning: A* and Dijkstra

## Key Ideas

- Path planning computes a collision-free route from a start state to a goal state over a map or graph representation of the environment.
- Dijkstra's algorithm guarantees shortest paths from a source in a weighted graph without using domain knowledge, while A* accelerates search by adding a heuristic estimate to the goal.
- The map representation and grid resolution are as important as the planning algorithm because they define the search space and the notion of traversability.
- An admissible heuristic allows A* to remain optimal while exploring fewer states than Dijkstra in many problems.
- Planning quality depends not only on shortest-path cost but also on whether the resulting path is feasible for the robot to follow.

## 1. What Path Planning Solves

Path planning decides how the robot should move from its current location to a goal while avoiding obstacles. In grid-based mobile robotics, this often becomes a shortest-path problem over free cells.

### 1.1 Core Definitions

- A **graph** consists of nodes and edges representing reachable states and transitions.
- A **cost-to-come** `g` is the accumulated path cost from the start to a node.
- A **heuristic** `h` estimates the remaining cost from a node to the goal.
- A **free cell** is a map cell the planner may traverse.
- **Admissible** means the heuristic never overestimates the true remaining cost.

### 1.2 Why This Matters

Without a planner, a robot has no systematic way to convert map knowledge into motion goals. Even when a local controller works well, it still needs a path structure to follow.

## 2. Dijkstra and A* Intuition

### 2.1 Dijkstra

Dijkstra expands outward from the start in order of increasing path cost. It is complete and optimal for nonnegative edge weights, but it does not prefer nodes that seem closer to the goal.

### 2.2 A*

A* ranks candidate nodes by:

```text
f = g + h
```

This means it prefers nodes that are both cheap so far and estimated to be close to the goal.

### 2.3 Why the Heuristic Matters

If the heuristic is informative and admissible, A* usually explores fewer states than Dijkstra while preserving optimality.

## 3. Planning Tradeoffs in Robotics

### 3.1 Resolution Tradeoff

A fine grid captures obstacles more precisely but increases search cost.

### 3.2 Static Versus Dynamic Obstacles

Classical A* and Dijkstra assume a mostly static search space. Dynamic obstacles often require replanning or a local planner layered on top.

### 3.3 Path Versus Executable Motion

A grid path may still require smoothing or trajectory generation before the controller can follow it safely.

## 4. Worked Example: A* Cost Calculation on a Small Grid

Suppose A* is evaluating a node with:

```text
g = 6
h = 4
```

### 4.1 Compute the A* Priority

```text
f = g + h = 6 + 4 = 10
```

### 4.2 Compare with Another Candidate

Another node has:

```text
g = 7
h = 2
f = 7 + 2 = 9
```

### 4.3 Interpret the Choice

Even though the second node has a higher path cost so far, A* prefers it because its lower estimated remaining cost gives it a smaller total priority:

```text
9 < 10
```

So the second node is expanded first.

Verification: the A* priorities are computed consistently because `6 + 4 = 10` and `7 + 2 = 9`, and the smaller `f` value is the one selected next.

## 5. Common Mistakes

1. **Heuristic overreach.** Using a heuristic that overestimates remaining cost can break A* optimality; keep the heuristic admissible when optimality matters.
2. **Map-planner disconnect.** Planning on a map that does not match robot size or obstacle inflation leads to unsafe paths; align the grid representation with robot footprint.
3. **Shortest-path obsession.** Optimizing only geometric path length may produce paths that are hard to track; consider downstream controller feasibility.
4. **Static-world assumption.** Using one static global path in a changing environment without replanning creates brittle behavior; plan for updates when the world changes.
5. **Resolution mismatch.** A coarse grid can hide narrow obstacles, while an overly fine grid can make search expensive without practical benefit; choose resolution deliberately.

## 6. Practical Checklist

- [ ] Confirm that the map representation matches the robot footprint and obstacle inflation assumptions.
- [ ] Use Dijkstra when no useful heuristic is available and A* when a sound heuristic exists.
- [ ] Verify heuristic admissibility before claiming A* optimality.
- [ ] Measure both search effort and path quality on representative maps.
- [ ] Smooth or convert raw grid paths before handing them to a controller.
- [ ] Replan when obstacle information changes materially.

## 7. References

- LaValle, Steven M. 2006. *Planning Algorithms*. Cambridge University Press. <https://lavalle.pl/planning/>
- Cormen, Thomas H., et al. 2022. *Introduction to Algorithms* (4th ed.). MIT Press.
- Hart, Peter E., Nils J. Nilsson, and Bertram Raphael. 1968. A Formal Basis for the Heuristic Determination of Minimum Cost Paths.
- Amit Patel. 2026. *A* Pages*. <https://theory.stanford.edu/~amitp/GameProgramming/>
- Thrun, Sebastian, Wolfram Burgard, and Dieter Fox. 2005. *Probabilistic Robotics*. MIT Press.
- Cyberbotics. 2026. *Webots User Guide*. <https://cyberbotics.com/doc/guide/>
- ROS. 2026. *Navigation Stack Concepts*. <https://navigation.ros.org/>
