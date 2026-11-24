"""Payoff functions of European options at maturity."""

import numpy as np
from numpy.typing import ArrayLike, NDArray


def call_payoff(S_T: ArrayLike, K: float) -> NDArray[np.float64]:
    """Payoff of a European call at maturity: max(S_T - K, 0).

    Parameters
    ----------
    S_T : array_like
        Underlying price(s) at maturity. Can be a scalar or an array
        (e.g. one value per Monte Carlo path).
    K : float
        Strike price.

    Returns
    -------
    ndarray
        Payoff(s), same shape as ``S_T``.
    """
    S_T = np.asarray(S_T, dtype=float)
    return np.maximum(S_T - K, 0.0)


def put_payoff(S_T: ArrayLike, K: float) -> NDArray[np.float64]:
    """Payoff of a European put at maturity: max(K - S_T, 0).

    Parameters
    ----------
    S_T : array_like
        Underlying price(s) at maturity.
    K : float
        Strike price.

    Returns
    -------
    ndarray
        Payoff(s), same shape as ``S_T``.
    """
    S_T = np.asarray(S_T, dtype=float)
    return np.maximum(K - S_T, 0.0)
