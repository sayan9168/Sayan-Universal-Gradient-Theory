"""
Sayan Universal Gradient (SUG) Theory
=====================================

A *proposed* theoretical framework exploring how a single scalar field --
the Sayan-Universal operator :math:`\\Theta_S` -- couples energy release,
thermal gradients and cosmic distance.

**Status disclaimer.** SUG is a speculative, original mathematical proposal.
It has **not** been peer reviewed and it has **not** been validated against
experimental data. Every derived operator is a hypothesis that is only
meaningful once its free parameters (reference scales and the calibration
constant :math:`K`) are fixed by observation. See ``paper/open_questions.md``.

Public API
----------
- ``operators.theta_s``          : local SUG field magnitude (point value).
- ``operators.sug_scalar``       : original base-10 magnitude used in ``main.py``.
- ``operators.sug_line_constant``: path-integrated (contour) SUG constant.
- ``operators.theta_critical_solve`` : solve radius / energy at a field threshold.
- ``nondim.dimensionless``       : maps physical inputs onto dimensionless ratios.
- ``phenomena.*``                : derived predictions (see module docstrings).
- ``plots``                      : figure generation helpers (import lazily;
                                  needs matplotlib).
"""

from . import operators, nondim, phenomena
from .constants import ReferenceScales, NUCLEAR_BLAST, STELLAR
from .operators import (
    sug_scalar,
    theta_s,
    sug_line_constant,
    theta_critical_radius,
    theta_critical_energy,
)
from .nondim import dimensionless

# ``plots`` is intentionally imported lazily (it requires matplotlib); use
# ``from sug_theory.plots import ...`` or ``python -m sug_theory.plots``.

__all__ = [
    "operators",
    "nondim",
    "phenomena",
    "ReferenceScales",
    "NUCLEAR_BLAST",
    "STELLAR",
    "sug_scalar",
    "theta_s",
    "sug_line_constant",
    "theta_critical_radius",
    "theta_critical_energy",
    "dimensionless",
]

__version__ = "2.0.0"
__author__ = "Sayan M."
