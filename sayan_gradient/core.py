"""Core definitions, reference scales, and non-dimensionalization for the SUG framework.

The Sayan Universal Gradient (SUG) framework couples released energy potential,
thermal gradients, and distance through dimensionless ratios against physically
meaningful reference scales:

.. math::

    e = \\frac{E_{nb}}{E_0}, \\qquad
    \\tau = \\frac{\\Delta T}{T_0}, \\qquad
    x = \\frac{r}{r_0}

where :math:`E_0, T_0, r_0` act as characteristic units of the theory for a
given regime (laboratory, nuclear blast, deep space, stellar), and :math:`K`
is the sole dimensionless calibration parameter.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence, Union

import numpy as np

# Type aliases
ArrayLike = Union[float, int, Sequence[float], np.ndarray]
ScalarOrArray = Union[float, np.ndarray]


class DimensionlessState(dict):
    """Container for dimensionless SUG parameters (e, tau, x).

    Inherits from :class:`dict` for full mapping compatibility (e.g., ``pytest.approx``,
    dictionary unpacking, ``state['e']``) while also providing attribute access
    (``state.e``, ``state.tau``, ``state.x``).

    Attributes
    ----------
    e : float or np.ndarray
        Dimensionless energy ratio :math:`e = E_{nb} / E_0`.
    tau : float or np.ndarray
        Dimensionless thermal gradient ratio :math:`\\tau = \\Delta T / T_0`.
    x : float or np.ndarray
        Dimensionless distance ratio :math:`x = r / r_0`.
    """

    def __init__(self, e: ScalarOrArray, tau: ScalarOrArray, x: ScalarOrArray) -> None:
        super().__init__(e=e, tau=tau, x=x)

    @property
    def e(self) -> ScalarOrArray:
        """Dimensionless energy ratio :math:`e = E_{nb} / E_0`."""
        return self["e"]

    @property
    def tau(self) -> ScalarOrArray:
        """Dimensionless thermal gradient ratio :math:`\\tau = \\Delta T / T_0`."""
        return self["tau"]

    @property
    def x(self) -> ScalarOrArray:
        """Dimensionless distance ratio :math:`x = r / r_0`."""
        return self["x"]

    def to_dict(self) -> dict[str, ScalarOrArray]:
        """Convert state to a standard Python dictionary."""
        return dict(self)


@dataclass(frozen=True)
class ReferenceScales:
    """Dimensionful reference quantities that make physical inputs dimensionless.

    Parameters
    ----------
    E0 : float
        Reference energy scale (same physical units as :math:`E_{nb}`, e.g., Joules or megatons).
        Must be strictly positive.
    T0 : float
        Reference thermal-gradient scale (same physical units as :math:`\\Delta T`, e.g., Kelvin).
        Must be strictly positive.
    r0 : float
        Reference distance scale (same physical units as :math:`r`, e.g., meters or astronomical units).
        Must be strictly positive.
    K : float
        Dimensionless calibration constant (default 1.0 until empirical fit).
        Must be non-negative.
    """

    E0: float = 1.0
    T0: float = 1.0
    r0: float = 1.0
    K: float = 1.0

    def __post_init__(self) -> None:
        if self.E0 <= 0:
            raise ValueError(f"Reference energy scale E0 must be strictly positive, got {self.E0}.")
        if self.T0 <= 0:
            raise ValueError(f"Reference temperature scale T0 must be strictly positive, got {self.T0}.")
        if self.r0 <= 0:
            raise ValueError(f"Reference distance scale r0 must be strictly positive, got {self.r0}.")
        if self.K < 0:
            raise ValueError(f"Calibration constant K must be non-negative, got {self.K}.")

    def dimensionless_energy(self, E_nb: ArrayLike) -> ScalarOrArray:
        """Compute dimensionless energy ratio :math:`e = E_{nb} / E_0`."""
        arr = np.asarray(E_nb, dtype=float)
        val = arr / self.E0
        return float(val) if arr.ndim == 0 else val

    def dimensionless_temperature(self, delta_T: ArrayLike) -> ScalarOrArray:
        """Compute dimensionless thermal gradient ratio :math:`\\tau = \\Delta T / T_0`."""
        arr = np.asarray(delta_T, dtype=float)
        val = arr / self.T0
        return float(val) if arr.ndim == 0 else val

    def dimensionless_distance(self, r: ArrayLike) -> ScalarOrArray:
        """Compute dimensionless distance ratio :math:`x = r / r_0`."""
        arr = np.asarray(r, dtype=float)
        val = arr / self.r0
        return float(val) if arr.ndim == 0 else val

    def to_dimensionless(
        self,
        E_nb: ArrayLike,
        delta_T: ArrayLike,
        r: ArrayLike,
    ) -> DimensionlessState:
        """Map physical quantities to dimensionless ratios.

        Parameters
        ----------
        E_nb : ArrayLike
            Released energy potential.
        delta_T : ArrayLike
            Thermal gradient.
        r : ArrayLike
            Radial distance from source.

        Returns
        -------
        DimensionlessState
            Container containing dimensionless ratios (e, tau, x).
        """
        validate_positive(E_nb, delta_T, r, names=["E_nb", "delta_T", "r"])
        e = self.dimensionless_energy(E_nb)
        tau = self.dimensionless_temperature(delta_T)
        x = self.dimensionless_distance(r)
        return DimensionlessState(e=e, tau=tau, x=x)

    def to_physical(
        self,
        e: ArrayLike,
        tau: ArrayLike,
        x: ArrayLike,
    ) -> tuple[ScalarOrArray, ScalarOrArray, ScalarOrArray]:
        """Convert dimensionless ratios back to physical units.

        Parameters
        ----------
        e : ArrayLike
            Dimensionless energy ratio.
        tau : ArrayLike
            Dimensionless thermal gradient ratio.
        x : ArrayLike
            Dimensionless distance ratio.

        Returns
        -------
        tuple of (E_nb, delta_T, r)
            Physical quantities in reference units.
        """
        e_arr = np.asarray(e, dtype=float) * self.E0
        tau_arr = np.asarray(tau, dtype=float) * self.T0
        x_arr = np.asarray(x, dtype=float) * self.r0
        return (
            float(e_arr) if e_arr.ndim == 0 else e_arr,
            float(tau_arr) if tau_arr.ndim == 0 else tau_arr,
            float(x_arr) if x_arr.ndim == 0 else x_arr,
        )


def validate_positive(
    *arrays: ArrayLike,
    names: Sequence[str] | None = None,
) -> list[np.ndarray]:
    """Validate that all provided input arrays contain strictly positive values (> 0).

    Parameters
    ----------
    *arrays : ArrayLike
        One or more numeric scalars or array-like collections.
    names : Sequence[str], optional
        Variable names corresponding to each array for informative error messages.

    Returns
    -------
    list of np.ndarray
        Float numpy arrays for each input.

    Raises
    ------
    ValueError
        If any element in any array is non-positive (<= 0) or NaN.
    """
    validated: list[np.ndarray] = []
    for idx, arg in enumerate(arrays):
        arr = np.asarray(arg, dtype=float)
        var_name = names[idx] if names and idx < len(names) else f"Argument {idx}"
        if np.isnan(arr).any():
            raise ValueError(f"{var_name} contains NaN values.")
        if np.any(arr <= 0):
            raise ValueError(f"{var_name} must be strictly positive (> 0).")
        validated.append(arr)
    return validated


def dimensionless(
    E_nb: ArrayLike,
    delta_T: ArrayLike,
    r: ArrayLike,
    scales: ReferenceScales | None = None,
) -> DimensionlessState:
    """Map physical inputs to their dimensionless SUG ratios.

    Parameters
    ----------
    E_nb : ArrayLike
        Released energy potential.
    delta_T : ArrayLike
        Thermal gradient.
    r : ArrayLike
        Distance from source.
    scales : ReferenceScales, optional
        Reference scales. If None, default unit scales (E0=1, T0=1, r0=1, K=1) are used.

    Returns
    -------
    DimensionlessState
        State holding ``{'e': e, 'tau': tau, 'x': x}``.
    """
    sc = scales if scales is not None else ReferenceScales()
    return sc.to_dimensionless(E_nb, delta_T, r)


# Standard physical reference presets
NUCLEAR_BLAST = ReferenceScales(E0=1.0, T0=1.0, r0=1.0, K=1.0)
STELLAR = ReferenceScales(E0=1.0e26, T0=1.0e4, r0=1.0e11, K=1.0)
DEEP_SPACE = ReferenceScales(E0=1.0e20, T0=2.7255, r0=1.0e9, K=1.0)
LABORATORY = ReferenceScales(E0=1.0e6, T0=100.0, r0=1.0, K=1.0)
