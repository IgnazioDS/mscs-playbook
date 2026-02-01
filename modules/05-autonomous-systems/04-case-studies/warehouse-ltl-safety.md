# Case Study: Warehouse LTL Safety Rules

## Overview
A warehouse robot fleet must obey safety rules while moving pallets. The system
uses LTL constraints to prevent entering forbidden zones during maintenance.

## Requirements
- No entry into maintenance cells while active
- Reach goal within a bounded number of steps
- Provide evidence of rule compliance

## Approach
- Model the floorplan as a transition system.
- Encode safety rules as LTL formulas.
- Use a verifier to check traces from a controller policy.

## Key Decisions
- Keep the state space coarse to ensure fast verification.
- Use explicit forbidden zones instead of learned penalties.
- Log violating traces for debugging.

## Outcomes
- Safety rules validated for default policy.
- Violations easily reproduced for bad policies.

## Pitfalls
- Under-approximating obstacles (missed collisions)
- Overly strict rules that prevent any plan

