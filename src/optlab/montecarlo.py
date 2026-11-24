"""Monte Carlo pricing of European options."""

import numpy as np

from optlab.gbm import simulate_terminal
from optlab.payoffs import call_payoff, put_payoff


def mc_price(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    n_paths: int,
    rng: np.random.Generator,
    option: str = "call",
) -> tuple[float, float]:
    S_T=simulate_terminal(S0,r,sigma,T,n_paths, rng)
    if option == "call":
        payoff = call_payoff(S_T, K)
    elif option == "put":
        payoff = put_payoff(S_T, K)
    else :
        raise ValueError("call or put ?")
    X= np.exp(-r*T) * payoff
    price = np.mean(X)
    se = X.std(ddof=1) / np.sqrt(n_paths)
    return((float(price), float(se)))
