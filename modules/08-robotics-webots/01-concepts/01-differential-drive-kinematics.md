# Differential Drive Kinematics

## Key Ideas

- Differential-drive kinematics describes how two independently driven wheels generate the robot's forward motion and rotation in the plane.
- The kinematic model is the foundation for odometry, controller design, and simulator verification because it converts wheel motions into pose changes.
- The model is geometric rather than dynamic: it explains feasible motion from wheel speeds and robot geometry, not force or slip behavior.
- Unit consistency matters because small mistakes in wheel radius, axle length, or angular units can create large downstream pose errors.
- A correct kinematic model is necessary but not sufficient for real performance, because wheel slip, encoder noise, and timing error still affect execution.

## 1. What Differential-Drive Kinematics Is

Differential-drive kinematics is the mathematical description of planar motion for a robot with two driven wheels on the same axle. By choosing different left and right wheel speeds, the robot can move straight, rotate in place, or follow an arc.

### 1.1 Core Definitions

- A **wheel radius** is the distance from the wheel center to the contact edge.
- The **axle length** or **track width** is the distance between the left and right wheel contact paths.
- **Linear velocity** is the forward speed of the robot body.
- **Angular velocity** is the rate of heading change.
- A **pose** is the robot state `(x, y, theta)` in a plane.

### 1.2 Why This Matters

Most entry-level mobile robots and many simulated robots in Webots use differential drive. If this model is wrong, every later estimate built on it, including odometry, localization, mapping, and control, inherits the error.

## 2. From Wheel Speeds to Robot Motion

### 2.1 Straight Motion

If both wheels rotate at the same speed, the robot moves forward or backward without turning.

### 2.2 In-Place Rotation

If the wheels spin at equal magnitude but opposite direction, the robot rotates around its center.

### 2.3 Arc Motion

If wheel speeds differ but have the same sign, the robot follows a circular arc.

## 3. Standard Kinematic Equations

### 3.1 Wheel Linear Speeds

Let:

```text
v_l = left wheel linear speed
v_r = right wheel linear speed
L = axle length
```

Then:

```text
v = (v_r + v_l) / 2
omega = (v_r - v_l) / L
```

### 3.2 Pose Update Intuition

For a short time interval `dt`, the robot heading changes by:

```text
delta_theta = omega * dt
```

and the position changes approximately by the forward speed along the current heading.

### 3.3 Why Small Timing Errors Matter

These updates are applied repeatedly. Even tiny bias in `dt`, wheel radius, or axle length accumulates over many steps.

## 4. Worked Example: Compute One Motion Step

Suppose a differential-drive robot has:

```text
wheel_radius = 0.05 m
axle_length = 0.30 m
left_wheel_angular_speed = 8 rad/s
right_wheel_angular_speed = 10 rad/s
dt = 0.1 s
initial_pose = (x = 0, y = 0, theta = 0)
```

### 4.1 Convert Angular Wheel Speeds to Linear Speeds

```text
v_l = wheel_radius * left_wheel_angular_speed
v_l = 0.05 * 8 = 0.40 m/s

v_r = wheel_radius * right_wheel_angular_speed
v_r = 0.05 * 10 = 0.50 m/s
```

### 4.2 Compute Robot Linear and Angular Velocity

```text
v = (0.50 + 0.40) / 2 = 0.45 m/s
omega = (0.50 - 0.40) / 0.30 = 0.10 / 0.30 = 0.3333... rad/s
```

### 4.3 Update the Pose for One Short Step

Heading change:

```text
delta_theta = omega * dt
delta_theta = 0.3333... * 0.1 = 0.03333... rad
```

Approximate forward displacement:

```text
delta_s = v * dt = 0.45 * 0.1 = 0.045 m
```

Because the initial heading is `0`, a short-step approximation gives:

```text
new_x = 0 + 0.045 = 0.045
new_y = 0
new_theta = 0.03333... rad
```

The robot moved slightly forward and turned slightly to the left.

Verification: the right wheel moves faster than the left, so the positive angular velocity and small leftward turn are consistent with the computed `omega = 0.3333... rad/s`.

## 5. Common Mistakes

1. **Unit confusion.** Mixing angular speed, linear speed, and wheel radius inconsistently produces incorrect motion estimates; convert all quantities carefully before integration.
2. **Wrong track width.** Using the wrong axle length changes the turn rate directly; calibrate the geometry against the actual robot or simulator model.
3. **Sign convention drift.** Inconsistent left-right or heading conventions create mirrored motion behavior; define and keep one coordinate convention throughout the pipeline.
4. **Long-step approximation abuse.** Applying simple short-step updates with very large `dt` increases integration error; use sufficiently small simulation steps or better integration.
5. **Slip blindness.** Treating the kinematic model as if it were exact physical truth ignores wheel slip and ground interaction; use it as a model, not as a guarantee.

## 6. Practical Checklist

- [ ] Confirm wheel radius, axle length, and coordinate-frame conventions before coding.
- [ ] Convert wheel angular speeds to linear speeds explicitly.
- [ ] Test the model on straight, arc, and in-place rotation scenarios.
- [ ] Keep simulation timestep assumptions consistent across kinematics and control code.
- [ ] Compare integrated pose against simulator or ground-truth motion traces.
- [ ] Recalibrate geometry if systematic turn or drift errors appear repeatedly.

## 7. References

- Thrun, Sebastian, Wolfram Burgard, and Dieter Fox. 2005. *Probabilistic Robotics*. MIT Press.
- Siciliano, Bruno, and Oussama Khatib, eds. 2016. *Springer Handbook of Robotics* (2nd ed.). Springer.
- Corke, Peter. 2017. *Robotics, Vision and Control* (2nd ed.). Springer.
- Cyberbotics. 2026. *Webots User Guide*. <https://cyberbotics.com/doc/guide/>
- Robotics Toolbox. 2026. *Mobile Robot Kinematics*. <https://petercorke.github.io/robotics-toolbox-python/mobile_vehicle_unicycle.html>
- Northwestern MSR. 2026. *Differential Drive Kinematics Notes*. <https://nu-msr.github.io/navigation_site/lectures/derive_kinematics.html>
- LaValle, Steven M. 2006. *Planning Algorithms*. Cambridge University Press. <https://lavalle.pl/planning/>
