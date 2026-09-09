# The Sayan Universal Gradient (SUG) Theory

### A Proposed Mathematical Framework Coupling Energy Release, Thermal
### Gradients and Cosmic Distance

**Author:** Sayan M. — 2026
**Repository:** `sayan9168/Sayan-Universal-Gradient-Theory`
**Version of this paper:** 2.0

---

> ## ⚠ Preprint notice — please read
> This document is a **proposed, speculative theoretical framework**.  It has
> **not been peer reviewed**, has **not been published in a scientific
> journal**, and has **not been validated against any experiment or
> observation**.  It is written with the structure and confidence of a
> research paper so that it can be examined, criticised and *tested* — not to
> imply that its claims are established.  Until the model's free parameter
> (the calibration constant :math:`K`) is fit to a real event, the theory
> predicts functional *shapes and ratios*, not absolute numbers.  Every
> limitation is catalogued in `open_questions.md`.

---

## Abstract

We introduce the **Sayan Universal Gradient (SUG)** theory: an original,
self-consistent proposal in which a single dimensionless scalar field
:math:`\theta_S` simultaneously organises three observables of a high-energy
source — the *released energy potential* :math:`E_{nb}`, the *local thermal
gradient* :math:`\Delta T`, and the *distance* :math:`r` from the source.
The field is defined on dimensionless ratios against stated reference scales
and decays logarithmically with distance,

$$
\theta_S(x) \;=\; K\, \frac{\sqrt{e}}{\tau\,\ln x}\,,\qquad
e=\frac{E_{nb}}{E_0},\ \ \tau=\frac{\Delta T}{T_0},\ \ x=\frac{r}{r_0},
$$

where :math:`K` is the model's single calibration constant.  Five postulates
anchor the framework (energy coupling, logarithmic decay, square-root energy
response, thermal antagonism, and a material threshold separating bound matter
from an information/energy degree of freedom).  From these, closed-form
expressions are derived for the *path-integrated (contour) field*, a
*destruction radius*, and a *breaking energy*.  We state six concrete,
falsifiable predictions — including one fully *parameter-free* relation — and
give an explicit validation roadmap.  SUG is offered as a testable research
programme awaiting its first confrontation with data.

---

## 1. Introduction & motivation

Classical treatments of high-energy events keep three ledger books largely
apart: how much energy was released, what thermal gradient is felt where, and
at what distance effects persist.  This separation is convenient but may hide
an underlying order.  SUG asks a deliberately unifying question:

> *Can a single scalar field organise a source's released energy, the local
> thermal gradient, and distance — and, if so, what geometric laws follow?*

The framework proposes such a field and works out its consequences with full
algebra.  Its signature and most testable assumption is **logarithmic decay
with distance** — a slow, long-reach fall-off that stands in sharp, useful
contrast to the classical inverse-square law and that can therefore be
falsified cleanly (Section 5, O2).

The remainder of the paper: postulates (§2), the formal framework and central
operator (§3), derived relations (§4), predictions and falsification tests
(§5), numerical illustration (§6), and open questions (§7).

---

## 2. Postulates

The framework stands on five explicit axioms, stated in full in
`paper/postulates.md`:

- **P-I (unification).** A single scalar field :math:`\theta_S` couples
  released energy, thermal gradient and distance.
- **P-II (logarithmic decay).** :math:`\theta_S` falls as :math:`1/\ln x`.
- **P-III (square-root energy).** :math:`\theta_S \propto \sqrt{E_{nb}}`.
- **P-IV (thermal antagonism).** :math:`\theta_S \propto 1/\Delta T`.
- **P-V (threshold).** A material threshold :math:`\theta_c` separates bound
  matter from an information/energy degree of freedom.

All derived structure below follows from these premises and the requirement
of dimensional consistency.

---

## 3. The formal framework

### 3.1 Reference scales and dimensionless ratios
To be dimensionally honest, physical inputs are normalised by reference scales
:math:`E_0, T_0, r_0` (the "units of the theory"), and one dimensionless
constant :math:`K` carries any calibration freedom:

$$
e=\frac{E_{nb}}{E_0},\qquad \tau=\frac{\Delta T}{T_0},\qquad x=\frac{r}{r_0}.
$$

### 3.2 The central operator
Postulates II–IV and dimensional consistency select the form

$$
\boxed{\;\theta_S(x) = \frac{K\sqrt{e}}{\tau\,\ln x},\qquad x>1\;}
$$

The point :math:`x=1` is a singularity marking the inner edge of the field
description (the "source core").  For :math:`x\le 1` the continuum field is
not defined.

### 3.3 The contour (path-integrated) field
Restricting the original closed-path integral to a radial segment and using
the logarithmic integral :math:`\operatorname{li}(x)=\int_0^x dt/\ln t`, the
integral is exact:

$$
\boxed{\;\Theta_S(a\to b)=\frac{K\sqrt{e}}{\tau}
   \bigl[\operatorname{li}(x_b)-\operatorname{li}(x_a)\bigr]\;}
$$

---

## 4. Derived relations (inverse problem)

Given a material threshold :math:`\theta_c` (Postulate V), setting
:math:`\theta_S=\theta_c` yields the geometry of destruction.

### 4.1 Destruction radius
$$
\boxed{\;x_c=\exp\!\Bigl(\frac{K\sqrt{e}}{\tau\,\theta_c}\Bigr),\qquad
        R_c = r_0\,x_c\;}
$$

Logarithmic decay in the field becomes *exponential* growth of the critical
radius with :math:`\sqrt{e}` — the "long reach" of the theory.

### 4.2 Breaking energy
$$
\boxed{\;E_c = E_0\Bigl(\frac{\tau\,\theta_c}{K}\Bigr)^2
        \bigl(\ln x\bigr)^2\;}
$$

Reach extends cheaply: the required energy grows only quadratically in
:math:`\ln x`.

### 4.3 Consistency
Two round-trip identities (:math:`\theta_S(x_c)=\theta_c` and
:math:`\theta_S(e_c,x)=\theta_c`) are enforced in the code and test suite.

---

## 5. Predictions and falsification

The most valuable element of the paper for a working researcher is the set of
*cleanly testable* statements (`paper/predictions.md`):

- **P1 — Shape test.** :math:`\ln R_c` vs :math:`\sqrt{E_{nb}}` must be a
  straight line.
- **P2 — Parameter-free test.** Extending a threshold from :math:`x_1` to
  :math:`x_2` costs energy in ratio :math:`(E_2/E_1)=(\ln x_2/\ln x_1)^2`,
  **independent of :math:`K` and :math:`\theta_c`**.
- **P3 — Thermal test.** :math:`\theta_S\propto 1/\tau` at fixed geometry.
- **P4 — Saturation test.** Field saturates as :math:`\sqrt{E}` grows.
- **P5 — Vacuum asymmetry.** Much larger reach in vacuum than in an
  attenuating atmosphere.
- **P6 — Field (not point-event) test.** Thermal and mechanical signatures are
  jointly organised by one functional form.

Falsification routes for each are tabulated in `predictions.md`.

---

## 6. Numerical illustration

The framework is implemented and reproduced in the `sug_theory` Python
package.  Running

```bash
python main.py
python -m sug_theory.plots --outdir figures
python -m pytest -q
```

generates the figures in `figures/` (field decay, thermal–distance energy map,
destruction radius, breaking energy) and verifies the algebraic identities.
**These figures illustrate the model; they are not measurements.**  Full
description in `paper/numerical_experiments.md`.

---

## 7. Open questions & honest limitations

A summary of the open problems developed in `paper/open_questions.md`:

1. **Calibration.** :math:`K` is free until fit to one real anchor event; only
   shapes/ratios are currently predictive.
2. **Inverse-square tension.** Logarithmic decay must be reconciled with the
   classical spreading of radiative flux.
3. **The source-core singularity** needs a physical cut-off prescription.
4. **Square-root energy response** is asserted, not derived.
5. **The material threshold** :math:`\theta_c` lacks a microphysical formula.
6. **No data yet.** No experiment or validated simulation tests SUG as of this
   writing.

---

## 8. Conclusion

SUG is presented as a *disciplined proposal*: a small set of explicit axioms,
a dimensionally honest central operator, closed-form consequences, and —
crucially — a set of falsifiable predictions with an explicit path to
validation.  Whether it survives contact with data is an open empirical
question; this framework is written so that the question can be answered
decisively rather than avoided.

---

## Citation

> M., Sayan. *The Sayan Universal Gradient (SUG) Theory: A Proposed Framework
> Coupling Energy Release, Thermal Gradients and Cosmic Distance.* GitHub
> repository `sayan9168/Sayan-Universal-Gradient-Theory`, 2026.

**Author contact / provenance:** See repository `README`.

---
*All rights reserved to the author.  Figures generated by `sug_theory/plots.py`.*
