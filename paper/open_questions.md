# Open Questions, Limitations & the Validation Agenda

> **Read this first.**  These notes state plainly what SUG is *not* yet: it is
> **not peer reviewed, not published in a journal, and not validated by any
> experiment**.  Presenting it as established physics would be misleading.
> The sections below make the open problems explicit so a future researcher
> (the author included) can work on them with honesty.

---

## O1 — The calibration problem (the single most important issue)

SUG contains one genuinely free parameter, the calibration constant :math:`K`,
plus three reference scales that are *choices of unit*, not physics.

- Until :math:`K` is fit to at least one real, well-measured event, **no
  absolute prediction** (a specific destruction radius in metres, a specific
  energy in joules) can be made.  Only *shapes* and *ratios* are predictive.
- **Open task.**  Identify one clean anchor event and calibrate :math:`K`.
  Then verify with a second event using the parameter-free energy ratio (P2).

---

## O2 — Tension with the inverse-square law

Postulate II (logarithmic decay) is in direct conceptual tension with the
best-established fact of radiative energy spreading: **intensity falls as
:math:`1/r^2`** in three-dimensional space because the same power spreads over
a growing sphere.

- SUG is proposed as a *field organising energy + temperature + distance*, not
  necessarily as a rival to the flux law.  Whether the two can coexist, or
  whether SUG should be understood as operating on a *derived/effective*
  quantity rather than raw flux, is **unresolved**.
- **Open task.**  Construct a derivation or re-scaling that shows exactly which
  physical observable SUG predicts, and reconcile it with energy
  conservation and the :math:`1/r^2` spread of radiation.

---

## O3 — The reference point / singularity

The field diverges at :math:`x=1` (:math:`r=r_0`).  The interpretation
proposed here ("edge of the source core") is an assumption.  A rigorous theory
must say how :math:`r_0` is chosen for a given source and what bounds the
divergence physically.  **Open task:** a regularity or cut-off prescription.

---

## O4 — Square-root energy response

Postulate III (:math:`\theta_S \propto \sqrt{E}`) is asserted, not derived.
Why the square root rather than, say, :math:`E^{1/3}` or :math:`E`?  **Open
task:** find a microphysical story (if one exists) that produces a square-root
coupling, or soften this to an explicit family :math:`\propto E^{\alpha}` and
treat :math:`\alpha` as a second parameter to be measured.

---

## O5 — The threshold :math:`\theta_c` is material-specific

Postulate V introduces a threshold but does not say how :math:`\theta_c` is
computed for a real material.  Until there is a prescription linking
:math:`\theta_c` to measurable material properties, the "destruction radius"
predictions cannot be turned into numbers.  **Open task:** a table of
:math:`\theta_c` values, or a sub-model for it.

---

## O6 — No experimental or observational data yet

As of this writing there are **no experiments, no simulations validated
against reality, and no published data sets** testing SUG.  The `figures/`
produced by the code are *illustrations of the mathematical model*, not
measurements.

---

## O7 — No external derivation

SUG is not derived from general relativity, quantum field theory, or
thermodynamics.  Its axioms are chosen for elegance and internal consistency.
That is a legitimate starting point for a *proposal*, but it is not yet a
*physical law*.  **Open task:** show SUG as the limit or consequence of an
established framework, or accept it as purely phenomenological pending data.

---

## The validation agenda (summary)

| Priority | Action | Criteria for "done" |
|---|---|---|
| 1 | Calibrate :math:`K` to one anchor event | reproduces one measured radius/energy |
| 2 | Test the parameter-free energy ratio (P2) | matches on an independent event |
| 3 | Test linearity of :math:`\ln R_c` vs :math:`\sqrt{E}` (P1) | straight line over a decade |
| 4 | Reconcile with inverse-square law (O2) | consistent, published argument |
| 5 | Prescribe :math:`\theta_c` for real materials (O5) | usable, testable numbers |

Until items 1–2 succeed, the correct scientific label for this material is
**"a proposed, self-consistent framework awaiting empirical validation."**
