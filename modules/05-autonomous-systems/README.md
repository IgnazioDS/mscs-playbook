# Autonomous Systems

## Status

- Docs complete
- Modeling implementations complete
- LTL checker complete
- Verification demo complete

## Overview

This module introduces modeling and verification foundations for autonomous
systems: state-based modeling, transition systems, temporal logic, LTI
dynamics, timed automata, hybrid automata, verification workflows, and
controller synthesis. It emphasizes formal specification, executable traces,
tool-aware reasoning, and the bridge between control theory and computer
science formal methods.

## Prerequisites

- Python 3.10+
- Virtual environment tooling (venv)
- Basic linear algebra and discrete math

## How to use this module

- Read the concept pages in order.
- Keep the cheat sheet nearby while modeling.
- Use the implementations to simulate and verify the smaller examples before
  moving to the case studies.

## Recommended learning path

1. Start with the shared modeling vocabulary, then the module overview, so the
   later formalisms have a common semantic frame.
2. Learn finite-state behavior and temporal specifications before moving into
   dense time and continuous dynamics.
3. Study LTI systems, timed automata, and hybrid systems as three different
   answers to the question "how does state evolve over time?"
4. Finish with the verification toolbox and controller synthesis once the model
   classes and property classes are already familiar.

## Quickstart

- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `python3 -m pip install -r modules/05-autonomous-systems/03-implementations/python/requirements.txt`
- `python3 -m pytest -q modules/05-autonomous-systems/03-implementations/python/tests`
- `python3 modules/05-autonomous-systems/03-implementations/python/src/demo.py`

## Concepts (reading order)

- [01 State, Trace, and Abstraction Foundations](01-concepts/01-state-trace-and-abstraction-foundations.md)
- [02 Unified Modeling Overview](01-concepts/02-unified-modeling-overview.md)
- [03 Sequential Circuits and Transition Systems](01-concepts/03-sequential-circuits-and-transition-systems.md)
- [04 LTL Basics and Trace Semantics](01-concepts/04-ltl-basics-trace-semantics.md)
- [05 Requirements: Safety, Liveness, Reachability](01-concepts/05-requirements-safety-liveness-reachability.md)
- [06 LTI Systems (Continuous and Discrete)](01-concepts/06-lti-systems-continuous-discrete.md)
- [07 Timed Automata Basics](01-concepts/07-timed-automata-basics.md)
- [08 Hybrid Systems Intuition](01-concepts/08-hybrid-systems-intuition.md)
- [09 Verification Toolbox](01-concepts/09-verification-toolbox.md)
- [10 Controller Synthesis Intuition](01-concepts/10-controller-synthesis-intuition.md)

## Concept-to-project bridge

- Read `01` through `05` before writing formal requirements or checking traces
  with the Python implementations.
- Read `06` through `08` before modeling physical plants, real-time deadlines,
  or cyber-physical switching behavior.
- Read `09` before choosing a verifier or interpreting a tool result.
- Read `10` once the verification material is comfortable enough that the
  verification-versus-synthesis distinction is clear.

## Cheat sheet

- [Autonomous Systems Cheat Sheet](02-cheatsheets/autonomous-systems-cheatsheet.md)

## Implementations

- [Python reference implementations](03-implementations/python/README.md)

## Demo

- `python3 modules/05-autonomous-systems/03-implementations/python/src/demo.py`
