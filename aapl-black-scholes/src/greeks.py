import numpy as np
from scipy.stats import norm

from black_scholes import _d1, _d2


def delta_call(S, K, T, r, sigma):
    """Calculate Delta for a European call option."""
    d1 = _d1(S, K, T, r, sigma)
    return norm.cdf(d1)


def delta_put(S, K, T, r, sigma):
    """Calculate Delta for a European put option."""
    d1 = _d1(S, K, T, r, sigma)
    return norm.cdf(d1) - 1


def gamma(S, K, T, r, sigma):
    """Calculate Gamma."""
    d1 = _d1(S, K, T, r, sigma)

    return (
        norm.pdf(d1)
        / (S * sigma * np.sqrt(T))
    )


def vega(S, K, T, r, sigma):
    """Calculate Vega."""
    d1 = _d1(S, K, T, r, sigma)

    return S * norm.pdf(d1) * np.sqrt(T)


def theta_call(S, K, T, r, sigma):
    """Calculate Theta for a European call option."""
    d1 = _d1(S, K, T, r, sigma)
    d2 = _d2(S, K, T, r, sigma)

    return (
        -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
        - r * K * np.exp(-r * T) * norm.cdf(d2)
    )


def rho_call(S, K, T, r, sigma):
    """Calculate Rho for a European call option."""
    d2 = _d2(S, K, T, r, sigma)

    return K * T * np.exp(-r * T) * norm.cdf(d2)