from itertools import combinations

from src.approx.vertex_cover_2approx import vertex_cover_2approx


def _is_cover(vertices: set[int], edges: list[tuple[int, int]]) -> bool:
    return all(u in vertices or v in vertices for u, v in edges)


def _optimal_vertex_cover_size(num_vertices: int, edges: list[tuple[int, int]]) -> int:
    for r in range(num_vertices + 1):
        for combo in combinations(range(num_vertices), r):
            if _is_cover(set(combo), edges):
                return r
    return num_vertices


def test_vertex_cover_2approx():
    # Happy path: cover all edges and respect the 2-approx bound on a small graph.
    num_vertices = 4
    edges = [(0, 1), (1, 2), (2, 3)]
    cover = set(vertex_cover_2approx(num_vertices, edges))
    assert _is_cover(cover, edges)
    opt = _optimal_vertex_cover_size(num_vertices, edges)
    assert len(cover) <= 2 * opt


def test_vertex_cover_empty():
    # Edge case: no edges means empty cover.
    assert vertex_cover_2approx(3, []) == set()
