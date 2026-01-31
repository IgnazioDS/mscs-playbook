# Indoor Mapping

TL;DR: Build a mapping pipeline for indoor facilities using SLAM, validate against Webots ground truth, and ship a map update workflow that operators can trust.

## Overview
- Problem: facilities need up-to-date maps for navigation and safety checks.
- Why it matters: outdated maps cause route failures and safety risks.
- Scope: single-robot mapping runs for offices and light industrial spaces.
- Stakeholders: robotics, facilities, safety, operations.
- Out of scope: multi-floor 3D mapping and semantic labeling.
- Deliverable: occupancy grid maps with update cadence and QA gates.
- Success: operators can approve maps with a simple checklist.
- Constraint: mapping runs must avoid active office hours.

## Requirements and Constraints
### Functional
- Create a new map within 30 minutes of exploration.
- Support loop closure to reduce drift.
- Export maps in standard formats for navigation stack.
- Provide map change summaries for operator review.

### Non-functional
- SLO: map error < 0.2 m in 95% of cells.
- Latency: offline map build completes in < 20 minutes.
- Cost: run on embedded CPU with limited memory.
- Safety: robot must avoid restricted zones during mapping.
- Reliability: mapping succeeds in 95% of runs.
- Data retention: raw logs kept for 30 days for audits.

### Assumptions
- Lidar provides adequate coverage for 2D mapping.
- The environment is mostly static during mapping runs.
- Floor surfaces are consistent; no frequent moving walls.
- Access to facility after hours is available for mapping.

## System Design
### Components
- Data logger captures lidar, odometry, and IMU.
- SLAM engine performs pose graph optimization.
- Map builder renders occupancy grid and metadata.
- QA checker validates map quality against thresholds.
- Map registry stores versions and approvals.

### Data Flow
1) Robot collects sensor logs during guided exploration.
2) SLAM engine builds a pose graph and closes loops.
3) Map builder generates occupancy grid and metadata.
4) QA checker validates coverage and error bounds.
5) Map registry publishes approved map version.

### Interfaces
- `POST /maps/build` with log_id and map params.
- `GET /maps/{map_id}` returns map artifacts and metadata.
- `POST /maps/{map_id}/approve` for operator signoff.

### Data Schemas
- `sensor_logs`: log_id, start_time, duration, sensors, checksum.
- `map_metadata`: map_id, resolution, bounds, error_estimate.
- `map_versions`: map_id, version, approved_by, approved_at.

## Data and Modeling Approach
- SLAM: graph-based SLAM with loop closure detection.
- Odometry fusion: integrate wheel encoders and IMU.
- Outlier rejection: discard scans with high motion distortion.
- Webots validation: replay simulated logs with known ground truth.
- Sim-to-real: calibrate lidar offset and wheel slip parameters.
- Map resolution: default 0.05 m per cell; configurable per facility.
- Pose graph: save intermediate checkpoints for partial recovery.

## Evaluation Plan
- Metrics: absolute trajectory error, map coverage, map error.
- Baselines: dead-reckoning-only mapping without loop closure.
- Acceptance gates:
  - Trajectory error < 0.2 m for 95% of poses.
  - Coverage > 90% of accessible area.
  - No large gaps in critical corridors.
- Sim-to-real: compare Webots ground truth and physical logs.

## Failure Modes and Mitigations
- Loop closure failures -> adjust scan matching thresholds.
- Dynamic obstacles during mapping -> schedule runs off-hours.
- Drift due to wheel slip -> fuse IMU and increase loop closures.
- Sparse features -> add fiducials or reflective markers.
- Sim-to-real gap -> validate with multiple Webots worlds.

## Operational Runbook
### Logging
- Record log_id, sensor health, and mapping parameters.
- Store pose graph stats and loop closure counts.

### Metrics
- Map error estimates, coverage percentage, build time.
- QA pass rate and approval turnaround time.

### Tracing
- Trace map_id from log ingestion to registry publish.

### Alerts
- Mapping failure or QA rejection.
- Map error exceeds threshold for two consecutive runs.
- Sensor dropout rate > 2% during logging.

### Rollback
- Keep prior approved map versions for rollback.
- Navigation stack always uses last approved map.

### On-call Checklist
- Verify sensor calibration and log completeness.
- Review QA report and map change summary.
- Re-run mapping in Webots before field retry.

## Security, Privacy, and Compliance
- Remove facility identifiers when sharing logs externally.
- Control access to map registry and approvals.
- Keep audit trails for approved map changes.

## Iteration Plan
- Add semantic labels for restricted and high-traffic zones.
- Introduce continuous mapping with incremental updates.
- Expand to 3D mapping for multi-level facilities.
