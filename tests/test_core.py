"""Unit tests for sayan_gradient.core module."""

from __future__ import annotations

import numpy as np
import pytest

from sayan_gradient.core import (
    DEEP_SPACE,
    LABORATORY,
    NUCLEAR_BLAST,
    STELLAR,
    DimensionlessState,
    ReferenceScales,
    dimensionless,
    validate_positive,
)


def test_reference_scales_defaults():
    scales = ReferenceScales()
    assert scales.E0 == 1.0
    assert scales.T0 == 1.0
    assert scales.r0 == 1.0
    assert scales.K == 1.0


@pytest.mark.parametrize(
    "E0,T0,r0,K",
    [
        (0.0, 1.0, 1.0, 1.0),
        (-1.0, 1.0, 1.0, 1.0),
        (1.0, 0.0, 1.0, 1.0),
        (1.0, -2.0, 1.0, 1.0),
        (1.0, 1.0, 0.0, 1.0),
        (1.0, 1.0, -0.5, 1.0),
        (1.0, 1.0, 1.0, -0.1),
    ],
)
def test_reference_scales_invalid(E0, T0, r0, K):
    with pytest.raises(ValueError):
        ReferenceScales(E0=E0, T0=T0, r0=r0, K=K)


def test_reference_scales_presets():
    assert NUCLEAR_BLAST.E0 == 1.0
    assert STELLAR.E0 == 1.0e26
    assert DEEP_SPACE.T0 == pytest.approx(2.7255)
    assert LABORATORY.E0 == 1.0e6


def test_dimensionless_state_mapping_and_attributes():
    state = DimensionlessState(e=10.0, tau=2.0, x=5.0)
    assert state.e == 10.0
    assert state.tau == 2.0
    assert state.x == 5.0
    assert state["e"] == 10.0
    assert state["tau"] == 2.0
    assert state["x"] == 5.0
    assert len(state) == 3
    assert set(state.keys()) == {"e", "tau", "x"}
    d = state.to_dict()
    assert d == {"e": 10.0, "tau": 2.0, "x": 5.0}


def test_to_dimensionless_and_back():
    scales = ReferenceScales(E0=100.0, T0=50.0, r0=20.0, K=1.5)
    state = scales.to_dimensionless(E_nb=500.0, delta_T=150.0, r=80.0)
    assert state.e == pytest.approx(5.0)
    assert state.tau == pytest.approx(3.0)
    assert state.x == pytest.approx(4.0)

    E_phys, T_phys, r_phys = scales.to_physical(state.e, state.tau, state.x)
    assert E_phys == pytest.approx(500.0)
    assert T_phys == pytest.approx(150.0)
    assert r_phys == pytest.approx(80.0)


def test_validate_positive():
    # Valid scalars and arrays
    arrs = validate_positive(1.0, [2.0, 3.0], np.array([4.0, 5.0]))
    assert len(arrs) == 3

    # Invalid cases
    with pytest.raises(ValueError, match="must be strictly positive"):
        validate_positive(0.0)
    with pytest.raises(ValueError, match="must be strictly positive"):
        validate_positive([-1.0, 2.0])
    with pytest.raises(ValueError, match="contains NaN"):
        validate_positive(np.array([1.0, np.nan]))


def test_dimensionless_convenience_function():
    state = dimensionless(50.0, 273.0, 1000.0)
    assert state == pytest.approx({"e": 50.0, "tau": 273.0, "x": 1000.0})
