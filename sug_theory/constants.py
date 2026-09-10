"""
Reference scales and calibration constant for the SUG framework.

Because the raw SUG expression mixes energy, temperature and a logarithm of
distance, it is only *dimensionally honest* once all three quantities are
written as dimensionless ratios against physically meaningful reference
scales, multiplied by a calibration constant :math:`K`.

Reference scales act like "units of the theory". They must be chosen by the
modeller for a particular regime (stellar, interplanetary, nuclear-blast,
laboratory). The calibration constant :math:`K` is the *only* free numeric
parameter of the model and must be fit to data before any prediction is
trusted.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceScales:
    """Dimensionful reference quantities that make SUG inputs dimensionless.

    Attributes
    ----------
    E0 : float
        Reference energy scale (same units as ``E_nb``).
    T0 : float
        Reference thermal-gradient scale (same units as ``delta_T``).
    r0 : float
        Reference distance scale (same units as ``r``).
    K : float
        Dimensionless calibration constant (default ``1.0`` until fit).
    """

    E0: float = 1.0
    T0: float = 1.0
    r0: float = 1.0
    K: float = 1.0

    def __post_init__(self) -> None:
        if self.E0 <= 0 or self.T0 <= 0 or self.r0 <= 0:
            raise ValueError("Reference scales must all be strictly positive.")
        if self.K < 0:
            raise ValueError("Calibration constant K must be non-negative.")


# Convenience presets ---------------------------------------------------------

NUCLEAR_BLAST = ReferenceScales(E0=1.0, T0=1.0, r0=1.0, K=1.0)
STELLAR = ReferenceScales(E0=1.0e26, T0=1.0e4, r0=1.0e11, K=1.0)
