# Concepts

Read these pages in numerical order. Later pages assume the motion, sensing,
and estimation foundations established by the earlier ones.

- [01 Differential Drive Kinematics](01-differential-drive-kinematics.md): the geometric model that relates wheel motion to body motion.
- [02 Odometry and Dead Reckoning](02-odometry-and-dead-reckoning.md): incremental pose estimation and the drift behavior that follows from it.
- [03 Sensors, Noise, and Filters](03-sensors-noise-and-filters.md): how sensing errors appear and how filtering stabilizes measurements.
- [04 Occupancy Grids and Mapping](04-occupancy-grids-and-mapping.md): discrete map construction from uncertain range measurements.
- [05 Localization Intuition: UKF and Particle Filters](05-localization-intuition-ukf-and-particle-filters.md): the main belief-state ideas behind nonlinear pose estimation.
- [06 Path Planning: A* and Dijkstra](06-path-planning-a-star-and-dijkstra.md): shortest-path planning on discretized maps.
- [07 Trajectory Generation and Controllers](07-trajectory-generation-and-controllers.md): the bridge from planned path to executable robot motion.
- [08 SLAM Overview and Tradeoffs](08-slam-overview-and-tradeoffs.md): joint pose and map estimation with loop-closure and uncertainty tradeoffs.
- [09 Webots Workflow and Controller Structure](09-webots-workflow-and-controller-structure.md): how to organize a simulation controller and reproducible Webots experiment loop.
