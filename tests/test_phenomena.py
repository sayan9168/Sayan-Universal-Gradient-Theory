"""Tests for derived SUG phenomena."""

from __future__ import annotations

import numpy as np
import pytest

from sayan_gradient import ReferenceScales, phenomena

SC = ReferenceScales(E0=1.0, T0=1.0, r0=1.0, K=1.0)


def test_vacuum_destruction_radius_matches_core():
    rd = phenomena.vacuum_destruction_radius(50.0, 1.0, 273.0, scales=SC)
    from sayan_gradient import theta_critical_radius

    rd_core = theta_critical_radius(50.0, 273.0, 1.0, scales=SC)
    assert rd == pytest.approx(rd_core)


def test_energy_breaking_matches_core():
    eb = phenomena.energy_breaking_threshold(100.0, 2.0, 273.0, scales=SC)
    from sayan_gradient import theta_critical_energy

    assert eb == pytest.approx(theta_critical_energy(100.0, 273.0, 2.0, scales=SC))


def test_thermal_profile_inverse():
    """tau predicted at the target field must reproduce that field."""
    tau = phenomena.thermal_profile(50.0, theta_target=3.0, r=10.0, scales=SC)
    from sayan_gradient import theta_s

    back = float(theta_s(50.0, tau, 10.0, scales=SC))
    assert back == pytest.approx(3.0, rel=1e-6)


def test_monotonic_destruction_radius():
    r1 = phenomena.vacuum_destruction_radius(1.0, 1.0, 273.0, scales=SC)
    r2 = phenomena.vacuum_destruction_radius(100.0, 1.0, 273.0, scales=SC)
    assert r2 > r1


def test_parameter_free_energy_ratio_p2():
    """P2: E2/E1 = (ln(x2)/ln(x1))^2 independent of K and theta_c."""
    ratio = phenomena.parameter_free_energy_ratio(10.0, 100.0, r0=1.0)
    expected = (np.log(100.0) / np.log(10.0)) ** 2  # 2^2 = 4.0
    assert ratio == pytest.approx(expected)

    # Verify that theta_critical_energy gives the exact same ratio
    e1 = phenomena.energy_breaking_threshold(10.0, theta_crit=1.5, delta_T=50.0, scales=SC)
    e2 = phenomena.energy_breaking_threshold(100.0, theta_crit=1.5, delta_T=50.0, scales=SC)
    assert (e2 / e1) == pytest.approx(ratio)


def test_calibrate_k_with_scipy():
    """Test fitting calibration parameter K from synthetic data."""
    true_k = 1.85
    test_scales = ReferenceScales(E0=10.0, T0=5.0, r0=2.0, K=true_k)

    energies = [20.0, 50.0, 100.0, 200.0]
    delta_ts = [10.0, 15.0, 20.0, 25.0]
    radii = [10.0, 25.0, 50.0, 100.0]

    from sayan_gradient import theta_s

    observed_thetas = [
        float(theta_s(e, dt, r, scales=test_scales))
        for e, dt, r in zip(energies, delta_ts, radii)
    ]

    fit_k, stderr = phenomena.calibrate_k(
        energies, delta_ts, radii, observed_thetas, scales=ReferenceScales(E0=10.0, T0=5.0, r0=2.0, K=1.0)
    )
    assert fit_k == pytest.approx(true_k, rel=1e-5)
    assert stderr >= 0.0


def test_solve_destruction_distance_root_finding():
    """Test solving destruction distance in a spatially varying thermal gradient."""
    # delta_T(r) = 200.0 / sqrt(r)
    def thermal_fn(r: float) -> float:
        return 200.0 / np.sqrt(r)

    E_nb = 500.0
    theta_crit = 0.5
    r_sol = phenomena.solve_destruction_distance(
        E_nb=E_nb,
        theta_crit=theta_crit,
        thermal_profile_fn=thermal_fn,
        r_bracket=(2.0, 5000.0),
        scales=SC,
    )

    from sayan_gradient import theta_s

    val_at_sol = float(theta_s(E_nb, thermal_fn(r_sol), r_sol, scales=SC))
    assert val_at_sol == pytest.approx(theta_crit, rel=1e-5)
