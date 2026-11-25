"""Black-Scholes closed-form prices for European options."""

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.stats import norm


def bs_price(
    S0: ArrayLike,
    K: float,
    r: float,
    sigma: float,
    T: float,
    option: str = "call",
) -> NDArray[np.float64]:
    """ Return the Black-Scholes price of a call/put """
    S0 = np.asarray(S0, dtype=float)
    d1 = ( np.log(S0/K) + (r + sigma**2 /2) * T ) / ( sigma * np.sqrt(T) )
    d2 = d1 - sigma * np.sqrt(T)
    if option == "call":
        return( S0 * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2))
    elif option == "put":
        return( K * np.exp(-r*T) * norm.cdf(-d2) - S0 * norm.cdf(-d1))
    else:
        raise ValueError("call or put?") 