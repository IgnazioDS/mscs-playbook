from src.rl.envs.gridworld import Gridworld
from src.rl.mc.mc_prediction import mc_prediction
from src.rl.mc.mc_control import mc_control
from src.rl.dp.policy_eval import policy_evaluation


def test_mc_prediction_close_to_dp():
    env = Gridworld(width=2, height=2, terminal_states={(1, 1): 0.0}, step_cost=-1.0, start_state=(0, 0))
    policy = {(0, 0): "R", (0, 1): "D", (1, 0): "R"}
    V_dp = policy_evaluation(env, policy, gamma=1.0)
    V_mc = mc_prediction(env, policy, episodes=200, gamma=1.0, seed=0)
    assert abs(V_mc[(0, 0)] - V_dp[(0, 0)]) < 0.5


def test_mc_control_improves_returns():
    env = Gridworld(width=3, height=3, terminal_states={(2, 2): 0.0}, step_cost=-1.0, start_state=(0, 0))
    Q = mc_control(env, episodes=200, gamma=1.0, epsilon=0.2, seed=0)
    best = max(Q[(0, 0)].values())
    assert best <= -2.0 + 1.0
