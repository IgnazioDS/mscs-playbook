import math

from src.ai.probability.bayes_net import BayesNet, BayesNode
from src.ai.probability.inference import query


def build_sprinkler_net():
    net = BayesNet()
    net.add_node(BayesNode("C", [], {(): 0.5}))
    net.add_node(
        BayesNode(
            "S",
            ["C"],
            {
                (True,): 0.1,
                (False,): 0.5,
            },
        )
    )
    net.add_node(
        BayesNode(
            "R",
            ["C"],
            {
                (True,): 0.8,
                (False,): 0.2,
            },
        )
    )
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


def test_query_sprinkler():
    net = build_sprinkler_net()
    dist = query(net, "R", {"W": True})
    assert math.isclose(dist[True], 0.357, abs_tol=0.02)


def test_query_conditioning():
    net = build_sprinkler_net()
    dist = query(net, "S", {"C": True})
    assert math.isclose(dist[True], 0.1, abs_tol=1e-6)
