# Glossary of Terms

| Term | Symbol | Definition |
|---|---|---|
| **Sayan–Universal field** | :math:`\theta_S` | The scalar field coupling energy, thermal gradient and distance; the theory's central object. |
| **Dimensionless source energy** | :math:`e` | :math:`E_{nb}/E_0`, released energy normalised by a reference scale. |
| **Released energy potential** | :math:`E_{nb}` | Energy made available by the source ("nuclear bombardment" potential in the original framing). |
| **Thermal gradient** | :math:`\Delta T` | Temperature contrast; in SUG it *antagonises* the field. |
| **Dimensionless thermal gradient** | :math:`\tau` | :math:`\Delta T/T_0`. |
| **Dimensionless distance** | :math:`x` | :math:`r/r_0`; the field is a function of :math:`x`. |
| **Reference scales** | :math:`E_0,T_0,r_0` | The "units of the theory" making inputs dimensionless. |
| **Calibration constant** | :math:`K` | The single free numeric parameter, to be fit to data. |
| **Logarithmic decay** | :math:`1/\ln x` | SUG's claim that the field falls logarithmically with distance (Postulate II). |
| **Critical threshold** | :math:`\theta_c` | Material/regime threshold above which matter transitions to information/energy (Postulate V). |
| **Destruction radius** | :math:`R_c` | Radius at which :math:`\theta_S = \theta_c`. |
| **Breaking energy** | :math:`E_c` | Source energy required to cross :math:`\theta_c` at a given distance. |
| **Logarithmic integral** | :math:`\operatorname{li}(x)` | :math:`\int_0^x dt/\ln t`; appears in the contour (path) form. |
| **Contour constant** | :math:`\Theta_S(a\to b)` | Path-integrated field over :math:`[r_a,r_b]`. |
| **Thermal antagonism** | — | The mechanism (Postulate IV) by which gradient damps the field. |
| **Source core** | :math:`x=1` | The divergence point / inner boundary where the field picture ends. |

---

# FAQ (Frequently Asked Questions)

**Is SUG a confirmed law of physics?**
No.  It is an original, self-consistent *proposal*.  It has not been peer
reviewed or experimentally validated.  See `open_questions.md`.

**Then why present it this formally?**
So it can be examined, criticised, and tested properly.  Writing axioms,
definitions and predictions precisely is exactly how a speculative idea
becomes a *testable* research programme rather than a vague claim.

**What is the theory actually claiming?**
That a single scalar field can organise a source's released energy, the local
thermal gradient and distance, and that its decay is logarithmic in distance.
Everything else (destruction radius, breaking energy, thermal map) is derived
from that.

**What is its most controversial point?**
Postulate II — logarithmic instead of inverse-square decay — because it
conflicts with how radiative flux spreads in 3D.  This is discussed in O2 and
is the point most likely to be falsified.

**How can it be tested?**
Start with the *parameter-free* prediction P2 (the energy ratio for extending
range), then calibrate :math:`K` on one anchor event and test P1's linear
plot.  Full roadmap in `predictions.md`.

**Is the Python implementation "proof"?**
No.  The code verifies the mathematics is implemented consistently and that
identities hold; it does **not** prove the physics.  Figures are illustrations
of the model, not data.

**Who owns the theory / how do I cite it?**
Sayan M. (2026).  See the citation block in the repository `README`.
