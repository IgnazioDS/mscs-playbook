from src.ta.simulate import simulate_ta
from src.ta.timed_automaton import Edge, TimedAutomaton


def test_ta_guard_transition():
    ta = TimedAutomaton(
        locations={"safe", "unsafe"},
        initial_location="safe",
        clocks=["x"],
        invariants={"safe": [("x", "<=", 2.0)]},
        edges=[Edge("safe", "unsafe", guard=[("x", ">=", 2.0)], resets=[])],
    )

    trace = simulate_ta(ta, T=5.0, dt=1.0)

    assert trace["invariant_violated"] is False
    assert trace["times"][2] == 2.0
    assert trace["locations"][2] == "unsafe"


def test_ta_invariant_violation():
    ta = TimedAutomaton(
        locations={"safe"},
        initial_location="safe",
        clocks=["x"],
        invariants={"safe": [("x", "<=", 2.0)]},
        edges=[],
    )

    trace = simulate_ta(ta, T=5.0, dt=1.0)

    assert trace["invariant_violated"] is True
    assert trace["times"] == [0.0, 1.0, 2.0, 3.0]
    assert trace["locations"][-1] == "safe"
