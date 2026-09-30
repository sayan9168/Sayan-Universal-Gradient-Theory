"""Derived physical phenomena and deep space analysis in SUG Theory.

This module provides the predictive, observable consequences of the Sayan Universal
Gradient Theory:
- Vacuum destruction radius (:func:`vacuum_destruction_radius`)
- Energy breaking threshold (:func:`energy_breaking_threshold`)
- Thermal profile inversion (:func:`thermal_profile`)
- Parameter-free energy scaling ratio (:func:`parameter_free_energy_ratio`, P2)
- Empirical calibration of :math:`K` via :mod:`scipy.optimize` (:func:`calibrate_k`)
- General root-solving for destruction distance in arbitrary thermal profiles (:func:`solve_destruction_distance`)
"""

from __future__ import annotations

from typing import Callable, Optional, Sequence, Tuple, Union

import numpy as np
import scipy.optimize as opt

from .core import ArrayLike, ReferenceScales, ScalarOrArray, validate_positive
from .operators import (
    theta_critical_energy,
    theta_critical_radius,
    theta_s,
)


def vacuum_destruction_radius(
    E_nb: ArrayLike,
    theta_crit: float,
    delta_T: ArrayLike,
    scales: ReferenceScales | None = None,
) -> ScalarOrArray:
    """Predict the vacuum destruction radius :math:`R_d`.

    In deep space vacuum there is no atmospheric attenuation, so geometric
    logarithmic decay dictates the distance beyond which a high-energy source
    can no longer sustain the field above a material's integrity threshold:

    .. math::

        R_d = r_0 \\exp\\!\\left(\\frac{K\\sqrt{e}}{\\tau\\,\\theta_c}\\right)

    Parameters
    ----------
    E_nb : ArrayLike
        Released source energy.
    theta_crit : float
        Critical threshold :math:`\\theta_c` for matter transition/disintegration.
    delta_T : ArrayLike
        Ambient thermal gradient.
    scales : ReferenceScales, optional
        Reference scales.

    Returns
    -------
    float or np.ndarray
        Destruction radius :math:`R_d`.
    """
    return theta_critical_radius(E_nb, delta_T, theta_crit, scales=scales)


def energy_breaking_threshold(
    r: ArrayLike,
    theta_crit: float,
    delta_T: ArrayLike,
    scales: ReferenceScales | None = None,
) -> ScalarOrArray:
    """Predict the source energy required to cross transition threshold at distance `r`.

    .. math::

        E_c = E_0 \\left(\\frac{\\tau\\,\\theta_c\\,\\ln(r/r_0)}{K}\\right)^2

    Parameters
    ----------
    r : ArrayLike
        Distance from source (:math:`r > r_0`).
    theta_crit : float
        Disintegration threshold :math:`\\theta_c`.
    delta_T : ArrayLike
        Thermal gradient.
    scales : ReferenceScales, optional
        Reference scales.

    Returns
    -------
    float or np.ndarray
        Required breaking energy :math:`E_c`.
    """
    return theta_critical_energy(r, delta_T, theta_crit, scales=scales)


def thermal_profile(
    E_nb: ArrayLike,
    theta_target: float,
    r: ArrayLike,
    scales: ReferenceScales | None = None,
) -> ScalarOrArray:
    """Predict the thermal gradient at distance `r` for a specified target field magnitude.

    Inverting :math:`\\theta_S = K \\sqrt{e} / (\\tau \\ln x)` for :math:`\\tau`:

    .. math::

        \\Delta T(r) = T_0 \\frac{K \\sqrt{e}}{\\theta_S\\, \\ln(r / r_0)}

    Parameters
    ----------
    E_nb : ArrayLike
        Source energy.
    theta_target : float
        Target field value (:math:`\\theta_S \\neq 0`).
    r : ArrayLike
        Distance (:math:`r > r_0`).
    scales : ReferenceScales, optional
        Reference scales.

    Returns
    -------
    float or np.ndarray
        Predicted thermal gradient :math:`\\Delta T`.
    """
    sc = scales if scales is not None else ReferenceScales()
    if theta_target == 0:
        raise ValueError("theta_target must be non-zero.")
    validate_positive(E_nb, r, names=["E_nb", "r"])

    r_arr = np.asarray(r, dtype=float)
    if np.any(r_arr <= sc.r0):
        raise ValueError(f"r must be strictly greater than reference scale r0={sc.r0}.")

    e = np.asarray(E_nb, dtype=float) / sc.E0
    x = r_arr / sc.r0
    tau = sc.K * np.sqrt(e) / (theta_target * np.log(x))
    dT = sc.T0 * tau
    return float(dT) if np.ndim(dT) == 0 else dT


def parameter_free_energy_ratio(
    r1: ArrayLike,
    r2: ArrayLike,
    r0: float = 1.0,
) -> ScalarOrArray:
    """Compute the parameter-free energy ratio for extending range from `r1` to `r2` (P2).

    Prediction P2 states that the energy multiplier required to extend a given
    destruction threshold from distance :math:`r_1` to :math:`r_2` at fixed thermal gradient
    is strictly independent of :math:`K` and :math:`\\theta_c`:

    .. math::

        \\frac{E_2}{E_1} = \\left( \\frac{\\ln(r_2 / r_0)}{\\ln(r_1 / r_0)} \\right)^2

    Parameters
    ----------
    r1 : ArrayLike
        Initial distance (:math:`r_1 > r_0`).
    r2 : ArrayLike
        Target distance (:math:`r_2 > r_0`).
    r0 : float, default 1.0
        Reference distance scale.

    Returns
    -------
    float or np.ndarray
        Required energy ratio :math:`E_2 / E_1`.
    """
    if r0 <= 0:
        raise ValueError("r0 must be strictly positive.")
    validate_positive(r1, r2, names=["r1", "r2"])

    r1_arr = np.asarray(r1, dtype=float)
    r2_arr = np.asarray(r2, dtype=float)

    if np.any(r1_arr <= r0) or np.any(r2_arr <= r0):
        raise ValueError(f"Distances must be strictly greater than reference r0={r0}.")

    ratio = (np.log(r2_arr / r0) / np.log(r1_arr / r0)) ** 2
    return float(ratio) if np.ndim(ratio) == 0 else ratio


def calibrate_k(
    energies: Sequence[float] | np.ndarray,
    delta_Ts: Sequence[float] | np.ndarray,
    radii: Sequence[float] | np.ndarray,
    observed_thetas: Sequence[float] | np.ndarray,
    scales: ReferenceScales | None = None,
) -> Tuple[float, float]:
    """Fit calibration parameter :math:`K` from experimental or observational event data.

    Uses non-linear least squares (:func:`scipy.optimize.curve_fit`) to fit :math:`K`
    across multiple empirical data points :math:`(E_i, \\Delta T_i, r_i, \\theta_{S,i})`.

    Parameters
    ----------
    energies : Sequence of float
        Observed source released energies.
    delta_Ts : Sequence of float
        Observed thermal gradients.
    radii : Sequence of float
        Observed distances from sources (:math:`r > r_0`).
    observed_thetas : Sequence of float
        Observed field values or critical threshold values.
    scales : ReferenceScales, optional
        Reference scales :math:`(E_0, T_0, r_0)`.

    Returns
    -------
    k_fit : float
        Optimal calibration constant :math:`K`.
    k_stderr : float
        Estimated standard error of :math:`K`.
    """
    sc = scales if scales is not None else ReferenceScales()

    e = np.asarray(energies, dtype=float) / sc.E0
    tau = np.asarray(delta_Ts, dtype=float) / sc.T0
    x = np.asarray(radii, dtype=float) / sc.r0
    y = np.asarray(observed_thetas, dtype=float)

    if np.any(x <= 1.0):
        raise ValueError(f"All radii must be strictly greater than reference r0={sc.r0}.")

    # Model: theta = K * (sqrt(e) / (tau * ln(x)))
    predictors = np.sqrt(e) / (tau * np.log(x))

    def model_fn(p, k_param):
        return k_param * p

    popt, pcov = opt.curve_fit(model_fn, predictors, y, p0=[1.0], bounds=(0, np.inf))
    k_fit = float(popt[0])
    k_stderr = float(np.sqrt(pcov[0, 0])) if pcov.size > 0 else 0.0
    return k_fit, k_stderr


def solve_destruction_distance(
    E_nb: float,
    theta_crit: float,
    thermal_profile_fn: Callable[[float], float],
    r_bracket: tuple[float, float] = (1.05, 1000.0),
    scales: ReferenceScales | None = None,
) -> float:
    """Find destruction distance in non-uniform or spatially varying thermal environments.

    Uses Brent's root-finding method (:func:`scipy.optimize.root_scalar`) to solve:

    .. math::

        \\theta_S(E_{nb}, \\Delta T(r), r) - \\theta_c = 0

    for arbitrary user-provided temperature functions :math:`\\Delta T(r)`.

    Parameters
    ----------
    E_nb : float
        Source energy.
    theta_crit : float
        Material critical threshold.
    thermal_profile_fn : Callable[[float], float]
        Function mapping radial distance `r` to local thermal gradient :math:`\\Delta T(r)`.
    r_bracket : tuple of (float, float), default (1.05, 1000.0)
        Radial search interval `(r_min, r_max)` with :math:`r_{min} > r_0`.
    scales : ReferenceScales, optional
        Reference scales.

    Returns
    -------
    float
        Radial distance where the field equals `theta_crit`.
    """
    sc = scales if scales is not None else ReferenceScales()
    r_min, r_max = r_bracket

    if r_min <= sc.r0:
        raise ValueError(f"Lower bracket r_min must be strictly greater than reference r0={sc.r0}.")

    def objective(r: float) -> float:
        dT = thermal_profile_fn(r)
        val = theta_s(E_nb, dT, r, scales=sc)
        return float(val) - theta_crit

    f_min = objective(r_min)
    f_max = objective(r_max)

    # Automatically expand r_max if signs match and objective is decreasing
    if f_min * f_max > 0:
        for factor in (10.0, 100.0, 1000.0):
            r_test = r_max * factor
            f_test = objective(r_test)
            if f_min * f_test <= 0:
                r_max = r_test
                break
        else:
            raise ValueError(
                f"Root is not bracketed in [{r_min}, {r_max}]: f(r_min)={f_min:.4e}, f(r_max)={f_max:.4e}. "
                "Adjust r_bracket or check thermal profile function."
            )

    sol = opt.root_scalar(objective, bracket=[r_min, r_max], method="brentq")
    if not sol.converged:
        raise RuntimeError(f"Root solver did not converge: {sol.flag}")
    return float(sol.root)
