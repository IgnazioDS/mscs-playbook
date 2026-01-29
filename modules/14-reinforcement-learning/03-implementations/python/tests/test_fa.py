from src.rl.envs.chain import ChainEnv
from src.rl.fa.features import chain_features
from src.rl.fa.linear_value import td0_linear, value_from_weights


def test_linear_value_updates():
    env = ChainEnv(length=5, start=2, reward_right=1.0)
    w = td0_linear(env, lambda s: chain_features(s, env.length), alpha=0.1, gamma=1.0, episodes=50, seed=0)
    v_start = value_from_weights(w, lambda s: chain_features(s, env.length), 2)
    v_left = value_from_weights(w, lambda s: chain_features(s, env.length), 1)
    assert v_start >= v_left
