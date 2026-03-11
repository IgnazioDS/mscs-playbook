# Sensors, Noise, and Filters

## Key Ideas

- Robotic sensing is never exact: measurements are affected by noise, bias, delay, quantization, and frame misalignment.
- Filtering is the process of turning noisy signals into more stable state estimates, but every filter trades noise reduction against responsiveness and model assumptions.
- Understanding the noise characteristics of a sensor matters more than memorizing filter names, because filter quality depends on how well its assumptions match the data.
- Bias and drift are often more dangerous than high-frequency noise because they quietly distort estimates over long horizons.
- Filtering is most useful when paired with logging and calibration so the team can compare raw and filtered behavior directly.

## 1. What Sensor Noise Means

Sensor noise is the discrepancy between the measured value and the underlying physical quantity the robot wants to estimate. Some of that discrepancy is random, and some is systematic.

### 1.1 Core Definitions

- **Noise** is random variation in a measurement.
- **Bias** is a consistent offset from the true value.
- **Drift** is slow change in the measurement bias over time.
- A **low-pass filter** suppresses rapid changes while preserving slower trends.
- **Sensor fusion** combines multiple sensors to estimate a state more reliably than any one sensor alone.

### 1.2 Why This Matters

Control, localization, and mapping all depend on sensor inputs. If the team does not understand the measurement quality, it becomes hard to know whether a downstream failure is caused by poor control, poor estimation, or simply bad raw sensing.

## 2. Common Noise Sources

### 2.1 Random Measurement Noise

This includes jitter in range sensors, encoder noise, and small camera or IMU measurement fluctuations.

### 2.2 Systematic Error

Examples include miscalibrated sensor scale, constant offset, or incorrect mounting orientation.

### 2.3 Environmental Effects

Lighting changes, reflective surfaces, wheel slip, and clutter can alter sensor quality even when the sensor itself is functioning normally.

## 3. Filter Intuition

### 3.1 Simple Smoothing

Moving averages and low-pass filters reduce high-frequency noise, but they also introduce lag.

### 3.2 Model-Based Filtering

Kalman-family filters combine prediction and correction, using both a motion model and sensor model to estimate state.

### 3.3 Why Tuning Matters

If the filter assumes sensors are more accurate than they really are, it becomes overconfident. If it assumes they are too noisy, it may respond too slowly.

## 4. Worked Example: Three-Sample Moving Average

Suppose a range sensor measures distance to a wall across five steps:

```text
raw = [1.00, 1.20, 0.90, 1.10, 1.00] meters
```

Use a moving average of window size `3` starting from the third sample.

### 4.1 Compute the First Smoothed Value

```text
avg_3 = (1.00 + 1.20 + 0.90) / 3
avg_3 = 3.10 / 3 = 1.0333... m
```

### 4.2 Compute the Next Smoothed Values

```text
avg_4 = (1.20 + 0.90 + 1.10) / 3
avg_4 = 3.20 / 3 = 1.0667... m

avg_5 = (0.90 + 1.10 + 1.00) / 3
avg_5 = 3.00 / 3 = 1.00 m
```

### 4.3 Interpret the Result

The filtered sequence:

```text
[1.0333..., 1.0667..., 1.00]
```

is less noisy than the raw measurements, but it also reacts more slowly to sudden changes. This illustrates the basic smoothing-lag tradeoff.

Verification: each filtered value is the arithmetic mean of the corresponding three-sample window, so the computed smoothed sequence is internally consistent.

## 5. Common Mistakes

1. **Noise-only thinking.** Treating all sensor error as random noise ignores bias, drift, and miscalibration; characterize systematic error separately.
2. **Over-smoothing.** Using a filter that removes noise but also removes needed responsiveness can destabilize control; tune smoothing against the task dynamics.
3. **Frame mismatch.** Filtering data in the wrong coordinate frame or mixing sensor frames carelessly corrupts the estimate; verify frame conventions before tuning.
4. **Blind trust in fused output.** Assuming a fused estimate must be better than raw signals can hide model mismatch; compare filtered output against reference behavior.
5. **No raw logging.** Keeping only filtered signals makes debugging much harder; log raw and filtered values together so filter effects are observable.

## 6. Practical Checklist

- [ ] Measure raw sensor behavior before selecting a filter.
- [ ] Distinguish random noise, bias, and drift in the sensor characterization.
- [ ] Start with simple filters and add model complexity only when needed.
- [ ] Tune filter parameters against logged data rather than guesswork alone.
- [ ] Verify coordinate frames and units before fusing multiple sensors.
- [ ] Plot raw and filtered signals together when debugging control or localization issues.

## 7. References

- Thrun, Sebastian, Wolfram Burgard, and Dieter Fox. 2005. *Probabilistic Robotics*. MIT Press.
- Maybeck, Peter S. 1979. *Stochastic Models, Estimation, and Control*. Academic Press.
- Grewal, Mohinder S., and Angus P. Andrews. 2015. *Kalman Filtering* (4th ed.). Wiley.
- Cyberbotics. 2026. *Sensors Guide*. <https://cyberbotics.com/doc/guide/sensors>
- ROS. 2026. *robot_localization Overview*. <https://docs.ros.org/en/noetic/api/robot_localization/html/index.html>
- Labbe, Roger R. 2026. *Kalman and Bayesian Filters in Python*. <https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python>
- Corke, Peter. 2017. *Robotics, Vision and Control* (2nd ed.). Springer.
