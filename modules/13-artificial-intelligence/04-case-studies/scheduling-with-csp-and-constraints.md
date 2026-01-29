# Scheduling with CSP and Constraints

## Problem and constraints
- Assign tasks to resources with time and capacity limits
- Enforce precedence and availability constraints
- Provide feasible schedules quickly

## Modeling choices
- Variables represent task start times and assignments
- Domains are feasible time slots or resources
- Constraints enforce precedence and capacity limits

## Algorithm choice and why
- Backtracking with MRV/LCV for efficient search
- AC-3 for constraint propagation

## Evaluation plan
- Measure feasibility rate and runtime
- Compare against greedy baselines
- Validate constraint satisfaction on random instances

## Failure modes and mitigations
- Over-constrained schedules: add soft constraints
- Large domains: discretize or prune
- Slow convergence: improve heuristics and propagation

## Operational considerations
- Support incremental updates for new tasks
- Provide explanations for infeasible constraints
- Monitor performance as problem size grows

## What I would ship checklist
- [ ] Constraint validation with unit tests
- [ ] Heuristic tuning for typical workloads
- [ ] Diagnostics for infeasible inputs
- [ ] Performance benchmarks by size
- [ ] User-facing schedule explanations
