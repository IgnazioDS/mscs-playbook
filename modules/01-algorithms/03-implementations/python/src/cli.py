from __future__ import annotations

import json
import sys
from typing import Any, Callable, Dict

from src.approx.vertex_cover_2approx import vertex_cover_2approx
from src.dp.fibonacci_memo import fibonacci
from src.dp.knapsack_01 import knapsack_01
from src.dp.longest_increasing_subsequence import lis_length
from src.greedy.huffman_coding import build_huffman_codes
from src.greedy.interval_scheduling import select_max_non_overlapping
from src.graphs.bfs import bfs_distances
from src.graphs.dfs import dfs_order
from src.graphs.dijkstra import dijkstra
from src.graphs.kruskal_mst import kruskal_mst
from src.graphs.topological_sort import topological_sort

Algorithm = Callable[[Dict[str, Any]], Any]


def _require_keys(payload: Dict[str, Any], keys: list[str]) -> None:
    missing = [k for k in keys if k not in payload]
    if missing:
        raise ValueError(f"missing keys: {', '.join(missing)}")


def _run_fibonacci(payload: Dict[str, Any]) -> Any:
    _require_keys(payload, ["n"])
    return fibonacci(int(payload["n"]))


def _run_knapsack(payload: Dict[str, Any]) -> Any:
    _require_keys(payload, ["values", "weights", "capacity"])
    return knapsack_01(list(payload["values"]), list(payload["weights"]), int(payload["capacity"]))


def _run_lis(payload: Dict[str, Any]) -> Any:
    _require_keys(payload, ["nums"])
    return lis_length(list(payload["nums"]))


def _run_interval(payload: Dict[str, Any]) -> Any:
    _require_keys(payload, ["intervals"])
    return select_max_non_overlapping([tuple(i) for i in payload["intervals"]])


def _run_huffman(payload: Dict[str, Any]) -> Any:
    _require_keys(payload, ["freqs"])
    return build_huffman_codes(dict(payload["freqs"]))


def _run_bfs(payload: Dict[str, Any]) -> Any:
    _require_keys(payload, ["graph", "start"])
    return bfs_distances(payload["graph"], payload["start"])


def _run_dfs(payload: Dict[str, Any]) -> Any:
    _require_keys(payload, ["graph", "start"])
    return dfs_order(payload["graph"], payload["start"])


def _run_dijkstra(payload: Dict[str, Any]) -> Any:
    _require_keys(payload, ["graph", "start"])
    return dijkstra(payload["graph"], payload["start"])


def _run_toposort(payload: Dict[str, Any]) -> Any:
    _require_keys(payload, ["graph"])
    return topological_sort(payload["graph"])


def _run_kruskal(payload: Dict[str, Any]) -> Any:
    _require_keys(payload, ["num_vertices", "edges"])
    edges = [tuple(e) for e in payload["edges"]]
    return kruskal_mst(int(payload["num_vertices"]), edges)


def _run_vertex_cover(payload: Dict[str, Any]) -> Any:
    _require_keys(payload, ["num_vertices", "edges"])
    edges = [tuple(e) for e in payload["edges"]]
    return sorted(vertex_cover_2approx(int(payload["num_vertices"]), edges))


ALGORITHMS: Dict[str, Algorithm] = {
    "fibonacci": _run_fibonacci,
    "knapsack_01": _run_knapsack,
    "lis": _run_lis,
    "interval_scheduling": _run_interval,
    "huffman": _run_huffman,
    "bfs": _run_bfs,
    "dfs": _run_dfs,
    "dijkstra": _run_dijkstra,
    "topological_sort": _run_toposort,
    "kruskal_mst": _run_kruskal,
    "vertex_cover": _run_vertex_cover,
}


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("Usage: python -m src.cli <algorithm> '<json_payload>'")
        print("Available:", ", ".join(sorted(ALGORITHMS.keys())))
        return 1

    algo_name = argv[1]
    payload_raw = argv[2]
    if algo_name not in ALGORITHMS:
        print(f"Unknown algorithm: {algo_name}")
        print("Available:", ", ".join(sorted(ALGORITHMS.keys())))
        return 1

    try:
        payload = json.loads(payload_raw)
        if not isinstance(payload, dict):
            raise ValueError("payload must be a JSON object")
        result = ALGORITHMS[algo_name](payload)
    except Exception as exc:  # keep CLI small and direct
        print(f"Error: {exc}")
        return 2

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
