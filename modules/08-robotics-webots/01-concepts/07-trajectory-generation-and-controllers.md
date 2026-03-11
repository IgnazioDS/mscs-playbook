# Trajectory Generation and Controllers

## Key Ideas

- Path planning decides where the robot should go, while trajectory generation and control decide how it should move there over time.
- A trajectory adds timing, velocity, and curvature constraints to a geometric path so that the motion is physically trackable.
- Controllers convert trajectory or waypoint information into actuator commands while continuously correcting tracking error.
- The quality of a controller depends on both the control law and the assumptions built into the trajectory or path it is asked to follow.
- Stable robot motion requires balancing responsiveness, smoothness, and safety rather than minimizing path error alone.

## 1. What Trajectory Generation and Control Do

Trajectory generation produces a time-parameterized motion plan, and the controller attempts to track it using feedback from the current robot state.

### 1.1 Core Definitions

- A **path** is a geometric route through space.
- A **trajectory** is a path with timing information such as velocity over time.
- **Tracking error** is the difference between desired and actual robot state.
- A **feedback controller** uses the measured state to reduce tracking error.
- **Pure pursuit** is a common path-following controller that steers toward a lookahead point on the path.

### 1.2 Why This Matters

Even a perfect global path is not enough if the robot cannot follow it smoothly. Planning, trajectory generation, and control must agree on curvature, timing, and actuator capability.

## 2. From Path to Executable Motion

### 2.1 Time Parameterization

A trajectory must assign speeds or timing to the geometric path so the robot respects velocity and turning constraints.

### 2.2 Tracking with Feedback

Controllers compare the current pose to the desired path or trajectory and generate steering or wheel commands to reduce the error.

### 2.3 Why Sharp Turns Matter

Paths with abrupt direction changes can be hard for a real controller to track without overshoot or oscillation, especially at speed.

## 3. Common Controller Intuition

### 3.1 PID-Style Correction

PID-style controllers correct based on present, accumulated, and changing error, but they require careful gain tuning.

### 3.2 Geometric Tracking

Pure pursuit and similar methods use geometric lookahead logic, which can be intuitive and effective for mobile robots.

### 3.3 Constraint Awareness

The best controller still fails if the requested trajectory violates what the robot can physically achieve.

## 4. Worked Example: Compute a Simple Tracking Error

Suppose the desired waypoint is:

```text
desired = (x = 3.0, y = 2.0)
```

and the current robot position is:

```text
current = (x = 2.6, y = 1.7)
```

### 4.1 Compute Position Error Components

```text
error_x = 3.0 - 2.6 = 0.4
error_y = 2.0 - 1.7 = 0.3
```

### 4.2 Compute Euclidean Position Error

```text
position_error = sqrt(0.4^2 + 0.3^2)
position_error = sqrt(0.16 + 0.09)
position_error = sqrt(0.25) = 0.5
```

### 4.3 Interpret the Result

The robot is `0.5 m` from the desired point. A controller would use that error, along with heading information and actuation limits, to decide how aggressively to steer and move forward.

Verification: the position error is correct because the displacement vector `(0.4, 0.3)` has Euclidean length `0.5`.

## 5. Common Mistakes

1. **Path-trajectory confusion.** Treating a geometric path as if it already included executable timing ignores actuator limits; convert paths into feasible trajectories before tracking.
2. **Gain-only debugging.** Blaming every tracking failure on controller gains ignores bad paths, pose estimates, or unrealistic speed commands; inspect the full motion pipeline.
3. **Constraint neglect.** Asking the controller to follow turns tighter than the robot can achieve produces oscillation or cut corners; enforce curvature and velocity limits upstream.
4. **No logging of error.** Tuning without tracking-error traces makes improvement guesswork; log error, control output, and timing together.
5. **Single-scenario tuning.** A controller that works only on one straight path may fail on sharp curves or speed changes; validate across representative maneuvers.

## 6. Practical Checklist

- [ ] Distinguish clearly between path planning output and time-parameterized trajectory output.
- [ ] Respect robot velocity and curvature limits when generating trajectories.
- [ ] Log tracking error, heading error, and control signals during tests.
- [ ] Tune controller gains or lookahead settings on multiple maneuver types.
- [ ] Check whether localization or odometry error is degrading control performance.
- [ ] Smooth or reparameterize paths that are too abrupt for the controller to follow.

## 7. References

- Coulter, R. Craig. 1992. *Implementation of the Pure Pursuit Path Tracking Algorithm*. Carnegie Mellon University.
- Siciliano, Bruno, and Oussama Khatib, eds. 2016. *Springer Handbook of Robotics* (2nd ed.). Springer.
- Corke, Peter. 2017. *Robotics, Vision and Control* (2nd ed.). Springer.
- LaValle, Steven M. 2006. *Planning Algorithms*. Cambridge University Press. <https://lavalle.pl/planning/>
- Cyberbotics. 2026. *Controller Programming*. <https://cyberbotics.com/doc/guide/controller-programming>
- ROS. 2026. *Navigation and Controller Concepts*. <https://navigation.ros.org/>
- Kelly, Alonzo. 2013. *Mobile Robotics: Mathematics, Models, and Methods*. Cambridge University Press.
