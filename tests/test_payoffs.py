import numpy as np

from optlab.payoffs import call_payoff, put_payoff


def test_call_payoff_values() -> None:
    S_T = np.array([80.0, 100.0, 130.0])
    np.testing.assert_allclose(call_payoff(S_T, K=100.0), [0.0, 0.0, 30.0])


def test_put_payoff_values() -> None:
    S_T = np.array([80.0, 100.0, 130.0])
    np.testing.assert_allclose(put_payoff(S_T, K=100.0), [20.0, 0.0, 0.0])


def test_payoffs_accept_scalar() -> None:
    assert float(call_payoff(130.0, K=100.0)) == 30.0
    assert float(put_payoff(80.0, K=100.0)) == 20.0


def test_call_minus_put_is_forward_payoff() -> None:
    # (S-K)^+ - (K-S)^+ = S - K for every S: the payoff identity behind put-call parity.
    S_T = np.linspace(0.0, 200.0, 401)
    np.testing.assert_allclose(call_payoff(S_T, 100.0) - put_payoff(S_T, 100.0), S_T - 100.0)


def test_payoffs_accept_python_list() -> None:
    np.testing.assert_allclose(call_payoff([80, 100, 130], K=100), [0.0, 0.0, 30.0])
