from src.ts.bfs_reachability import bfs_reachable, reconstruct_path
from src.ts.transition_system import TransitionSystem


def test_bfs_reachability_path():
    ts = TransitionSystem()
    ts.add_transition("A", "B")
    ts.add_transition("B", "C")
    ts.add_transition("A", "D")
    ts.add_transition("D", "C")

    found, parent = bfs_reachable(ts, "A", "C")
    path = reconstruct_path(parent, "A", "C")

    assert found is True
    assert path == ["A", "B", "C"]


def test_bfs_reachability_unreachable():
    ts = TransitionSystem()
    ts.add_transition("A", "B")
    ts.add_transition("B", "C")

    found, parent = bfs_reachable(ts, "C", "A")
    path = reconstruct_path(parent, "C", "A")

    assert found is False
    assert path == []
