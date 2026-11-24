import numpy as np
import pytest

from optlab.montecarlo import mc_price

S0, K, R, SIGMA, T = 100.0, 100.0, 0.03, 0.20, 1.0
N = 1_000_000
BS_CALL_ATM = 9.413403383853016  # Black-Scholes closed form for these parameters


def test_returns_price_and_std_error() -> None:
    price, se = mc_price(S0, K, R, SIGMA, T, 1000, rng=np.random.default_rng(0))
    assert isinstance(price, float) and isinstance(se, float)
    assert se > 0


def test_call_matches_black_scholes_within_ci() -> None:
    price, se = mc_price(S0, K, R, SIGMA, T, N, rng=np.random.default_rng(1))
    assert abs(price - BS_CALL_ATM) < 1.96 * se * 2  # loose: 2x the 95% half-width


def test_zero_strike_call_is_worth_the_stock() -> None:
    # A call with K = 0 pays S_T: its price must be S0 (discounted S is a Q-martingale).
    price, se = mc_price(S0, 0.0, R, SIGMA, T, N, rng=np.random.default_rng(2))
    assert abs(price - S0) < 4 * se


def test_put_call_parity() -> None:
    c, se_c = mc_price(S0, K, R, SIGMA, T, N, rng=np.random.default_rng(3), option="call")
    p, se_p = mc_price(S0, K, R, SIGMA, T, N, rng=np.random.default_rng(4), option="put")
    assert abs((c - p) - (S0 - K * np.exp(-R * T))) < 4 * np.hypot(se_c, se_p)


def test_zero_vol_is_discounted_intrinsic_value() -> None:
    # sigma = 0: S_T = S0 e^{rT} for sure, so call = max(S0 - K e^{-rT}, 0), no error.
    price, se = mc_price(S0, 90.0, R, 0.0, T, 100, rng=np.random.default_rng(5))
    assert price == pytest.approx(S0 - 90.0 * np.exp(-R * T))
    assert se == pytest.approx(0.0)


def test_std_error_shrinks_like_one_over_sqrt_n() -> None:
    _, se_small = mc_price(S0, K, R, SIGMA, T, 10_000, rng=np.random.default_rng(6))
    _, se_big = mc_price(S0, K, R, SIGMA, T, 40_000, rng=np.random.default_rng(7))
    assert se_big / se_small == pytest.approx(0.5, rel=0.05)


def test_unknown_option_type_raises() -> None:
    with pytest.raises(ValueError):
        mc_price(S0, K, R, SIGMA, T, 10, rng=np.random.default_rng(8), option="straddle")
