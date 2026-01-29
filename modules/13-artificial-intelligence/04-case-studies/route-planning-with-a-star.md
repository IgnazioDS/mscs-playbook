# Route Planning with A*

## Problem and constraints
- Find shortest paths between locations with weighted edges
- Handle dynamic traffic updates and blocked routes
- Require fast response times for user queries

## Modeling choices
- Graph with nodes as intersections and weighted edges
- Heuristic using straight-line distance
- Closed set to avoid revisiting nodes

## Algorithm choice and why
- A* balances optimality and efficiency
- Admissible heuristic guarantees optimal routes

## Evaluation plan
- Compare against baseline UCS on sampled routes
- Measure path length, runtime, and node expansions
- Validate on known shortest paths

## Failure modes and mitigations
- Non-admissible heuristic: enforce heuristic bounds
- Graph errors or missing edges: validate data integrity
- Slow performance on dense graphs: prune or precompute

## Operational considerations
- Cache popular routes
- Update edge weights with traffic feeds
- Monitor latency and fallback to UCS if needed

## What I would ship checklist
- [ ] Verified heuristic admissibility
- [ ] Regression suite for routing correctness
- [ ] Latency benchmarks per region
- [ ] Monitoring for data drift and outages
- [ ] Rollback plan for weight updates
