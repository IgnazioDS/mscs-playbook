from src.robotics.filters import alpha_beta_filter, moving_average


def test_moving_average_smooths():
    seq = [0, 0, 10, 10, 10]
    smoothed = moving_average(seq, window=3)
    assert smoothed[2] < seq[2]


def test_alpha_beta_filter_reduces_noise():
    measurements = [0, 0, 10, 10, 10]
    xs, vs = alpha_beta_filter(measurements, alpha=0.2, beta=0.1, dt=1.0)
    assert len(xs) == len(measurements)
    assert xs[2] < measurements[2]
