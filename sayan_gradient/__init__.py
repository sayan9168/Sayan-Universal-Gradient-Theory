"""Sayan Universal Gradient (SUG) Theory - Python Package (`sayan-gradient`).

A mathematical framework for mapping universal thermal gradients and nuclear
energy destruction limits, featuring the :math:`\\Theta_S` (Theta-s) operator for
deep space analysis.

Published on Zenodo (DOI: 10.5281/ZENODO.22723745).

Key Modules:
- :mod:`sayan_gradient.core`: ReferenceScales, non-dimensionalization, presets.
- :mod:`sayan_gradient.operators`: The :math:`\\Theta_S` operator, line integrals, spatial gradients.
- :mod:`sayan_gradient.phenomena`: Vacuum destruction radius, breaking energy, calibration.
- :mod:`sayan_gradient.visualization`: Publication-quality plots (Matplotlib) and interactive views (Plotly).
"""

from __future__ import annotations

from . import core, operators, phenomena, visualization
from .core import (
    DEEP_SPACE,
    LABORATORY,
    NUCLEAR_BLAST,
    STELLAR,
    DimensionlessState,
    ReferenceScales,
    dimensionless,
    validate_positive,
)
from .operators import (
    Source2D,
    ThetaSOperator,
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
from .phenomena import (
    calibrate_k,
    energy_breaking_threshold,
    parameter_free_energy_ratio,
    solve_destruction_distance,
    thermal_profile,
    vacuum_destruction_radius,
)
from .visualization import (
    plot_breaking_energy,
    plot_deep_space_field_2d,
    plot_field_decay,
    plot_surface_3d,
    plot_thermal_energy_map,
    plot_vacuum_destruction_radius,
)

__version__ = "2.1.0"
__author__ = "Sayan M."
__doi__ = "10.5281/ZENODO.22723745"

__all__ = [
    # Core
    "ReferenceScales",
    "DimensionlessState",
    "dimensionless",
    "validate_positive",
    "NUCLEAR_BLAST",
    "STELLAR",
    "DEEP_SPACE",
    "LABORATORY",
    # Operators
    "ThetaSOperator",
    "Source2D",
    "theta_s",
    "legacy_theta_s",
    "sug_scalar",
    "logarithmic_integral",
    "theta_s_line_integral",
    "sug_line_constant",
    "theta_s_gradient",
    "theta_critical_radius",
    "theta_critical_energy",
    "spatial_field_2d",
    # Phenomena
    "vacuum_destruction_radius",
    "energy_breaking_threshold",
    "thermal_profile",
    "parameter_free_energy_ratio",
    "calibrate_k",
    "solve_destruction_distance",
    # Visualization
    "plot_field_decay",
    "plot_thermal_energy_map",
    "plot_vacuum_destruction_radius",
    "plot_breaking_energy",
    "plot_surface_3d",
    "plot_deep_space_field_2d",
    # Modules
    "core",
    "operators",
    "phenomena",
    "visualization",
]
