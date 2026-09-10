"""Dimensionless re-scaling of physical SUG inputs.

Working with dimensionless ratios is what keeps the theory internally
consistent and lets one compare very different regimes on one axis.
"""

from __future__ import annotations

import numpy as np

from .constants import ReferenceScales


def dimensionless(
    E_nb: float,
    delta_T: float,
    r: float,
    scales: ReferenceScales | None = None,
) -> dict[str, float]:
    """Map physical inputs onto their dimensionless SUG ratios.

    Returns ``{"e": e, "tau": tau, "x": x}``.
    """
    sc = scales or ReferenceScales()
    if not (E_nb > 0 and delta_T > 0 and r > 0):
        raise ValueError("E_nb, delta_T and r must all be strictly positive.")
    return {
        "e": E_nb / sc.E0,
        "tau": delta_T / sc.T0,
        "x": r / sc.r0,
    }
