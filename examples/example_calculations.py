"""
Worked numerical examples for the SUG framework.

Each example picks reference scales for a physical regime, computes a few
operators and prints them.  Treat the outputs as *illustrative* -- they are
only meaningful once K is calibrated for the regime.
"""

from __future__ import annotations

import os
import sys

# Make `sug_theory` importable when this script is run directly from the repo
# root without installing the package.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np

from sug_theory import (
    ReferenceScales,
    theta_s,
    theta_critical_energy,
    theta_critical_radius,
    sug_line_constant,
)


def stellar_regime() -> None:
    """Illustrate the framework on a stellarly-scaled problem."""
    sc = ReferenceScales(E0=1e26, T0=1e4, r0=1e11, K=1.0)
    E_nb = 1e27      # Joules-ish scale
    delta_T = 3e4
    print("--- Stellar regime ---")
    for r in (1e12, 5e12, 1e13):
        print(f"  r = {r:.1e}: |theta_S| = {float(theta_s(E_nb, delta_T, r, scales=sc)):.4f}")
    rd = theta_critical_radius(E_nb, delta_T, theta_crit=1.0, scales=sc)
    print(f"  vacuum destruction radius ~ {rd:.2e}")


def blast_regime() -> None:
    """Compare an atmospheric vs vacuum prediction qualitatively."""
    sc = ReferenceScales(E0=1.0, T0=1.0, r0=1.0, K=1.0)
    E_nb = 50.0
    delta_T = 273.0
    print("--- Vacuum scaling example ---")
    x = np.array([2.0, 5.0, 20.0, 100.0])
    vals = theta_s(E_nb, delta_T, x, scales=sc)
    for xi, v in zip(x, vals):
        print(f"  x = {xi:>6.1f}   |theta_S| = {float(v):.4f}")


if __name__ == "__main__":
    stellar_regime()
    blast_regime()
