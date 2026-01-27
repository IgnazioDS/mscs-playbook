"""Timed automaton simulation.

Semantics (deterministic):
1) Check invariant at current location. If violated, stop.
2) Advance time by dt (all clocks increase).
3) Choose the first enabled edge (list order) unless policy selects an index.
4) Apply resets and update location.
"""

from __future__ import annotations

from typing import Callable, Dict, List

from src.ta.timed_automaton import Constraint, Edge, TimedAutomaton, constraints_hold

Policy = Callable[[List[Edge], str, Dict[str, float], int], int]


def _check_invariant(ta: TimedAutomaton, location: str, clocks: Dict[str, float]) -> bool:
    constraints = ta.invariants.get(location, [])
    return constraints_hold(constraints, clocks)


def simulate_ta(
    ta: TimedAutomaton,
    T: float,
    dt: float,
    policy: Policy | int | None = None,
) -> Dict[str, List]:
    if dt <= 0:
        raise ValueError("dt must be positive")
    if T < 0:
        raise ValueError("T must be non-negative")

    steps = int(T / dt)
    time = 0.0
    location = ta.initial_location
    clocks = {name: 0.0 for name in ta.clocks}

    trace_times: List[float] = [time]
    trace_locations: List[str] = [location]
    trace_clocks: List[Dict[str, float]] = [dict(clocks)]

    invariant_violated = False

    for step in range(steps):
        if not _check_invariant(ta, location, clocks):
            invariant_violated = True
            break

        time += dt
        for name in clocks:
            clocks[name] += dt

        enabled = ta.enabled_edges(location, clocks)
        if enabled:
            if callable(policy):
                chosen_index = policy(enabled, location, dict(clocks), step)
            elif isinstance(policy, int):
                chosen_index = policy
            else:
                chosen_index = 0

            chosen = enabled[chosen_index]
            location = chosen.target
            for clock in chosen.resets:
                if clock in clocks:
                    clocks[clock] = 0.0

        trace_times.append(time)
        trace_locations.append(location)
        trace_clocks.append(dict(clocks))

    return {
        "times": trace_times,
        "locations": trace_locations,
        "clock_values": trace_clocks,
        "invariant_violated": invariant_violated,
    }
