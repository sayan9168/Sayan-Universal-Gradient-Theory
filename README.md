# sayan-gradient: Sayan Universal Gradient Theory in Python

[![PyPI version](https://img.shields.io/badge/pypi-v2.1.0-blue.svg)](https://pypi.org/project/sayan-gradient/)
[![Python versions](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://pypi.org/project/sayan-gradient/)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2FZENODO.22723906-blue.svg)](https://doi.org/10.5281/ZENODO.22723906)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-49%20passed-brightgreen.svg)]()

> **Production-ready Python package for computational physics, mathematical modeling of universal thermal gradients, nuclear energy destruction limits, and deep space analysis featuring the $\Theta_s$ (Theta-s) operator.**

Published on Zenodo: **[DOI: 10.5281/ZENODO.22723906](https://doi.org/10.5281/ZENODO.22723906)**  
GitHub: [sayan9168/Sayan-Universal-Gradient-Theory](https://github.com/sayan9168/Sayan-Universal-Gradient-Theory)

---

## ⚠ Scientific Status Note

**SUG is an original, speculative theoretical proposal.** It has not yet undergone formal journal peer-review or direct empirical validation against observation. It is structured with mathematical rigor and reproducible scientific code so that its hypotheses can be evaluated, falsified, and tested against real-world astrophysical or high-energy data.

Before applying numerical predictions, please consult the validation roadmap in [`paper/open_questions.md`](paper/open_questions.md) and [`paper/predictions.md`](paper/predictions.md).

---

## Mathematical Formulation

The Sayan Universal Gradient (SUG) framework proposes that a single scalar field, the **Sayan-Universal Field** $\Theta_S$, simultaneously couples the **energy potential released by a source** ($E_{nb}$), the **local ambient thermal gradient** ($\Delta T$), and the **distance** ($r$) from the source.

### 1. Dimensionless Scaling and Reference Scales
To ensure dimensional consistency, physical inputs are expressed as dimensionless ratios against characteristic reference scales $(E_0, T_0, r_0)$:

$$e = \frac{E_{nb}}{E_0}, \qquad \tau = \frac{\Delta T}{T_0}, \qquad x = \frac{r}{r_0}$$

### 2. The Central $\Theta_s$ Operator (Point Field Magnitude)
The dimensionless field magnitude is governed by:

$$\theta_S(x) = K \, \frac{\sqrt{e}}{\tau \, \ln x} = K \, \frac{\sqrt{E_{nb}/E_0}}{(\Delta T/T_0) \, \ln(r/r_0)}, \qquad x > 1$$

where $K$ is the model's dimensionless calibration constant (default $1.0$ until empirical fitting). The inner boundary $x \le 1$ ($r \le r_0$) represents the **source core singularity**, inside which the continuum field representation ceases.

### 3. Radial Path-Integrated Operator (Contour Form)
The line integral along a radial path $[r_a, r_b]$ ($r_b > r_a > r_0$) evaluates in closed form using the logarithmic integral $\operatorname{li}(x) = \operatorname{Ei}(\ln x)$:

$$\Theta_S(a \to b) = \int_{r_a}^{r_b} \frac{\sqrt{e}}{\tau \ln(r/r_0)} \, dr = \frac{K \sqrt{e}}{\tau} \Bigl[ \operatorname{li}(x_b) - \operatorname{li}(x_a) \Bigr]$$

### 4. Spatial Radial Derivative (Field Gradient)
The rate of field decay with distance is:

$$\frac{d\theta_S}{dr} = - \frac{K \sqrt{e}}{\tau \, r_0 x \, (\ln x)^2} = - \frac{\theta_S(r)}{r \, \ln(r/r_0)}$$

### 5. Deep Space Vacuum Destruction Limits
Given a critical material disintegration threshold $\theta_c$ (Postulate V):
- **Vacuum Destruction Radius ($R_d$):**
  $$R_d = r_0 \exp\!\left( \frac{K \sqrt{e}}{\tau \, \theta_c} \right)$$
- **Energy Breaking Threshold ($E_c$):**
  $$E_c = E_0 \left( \frac{\tau \, \theta_c \, \ln(r/r_0)}{K} \right)^2$$
- **Parameter-Free Energy Ratio (Prediction P2):**
  $$\frac{E_2}{E_1} = \left( \frac{\ln(r_2/r_0)}{\ln(r_1/r_0)} \right)^2$$
  *Notice that this scaling ratio is strictly independent of $K$ and $\theta_c$!*

---

## Package Directory Structure

```text
Sayan-Universal-Gradient-Theory/
├── pyproject.toml              # PyPI build configuration (PEP 517 / 621)
├── setup.py                    # Legacy build support
├── requirements.txt            # Package dependencies
├── LICENSE                     # MIT License
├── README.md                   # Documentation and usage guide
├── sayan_gradient/             # Primary production package
│   ├── __init__.py             # Public API and package metadata
│   ├── core.py                 # ReferenceScales, DimensionlessState, validation, presets
│   ├── operators.py            # Θ_s operator, contour line integral, spatial gradient, 2D field
│   ├── phenomena.py            # Vacuum destruction limits, breaking energy, SciPy calibration
│   └── visualization.py        # Publication Matplotlib & interactive Plotly visualization
├── sug_theory/                 # Backwards-compatibility alias module
├── notebooks/                  # Interactive Jupyter notebook examples
│   ├── 01_thetas_operator_basics.ipynb
│   ├── 02_deep_space_destruction_limits.ipynb
│   └── 03_thermal_mapping_and_visualization.ipynb
├── tests/                      # Pytest unit and integration test suite
│   ├── test_core.py
│   ├── test_operators.py
│   ├── test_phenomena.py
│   └── test_visualization.py
├── figures/                    # Pre-generated theory plots
├── paper/                      # Formal written theory and postulates
└── main.py                     # CLI end-to-end demonstration
```

---

## Installation

### From PyPI

```bash
# Core package (NumPy and SciPy)
pip install sayan-gradient

# With visualization backends (Matplotlib and Plotly)
pip install "sayan-gradient[plots]"

# Complete development environment (including notebooks and pytest)
pip install "sayan-gradient[all]"
```

### From Source

```bash
git clone https://github.com/sayan9168/Sayan-Universal-Gradient-Theory.git
cd Sayan-Universal-Gradient-Theory
pip install -e ".[all]"
```

---

## Quickstart & Usage Examples

### 1. Basic Field Evaluation

```python
from sayan_gradient import ReferenceScales, theta_s, legacy_theta_s

# Define physical parameters
E_nb = 50.0      # Released energy potential
delta_T = 273.0  # Thermal gradient
r = 1000.0       # Radial distance

# 1. Dimensionless natural-log operator (Modern)
sc = ReferenceScales(E0=1.0, T0=1.0, r0=1.0, K=1.0)
field_val = theta_s(E_nb, delta_T, r, scales=sc)
print(f"|θ_S| = {float(field_val):.6f}")
# Output: |θ_S| = 0.003750

# 2. Legacy base-10 scalar (from original Zenodo release)
legacy_val = legacy_theta_s(E_nb, delta_T, r)
print(f"Legacy Θ_S^(10) = {legacy_val:.6f}")
# Output: Legacy Θ_S^(10) = 0.008634
```

### 2. Vectorized Evaluation & Radial Decay

```python
import numpy as np
from sayan_gradient import theta_s

distances = np.array([2.0, 5.0, 10.0, 50.0, 100.0])
field = theta_s(E_nb=100.0, delta_T=50.0, r=distances)

for dist, val in zip(distances, field):
    print(f"r = {dist:5.1f} | |θ_S| = {val:.5f}")
```

### 3. Radial Contour Integration with SciPy

```python
from sayan_gradient import theta_s_line_integral

# Integrated field along radial path [r_a, r_b] via SciPy's logarithmic integral (sp.expi)
line_val = theta_s_line_integral(E_nb=50.0, delta_T=273.0, r_a=2.0, r_b=1000.0)
print(f"Path integral Θ_S(a->b) = {line_val:.6f}")
# Output: 4.573258
```

### 4. Deep Space Vacuum Destruction Limits

```python
from sayan_gradient import (
    vacuum_destruction_radius,
    energy_breaking_threshold,
    parameter_free_energy_ratio,
)

# Predict vacuum destruction radius for material threshold theta_c = 1.0
R_d = vacuum_destruction_radius(E_nb=100.0, theta_crit=1.0, delta_T=1.0)
print(f"Destruction radius R_d = {R_d:.2f} r0")
# Output: 22026.47 r0 (exponential reach in deep space)

# Predict breaking energy required at distance r = 500.0
E_c = energy_breaking_threshold(r=500.0, theta_crit=1.0, delta_T=1.0)
print(f"Required source energy E_c = {E_c:.2f} E0")

# Parameter-free energy ratio to extend reach from x1=10 to x2=100
ratio = parameter_free_energy_ratio(r1=10.0, r2=100.0)
print(f"Energy multiplier: {ratio:.2f}x (exactly 4.0x)")
```

### 5. Empirical Calibration of $K$ with SciPy Optimization

```python
from sayan_gradient import calibrate_k

# Observed event measurements: (energies, thermal gradients, radii, observed field)
obs_E = [10.0, 25.0, 50.0, 100.0]
obs_dT = [1.0, 1.5, 2.0, 2.5]
obs_r = [5.0, 12.0, 20.0, 40.0]
obs_thetas = [4.57, 3.65, 3.52, 3.84]

k_fit, k_err = calibrate_k(obs_E, obs_dT, obs_r, obs_thetas)
print(f"Fitted calibration constant: K = {k_fit:.4f} ± {k_err:.4f}")
```

### 6. Object-Oriented Interface (`ThetaSOperator`)

```python
from sayan_gradient import ThetaSOperator, ReferenceScales

scales = ReferenceScales(E0=1e20, T0=2.7, r0=1e9, K=1.2)  # Deep space scales
op = ThetaSOperator(scales)

# Evaluate, compute gradient, and solve critical radius
val = op(E_nb=5e20, delta_T=5.4, r=2e10)
grad = op.gradient(E_nb=5e20, delta_T=5.4, r=2e10)
r_crit = op.critical_radius(E_nb=5e20, delta_T=5.4, theta_crit=0.5)
```

---

## Visualization

The `sayan_gradient.visualization` module provides both static Matplotlib figures and interactive Plotly visualizations:

```python
from sayan_gradient import (
    plot_field_decay,
    plot_thermal_energy_map,
    plot_vacuum_destruction_radius,
    plot_surface_3d,
)

# 1. Matplotlib static decay curves
fig1 = plot_field_decay(energies=[0.5, 1.0, 2.0, 4.0], backend="matplotlib")

# 2. 2D Thermal-Distance Energy Heatmap
fig2 = plot_thermal_energy_map(energy=1.0, backend="matplotlib")

# 3. Interactive 3D Plotly Surface
fig3 = plot_surface_3d(energy=1.0, backend="plotly")
# fig3.show()
```

---

## Jupyter Notebook Examples

Interactive Jupyter notebooks are included in the `notebooks/` directory:

1. **`notebooks/01_thetas_operator_basics.ipynb`**:
   Comprehensive walk-through of the $\Theta_s$ operator, dimensionless scaling, singularity boundary, path integrals with SciPy, and radial gradients.
2. **`notebooks/02_deep_space_destruction_limits.ipynb`**:
   Deep space nuclear energy destruction limits, vacuum destruction radius, energy breaking thresholds, verification of Prediction P2, and model calibration via `scipy.optimize`.
3. **`notebooks/03_thermal_mapping_and_visualization.ipynb`**:
   Thermal-distance contour maps, multi-source deep space simulation and superposition, and interactive 3D Plotly visualizations.

To launch the notebooks:

```bash
jupyter notebook notebooks/
```

---

## Running the Test Suite

The test suite covers all mathematical identities, non-dimensionalization, vectorization, edge cases, root-solving, and plotting backends:

```bash
pytest -v
```

---

## Formal Written Documentation

In-depth theoretical documentation is available in the [`paper/`](paper/) directory:
- [`paper/theory_paper.md`](paper/theory_paper.md) — Main research paper.
- [`paper/postulates.md`](paper/postulates.md) — The five axioms (unification, logarithmic decay, square-root energy, thermal antagonism, critical threshold).
- [`paper/formal_framework.md`](paper/formal_framework.md) — Mathematical derivations and closed-form solutions.
- [`paper/predictions.md`](paper/predictions.md) — Falsifiable predictions and validation roadmap.
- [`paper/open_questions.md`](paper/open_questions.md) — Limitations, tensions with inverse-square law, and open questions.
- [`paper/glossary.md`](paper/glossary.md) — Physical and mathematical glossary.

---

## Citation

If you use `sayan-gradient` or the Sayan Universal Gradient Theory in your research, please cite:

```bibtex
@misc{sayan_gradient_theory_2026,
  author       = {M., Sayan},
  title        = {The Sayan Universal Gradient (SUG) Theory: A Proposed Mathematical Framework Coupling Energy Release, Thermal Gradients and Cosmic Distance},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/ZENODO.22723906},
  url          = {https://doi.org/10.5281/ZENODO.22723906}
}
```

---

## License

Distributed under the [MIT License](LICENSE).  
Copyright © 2026 Sayan M. All Rights Reserved.
