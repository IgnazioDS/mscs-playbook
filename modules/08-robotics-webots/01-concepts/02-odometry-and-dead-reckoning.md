# Odometry and Dead Reckoning

## Key Ideas

- Odometry estimates robot pose by integrating wheel or motion measurements over time, while dead reckoning refers to navigation based on that accumulated estimate without external correction.
- Odometry is indispensable because it provides a continuous local motion estimate even when absolute position sensors are unavailable.
- The central weakness of dead reckoning is drift: small wheel, timing, and slip errors accumulate into large pose errors over time.
- Good odometry practice depends on calibration, consistent timing, and realistic uncertainty expectations rather than on assuming the integrated path is ground truth.
- Odometry is best understood as a baseline estimate that later sensors or localization methods must correct.

## 1. What Odometry Does

Odometry uses measured wheel motion or similar incremental signals to estimate how the robot pose changed from one time step to the next. By chaining these increments together, the system obtains an ongoing pose estimate.

### 1.1 Core Definitions

- An **encoder** measures wheel rotation, usually as ticks or angle increments.
- **Dead reckoning** is pose estimation by accumulating incremental motion without external correction.
- **Drift** is the growth of estimation error over time.
- A **systematic error** is repeatable bias such as incorrect wheel radius calibration.
- A **random error** is variable noise such as jitter or uneven traction.

### 1.2 Why This Matters

Nearly every mobile-robot stack uses odometry as one input to localization, mapping, or controller feedback. If odometry is misunderstood, later filters or planners will be forced to compensate for errors that should have been characterized earlier.

## 2. How Odometry Is Computed

### 2.1 Wheel Displacements

Encoders measure how far each wheel traveled over the last time interval.

### 2.2 Incremental Pose Update

From the wheel displacements, the robot estimates forward motion and heading change using the differential-drive geometry.

### 2.3 Cumulative Error

Every update contains some error. Summed over many steps, those errors create growing uncertainty even if each step seems small.

## 3. Why Dead Reckoning Drifts

### 3.1 Calibration Error

If wheel radius or axle length is wrong, every update is biased.

### 3.2 Slip and Surface Effects

Real wheels may slide, skid, or roll unevenly relative to the model.

### 3.3 Timing and Quantization

Coarse encoder resolution or stale timing can distort the displacement estimate, especially at low speeds or sharp turns.

## 4. Worked Example: One Odometry Update from Encoder Distances

Suppose a differential-drive robot has:

```text
left_wheel_distance = 0.20 m
right_wheel_distance = 0.24 m
axle_length = 0.40 m
initial_pose = (x = 1.0, y = 2.0, theta = 0)
```

### 4.1 Compute Average Forward Distance

```text
delta_s = (0.24 + 0.20) / 2 = 0.44 / 2 = 0.22 m
```

### 4.2 Compute Heading Change

```text
delta_theta = (0.24 - 0.20) / 0.40 = 0.04 / 0.40 = 0.10 rad
```

### 4.3 Approximate Updated Pose

Using a short-step approximation from `theta = 0`:

```text
new_x = 1.0 + 0.22 = 1.22
new_y = 2.0
new_theta = 0.10 rad
```

The robot moved forward about `0.22 m` and turned slightly left because the right wheel traveled farther.

Verification: the sign of `delta_theta` is positive because the right wheel displacement exceeds the left, so the updated pose with a small leftward turn is consistent with the wheel data.

## 5. Common Mistakes

1. **Ground-truth assumption.** Treating odometry as exact position knowledge ignores cumulative drift; use it as an estimate with uncertainty, not as truth.
2. **Calibration neglect.** Failing to calibrate wheel radius and axle length creates systematic pose bias; validate geometry against known motions.
3. **Slip ignorance.** Assuming wheel distance always equals body motion hides major error sources on turns or rough surfaces; expect slip in real or aggressive simulated maneuvers.
4. **Timestamp mismatch.** Using stale or inconsistent time intervals corrupts the integration process; synchronize encoder reads and updates carefully.
5. **No drift monitoring.** Running dead reckoning without comparison to landmarks, localization, or simulator truth makes drift invisible until it is large; log and compare trajectories regularly.

## 6. Practical Checklist

- [ ] Verify encoder interpretation, units, and update timing before trusting the pose estimate.
- [ ] Calibrate wheel radius and axle length using simple straight and turning tests.
- [ ] Plot odometry trajectories against simulator or external reference when available.
- [ ] Expect drift to grow and plan for later correction through localization or mapping.
- [ ] Log left and right wheel increments separately instead of only the fused pose.
- [ ] Treat sharp turns and slippery surfaces as high-risk drift scenarios.

## 7. References

- Thrun, Sebastian, Wolfram Burgard, and Dieter Fox. 2005. *Probabilistic Robotics*. MIT Press.
- Siciliano, Bruno, and Oussama Khatib, eds. 2016. *Springer Handbook of Robotics* (2nd ed.). Springer.
- Corke, Peter. 2017. *Robotics, Vision and Control* (2nd ed.). Springer.
- Cyberbotics. 2026. *Webots User Guide*. <https://cyberbotics.com/doc/guide/>
- ROS. 2026. *robot_localization Overview*. <https://docs.ros.org/en/noetic/api/robot_localization/html/index.html>
- Northwestern MSR. 2026. *Odometry Notes*. <https://nu-msr.github.io/navigation_site/lectures/odometry.html>
- LaValle, Steven M. 2006. *Planning Algorithms*. Cambridge University Press. <https://lavalle.pl/planning/>
