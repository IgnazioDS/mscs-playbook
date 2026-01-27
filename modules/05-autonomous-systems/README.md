# 05-autonomous-systems

## Status
- Docs complete (concepts + cheat sheet)
- Implementations pending
- Case studies pending
- Verification demo pending

## Overview
This module introduces modeling and verification foundations for autonomous
systems: LTI dynamics, transition systems, timed automata, and hybrid intuition.
It emphasizes requirements (safety/liveness/reachability), lightweight checks,
and controller synthesis intuition.

## Prerequisites
- Python 3.10+
- Virtual environment tooling (venv)
- Basic linear algebra and discrete math

## How to use this module
1) Read the concept pages in order
2) Keep the cheat sheet nearby while modeling
3) Use implementations to simulate and verify toy systems

## Concepts
- [Unified Modeling Overview](01-concepts/unified-modeling-overview.md)
- [LTI Systems (Continuous and Discrete)](01-concepts/lti-systems-continuous-discrete.md)
- [Sequential Circuits and Transition Systems](01-concepts/sequential-circuits-and-transition-systems.md)
- [Timed Automata Basics](01-concepts/timed-automata-basics.md)
- [Hybrid Systems Intuition](01-concepts/hybrid-systems-intuition.md)
- [Requirements: Safety, Liveness, Reachability](01-concepts/requirements-safety-liveness-reachability.md)
- [LTL Basics and Trace Semantics](01-concepts/ltl-basics-trace-semantics.md)
- [Verification Toolbox](01-concepts/verification-toolbox.md)
- [Controller Synthesis Intuition](01-concepts/controller-synthesis-intuition.md)

## Cheat sheet
- [Autonomous Systems Cheat Sheet](02-cheatsheets/autonomous-systems-cheatsheet.md)

## Implementations
- Python reference implementations will live in
  `03-implementations/python/README.md` (added in the implementation branches).

## Tests
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r modules/05-autonomous-systems/03-implementations/python/requirements.txt`
- `python -m pytest -q modules/05-autonomous-systems/03-implementations/python/tests`

## Verification demo
- `python modules/05-autonomous-systems/03-implementations/python/src/demo.py`
