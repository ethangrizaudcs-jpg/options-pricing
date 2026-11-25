import numpy as np
import pytest

from optlab.black_scholes import bs_price
from optlab.montecarlo import mc_price

S0, K, R, SIGMA, T = 100.0, 100.0, 0.03, 0.20, 1.0


def test_atm_call_reference_value() -> None:
    assert float(bs_price(S0, K, R, SIGMA, T)) == pytest.approx(9.413403383853016, abs=1e-10)


@pytest.mark.parametrize("strike", [80.0, 100.0, 120.0])
def test_put_call_parity(strike: float) -> None:
    c = bs_price(S0, strike, R, SIGMA, T, option="call")
    p = bs_price(S0, strike, R, SIGMA, T, option="put")
    assert float(c - p) == pytest.approx(S0 - strike * np.exp(-R * T), abs=1e-10)


@pytest.mark.parametrize("option", ["call", "put"])
def test_matches_monte_carlo(option: str) -> None:
    mc, se = mc_price(S0, 110.0, R, 0.25, 0.5, 1_000_000, np.random.default_rng(0), option)
    assert abs(float(bs_price(S0, 110.0, R, 0.25, 0.5, option)) - mc) < 4 * se


def test_vectorised_over_spot() -> None:
    spots = np.array([80.0, 100.0, 120.0])
    prices = bs_price(spots, K, R, SIGMA, T)
    assert prices.shape == (3,)
    assert np.all(np.diff(prices) > 0)  # call price increases with spot


def test_short_maturity_tends_to_intrinsic_value() -> None:
    for s in [90.0, 110.0]:
        assert float(bs_price(s, K, R, SIGMA, 1e-10)) == pytest.approx(max(s - K, 0.0), abs=1e-6)
        assert float(bs_price(s, K, R, SIGMA, 1e-10, "put")) == pytest.approx(max(K - s, 0.0), abs=1e-6)


def test_zero_vol_tends_to_discounted_forward_intrinsic() -> None:
    # sigma -> 0: S_T = S0 e^{rT} for sure, so call -> max(S0 - K e^{-rT}, 0)
    for s in [90.0, 110.0]:
        assert float(bs_price(s, K, R, 1e-10, T)) == pytest.approx(max(s - K * np.exp(-R * T), 0.0), abs=1e-6)


def test_no_arbitrage_bounds() -> None:
    spots = np.linspace(50.0, 150.0, 21)
    c = bs_price(spots, K, R, SIGMA, T)
    assert np.all(c >= np.maximum(spots - K * np.exp(-R * T), 0.0) - 1e-12)
    assert np.all(c <= spots)


def test_unknown_option_type_raises() -> None:
    with pytest.raises(ValueError):
        bs_price(S0, K, R, SIGMA, T, option="straddle")
