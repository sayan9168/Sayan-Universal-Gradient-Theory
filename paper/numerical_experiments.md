# Numerical Experiments

This document shows how the code in `sug_theory/` *implements* the formal
framework, and presents the figures it produces.  These figures are
**illustrations of the model**, not measurements of nature — see
`open_questions.md`.

All figures are generated reproducibly with:

```bash
python -m sug_theory.plots --outdir figures
```

---

## Figure 1 — Field decay with distance

`fig_field_decay.png` plots the SUG field magnitude :math:`|\theta_S|` against
dimensionless distance :math:`x`, for several source energies at fixed
thermal gradient.

**Reading.**  Each curve falls slowly (logarithmically) and monotonically,
flattening as :math:`x` grows.  Higher energy shifts the whole curve upward
(square-root compression: doubling `e` from 2 to 4 does *not* double the
field).  The slow tail is the theory's "long reach" signature.

## Figure 2 — Thermal–distance energy map

`fig_thermal_energy_map.png` is a heat map of :math:`|\theta_S|` over the
:math:`(\tau, x)` plane for a single source energy, with contours overlaid.

**Reading.**  Field strength is highest at small :math:`\tau` (cold) and small
:math:`x` (near), and is suppressed diagonally toward large :math:`\tau`.
Contours trace the trade-off: to hold the same field, moving closer in
:math:`x` can compensate for a larger thermal gradient :math:`\tau`.  This is
the two-dimensional "thermal mapping" that a single scalar field provides.

## Figure 3 — Vacuum destruction radius vs energy

`fig_vacuum_destruction_radius.png` plots the predicted destruction radius
:math:`x_c` (log-scale) versus dimensionless source energy :math:`e`, for
several thresholds.

**Reading.**  Because :math:`\ln x_c = K\sqrt{e}/(\tau\theta_c)`, each curve is
a straight line on this (log-:math:`x`, linear-:math:`\sqrt{e}` style) view —
*exponential growth of radius with :math:`\sqrt{e}`*.  Lower thresholds sit
higher, i.e. reach farther.  This directly embodies prediction **P1**.

## Figure 4 — Breaking energy vs distance

`fig_breaking_energy.png` plots the energy :math:`e_b` needed to cross a
threshold at distance :math:`x` (log-scale), for several thresholds.

**Reading.**  Because :math:`e_b = [\tau\theta_c\ln x/K]^2`, the curves rise
*quadratically in the logarithm* — remarkably gentle.  Extending reach from
:math:`x=2` to :math:`x=10` requires a far smaller multiplier than any
power-law model would demand.  This embodies prediction **P2**'s cheap-range
message.

---

## Reproducing the worked example

The headline scalar example from the original repository is preserved in
`main.py` and tested in `tests/`:

```python
from sug_theory import sug_scalar
sug_scalar(E_nb=50.0, delta_T=273.0, r=1000.0)   # matches the hand formula
```

Run the full demonstration:

```bash
python main.py
```

Run the tests:

```bash
python -m pytest -q
```
