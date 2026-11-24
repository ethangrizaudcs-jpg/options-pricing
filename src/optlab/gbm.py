"""Simulation of the underlying price under geometric Brownian motion."""

import numpy as np
from numpy.typing import NDArray


def simulate_terminal(
    S0: float,
    mu: float,
    sigma: float,
    T: float,
    n_paths: int,
    rng: np.random.Generator,
) -> NDArray[np.float64]:
    """Simulate n_paths values of the spot at the time T under GBM (sigma annualised, T in years)"""
    Z = rng.standard_normal(n_paths)
    S_T = S0 * np.exp((mu - (sigma**2)/2) * T + sigma * np.sqrt(T) * Z)
    return(S_T)
