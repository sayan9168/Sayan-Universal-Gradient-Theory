"""Mathematical operators for the Sayan Universal Gradient (SUG) Theory.

This module implements the core operator :math:`\\Theta_S` (Theta-s), which couples
released energy potential, local thermal gradients, and cosmic distance:

.. math::

    \\theta_S(x) = K\\, \\frac{\\sqrt{e}}{\\tau\\, \\ln x}, \\qquad x = \\frac{r}{r_0} > 1

along with the closed-form radial contour integral using the logarithmic integral
:math:`\\operatorname{li}(x)` via :mod:`scipy.special`, spatial gradient operators,
and critical threshold inversions.
"""

from __future__ import annotations

from typing import Callable, Literal, NamedTuple, Optional, Sequence, Union

import numpy as np
import scipy.integrate as spi
import scipy.special as sp

from .core import ArrayLike, ReferenceScales, ScalarOrArray, validate_positive


class Source2D(NamedTuple):
    """Energetic point source in a 2D spatial plane.

    Attributes
    ----------
    x : float
        X coordinate of the source in physical units.
    y : float
        Y coordinate of the source in physical units.
    energy : float
        Released nuclear/bombardment energy potential :math:`E_{nb}`.
    """

    x: float
    y: float
    energy: float


def theta_s(
    E_nb: ArrayLike,
    delta_T: ArrayLike,
    r: ArrayLike,
    scales: ReferenceScales | None = None,
) -> np.ndarray:
    """Evaluate the local Sayan-Universal field magnitude :math:`|\\theta_S(x)|`.

    .. math::

        \\theta_S(x) = K\\, \\frac{\\sqrt{E_{nb}/E_0}}{(\\Delta T/T_0)\\, \\ln(r/r_0)}
                     = K\\, \\frac{\\sqrt{e}}{\\tau\\, \\ln x}

    Parameters
    ----------
    E_nb : ArrayLike
        Energy potential released by the source (:math:`E_{nb} > 0`).
    delta_T : ArrayLike
        Thermal gradient at the point of interest (:math:`\\Delta T > 0`).
    r : ArrayLike
        Radial distance from the source (:math:`r > 0`).
    scales : ReferenceScales, optional
        Reference scales :math:`(E_0, T_0, r_0)` and calibration constant :math:`K`.
        Defaults to unit scales (E0=1, T0=1, r0=1, K=1).

    Returns
    -------
    np.ndarray
        Evaluated field magnitude. Points on or inside the source core (:math:`r \\le r_0`,
        i.e., :math:`x \\le 1`) diverge and are returned as ``np.nan``.

    Raises
    ------
    ValueError
        If any element of `E_nb`, `delta_T`, or `r` is non-positive (<= 0).
    """
    sc = scales if scales is not None else ReferenceScales()
    validate_positive(E_nb, delta_T, r, names=["E_nb", "delta_T", "r"])

    e = np.asarray(E_nb, dtype=float) / sc.E0
    tau = np.asarray(delta_T, dtype=float) / sc.T0
    x = np.asarray(r, dtype=float) / sc.r0

    with np.errstate(divide="ignore", invalid="ignore"):
        val = sc.K * np.sqrt(e) / (tau * np.log(x))

    # The field is undefined on and inside the source core (x <= 1).
    val = np.where(x <= 1.0, np.nan, val)
    return val


def legacy_theta_s(E_nb: float, delta_T: float, r: float) -> float:
    """Evaluate the legacy base-10 scalar magnitude :math:`\\Theta_S^{(10)}`.

    .. math::

        \\Theta_S^{(10)} = \\frac{\\sqrt{E_{nb}}}{\\Delta T\\, \\log_{10}(r)}

    Reproduced from the original Zenodo formulation to ensure historical reproducibility.
    This corresponds to the uncalibrated case :math:`K = 1, E_0 = T_0 = r_0 = 1`
    evaluated in base-10 logarithms.

    Parameters
    ----------
    E_nb : float
        Released energy (:math:`E_{nb} > 0`).
    delta_T : float
        Thermal gradient (:math:`\\Delta T \\neq 0`).
    r : float
        Distance (:math:`r > 1`).

    Returns
    -------
    float
        Legacy scalar magnitude.
    """
    if E_nb <= 0 or delta_T == 0 or r <= 1.0:
        raise ValueError("Legacy scalar requires E_nb > 0, delta_T != 0 and r > 1.")
    return float(np.sqrt(E_nb) / (delta_T * np.log10(r)))


# Alias for backward compatibility
sug_scalar = legacy_theta_s


def logarithmic_integral(x: ArrayLike) -> np.ndarray:
    """Evaluate the logarithmic integral :math:`\\operatorname{li}(x)` for :math:`x > 1`.

    .. math::

        \\operatorname{li}(x) = \\int_0^x \\frac{dt}{\\ln t} = \\operatorname{Ei}(\\ln x)

    Computed accurately using :func:`scipy.special.expi`.

    Parameters
    ----------
    x : ArrayLike
        Dimensionless evaluation points (:math:`x > 1`).

    Returns
    -------
    np.ndarray
        Values of :math:`\\operatorname{li}(x)`.

    Raises
    ------
    ValueError
        If any element of `x` is :math:`\\le 1`.
    """
    x_arr = np.asarray(x, dtype=float)
    if np.any(x_arr <= 1.0):
        raise ValueError("li(x) is defined in this domain only for x > 1.")
    return np.asarray(sp.expi(np.log(x_arr)))


def theta_s_line_integral(
    E_nb: float,
    delta_T: float,
    r_a: float,
    r_b: float,
    scales: ReferenceScales | None = None,
    method: Literal["exact", "quad"] = "exact",
) -> float:
    """Evaluate the path-integrated SUG operator along a radial segment :math:`[r_a, r_b]`.

    .. math::

        \\Theta_S(a \\to b) = \\int_{r_a}^{r_b} \\frac{\\sqrt{e}}{\\tau\\, \\ln(r/r_0)}\\, dr
            = \\frac{K\\, r_0\\, \\sqrt{e}}{\\tau}
              \\Bigl[\\operatorname{li}(x_b) - \\operatorname{li}(x_a)\\Bigr]

    where :math:`\\operatorname{li}` is the logarithmic integral. In dimensionless
    path length units (:math:`dr' = dx = dr/r_0`), the invariant contour constant is:

    .. math::

        \\Theta_S^{(x)}(a \\to b) = \\frac{K\\sqrt{e}}{\\tau}
            \\Bigl[\\operatorname{li}(x_b) - \\operatorname{li}(x_a)\\Bigr]

    Parameters
    ----------
    E_nb : float
        Released energy potential.
    delta_T : float
        Thermal gradient.
    r_a : float
        Initial radial distance (:math:`r_a > r_0`).
    r_b : float
        Terminal radial distance (:math:`r_b > r_0`).
    scales : ReferenceScales, optional
        Reference scales and calibration constant.
    method : {"exact", "quad"}, default "exact"
        Integration method: "exact" uses closed-form :func:`scipy.special.expi`,
        while "quad" uses adaptive numerical quadrature via :func:`scipy.integrate.quad`.

    Returns
    -------
    float
        Integrated path constant.

    Raises
    ------
    ValueError
        If `r_a` or `r_b` is not strictly greater than :math:`r_0`.
    """
    sc = scales if scales is not None else ReferenceScales()
    if not (r_a > sc.r0 and r_b > sc.r0):
        raise ValueError(
            f"Both radii (r_a={r_a}, r_b={r_b}) must be strictly greater than reference r0={sc.r0}."
        )
    if E_nb <= 0 or delta_T <= 0:
        raise ValueError("E_nb and delta_T must be strictly positive.")

    e = E_nb / sc.E0
    tau = delta_T / sc.T0
    xa = r_a / sc.r0
    xb = r_b / sc.r0

    if method == "exact":
        li_b = float(sp.expi(np.log(xb)))
        li_a = float(sp.expi(np.log(xa)))
        return float(sc.K * (np.sqrt(e) / tau) * (li_b - li_a))

    if method == "quad":
        integrand = lambda x: 1.0 / np.log(x)
        val, _ = spi.quad(integrand, xa, xb)
        return float(sc.K * (np.sqrt(e) / tau) * val)

    raise ValueError(f"Unknown integration method '{method}'. Supported: 'exact', 'quad'.")


# Alias for backward compatibility
sug_line_constant = theta_s_line_integral


def theta_s_gradient(
    E_nb: ArrayLike,
    delta_T: ArrayLike,
    r: ArrayLike,
    scales: ReferenceScales | None = None,
) -> ScalarOrArray:
    """Compute the spatial radial derivative of the field :math:`\\frac{d\\theta_S}{dr}`.

    .. math::

        \\frac{d\\theta_S}{dr} = - \\frac{K \\sqrt{e}}{\\tau\\, r\\, (\\ln(r/r_0))^2}
                                = - \\frac{\\theta_S(r)}{r\\, \\ln(r/r_0)}

    Parameters
    ----------
    E_nb : ArrayLike
        Source energy.
    delta_T : ArrayLike
        Thermal gradient.
    r : ArrayLike
        Radial distance (:math:`r > r_0`).
    scales : ReferenceScales, optional
        Reference scales.

    Returns
    -------
    float or np.ndarray
        Radial spatial gradient :math:`d\\theta_S/dr`.
    """
    sc = scales if scales is not None else ReferenceScales()
    validate_positive(E_nb, delta_T, r, names=["E_nb", "delta_T", "r"])

    e = np.asarray(E_nb, dtype=float) / sc.E0
    tau = np.asarray(delta_T, dtype=float) / sc.T0
    x = np.asarray(r, dtype=float) / sc.r0

    with np.errstate(divide="ignore", invalid="ignore"):
        grad = - (sc.K * np.sqrt(e)) / (tau * sc.r0 * x * (np.log(x) ** 2))

    grad = np.where(x <= 1.0, np.nan, grad)
    return float(grad) if np.ndim(grad) == 0 else grad


def theta_critical_radius(
    E_nb: ArrayLike,
    delta_T: ArrayLike,
    theta_crit: float,
    scales: ReferenceScales | None = None,
) -> ScalarOrArray:
    """Compute the critical destruction distance :math:`R_c` where :math:`\\theta_S = \\theta_c`.

    Inverting :math:`\\theta_S(x) = \\theta_c` yields:

    .. math::

        x_c = \\exp\\!\\left(\\frac{K\\sqrt{e}}{\\tau\\,\\theta_c}\\right)
        \\implies R_c = r_0\\, x_c

    Parameters
    ----------
    E_nb : ArrayLike
        Source released energy.
    delta_T : ArrayLike
        Thermal gradient.
    theta_crit : float
        Critical field threshold for material disintegration (:math:`\\theta_c \\neq 0`).
    scales : ReferenceScales, optional
        Reference scales.

    Returns
    -------
    float or np.ndarray
        Predicted critical radius :math:`R_c`.
    """
    sc = scales if scales is not None else ReferenceScales()
    if theta_crit == 0:
        raise ValueError("theta_crit must be non-zero.")
    validate_positive(E_nb, delta_T, names=["E_nb", "delta_T"])

    e = np.asarray(E_nb, dtype=float) / sc.E0
    tau = np.asarray(delta_T, dtype=float) / sc.T0
    x_c = np.exp(sc.K * np.sqrt(e) / (tau * theta_crit))
    r_c = sc.r0 * x_c
    return float(r_c) if np.ndim(r_c) == 0 else r_c


def theta_critical_energy(
    r: ArrayLike,
    delta_T: ArrayLike,
    theta_crit: float,
    scales: ReferenceScales | None = None,
) -> ScalarOrArray:
    """Compute the breaking energy :math:`E_c` required to reach threshold :math:`\\theta_c` at `r`.

    .. math::

        e_c = \\left(\\frac{\\tau\\,\\theta_c\\,\\ln(r/r_0)}{K}\\right)^2
        \\implies E_c = E_0\\, e_c

    Parameters
    ----------
    r : ArrayLike
        Distance from source (:math:`r > r_0`).
    delta_T : ArrayLike
        Thermal gradient.
    theta_crit : float
        Critical field threshold (:math:`\\theta_c \\neq 0`).
    scales : ReferenceScales, optional
        Reference scales.

    Returns
    -------
    float or np.ndarray
        Source energy :math:`E_c` required.
    """
    sc = scales if scales is not None else ReferenceScales()
    if theta_crit == 0:
        raise ValueError("theta_crit must be non-zero.")
    validate_positive(r, delta_T, names=["r", "delta_T"])

    r_arr = np.asarray(r, dtype=float)
    if np.any(r_arr <= sc.r0):
        raise ValueError(f"r must be strictly greater than reference scale r0={sc.r0}.")

    tau = np.asarray(delta_T, dtype=float) / sc.T0
    x = r_arr / sc.r0
    e_c = (tau * theta_crit * np.log(x) / sc.K) ** 2
    E_c = sc.E0 * e_c
    return float(E_c) if np.ndim(E_c) == 0 else E_c


def spatial_field_2d(
    sources: Sequence[Source2D | tuple[float, float, float]],
    grid_x: np.ndarray,
    grid_y: np.ndarray,
    delta_T: ArrayLike = 1.0,
    scales: ReferenceScales | None = None,
    superposition: Literal["linear", "root_sum_squares"] = "linear",
) -> np.ndarray:
    """Compute the 2D spatial field distribution from one or more energetic sources.

    Parameters
    ----------
    sources : Sequence of Source2D or tuple of (x, y, energy)
        Collection of point sources in the plane.
    grid_x : np.ndarray
        2D meshgrid of X coordinates.
    grid_y : np.ndarray
        2D meshgrid of Y coordinates.
    delta_T : ArrayLike, default 1.0
        Thermal gradient at each point (scalar or 2D array matching grid shape).
    scales : ReferenceScales, optional
        Reference scales.
    superposition : {"linear", "root_sum_squares"}, default "linear"
        Method used to combine multiple source fields.

    Returns
    -------
    np.ndarray
        Combined 2D scalar field array.
    """
    sc = scales if scales is not None else ReferenceScales()
    total_field = np.zeros_like(grid_x, dtype=float)

    for src in sources:
        if isinstance(src, Source2D):
            sx, sy, se = src.x, src.y, src.energy
        else:
            sx, sy, se = src[0], src[1], src[2]

        dist = np.hypot(grid_x - sx, grid_y - sy)
        field_i = theta_s(se, delta_T, dist, scales=sc)
        # Outside core (where dist > r0), add field
        valid_mask = np.isfinite(field_i)

        if superposition == "linear":
            total_field = np.where(valid_mask, total_field + np.nan_to_num(field_i, nan=0.0), total_field)
        elif superposition == "root_sum_squares":
            total_field = np.where(valid_mask, total_field + np.nan_to_num(field_i, nan=0.0) ** 2, total_field)

    if superposition == "root_sum_squares":
        total_field = np.sqrt(total_field)

    return total_field


class ThetaSOperator:
    """Object-oriented interface for the Sayan-Universal :math:`\\Theta_S` operator.

    Encapsulates reference scales and provides methods for field evaluation,
    line integration, spatial gradient computation, and threshold inversions.

    Parameters
    ----------
    scales : ReferenceScales, optional
        Reference scales and calibration constant. Defaults to unit scales.
    """

    def __init__(self, scales: ReferenceScales | None = None) -> None:
        self.scales = scales if scales is not None else ReferenceScales()

    def __call__(self, E_nb: ArrayLike, delta_T: ArrayLike, r: ArrayLike) -> np.ndarray:
        """Evaluate the field at (E_nb, delta_T, r)."""
        return theta_s(E_nb, delta_T, r, scales=self.scales)

    def evaluate(self, E_nb: ArrayLike, delta_T: ArrayLike, r: ArrayLike) -> np.ndarray:
        """Evaluate the field at (E_nb, delta_T, r)."""
        return theta_s(E_nb, delta_T, r, scales=self.scales)

    def line_integral(
        self,
        E_nb: float,
        delta_T: float,
        r_a: float,
        r_b: float,
        method: Literal["exact", "quad"] = "exact",
    ) -> float:
        """Evaluate the radial path-integrated field between `r_a` and `r_b`."""
        return theta_s_line_integral(E_nb, delta_T, r_a, r_b, scales=self.scales, method=method)

    def gradient(self, E_nb: ArrayLike, delta_T: ArrayLike, r: ArrayLike) -> ScalarOrArray:
        """Compute the spatial radial gradient :math:`d\\theta_S/dr`."""
        return theta_s_gradient(E_nb, delta_T, r, scales=self.scales)

    def critical_radius(
        self,
        E_nb: ArrayLike,
        delta_T: ArrayLike,
        theta_crit: float,
    ) -> ScalarOrArray:
        """Compute critical destruction radius :math:`R_c`."""
        return theta_critical_radius(E_nb, delta_T, theta_crit, scales=self.scales)

    def critical_energy(
        self,
        r: ArrayLike,
        delta_T: ArrayLike,
        theta_crit: float,
    ) -> ScalarOrArray:
        """Compute breaking energy :math:`E_c`."""
        return theta_critical_energy(r, delta_T, theta_crit, scales=self.scales)

    def spatial_field_2d(
        self,
        sources: Sequence[Source2D | tuple[float, float, float]],
        grid_x: np.ndarray,
        grid_y: np.ndarray,
        delta_T: ArrayLike = 1.0,
        superposition: Literal["linear", "root_sum_squares"] = "linear",
    ) -> np.ndarray:
        """Compute 2D field map over spatial coordinates."""
        return spatial_field_2d(
            sources, grid_x, grid_y, delta_T=delta_T, scales=self.scales, superposition=superposition
        )

    def __repr__(self) -> str:
        return f"ThetaSOperator(scales={self.scales})"
