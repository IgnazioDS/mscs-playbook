from src.rl.envs.gridworld import Gridworld
from src.rl.dp.policy_eval import policy_evaluation
from src.rl.dp.value_iteration import value_iteration
from src.rl.dp.policy_iteration import policy_iteration


def test_policy_eval_known_values():
    env = Gridworld(width=2, height=2, terminal_states={(1, 1): 0.0}, step_cost=-1.0, start_state=(0, 0))
    policy = {
        (0, 0): "R",
        (0, 1): "D",
        (1, 0): "R",
    }
    V = policy_evaluation(env, policy, gamma=1.0)
    assert V[(0, 1)] == 0.0
    assert V[(0, 0)] == -1.0


def test_value_iteration_better_than_random():
    env = Gridworld(width=3, height=3, terminal_states={(2, 2): 0.0}, step_cost=-1.0, start_state=(0, 0))
    random_policy = {s: {a: 1.0 / len(env.actions(s)) for a in env.actions(s)} for s in env.states() if env.actions(s)}
    V_rand = policy_evaluation(env, random_policy, gamma=1.0)
    V_opt, policy = value_iteration(env, gamma=1.0)
    assert V_opt[(0, 0)] >= V_rand[(0, 0)]


def test_policy_iteration_matches_value_iteration():
    env = Gridworld(width=3, height=3, terminal_states={(2, 2): 0.0}, step_cost=-1.0, start_state=(0, 0))
    _, policy_vi = value_iteration(env, gamma=1.0)
    _, policy_pi = policy_iteration(env, gamma=1.0)
    assert policy_pi[(0, 0)] == policy_vi[(0, 0)]
