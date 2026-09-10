# SUG — Predictions & a Testing Roadmap

A framework is only as good as the things it dares to predict *and* the way it
could be shown wrong.  Below is a catalogue of concrete, ideally-falsifiable
statements that follow from `formal_framework.md`.  Each is written so that,
in principle, an experiment or observation could confirm or reject it.

> **Important caveat.**  Every numerical prediction requires the reference
> scales :math:`(E_0,T_0,r_0)` and the calibration constant :math:`K` to be
> fixed first.  Until :math:`K` is fit to at least one anchor event, the
> theory makes *shape* predictions (functional forms, monotonicities, ratios)
> rather than absolute numbers.

---

## P1 — A strong *shape* prediction: logarithmic reach

**Statement.**  In vacuum, the threshold-distance for a source grows
exponentially in the source's control parameter:

$$
\ln R_c \propto \sqrt{E_{nb}} \qquad (\tau, \theta_c \text{ fixed}).
$$

Equivalently, **plotting :math:`\ln R_c` against :math:`\sqrt{E_{nb}}` must be
a straight line.**  A graph of :math:`\ln R_c` vs :math:`E_{nb}` or vs
:math:`\ln E_{nb}` would *not* be linear — an easy visual falsification.

**Test.**  Scale up released energy and measure how far the destructive
threshold moves in vacuum.

---

## P2 — Long-reach ratio (the most aggressive claim)

**Statement.**  Moving a threshold from distance :math:`x_1` to :math:`x_2`
costs energy in the ratio

$$
\frac{E_2}{E_1} = \left(\frac{\ln x_2}{\ln x_1}\right)^2 ,
$$

independent of the material threshold and the calibration constant
(so long as :math:`\tau` is fixed).  This ratio is *parameter-free* and is
therefore the cleanest test SUG offers.

**Numerical illustration.**  From :math:`x=10` to :math:`x=100` the ratio is
:math:`[\ln100/\ln10]^2 = [4.605/2.303]^2 = 4.0`.  From :math:`x=100` to
:math:`x=1000` it is again :math:`4.0`.  A theory with power-law fall-off
would demand a vastly larger energy ratio.  **If real data require a much
bigger energy multiplier for the same range extension, SUG's logarithmic
ansatz is wrong.**

---

## P3 — Thermal antagonism

**Statement.**  For fixed source energy and distance, the field strength is
inversely proportional to the ambient thermal gradient:

$$
\theta_S \propto 1/\tau .
$$

**Test.**  Hold the source fixed and raise ambient temperature (gradient);
the observed "disturbance strength" at a fixed point should fall
hyperbolically.  A measurement that is flat in temperature would reject the
coupling direction of Postulate IV.

---

## P4 — Square-root energy saturation

**Statement.**  Doubling energy multiplies the field by :math:`\sqrt{2}` and
the destruction radius by a factor :math:`\exp\bigl[(K/\tau\theta_c)(\sqrt{2}-1)\sqrt{e}\bigr]`
— i.e. only mildly.  Above a certain energy the *field* returns diminish,
even though the *radius* keeps climbing exponentially.

**Test.**  A saturation curve in field-vs-energy is a distinctive, falsifiable
signature that distinguishes SUG from linear energy response models.

---

## P5 — Vacuum/atmosphere asymmetry

**Statement.**  Because the field decays only logarithmically, the same source
projects a much larger destructive influence in vacuum than inside an
attenuating atmosphere, where scattering and absorption impose additional
:math:`e^{-\mu x}`-type suppression on top of the SUG field.  The theory thus
qualitatively predicts: **a blast in deep space affects a far greater volume
than an identical blast in an atmosphere.**

---

## P6 — A field, not point events

**Statement.**  Thermal and mechanical signatures of a high-energy event
should be *spatially continuous and jointly organised* by a single field,
rather than described by independent radial profiles per channel.  Correlations
between the thermal and mechanical channels should follow the SUG field's
single functional form.

---

## Summary table

| # | Prediction | Parameter-free? | Most direct falsification |
|---|---|---|---|
| P1 | :math:`\ln R_c \propto \sqrt{E}` linear | no | plot :math:`\ln R_c` vs :math:`\sqrt{E}` |
| P2 | energy-ratio :math:`=(\ln x_2/\ln x_1)^2` | **yes** | need far larger energy for range |
| P3 | :math:`\theta_S\propto1/\tau` | no | vary temperature, field must fall |
| P4 | saturating field vs energy | no | field-vs-energy must saturate |
| P5 | larger influence in vacuum | no | compare vacuum vs atmospheric blast |
| P6 | single organising field | yes (form) | channels decorrelate |

---

## Minimal validation roadmap

1. **Anchor calibration (1 event).**  Choose one well-measured high-energy
   event, fix :math:`E_0,T_0,r_0` to convenient units, and solve for
   :math:`K` so the threshold matches one observed radius.  This removes the
   only free constant.
2. **Parameter-free check.**  Use P2's energy-ratio (no :math:`K` needed) on a
   *second* event at a different range.  If it holds, SUG earns its keep.
3. **Decay-shape check.**  Measure :math:`\ln R_c` vs :math:`\sqrt{E}` over a
   decade of energies (P1 linearity).
4. **Thermal check.**  Sweep ambient temperature at fixed geometry (P3).
5. **Publish the negative results.**  A failed prediction is as valuable as a
   successful one for deciding whether to keep the framework.

The honest framing: this roadmap is exactly what is *not yet done*.  Until
steps 1–2 are performed, SUG remains a self-consistent proposal awaiting its
first confrontation with data.
