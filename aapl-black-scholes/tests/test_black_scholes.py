import sys
import numpy as np
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from src.black_scholes import call_price, put_price


def test_call_price():
    price = call_price(
        S=100,
        K=100,
        T=1,
        r=0.05,
        sigma=0.2,
    )

    assert abs(price - 10.4506) < 0.001


def test_put_price():
    price = put_price(
        S=100,
        K=100,
        T=1,
        r=0.05,
        sigma=0.2,
    )

    assert abs(price - 5.5735) < 0.001


def test_put_call_parity():
    S = 100
    K = 100
    T = 1
    r = 0.05
    sigma = 0.2

    call = call_price(S, K, T, r, sigma)
    put = put_price(S, K, T, r, sigma)

    expected_difference = S - K * np.exp(-r * T)

    assert abs((call - put) - expected_difference) < 0.001