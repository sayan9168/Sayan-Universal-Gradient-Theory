"""
Derived SUG phenomena (predictive layer).

The operators in :mod:`sug_theory.operators` describe the field itself.  This
module assembles the *observable consequences* that the theory proposes and
that experiments could in principle confirm or refute:

- ``vacuum_destruction_radius`` -- the radius beyond which a high-energy
  source in vacuum can no longer keep the local field above a material's
  destruction threshold.
- ``energy_breaking_threshold`` -- the source energy at which matter at a
  given distance crosses the "information / energy transition" threshold.
- ``thermal_profile`` -- the thermal gradient the field *predicts* as a
  function of distance for fixed source energy.

All of these are presented as *testable mappings*, not as established laws.
"""

from __future__ import annotations

import numpy as np

from .constants import ReferenceScales


def vacuum_destruction_radius(
    E_nb: float,
    theta_crit: float,
    delta_T: float,
    scales: ReferenceScales | None = None,
) -> float:
    """Predict the vacuum destruction radius.

    In vacuum there is no atmospheric attenuation, so the only "switch-off"
    of destruction is the geometric fall-off encoded in ``1/ln(r/r0)``.
    Requiring :math:`\\theta_S \\ge \\theta_c` yields

    .. math::

        R_d = r_0 \\exp\\!\\Bigl(\\frac{K\\sqrt{e}}{\\tau\\,\\theta_c}\\Bigr).

    Returns
    -------
    float
        A *distance scale* (the model's prediction).  To be validated, the
        reference scales and :math:`K` must first be calibrated to one known
        event.
    """
    return theta_critical_radius(E_nb, delta_T, theta_crit, scales)


def energy_breaking_threshold(
    r: float,
    theta_crit: float,
    delta_T: float,
    scales: ReferenceScales | None = None,
) -> float:
    """Predict the energy needed to cross the transition threshold at ``r``."""
    from .operators import theta_critical_energy

    return theta_critical_energy(r, delta_T, theta_crit, scales)


def thermal_profile(
    E_nb: float,
    theta_target: float,
    r: float,
    scales: ReferenceScales | None = None,
) -> float:
    """Predicted thermal gradient at distance ``r`` for a target field value.

    .. math::

        \\tau(r) = \\frac{K\\sqrt{e}}{\\theta_S\\, \\ln x}.
    """
    from .operators import _log

    sc = scales or ReferenceScales()
    if theta_target == 0:
        raise ValueError("theta_target must be non-zero.")
    if not (E_nb > 0 and r > sc.r0):
        raise ValueError("E_nb > 0 and r > r0 required.")
    e = E_nb / sc.E0
    x = r / sc.r0
    tau = sc.K * np.sqrt(e) / (theta_target * np.log(x))
    return float(sc.T0 * tau)


# Re-export to keep the docstring's references true --------------------------- #
def theta_critical_radius(E_nb, delta_T, theta_crit, scales=None):
    """See :func:`sug_theory.operators.theta_critical_radius`."""
    from .operators import theta_critical_radius as _f

    return _f(E_nb, delta_T, theta_crit, scales)
