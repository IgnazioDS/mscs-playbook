from __future__ import annotations

from dataclasses import dataclass

from ..probability.bayes_net import BayesNet, BayesNode
from ..probability.inference import query
from .reporting import write_markdown_report


@dataclass(frozen=True)
class DiagnosisResult:
    seed: int
    evidence: dict[str, bool]
    rain: float
    sprinkler: float


def _build_sprinkler_net() -> BayesNet:
    net = BayesNet()
    net.add_node(BayesNode("C", [], {(): 0.5}))
    net.add_node(BayesNode("S", ["C"], {(True,): 0.1, (False,): 0.5}))
    net.add_node(BayesNode("R", ["C"], {(True,): 0.8, (False,): 0.2}))
    net.add_node(
        BayesNode(
            "W",
            ["S", "R"],
            {
                (True, True): 0.99,
                (True, False): 0.90,
                (False, True): 0.90,
                (False, False): 0.0,
            },
        )
    )
    return net


def run_diagnosis(seed: int = 42, out: str | None = None) -> str:
    net = _build_sprinkler_net()
    evidence = {"W": True}
    rain_dist = query(net, "R", evidence)
    sprinkler_dist = query(net, "S", evidence)
    rain = round(rain_dist[True], 3)
    sprinkler = round(sprinkler_dist[True], 3)

    output_lines = [
        "task: diagnose",
        f"seed: {seed}",
        f"evidence: {evidence}",
        "query_results:",
        f"  P(Rain=1): {rain:.3f}",
        f"  P(Sprinkler=1): {sprinkler:.3f}",
    ]
    output = "\n".join(output_lines)

    if out:
        sections = [
            ("Inputs", f"seed: {seed}\nevidence: {evidence}"),
            ("Outputs", "\n".join(output_lines[3:])),
        ]
        write_markdown_report(out, "Diagnosis Report", sections, notes="Exact inference via enumeration.")

    return output
