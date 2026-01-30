# Multi-Robot Coordination

TL;DR: Coordinate multiple mobile robots in shared corridors using a fleet manager, validate with multi-robot Webots scenarios, and ship safe congestion control policies.

## Overview
- Problem: multiple robots sharing narrow corridors cause deadlocks and delays.
- Why it matters: throughput drops when robots block each other.
- Scope: 5 to 20 robots in a single facility.
- Stakeholders: robotics, operations, safety, logistics.
- Out of scope: inter-facility routing and long-haul logistics.
- Deliverable: fleet coordination service with safety guarantees.
- Success: operators can increase fleet size without changing layouts.
- Constraint: shared corridors must remain open to humans.
- Note: coordination must respect manual forklift crossings.

## Requirements and Constraints
### Functional
- Assign tasks and routes to each robot with priority rules.
- Prevent collisions and deadlocks in shared zones.
- Support human override and emergency stop per robot.
- Provide real-time fleet status and congestion metrics.

### Non-functional
- SLO: 99% of tasks complete within SLA window.
- Latency: fleet manager decisions < 250 ms.
- Cost: central planner runs on a single server.
- Safety: maintain 0.6 m minimum inter-robot distance.
- Reliability: degrade gracefully when comms are intermittent.
- Capacity: handle up to 50 concurrent tasks in the queue.

### Assumptions
- Robots publish pose and status at 5 to 10 Hz.
- Wi-Fi coverage is stable but may include short outages.
- Robots share a common coordinate frame and map version.
- Battery swaps are handled outside of task scheduling.

## System Design
### Components
- Fleet manager schedules tasks and assigns routes.
- Coordination layer manages shared zones and reservations.
- Robot agent reports status and follows assigned plan.
- Map server provides shared map and zones.
- Safety monitor enforces distance and speed limits.

### Data Flow
1) Tasks enter the queue with priority and deadline.
2) Fleet manager assigns tasks and paths.
3) Coordination layer reserves shared zones and locks passages.
4) Robot agents execute paths and report progress.
5) Fleet manager updates status and replans when needed.

### Interfaces
- `POST /tasks` with pickup/dropoff and priority.
- `GET /fleet/status` for robot states and congestion.
- `POST /fleet/override` to pause or reroute a robot.

### Data Schemas
- `tasks`: task_id, priority, deadline, pickup, dropoff.
- `robot_state`: robot_id, pose, battery, status, current_task.
- `zone_reservation`: zone_id, robot_id, start_time, end_time.

## Data and Modeling Approach
- Coordination: reservation-based traffic control for narrow zones.
- Planning: global route with time-expanded cost for congestion.
- Local avoidance: reciprocal velocity obstacles (RVO) for nearby robots.
- Sim-to-real: add comms delays and packet loss in simulation.
- Webots validation: multi-robot worlds with shared corridors.

## Evaluation Plan
- Metrics: throughput, average task time, deadlock rate.
- Safety: near-miss count and distance violations.
- Baselines: independent planners without coordination.
- Sim-to-real: compare Webots congestion patterns to field logs.
- Acceptance gates:
  - Deadlock rate < 0.5% across 1,000 tasks.
  - Throughput improvement >= 15% vs baseline.
  - No collisions in 2,000 simulated runs.

## Failure Modes and Mitigations
- Deadlocks in narrow corridors -> zone reservations with timeouts.
- Comms loss -> local safe stop and recovery protocol.
- Priority inversion -> enforce task aging and fairness.
- Map inconsistencies -> centralized map versioning.
- Sim-to-real gap -> stress tests with randomized delays.

## Operational Runbook
### Logging
- Log task assignments, zone reservations, and replans.
- Store robot telemetry with run_id and map version.

### Metrics
- Task completion time, idle time, congestion index.
- Reservation conflicts and override frequency.

### Tracing
- Trace task_id from assignment through completion.

### Alerts
- Repeated deadlocks in the same zone.
- Fleet manager latency > 500 ms.
- Robot disconnects > 30 seconds.

### Rollback
- Revert to last stable fleet policy and map version.
- Enable conservative mode with lower speed limits.

### On-call Checklist
- Inspect zone reservation logs and conflict hotspots.
- Validate comms health and robot agent versions.
- Replay Webots scenario for regression testing.

## Security, Privacy, and Compliance
- Authenticate robot agents and fleet API calls.
- Limit access to override and stop commands.
- Keep audit logs for safety incidents.

## Iteration Plan
- Add learning-based congestion predictions.
- Introduce multi-floor coordination and elevator scheduling.
- Support heterogeneous robot capabilities and load constraints.
