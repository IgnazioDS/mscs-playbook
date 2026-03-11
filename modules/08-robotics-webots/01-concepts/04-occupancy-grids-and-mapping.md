# Occupancy Grids and Mapping

## Key Ideas

- Occupancy-grid mapping represents space as discrete cells whose state reflects whether the robot believes they are occupied, free, or unknown.
- Grid maps are attractive because they are conceptually simple, support sensor updates incrementally, and connect naturally to planning on discretized space.
- The quality of a grid map depends strongly on resolution, sensor model assumptions, and the quality of the pose estimate used for each update.
- Mapping and localization are tightly coupled because a bad pose estimate can smear or distort the map even when the sensor model is otherwise correct.
- Grid design is always a tradeoff between memory, spatial precision, computational cost, and robustness.

## 1. What Occupancy Grids Represent

An occupancy grid divides the environment into cells and assigns each cell a belief about whether it is occupied. Unknown cells reflect lack of evidence rather than confirmed free space.

### 1.1 Core Definitions

- A **cell** is one discrete spatial unit in the grid.
- **Resolution** is the physical size represented by each cell.
- An **inverse sensor model** estimates how a measurement changes occupancy belief in the traversed cells.
- **Ray casting** traces a sensor beam through the grid to update free and occupied cells.
- A **log-odds representation** is a numerically convenient way to accumulate occupancy evidence.

### 1.2 Why This Matters

Occupancy grids are widely used in mobile robotics because they convert uncertain sensor data into a geometric structure that can be visualized, updated online, and used by planners.

## 2. How Grid Mapping Works

### 2.1 Discretize the Environment

The world is divided into cells with chosen bounds and resolution.

### 2.2 Update with Sensor Measurements

A range measurement suggests that cells along the beam before the hit are free, while the cell at the hit location is likely occupied.

### 2.3 Repeat Over Time

As the robot moves, the map becomes more complete, though uncertainty remains where the robot has not observed or where pose error accumulates.

## 3. Key Tradeoffs

### 3.1 Resolution Tradeoff

A finer grid captures more detail but uses more memory and computation.

### 3.2 Sensor Model Tradeoff

A simplistic sensor model is easy to implement but may mis-handle noisy or wide beams. A more realistic model is more robust but more complex.

### 3.3 Pose Dependence

If the robot pose is wrong, the same wall may be written into different cells across time, creating blurred or doubled structures.

## 4. Worked Example: Grid Resolution and Cell Count

Suppose a robot maps a rectangular room of:

```text
width = 6 m
height = 4 m
```

Choose a grid resolution of:

```text
cell_size = 0.20 m
```

### 4.1 Compute the Number of Cells Along Each Dimension

```text
cells_x = 6 / 0.20 = 30
cells_y = 4 / 0.20 = 20
```

### 4.2 Compute Total Cell Count

```text
total_cells = 30 * 20 = 600
```

### 4.3 Compare with a Finer Resolution

If the team halves the cell size to `0.10 m`:

```text
cells_x = 6 / 0.10 = 60
cells_y = 4 / 0.10 = 40
total_cells = 60 * 40 = 2,400
```

The finer map has four times as many cells as the `0.20 m` map. This shows why grid resolution strongly affects cost.

Verification: halving the cell size doubles the number of cells in each dimension, so the total cell count increases from `600` to `2,400`, which is exactly four times larger.

## 5. Common Mistakes

1. **Resolution extremism.** Choosing a grid that is too coarse hides obstacles, while choosing one that is too fine wastes memory and update time; match resolution to robot size and task needs.
2. **Unknown-free confusion.** Treating unobserved cells as free space creates unsafe planning assumptions; keep unknown and free logically distinct unless the application justifies otherwise.
3. **Pose-error denial.** Assuming the map quality depends only on the sensor model ignores localization drift; evaluate mapping together with pose quality.
4. **Beam-model oversimplification.** Updating only hit cells without reasoning about free space along the beam produces weak maps; implement the inverse sensor logic consistently.
5. **No visualization loop.** Failing to visualize intermediate maps delays detection of smeared walls and alignment bugs; inspect the evolving grid regularly.

## 6. Practical Checklist

- [ ] Choose grid resolution relative to robot footprint and obstacle detail requirements.
- [ ] Keep unknown, free, and occupied states conceptually separate.
- [ ] Validate sensor updates on simple scenes before scaling to larger maps.
- [ ] Check mapping output against known geometry or simulator truth when possible.
- [ ] Monitor whether pose drift is distorting the map over time.
- [ ] Visualize maps frequently during development and debugging.

## 7. References

- Thrun, Sebastian, Wolfram Burgard, and Dieter Fox. 2005. *Probabilistic Robotics*. MIT Press.
- Elfes, Alberto. 1989. Using Occupancy Grids for Mobile Robot Perception and Navigation. *Computer* 22(6).
- Moravec, Hans P., and Alberto Elfes. 1985. High Resolution Maps from Wide Angle Sonar. <https://www.ri.cmu.edu/publications/high-resolution-maps-from-wide-angle-sonar/>
- ROS. 2026. *navigation_msgs/OccupancyGrid*. <https://docs.ros.org/en/noetic/api/nav_msgs/html/msg/OccupancyGrid.html>
- LaValle, Steven M. 2006. *Planning Algorithms*. Cambridge University Press. <https://lavalle.pl/planning/>
- Corke, Peter. 2017. *Robotics, Vision and Control* (2nd ed.). Springer.
