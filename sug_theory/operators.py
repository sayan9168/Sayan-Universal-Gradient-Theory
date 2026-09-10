"""
Core SUG operators.

Definitions
-----------
Every quantity is evaluated on dimensionless ratios

.. math::

    e = \\frac{E_{nb}}{E_0}, \\qquad
    \\tau = \\frac{\\Delta T}{T_0}, \\qquad
    x = \\frac{r}{r_0},

so that the theory contains no hidden dimensions.  The central field is

.. math::

    \\theta_S(x) = K\\, \\frac{\\sqrt{e}}{\\tau\\, \\ln x}, \\qquad x > 1 .

The scalar magnitude reported by the legacy ``main.py`` is the special
illustrative case ``K = 1, e = E_nb, tau = delta_T, x = r`` evaluated in
base-10 logarithms:

.. math::

    \\Theta_S^{(10)} = \\frac{\\sqrt{E_{nb}}}{\\Delta T\\, \\log_{10} r}.
"""

from __future__ import annotations

from typing import Union

import numpy as np

from .constants import ReferenceScales

Number = Union[float, np.ndarray]


def _log(x: np.ndarray, base: float) -> np.ndarray:
    """Natural logarithm rescaled to an arbitrary base (vectorised)."""
    x = np.asarray(x, dtype=float)
    return np.log(x) / np.log(base)


def _validate_positive(*args, name: str) -> np.ndarray:
    """Validate strictly positive arguments and return a float array."""
    arr = np.asarray(args[0], dtype=float)
    for a in args:
        if np.any(np.asarray(a, dtype=float) <= 0):
            raise ValueError(f"{name}: all arguments must be strictly positive.")
    return arr


def theta_s(
    E_nb: Number,
    delta_T: Number,
    r: Number,
    scales: ReferenceScales | None = None,
) -> np.ndarray:
    """Local SUG field magnitude (point value).

    Parameters
    ----------
    E_nb : energy potential released by the source.
    delta_T : thermal gradient at the point of interest.
    r : distance from the source.
    scales : reference scales and calibration constant.

    Returns
    -------
    |theta_S(x)| on the (possibly vectorised) inputs.  Points at or below
    ``r0`` are undefined and returned as ``nan`` (the logarithm diverges).
    """
    sc = scales or ReferenceScales()
    E = np.asarray(E_nb, dtype=float)
    dT = np.asarray(delta_T, dtype=float)
    rr = np.asarray(r, dtype=float)
    if np.any(E <= 0) or np.any(dT <= 0) or np.any(rr <= 0):
        raise ValueError("E_nb, delta_T and r must all be strictly positive.")

    e = E / sc.E0
    tau = dT / sc.T0
    x = rr / sc.r0

    with np.errstate(divide="ignore", invalid="ignore"):
        val = sc.K * np.sqrt(e) / (tau * np.log(x))
    # The field is undefined on and inside the source core (x <= 1).
    val = np.where(np.asarray(x) <= 1.0, np.nan, val)
    return val


def sug_scalar(E_nb: float, delta_T: float, r: float) -> float:
    """Legacy base-10 scalar magnitude (identical to the original ``main.py``).

    Reproduced here so earlier results remain reproducible.  This is the
    illustrative ``K = 1`` case and carries no physical units by itself.
    """
    if E_nb <= 0 or delta_T == 0 or r <= 1:
        raise ValueError(
            "Legacy scalar requires E_nb > 0, delta_T != 0 and r > 1."
        )
    return float(np.sqrt(E_nb) / (delta_T * np.log10(r)))


# --------------------------------------------------------------------------- #
# The logarithmic-integral (contour) constant
# --------------------------------------------------------------------------- #
def _logarithmic_integral(x: np.ndarray) -> np.ndarray:
    """Euler-series logarithmic integral ``li(x)`` for ``x > 1``.

    ``li(x) = gamma + ln(ln x) + sum_k (ln x)^k / (k * k!)``
    Accurate and vectorised via a truncated, converging series.
    """
    x = np.asarray(x, dtype=float)
    if np.any(x <= 1):
        raise ValueError("li(x) is defined here only for x > 1.")
    lnx = np.log(x)
    lnlnx = np.log(lnx)
    gamma = 0.57721566490153286060651209
    out = gamma + lnlnx
    term = np.ones_like(x)
    for k in range(1, 80):  # rapidly convergent for typical x
        term = term * lnx / k  # = (ln x)^k / k!
        out = out + term / k
    return out


def sug_line_constant(
    E_nb: float,
    delta_T: float,
    r_a: float,
    r_b: float,
    scales: ReferenceScales | None = None,
) -> float:
    """Path-integrated SUG constant along a radial segment ``[r_a, r_b]``.

    .. math::

        \\Theta_S = K \\frac{\\sqrt{e}}{\\tau}\\
            \\bigl[\\operatorname{li}(x_b) - \\operatorname{li}(x_a)\\bigr]

    where :math:`\\operatorname{li}` is the logarithmic integral.  This is the
    closed-form evaluation of the contour expression in the original paper
    (the :math:`\\oint` of :math:`\\sqrt{E}/(\\Delta T \\log r)\\, dr`).
    """
    sc = scales or ReferenceScales()
    if not (r_a > sc.r0 and r_b > sc.r0):
        raise ValueError("Both radii must be larger than the reference r0.")
    e = E_nb / sc.E0
    tau = delta_T / sc.T0
    xa = r_a / sc.r0
    xb = r_b / sc.r0
    return float(sc.K * np.sqrt(e) / tau * (_logarithmic_integral(np.array(xb)) - _logarithmic_integral(np.array(xa))))


# --------------------------------------------------------------------------- #
# Inverse / threshold solutions
# --------------------------------------------------------------------------- #
def theta_critical_radius(
    E_nb: float,
    delta_T: float,
    theta_crit: float,
    scales: ReferenceScales | None = None,
) -> float:
    """Distance at which the field equals a critical magnitude.

    Inverting :math:`\\theta_S = \\theta_c` (energy ``E_nb`` fixed) gives

    .. math::

        x_c = \\exp\\!\\Bigl(\\frac{K\\sqrt{e}}{\\tau\\,\\theta_c}\\Bigr)
        \\;\\Rightarrow\\; R_c = r_0\\, x_c .
    """
    sc = scales or ReferenceScales()
    if theta_crit == 0:
        raise ValueError("theta_crit must be non-zero.")
    e = E_nb / sc.E0
    tau = delta_T / sc.T0
    x_c = np.exp(sc.K * np.sqrt(e) / (tau * theta_crit))
    return float(sc.r0 * x_c)


def theta_critical_energy(
    r: float,
    delta_T: float,
    theta_crit: float,
    scales: ReferenceScales | None = None,
) -> float:
    """Source energy required for the field to reach a critical magnitude at ``r``.

    .. math::

        e_c = \\Bigl(\\frac{\\tau\\,\\theta_c\\,\\ln x}{K}\\Bigr)^2
        \\;\\Rightarrow\\; E_c = E_0\\, e_c .
    """
    sc = scales or ReferenceScales()
    if theta_crit == 0:
        raise ValueError("theta_crit must be non-zero.")
    if not r > sc.r0:
        raise ValueError("r must be larger than reference r0.")
    tau = delta_T / sc.T0
    x = r / sc.r0
    e_c = (tau * theta_crit * np.log(x) / sc.K) ** 2
    return float(sc.E0 * e_c)
