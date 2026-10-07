# Frequently Asked Questions

This page is a quick guide to the Sayan Universal Gradient (SUG) proposal and
its software. For the detailed derivations, see
[`formal_framework.md`](formal_framework.md); for caveats and unresolved work,
see [`open_questions.md`](open_questions.md).

> **Scientific status:** SUG is a proposed framework. It has not been
> peer-reviewed or validated by experiment or observation. Equations and
> figures in this repository describe the model; they are not evidence that its
> physical claims are true.

## What does SUG propose?

SUG proposes a dimensionless scalar field, written `θ_S`, that couples a
source's released energy, a thermal-gradient input, and distance from the
source. Its central relation is

```text
θ_S(x) = K √e / (τ ln x),    x > 1
```

where `e = E_nb / E_0` is dimensionless source energy, `τ = ΔT / T_0` is the
dimensionless thermal input, `x = r / r_0` is dimensionless distance, and `K`
is a dimensionless calibration constant. The proposed dependencies are
square-root growth with energy, inverse dependence on `τ`, and logarithmic
decay with distance.

## Is SUG an established law of physics?

No. It is a speculative proposal, not a confirmed physical law. It has not yet
been validated against data, and its parameters and physical interpretation
need further work. See [`open_questions.md`](open_questions.md) for the known
limitations and [`predictions.md`](predictions.md) for proposed tests.

## What do the symbols and reference scales mean?

- `E_nb` is the source energy used by the model and `E_0` is its reference
  energy scale.
- `ΔT` is the model's thermal-gradient or temperature-contrast input and
  `T_0` is its reference temperature scale. Its operational definition for a
  real measurement remains an open question.
- `r` is radial distance and `r_0` is the reference length scale. The ratio
  `x = r / r_0` must be greater than one for the stated field domain.
- `K` is a dimensionless calibration constant. It is not established by the
  equations alone.

The ratios make the logarithm dimensionless and make `θ_S` dimensionless. The
reference scales must be stated when interpreting an application; they are
not universal measured constants supplied by the theory.

## Why is the field only defined for `x > 1`?

At `x = 1`, `ln x` is zero and the expression is singular. SUG treats this as
the inner boundary of its continuum field description (the proposed source
core). The formulation in this repository does not prescribe a physical
regularization at that boundary. Although `ln x` can be evaluated for some
other positive `x`, the stated model domain is specifically `x > 1`.

## Does `θ_S` represent temperature or measured energy density?

Not by itself. It is a dimensionless model quantity. Connecting it to a
specific, measurable physical observable is an unresolved part of the
proposal; do not interpret `θ_S` as a temperature, a radiative flux, or a
measured material property without a separate, justified mapping.

## What are the destruction radius and breaking energy?

Given a chosen critical threshold `θ_c`, SUG algebraically solves for the
radius at which the proposed field reaches that threshold and for the source
energy needed to reach it at a specified distance:

```text
R_c = r_0 exp(K √e / (τ θ_c))
E_c = E_0 (τ θ_c ln x / K)²
```

These are consequences of the model's equation, not validated predictions for
real materials. Absolute numerical predictions require defensible reference
scales, a calibrated `K`, and a physically meaningful threshold `θ_c`.

## What is the parameter-free energy-ratio prediction?

For fixed thermal input and threshold, the model gives

```text
E_2 / E_1 = (ln x_2 / ln x_1)²
```

The ratio cancels `K` and `θ_c`, making it a proposed shape test. It still
requires a clearly defined observable and controlled, comparable conditions.
It has not yet been confirmed by data. The assumptions and proposed
falsification route are detailed as prediction P2 in
[`predictions.md`](predictions.md).

## What does the path-integrated operator calculate?

For a radial path with `x_b > x_a > 1`, the path constant in dimensionless
length units (`dx = dr / r_0`) is a difference of logarithmic integrals:

```text
Θ_S^(x)(a → b) = (K √e / τ) [li(x_b) − li(x_a)]
```

For an integral with physical path-length element `dr`, multiply the right-hand
side by `r_0`. The package's `theta_s_line_integral` returns the dimensionless
path constant. This is a radial line integral over the stated interval; it
should not be confused with an arbitrary closed-loop integral, and the path
and its limits must be specified.

## Why does SUG use logarithmic decay instead of inverse-square decay?

Logarithmic decay is a defining postulate of SUG, not a result derived from
radiation transport. It is in tension with the familiar inverse-square
spreading of radiative intensity in three spatial dimensions. Whether SUG
refers to a distinct effective observable, and how it can coexist with energy
conservation and established physics, remain open questions; see
[`open_questions.md`](open_questions.md#o2--tension-with-the-inverse-square-law).

## Does the Python package prove the theory?

No. The software implements the stated equations and tests mathematical and
numerical relationships in that implementation. Passing tests establishes
neither that the postulates describe nature nor that the model's outputs match
real-world observations. Repository figures are illustrations of model
calculations, not experimental measurements.

## How should I cite or contribute?

Citation metadata is provided in the repository's [`CITATION.cff`](../CITATION.cff).
The project DOI is [10.5281/zenodo.22723745](https://doi.org/10.5281/zenodo.22723745).
For contributions, see [`CONTRIBUTING.md`](../CONTRIBUTING.md). Use the theory
discussion issue template for questions about assumptions, derivations, or
possible tests.
