import numpy as np

from optlab.gbm import simulate_terminal

S0, MU, SIGMA, T = 100.0, 0.07, 0.20, 1.0
N = 1_000_000


def test_shape_and_positivity() -> None:
    S_T = simulate_terminal(S0, MU, SIGMA, T, n_paths=1000, rng=np.random.default_rng(0))
    assert S_T.shape == (1000,)
    assert np.all(S_T > 0)


def test_same_seed_same_paths() -> None:
    a = simulate_terminal(S0, MU, SIGMA, T, 100, rng=np.random.default_rng(42))
    b = simulate_terminal(S0, MU, SIGMA, T, 100, rng=np.random.default_rng(42))
    np.testing.assert_array_equal(a, b)


def test_mean_is_S0_exp_mu_T() -> None:
    # E[S_T] = S0 * exp(mu * T): checked within 4 Monte Carlo standard errors.
    S_T = simulate_terminal(S0, MU, SIGMA, T, N, rng=np.random.default_rng(1))
    std_error = S_T.std() / np.sqrt(N)
    assert abs(S_T.mean() - S0 * np.exp(MU * T)) < 4 * std_error


def test_log_return_is_gaussian_with_right_moments() -> None:
    # log(S_T / S0) ~ N((mu - sigma^2 / 2) T, sigma^2 T)
    S_T = simulate_terminal(S0, MU, SIGMA, T, N, rng=np.random.default_rng(2))
    log_ret = np.log(S_T / S0)
    assert abs(log_ret.mean() - (MU - SIGMA**2 / 2) * T) < 1e-3
    assert abs(log_ret.var() - SIGMA**2 * T) < 1e-3


def test_zero_vol_is_deterministic() -> None:
    S_T = simulate_terminal(S0, MU, 0.0, T, 10, rng=np.random.default_rng(3))
    np.testing.assert_allclose(S_T, S0 * np.exp(MU * T))
