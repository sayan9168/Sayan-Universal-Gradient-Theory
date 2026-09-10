# The Sayan Universal Gradient (SUG) — Formal Framework

> This is the mathematical core of the theory.  It defines the operator, makes
> it dimensionally honest, and derives every secondary relation used
> elsewhere.  All definitions are consistent with the code in
> `sug_theory/`.

**Notation.**  We use *dimensionless* quantities throughout so that no hidden
dimensions creep into the algebra.  Physical inputs are normalised by
reference scales:

| Symbol | Meaning | Definition |
|---|---|---|
| :math:`e` | dimensionless source energy | :math:`e = E_{nb}/E_0` |
| :math:`\tau` | dimensionless thermal gradient | :math:`\tau = \Delta T/T_0` |
| :math:`x` | dimensionless distance | :math:`x = r/r_0` |
| :math:`K` | calibration constant (dimensionless) | free, to be fit |

---

## 1. The central operator

The **Sayan–Universal field** at a point is

$$
\boxed{\;\theta_S(x) \;=\; K\, \frac{\sqrt{e}}{\tau\, \ln x}\,, \qquad x > 1\;}
$$

### Why this form
By construction (Postulates II, III, IV):

- :math:`\theta_S \propto \sqrt{e}` — square-root energy response (P-III);
- :math:`\theta_S \propto 1/\tau` — thermal antagonism (P-IV);
- :math:`\theta_S \propto 1/\ln x` — logarithmic geometric decay (P-II);
- :math:`\theta_S` is *dimensionless* — every input is a ratio.

The reference point :math:`x=1` (i.e. :math:`r=r_0`) is a **singularity**:
the field diverges there because :math:`\ln 1 = 0`.  Physically this marks
the edge of the "source core" — a radius inside which the continuum field
description breaks down.  It is not a defect of the theory but its statement
of where the field picture ends and the source begins.

---

## 2. Dimensional honesty (why ratios, not raw units)

A naive reading of the earlier scalar form

$$
\Theta_S = \frac{\sqrt{E_{nb}}}{\Delta T\,\log_{10} r}
$$

is dimensionally awkward: :math:`\sqrt{\text{energy}}/[\text{temperature}]
` does not cancel, and a logarithm of a dimensionful distance is formally
undefined.  The framework resolves both issues by **declaring reference
scales** :math:`E_0, T_0, r_0` and working with ratios.  Any defensible
theory must state its units; SUG states them as reference scales plus one
dimensionless constant :math:`K`.

The earlier form is recovered as the special illustrative case
:math:`K=1,\; E_0=T_0=r_0=1` evaluated with base-10 logarithms — a convenient
*laboratory* case, not a different theory.

---

## 3. The contour (path-integrated) form

The original formulation wrote the operator with a closed-path integral:

$$
\Theta_S = \oint \frac{\sqrt{E_{nb}}}{\Delta T\,\log r}\, dr .
$$

Restricting to a *radial* path from :math:`r_a` to :math:`r_b`, and using the
logarithmic integral

$$
\operatorname{li}(x) \;=\; \int_0^x \frac{dt}{\ln t}
      \;=\; \gamma + \ln\ln x + \sum_{k=1}^{\infty}\frac{(\ln x)^k}{k\,k!},
\qquad x>1,
$$

the integral is exact:

$$
\boxed{\;\Theta_S(a\to b) \;=\; \frac{K\sqrt{e}}{\tau}
      \Bigl[\operatorname{li}(x_b) - \operatorname{li}(x_a)\Bigr]\;}
$$

This is the "global" version of the field: the field integrated along the
path, in closed form.  It appears in the code as
`sug_line_constant(E_nb, delta_T, r_a, r_b)`.

---

## 4. Inverse problem: given a threshold, find the geometry

Postulate V supplies a material threshold :math:`\theta_c`.  Setting
:math:`\theta_S = \theta_c` and solving isolates the geometry.

### 4a. Critical (destruction) radius

Holding :math:`e,\tau` fixed:

$$
\frac{K\sqrt{e}}{\tau \ln x_c} = \theta_c
\;\;\Longrightarrow\;\;
\ln x_c = \frac{K\sqrt{e}}{\tau\,\theta_c}
\;\;\Longrightarrow\;\;
\boxed{\;x_c = \exp\!\Bigl(\frac{K\sqrt{e}}{\tau\,\theta_c}\Bigr),\quad
        R_c = r_0\, x_c\;}
$$

**Reading.**  Because the field decays *logarithmically*, the critical radius
grows *exponentially* in :math:`\sqrt{e}/(\tau\theta_c)`.  Even a modestly
strong source projects a threshold far into space in vacuum — the theory's
headline "long-reach" prediction.

### 4b. Breaking energy

Holding :math:`\tau, x` fixed:

$$
e_c = \Bigl(\frac{\tau\,\theta_c\,\ln x}{K}\Bigr)^2
\;\;\Longrightarrow\;\;
\boxed{\;E_c = E_0\Bigl(\frac{\tau\,\theta_c}{K}\Bigr)^2
        \bigl(\ln x\bigr)^2\;}
$$

**Reading.**  The energy required to cross a threshold at a distance grows
*only quadratically* in the logarithm of distance.  Because :math:`(\ln x)^2`
rises slowly, the theory says *surprisingly little* extra energy is needed to
extend an effect from :math:`x=10` to :math:`x=1000` — again a long-reach
signature.

---

## 5. Consistency identities

Two identities link the operators and are enforced by the test suite:

1. **Radius round-trip.** The field evaluated at its critical radius equals
   the threshold:

   $$
   \theta_S\bigl(x_c\bigr) = \theta_c .
   $$

2. **Energy round-trip.** The field produced by the breaking energy at the
   target distance equals the threshold:

   $$
   \theta_S(e_c,\, x) = \theta_c .
   $$

These are algebraic rearrangements of the same definition; they guarantee the
code is a faithful implementation of the mathematics.

---

## 6. Where the classical anchors sit

The framework is *not* presented in a vacuum.  It deliberately speaks the
language of adjacent, established ideas so it can be compared against them:

| SUG element | Classical anchor | Relation / tension |
|---|---|---|
| Energy entering as a field driver | Relativistic energy, radiation flux | SUG uses :math:`\sqrt{E}`, not :math:`E/x^2` |
| Thermal antagonism | Thermodynamics, cooling laws | Direction of coupling must be checked against data |
| Threshold → phase change | Critical phenomena, phase transitions | Postulate V is the phase-transition analogue |
| Logarithmic decay | Coulomb/log potentials in 2D, gravitational potential | Must be reconciled with the 3D inverse-square law |

The *tensions* in the last column are examined honestly in
`open_questions.md`.  A theory is judged by what it predicts *and* by where
it is expected to break.
