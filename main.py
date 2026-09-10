"""
Sayan Universal Gradient (SUG) Theory -- command-line demonstration.

This script walks through the framework end to end:

    1. Legacy scalar magnitude (the original base-10 result).
    2. Dimensionless field |theta_S(x)|.
    3. The path-integrated (contour) constant along a radial segment.
    4. Derived predictions: vacuum destruction radius & breaking energy.

Run::

    python main.py
"""

from __future__ import annotations

import numpy as np

from sug_theory import (
    ReferenceScales,
    dimensionless,
    sug_line_constant,
    sug_scalar,
    theta_s,
    theta_critical_energy,
    theta_critical_radius,
)

SCALES = ReferenceScales(E0=1.0, T0=1.0, r0=1.0, K=1.0)


def _rule(title: str) -> None:
    print("\n" + "=" * 62)
    print(title)
    print("=" * 62)


def main() -> None:
    # --- Worked, reproducible example (kept from the original paper) --------
    distance = 1000.0   # dimensionless distance units (> 1)
    energy = 50.0       # dimensionless energy units
    temp_diff = 273.0   # dimensionless thermal gradient
    theta_crit = 1.0    # illustrative material threshold

    _rule("1.  Legacy base-10 scalar magnitude")
    print(f"   E_nb      = {energy}")
    print(f"   Delta_T   = {temp_diff}")
    print(f"   r         = {distance}")
    print(f"   Theta_S   = sqrt(E_nb) / (Delta_T * log10(r))")
    print(f"             = {sug_scalar(energy, temp_diff, distance):.6f}")

    _rule("2.  Dimensionless field magnitude")
    dim = dimensionless(energy, temp_diff, distance, scales=SCALES)
    print(f"   e   = E_nb/E0   = {dim['e']}")
    print(f"   tau = Delta_T/T0= {dim['tau']}")
    print(f"   x   = r/r0      = {dim['x']}")
    print(f"   |theta_S(x)|    = {theta_s(energy, temp_diff, distance, scales=SCALES):.6f}")

    _rule("3.  Path-integrated (contour) SUG constant over [2, 1000]")
    cst = sug_line_constant(energy, temp_diff, r_a=2.0, r_b=distance, scales=SCALES)
    print(f"   Theta_S(a->b)   = {cst:.6f}")

    _rule("4.  Derived predictions")
    r_d = theta_critical_radius(energy, temp_diff, theta_crit, scales=SCALES)
    e_b = theta_critical_energy(1.5 * distance, temp_diff, theta_crit, scales=SCALES)
    print(f"   theta_crit      = {theta_crit}")
    print(f"   vacuum destruction radius R_d       = {r_d:.3f}")
    print(f"   breaking energy at r = {1.5*distance:.0f}           = {e_b:.3f}")

    _rule("Field scan vs distance")
    for x in (2.0, 5.0, 10.0, 100.0):
        val = theta_s(energy, temp_diff, x, scales=SCALES)
        print(f"   x = {x:>6.1f}   |theta_S| = {float(val):.5f}")

    print("\nDone. Note: predictions require calibration of K and reference scales.")
    print("See paper/open_questions.md for the validation roadmap.")


if __name__ == "__main__":
    main()
