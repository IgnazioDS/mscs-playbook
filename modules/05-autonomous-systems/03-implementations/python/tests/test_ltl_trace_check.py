from src.ltl.ast import AP, And, F, G, Not, Or, U, X
from src.ltl.trace_check import check


def test_atomic_and_boolean_ops():
    trace = [
        {"p"},
        {"q"},
    ]
    assert check(AP("p"), trace) is True
    assert check(AP("q"), trace) is False
    assert check(And(AP("p"), Not(AP("q"))), trace) is True
    assert check(Or(AP("q"), AP("p")), trace) is True


def test_next_at_last_state_is_false():
    trace = [{"p"}]
    assert check(X(AP("p")), trace) is False


def test_globally_and_eventually():
    trace = [
        {"ok"},
        {"ok"},
        {"bad"},
    ]
    assert check(G(AP("ok")), trace) is False
    assert check(F(AP("bad")), trace) is True


def test_until_holds_and_fails():
    trace_hold = [
        {"a"},
        {"a"},
        {"b"},
    ]
    trace_fail = [
        {"a"},
        {"c"},
        {"a"},
    ]
    assert check(U(AP("a"), AP("b")), trace_hold) is True
    assert check(U(AP("a"), AP("b")), trace_fail) is False


def test_safety_property():
    trace = [
        {"ok"},
        {"ok"},
        {"ok"},
    ]
    assert check(G(Not(AP("bad"))), trace) is True


def test_reachability_property():
    trace = [
        {"start"},
        {"mid"},
        {"goal"},
    ]
    assert check(F(AP("goal")), trace) is True


def test_nonzero_start_time():
    trace = [
        {"bad"},
        {"ok"},
        {"ok"},
    ]
    assert check(G(Not(AP("bad"))), trace, t0=1) is True
