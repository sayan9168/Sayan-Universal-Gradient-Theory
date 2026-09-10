"""Unit tests for the core SUG operators."""

from __future__ import annotations

import math

import numpy as np
import pytest

from sug_theory import (
    ReferenceScales,
    dimensionless,
    sug_line_constant,
    sug_scalar,
    theta_s,
    theta_critical_energy,
    theta_critical_radius,
)

SC = ReferenceScales(E0=1.0, T0=1.0, r0=1.0, K=1.0)


def test_sug_scalar_matches_formula():
    # Reproduce the exact original hand formula.
    expected = math.sqrt(50.0) / (273.0 * math.log10(1000.0))
    assert sug_scalar(50.0, 273.0, 1000.0) == pytest.approx(expected)


def test_theta_s_dimensional_invariance():
    """theta_s depends only on dimensionless ratios -> scale-invariant."""
    v1 = float(theta_s(50, 273, 1000, scales=SC))
    big = ReferenceScales(E0=10.0, T0=10.0, r0=10.0, K=1.0)
    v2 = float(theta_s(500, 2730, 10000, scales=big))
    assert v1 == pytest.approx(v2, rel=1e-9)


def test_theta_s_inverse_relations():
    """Field equals the critical threshold exactly at the critical radius."""
    r_c = theta_critical_radius(50.0, 273.0, 1.0, scales=SC)
    val = float(theta_s(50.0, 273.0, r_c, scales=SC))
    assert val == pytest.approx(1.0, rel=1e-9)


def test_breaking_energy_round_trip():
    e_b = theta_critical_energy(100.0, 273.0, 2.0, scales=SC)
    val = float(theta_s(e_b, 273.0, 100.0, scales=SC))
    assert val == pytest.approx(2.0, rel=1e-9)


def test_theta_s_diverges_at_reference_radius():
    val = theta_s(50.0, 273.0, 1.0, scales=SC)
    assert math.isnan(float(val))


def test_line_constant_positive_and_increasing():
    a = sug_line_constant(50.0, 273.0, 2.0, 10.0, scales=SC)
    b = sug_line_constant(50.0, 273.0, 2.0, 100.0, scales=SC)
    assert a > 0 and b > a


def test_dimensionless_ratios():
    d = dimensionless(50.0, 273.0, 1000.0, scales=SC)
    assert d == pytest.approx({"e": 50.0, "tau": 273.0, "x": 1000.0})


def test_vectorized_field():
    r = np.array([2.0, 5.0, 10.0])
    out = theta_s(50.0, 273.0, r, scales=SC)
    assert out.shape == (3,)
    assert np.all(np.isfinite(out))


@pytest.mark.parametrize("fn,args", [
    (theta_s, (0.0, 273.0, 10.0)),      # zero energy
    (theta_s, (50.0, 0.0, 10.0)),       # zero temperature
    (theta_s, (50.0, 273.0, 0.0)),      # zero distance
    (theta_critical_radius, (50.0, 273.0, 0.0)),  # zero threshold
])
def test_invalid_inputs_raise(fn, args):
    with pytest.raises(ValueError):
        fn(*args, scales=SC) if "scales" in fn.__code__.co_varnames else fn(*args)
