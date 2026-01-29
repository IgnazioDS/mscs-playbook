from src.rl.envs.gridworld import Gridworld
from src.rl.td.q_learning import q_learning
from src.rl.td.sarsa import sarsa
from src.rl.td.expected_sarsa import expected_sarsa


def test_q_learning_converges_on_gridworld():
    env = Gridworld(width=3, height=3, terminal_states={(2, 2): 0.0}, step_cost=-1.0, start_state=(0, 0))
    Q = q_learning(env, episodes=200, alpha=0.5, gamma=1.0, epsilon=0.1, seed=0)
    best = max(Q[(0, 0)].values())
    assert best <= -2.0 + 0.5


def test_sarsa_vs_q_learning_diff():
    env = Gridworld(width=3, height=3, terminal_states={(2, 2): 0.0}, step_cost=-1.0, start_state=(0, 0))
    Q_sarsa = sarsa(env, episodes=50, alpha=0.5, gamma=1.0, epsilon=0.2, seed=1)
    Q_q = q_learning(env, episodes=50, alpha=0.5, gamma=1.0, epsilon=0.2, seed=1)
    assert Q_sarsa[(0, 0)] != Q_q[(0, 0)]


def test_expected_sarsa_equals_sarsa_greedy():
    env = Gridworld(width=3, height=3, terminal_states={(2, 2): 0.0}, step_cost=-1.0, start_state=(0, 0))
    Q_sarsa = sarsa(env, episodes=50, alpha=0.5, gamma=1.0, epsilon=0.0, seed=2)
    Q_exp = expected_sarsa(env, episodes=50, alpha=0.5, gamma=1.0, epsilon=0.0, seed=2)
    assert Q_sarsa[(0, 0)] == Q_exp[(0, 0)]
