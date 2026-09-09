# The Sayan Universal Gradient (SUG) Theory

### *A Proposed Mathematical Framework for Coupling Energy Release, Thermal
Gradients and Cosmic Distance*

<p align="center"><b>Author:</b> Sayan M. · <b>Status:</b> Speculative research
framework (not peer-reviewed) · <b>Language:</b> English</p>

---

## ⚠ Important status note

**SUG is an original, speculative proposal.  It is not peer reviewed, not
published, and not validated against experiments.**  It is written with the
structure and confidence of a research programme so it can be examined and
*tested* — not to imply its claims are established.  Its single free
parameter, the calibration constant :math:`K`, has not yet been fit to data,
so the theory currently predicts functional *shapes and ratios* rather than
absolute numbers.  **Please read [`paper/open_questions.md`](paper/open_questions.md)
before treating any prediction as physical.**

---

## What is SUG?

The **Sayan Universal Gradient (SUG)** theory asks a unifying question:

> *Can a single scalar field organise a high-energy source's released energy,
> the local thermal gradient, and distance — and, if so, what geometric laws
> follow?*

The answer it proposes is the **Sayan–Universal field** :math:`\Theta_S`,
defined on dimensionless ratios against stated reference scales:

$$
\Theta_S(x) \;=\; K\,\frac{\sqrt{E_{nb}/E_0}}{(\Delta T/T_0)\,\ln(r/r_0)}
      \;=\; K\,\frac{\sqrt{e}}{\tau\,\ln x}.
$$

Its signature idea is **logarithmic decay with distance** — a slow, long-reach
fall-off that is cleanly falsifiable against the classical inverse-square law.

---

## Repository layout

```
├── README.md                     ← you are here
├── paper/                        ← the written theory (start here)
│   ├── theory_paper.md           ←   umbrella research paper
│   ├── postulates.md             ←   the five axioms
│   ├── formal_framework.md       ←   definitions & full algebra
│   ├── predictions.md            ←   falsifiable predictions + testing roadmap
│   ├── numerical_experiments.md  ←   what the code does, with figures
│   ├── open_questions.md         ←   ⚠ honest limitations & agenda
│   ├── glossary.md / faq.md      ←   reference material
│   └── references.md             ←   intellectual context
├── sug_theory/                   ← Python implementation (a real library)
│   ├── operators.py              ←   central operators & inversions
│   ├── nondim.py                 ←   dimensionless re-scaling
│   ├── phenomena.py              ←   derived predictions layer
│   ├── plots.py                  ←   figure generation
│   └── constants.py              ←   reference scales & calibration K
├── figures/                      ← generated plots (see below)
├── examples/                     ← worked example scripts
├── tests/                        ← pytest suite (identities & edge cases)
├── main.py                       ← end-to-end CLI demonstration
├── pyproject.toml / requirements.txt
└── LICENSE
```

---

## Quickstart

```bash
# 1) End-to-end demonstration (legacy scalar → dimensionless field → inverses)
python main.py

# 2) Generate the figures (needs matplotlib)
python -m sug_theory.plots --outdir figures

# 3) Run the test suite (needs pytest)
python -m pytest -q
```

### Worked example (kept from the original paper)

```python
from sug_theory import sug_scalar

sug_scalar(E_nb=50.0, delta_T=273.0, r=1000.0)
# = sqrt(50) / (273 * log10(1000)) ≈ 0.00527   (legacy base-10 scalar)
```

The modern, dimensionless operators:

```python
from sug_theory import theta_s, sug_line_constant, theta_critical_radius

SC = ReferenceScales(E0=1.0, T0=1.0, r0=1.0, K=1.0)

theta_s(E_nb=50, delta_T=273, r=1000, scales=SC)   # point field value
sug_line_constant(50, 273, r_a=2, r_b=1000)        # path-integrated (contour) field
theta_critical_radius(50, 273, theta_crit=1.0)     # destruction radius at threshold
```

---

## The five postulates (summary)

1. **P-I — Unification:** one scalar field couples energy, thermal gradient,
   and distance.
2. **P-II — Logarithmic decay:** :math:`\theta_S \propto 1/\ln x`.
3. **P-III — Square-root energy:** :math:`\theta_S \propto \sqrt{E_{nb}}`.
4. **P-IV — Thermal antagonism:** :math:`\theta_S \propto 1/\Delta T`.
5. **P-V — Threshold:** a material threshold :math:`\theta_c` separates bound
   matter from an information/energy degree of freedom.

Full statements, with consequences, are in [`paper/postulates.md`](paper/postulates.md).

---

## Headline predictions (all falsifiable)

- **P1 (shape):** :math:`\ln R_c` vs :math:`\sqrt{E_{nb}}` is a straight line.
- **P2 (parameter-free!):** extending a threshold from :math:`x_1` to
  :math:`x_2` costs energy in ratio
  :math:`(E_2/E_1) = (\ln x_2/\ln x_1)^2` — *independent of* :math:`K` *and*
  :math:`\theta_c`.
- **P3 (thermal):** :math:`\theta_S\propto 1/\tau` at fixed geometry.
- **P4 (saturation):** the field saturates as :math:`\sqrt{E}` grows.
- **P5 (vacuum asymmetry):** reach is much larger in vacuum than in an
  attenuating atmosphere.
- **P6 (field test):** thermal & mechanical signatures share one functional
  form.

Details and falsification routes: [`paper/predictions.md`](paper/predictions.md).

---

## Reading order for a researcher

1. [`paper/theory_paper.md`](paper/theory_paper.md) — the full paper.
2. [`paper/postulates.md`](paper/postulates.md) — the axioms.
3. [`paper/formal_framework.md`](paper/formal_framework.md) — the mathematics.
4. [`paper/predictions.md`](paper/predictions.md) — how to test it.
5. [`paper/open_questions.md`](paper/open_questions.md) — **the honest limits.**
6. [`paper/numerical_experiments.md`](paper/numerical_experiments.md) — the code.

---

## How to cite

> M., Sayan. *The Sayan Universal Gradient (SUG) Theory: A Proposed Framework
> Coupling Energy Release, Thermal Gradients and Cosmic Distance.* GitHub
> repository `sayan9168/Sayan-Universal-Gradient-Theory`, 2026.

---

© 2026 Sayan M. All Rights Reserved.
Distributed under the [MIT License](LICENSE).
