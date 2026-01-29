from src.ai.mdp.mdp import MDP
from src.ai.mdp.value_iteration import value_iteration
from src.ai.mdp.policy_eval import policy_evaluation


def build_tiny_mdp():
    states = ["s0", "s1", "s2"]
    actions = {"s0": ["a", "b"], "s1": [], "s2": []}
    transitions = {
        ("s0", "a", "s1"): 1.0,
        ("s0", "b", "s2"): 1.0,
    }
    rewards = {
        ("s0", "a", "s1"): 1.0,
        ("s0", "b", "s2"): 0.0,
    }
    return MDP(states, actions, transitions, rewards, gamma=0.9)


def test_value_iteration_policy():
    mdp = build_tiny_mdp()
    V, policy = value_iteration(mdp, theta=1e-6)
    assert policy["s0"] == "a"
    assert V["s0"] > 0.9


def test_policy_evaluation():
    mdp = build_tiny_mdp()
    policy = {"s0": "a"}
    V = policy_evaluation(mdp, policy, theta=1e-6)
    assert V["s0"] > 0.9
