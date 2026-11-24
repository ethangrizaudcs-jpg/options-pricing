"""Payoff functions of European options at maturity."""

import numpy as np
from numpy.typing import ArrayLike, NDArray


def call_payoff(S_T: ArrayLike, K: float) -> NDArray[np.float64]:
    """Call payoff max(S_T-K,0), works on scalars and arrays"""
    S_T = np.asarray(S_T, dtype=float)
    return np.maximum(S_T - K, 0.0)


def put_payoff(S_T: ArrayLike, K: float) -> NDArray[np.float64]:
    """Put payoff max(K-S_T,0), works on scalars and arrays"""
    S_T = np.asarray(S_T, dtype=float)
    return np.maximum(K - S_T, 0.0)
