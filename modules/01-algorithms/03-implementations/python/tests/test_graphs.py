import pytest

from src.graphs.bfs import bfs_distances
from src.graphs.dfs import dfs_order
from src.graphs.dijkstra import dijkstra
from src.graphs.kruskal_mst import kruskal_mst
from src.graphs.topological_sort import topological_sort


def test_bfs_distances():
    graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
    distances = bfs_distances(graph, "A")
    assert distances == {"A": 0, "B": 1, "C": 1, "D": 2}


def test_dfs_order():
    graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
    assert dfs_order(graph, "A") == ["A", "B", "D", "C"]


def test_dijkstra():
    graph = {
        "A": [("B", 1), ("C", 4)],
        "B": [("C", 2), ("D", 5)],
        "C": [("D", 1)],
        "D": [],
    }
    distances = dijkstra(graph, "A")
    assert distances == {"A": 0, "B": 1, "C": 3, "D": 4}


def test_topological_sort():
    graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
    order = topological_sort(graph)
    position = {node: idx for idx, node in enumerate(order)}
    for u, neighbors in graph.items():
        for v in neighbors:
            assert position[u] < position[v]


def test_topological_sort_cycle():
    graph = {"A": ["B"], "B": ["A"]}
    with pytest.raises(ValueError):
        topological_sort(graph)


def test_kruskal_mst():
    edges = [
        (0, 1, 10),
        (0, 2, 6),
        (0, 3, 5),
        (1, 3, 15),
        (2, 3, 4),
    ]
    total, mst = kruskal_mst(4, edges)
    assert total == 19
    assert len(mst) == 3
