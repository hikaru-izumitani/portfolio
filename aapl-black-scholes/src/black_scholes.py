import numpy as np
from scipy.stats import norm


def _d1(S, K, T, r, sigma):
    return (
        np.log(S / K) + (r + 0.5 * sigma**2) * T
    ) / (sigma * np.sqrt(T))


def _d2(S, K, T, r, sigma):
    return _d1(S, K, T, r, sigma) - sigma * np.sqrt(T)


def call_price(S, K, T, r, sigma):
    """
    Calculate the Black-Scholes price of a European call option.

    Parameters
    ----------
    S : float
        Current stock price.
    K : float
        Strike price.
    T : float
        Time to expiration in years.
    r : float
        Continuously compounded risk-free interest rate.
    sigma : float
        Volatility of the underlying asset.

    Returns
    -------
    float
        Theoretical call option price.
    """
    d1 = _d1(S, K, T, r, sigma)
    d2 = _d2(S, K, T, r, sigma)

    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


def put_price(S, K, T, r, sigma):
    """
    Calculate the Black-Scholes price of a European put option.
    """
    d1 = _d1(S, K, T, r, sigma)
    d2 = _d2(S, K, T, r, sigma)

    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)