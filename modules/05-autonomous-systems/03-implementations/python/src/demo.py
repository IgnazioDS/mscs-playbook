"""Verification demo for Module 05.

Runs small examples for:
- TS + LTL safety/reachability
- Timed automaton safety detection
- Greedy safety policy (toy synthesis intuition)
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Set
import sys

import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.ltl.ast import AP, F, G, Not
from src.ltl.trace_check import check
from src.synthesis.safety_policy import choose_next_state
from src.ta.simulate import simulate_ta
from src.ta.timed_automaton import Edge, TimedAutomaton
from src.ts.transition_system import TransitionSystem
from src.verify.bounded_reachability import bounded_find_path
from src.verify.invariants import check_invariant_over_trajectory
from src.lti.lti import simulate_discrete


def _print_header(title: str) -> None:
    print("=" * 60)
    print(title)
    print("=" * 60)


def example_ts_ltl() -> None:
    _print_header("Example A: Transition System + LTL")

    ts = TransitionSystem()
    ts.add_transition("s0", "s1")
    ts.add_transition("s1", "goal")
    ts.add_transition("s1", "bad")
    ts.add_transition("bad", "bad")
    ts.add_transition("goal", "goal")

    def label(state: str) -> Set[str]:
        labels: Set[str] = set()
        if state == "bad":
            labels.add("bad")
        if state == "goal":
            labels.add("goal")
        return labels

    safe_trace_states = ["s0", "s1", "goal"]
    unsafe_trace_states = ["s0", "s1", "bad"]

    safe_trace = [label(s) for s in safe_trace_states]
    unsafe_trace = [label(s) for s in unsafe_trace_states]

    safety = G(Not(AP("bad")))
    reach = F(AP("goal"))

    safe_safety = check(safety, safe_trace)
    unsafe_safety = check(safety, unsafe_trace)
    safe_reach = check(reach, safe_trace)
    unsafe_reach = check(reach, unsafe_trace)

    print("Safety property G(!bad):")
    print(f"  safe trace  -> {'PASS' if safe_safety else 'FAIL'}")
    print(f"  unsafe trace -> {'PASS' if unsafe_safety else 'FAIL'}")

    print("Reachability property F(goal):")
    print(f"  safe trace  -> {'PASS' if safe_reach else 'FAIL'}")
    print(f"  unsafe trace -> {'PASS' if unsafe_reach else 'FAIL'}")

    path = bounded_find_path(ts, "s0", "goal", k=3)
    print(f"Bounded reachability path to goal (k=3): {path}")


def example_ta_safety() -> None:
    _print_header("Example B: Timed Automaton Safety")

    ta = TimedAutomaton(
        locations={"safe", "unsafe"},
        initial_location="safe",
        clocks=["x"],
        invariants={"safe": [("x", "<=", 2.0)]},
        edges=[Edge("safe", "unsafe", guard=[("x", ">=", 2.0)], resets=[])],
    )

    trace = simulate_ta(ta, T=5.0, dt=1.0)
    locations = trace["locations"]
    times = trace["times"]

    violation_idx = None
    if "unsafe" in locations:
        violation_idx = locations.index("unsafe")
        print(f"Reached unsafe at t={times[violation_idx]} in location={locations[violation_idx]}")
    elif trace["invariant_violated"]:
        violation_idx = len(locations) - 1
        print(f"Invariant violated at t={times[violation_idx]} in location={locations[violation_idx]}")
    else:
        print("No safety violation detected in simulation.")


def example_synthesis_policy() -> None:
    _print_header("Example C: Toy Safety Policy")

    ts = TransitionSystem()
    ts.add_transition("s0", "s1")
    ts.add_transition("s1", "bad")
    ts.add_transition("s1", "goal")
    ts.add_transition("goal", "goal")
    ts.add_transition("bad", "bad")

    bad_states = {"bad"}
    current = "s0"
    trace_states: List[str] = [current]

    for _ in range(3):
        nxt = choose_next_state(ts, current, bad_states)
        if nxt is None:
            break
        trace_states.append(nxt)
        current = nxt

    trace = [
        {"bad"} if s == "bad" else set() for s in trace_states
    ]

    safety = G(Not(AP("bad")))
    print(f"Greedy trace: {trace_states}")
    print(f"G(!bad) on greedy trace -> {'PASS' if check(safety, trace) else 'FAIL'}")


def example_lti_invariant() -> None:
    _print_header("Example D: LTI Invariant Check")

    A = np.array([[1.0]])
    B = np.array([[1.0]])
    x0 = np.array([0.0])
    U = np.array([1.0, 1.0, 1.0])

    X = simulate_discrete(A, B, x0, U)
    ok, idx = check_invariant_over_trajectory(X, lambda x: abs(x[0]) <= 10.0)
    print(f"Invariant |x|<=10 holds: {ok} (first bad index: {idx})")


def main() -> None:
    example_ts_ltl()
    example_ta_safety()
    example_synthesis_policy()
    example_lti_invariant()


if __name__ == "__main__":
    main()
