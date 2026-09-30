"""Sayan Universal Gradient (SUG) Theory - Compatibility Module.

This module re-exports functions from the primary `sayan_gradient` package
to maintain backwards compatibility with existing scripts.
"""

from sayan_gradient import (
    NUCLEAR_BLAST,
    STELLAR,
    ReferenceScales,
    dimensionless,
    sug_line_constant,
    sug_scalar,
    theta_critical_energy,
    theta_critical_radius,
    theta_s,
)
from sayan_gradient import core as nondim
from sayan_gradient import operators, phenomena
from . import plots

__all__ = [
    "operators",
    "nondim",
    "phenomena",
    "plots",
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

__version__ = "2.1.0"
__author__ = "Sayan M."
