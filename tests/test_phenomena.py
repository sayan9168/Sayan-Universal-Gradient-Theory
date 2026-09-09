"""Tests for derived SUG phenomena."""

from __future__ import annotations

import pytest

from sug_theory import ReferenceScales, phenomena

SC = ReferenceScales(E0=1.0, T0=1.0, r0=1.0, K=1.0)


def test_vacuum_destruction_radius_matches_core():
    rd = phenomena.vacuum_destruction_radius(50.0, 1.0, 273.0, scales=SC)
    rd_core = phenomena.theta_critical_radius(50.0, 273.0, 1.0, scales=SC)
    assert rd == pytest.approx(rd_core)


def test_energy_breaking_matches_core():
    eb = phenomena.energy_breaking_threshold(100.0, 2.0, 273.0, scales=SC)
    from sug_theory import theta_critical_energy

    assert eb == pytest.approx(theta_critical_energy(100.0, 273.0, 2.0, scales=SC))


def test_thermal_profile_inverse():
    """tau predicted at the target field must reproduce that field."""
    tau = phenomena.thermal_profile(50.0, theta_target=3.0, r=10.0, scales=SC)
    from sug_theory import theta_s

    back = float(theta_s(50.0, tau, 10.0, scales=SC))
    assert back == pytest.approx(3.0, rel=1e-6)


def test_monotonic_destruction_radius():
    r1 = phenomena.vacuum_destruction_radius(1.0, 1.0, 273.0, scales=SC)
    r2 = phenomena.vacuum_destruction_radius(100.0, 1.0, 273.0, scales=SC)
    assert r2 > r1
