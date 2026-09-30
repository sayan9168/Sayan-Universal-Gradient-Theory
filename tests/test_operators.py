"""Unit tests for the core SUG operators."""

from __future__ import annotations

import math

import numpy as np
import pytest

from sayan_gradient import (
    ReferenceScales,
    Source2D,
    ThetaSOperator,
    dimensionless,
    legacy_theta_s,
    logarithmic_integral,
    spatial_field_2d,
    sug_line_constant,
    sug_scalar,
    theta_critical_energy,
    theta_critical_radius,
    theta_s,
    theta_s_gradient,
    theta_s_line_integral,
)

SC = ReferenceScales(E0=1.0, T0=1.0, r0=1.0, K=1.0)


def test_sug_scalar_matches_formula():
    expected = math.sqrt(50.0) / (273.0 * math.log10(1000.0))
    assert sug_scalar(50.0, 273.0, 1000.0) == pytest.approx(expected)
    assert legacy_theta_s(50.0, 273.0, 1000.0) == pytest.approx(expected)


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


def test_line_integral_exact_vs_quadrature():
    """Compare exact SciPy expi against numerical quadrature quad."""
    val_exact = theta_s_line_integral(100.0, 300.0, 2.0, 20.0, scales=SC, method="exact")
    val_quad = theta_s_line_integral(100.0, 300.0, 2.0, 20.0, scales=SC, method="quad")
    assert val_exact == pytest.approx(val_quad, rel=1e-5)


def test_logarithmic_integral_computation():
    xs = np.array([2.0, 5.0, 10.0])
    li_vals = logarithmic_integral(xs)
    assert len(li_vals) == 3
    assert np.all(li_vals > 0)
    with pytest.raises(ValueError):
        logarithmic_integral(0.5)


def test_theta_s_gradient():
    """Test spatial radial derivative matches numerical finite difference."""
    E = 50.0
    dT = 273.0
    r = 10.0
    analytic_grad = theta_s_gradient(E, dT, r, scales=SC)

    dr = 1e-6
    v_plus = float(theta_s(E, dT, r + dr, scales=SC))
    v_minus = float(theta_s(E, dT, r - dr, scales=SC))
    num_grad = (v_plus - v_minus) / (2 * dr)

    assert analytic_grad == pytest.approx(num_grad, rel=1e-5)
    assert analytic_grad < 0  # Field decays monotonically


def test_dimensionless_ratios():
    d = dimensionless(50.0, 273.0, 1000.0, scales=SC)
    assert d == pytest.approx({"e": 50.0, "tau": 273.0, "x": 1000.0})


def test_vectorized_field():
    r = np.array([2.0, 5.0, 10.0])
    out = theta_s(50.0, 273.0, r, scales=SC)
    assert out.shape == (3,)
    assert np.all(np.isfinite(out))


def test_thetas_operator_class():
    op = ThetaSOperator(SC)
    val = op(50.0, 273.0, 10.0)
    assert float(val) == pytest.approx(float(theta_s(50.0, 273.0, 10.0, scales=SC)))

    rc = op.critical_radius(50.0, 273.0, 1.0)
    assert rc == pytest.approx(theta_critical_radius(50.0, 273.0, 1.0, scales=SC))

    ec = op.critical_energy(100.0, 273.0, 1.0)
    assert ec == pytest.approx(theta_critical_energy(100.0, 273.0, 1.0, scales=SC))

    grad = op.gradient(50.0, 273.0, 10.0)
    assert grad == pytest.approx(theta_s_gradient(50.0, 273.0, 10.0, scales=SC))


def test_spatial_field_2d_superposition():
    sources = [
        Source2D(x=-5.0, y=0.0, energy=100.0),
        Source2D(x=5.0, y=0.0, energy=100.0),
    ]
    grid_x, grid_y = np.meshgrid(np.linspace(-10, 10, 50), np.linspace(-10, 10, 50))
    f_lin = spatial_field_2d(sources, grid_x, grid_y, delta_T=1.0, scales=SC, superposition="linear")
    f_rss = spatial_field_2d(sources, grid_x, grid_y, delta_T=1.0, scales=SC, superposition="root_sum_squares")

    assert f_lin.shape == (50, 50)
    assert f_rss.shape == (50, 50)
    # Field at midpoint (0, 0) should be symmetric and positive
    mid_idx = 25
    assert f_lin[mid_idx, mid_idx] > 0
    assert f_lin[mid_idx, mid_idx] >= f_rss[mid_idx, mid_idx]


@pytest.mark.parametrize(
    "fn,args",
    [
        (theta_s, (0.0, 273.0, 10.0)),
        (theta_s, (50.0, 0.0, 10.0)),
        (theta_s, (50.0, 273.0, 0.0)),
        (theta_critical_radius, (50.0, 273.0, 0.0)),
    ],
)
def test_invalid_inputs_raise(fn, args):
    with pytest.raises(ValueError):
        fn(*args, scales=SC) if "scales" in fn.__code__.co_varnames else fn(*args)
