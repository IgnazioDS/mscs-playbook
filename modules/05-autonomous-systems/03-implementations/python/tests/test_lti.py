import numpy as np

from src.lti.discretization import zoh_discretize
from src.lti.lti import simulate_discrete


def test_simulate_discrete_1d():
    A = np.array([[1.0]])
    B = np.array([[1.0]])
    x0 = np.array([0.0])
    U = np.array([1.0, 1.0, 1.0])

    X = simulate_discrete(A, B, x0, U)

    assert X.shape == (4, 1)
    assert np.allclose(X.squeeze(), np.array([0.0, 1.0, 2.0, 3.0]))


def test_simulate_discrete_scalar_input_shape():
    A = np.array([[1.0]])
    B = np.array([[2.0]])
    x0 = np.array([1.0])
    U = np.array([0.0, 1.0])

    X = simulate_discrete(A, B, x0, U)

    assert X.shape == (3, 1)
    assert np.allclose(X.squeeze(), np.array([1.0, 1.0, 3.0]))


def test_zoh_discretize_simple_integrator():
    Ac = np.array([[0.0]])
    Bc = np.array([[1.0]])
    Ad, Bd = zoh_discretize(Ac, Bc, dt=0.1)

    assert np.allclose(Ad, np.array([[1.0]]), atol=1e-6)
    assert np.allclose(Bd, np.array([[0.1]]), atol=1e-6)
