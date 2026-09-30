"""
Sayan Universal Gradient (SUG) Theory -- interactive Streamlit application.

Run it with::

    streamlit run app.py

or, to test that everything imports cleanly without a browser::

    python -c "import app"

What the app exposes
--------------------
* the central Theta_S operator  |theta_S| = K sqrt(e) / (tau ln x)
* the vacuum destruction radius  R_d = r0 exp(K sqrt(e) / (tau theta_c))
* the energy breaking threshold  E_c  = E0 (tau theta_c ln x / K)^2
* an interactive Plotly 3-D surface of the field (same construction as
  ``sayan_gradient.visualization.plot_surface_3d``, but with the second
  surface axis switchable between source energy and thermal gradient)
* the parameter-free energy ratio of Prediction P2, which contains neither
  the calibration constant K nor the material threshold theta_c
* the single-anchor calibration of K described in the paper

Scientific status
-----------------
SUG is a *proposed, unvalidated* framework.  K is not calibrated to data, so
the numbers below are model output, not measurements.  Nothing in this app is
a prediction about nature until K is fitted to a real anchor event.
"""

from __future__ import annotations

import math
import os
import sys
from typing import Any

import numpy as np

# Make the in-repository package importable even when sayan-gradient has not
# been pip-installed (e.g. `streamlit run app.py` from a fresh clone).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

try:
    from sayan_gradient import (  # noqa: E402
        DEEP_SPACE,
        LABORATORY,
        NUCLEAR_BLAST,
        STELLAR,
        ReferenceScales,
        calibrate_k,
        energy_breaking_threshold,
        parameter_free_energy_ratio,
        theta_s,
        theta_s_gradient,
        theta_s_line_integral,
        vacuum_destruction_radius,
    )
    from sayan_gradient.visualization import plot_surface_3d  # noqa: E402

    IMPORT_ERROR: str | None = None
except ImportError as exc:  # pragma: no cover - user-facing failure path
    IMPORT_ERROR = f"{exc}"
    st.title("Sayan Universal Gradient (SUG) Theory")
    st.error(
        "The `sayan_gradient` package could not be imported.\n\n"
        f"```\n{IMPORT_ERROR}\n```\n\n"
        "Install the dependencies and try again:\n\n"
        "```bash\npip install -r requirements.txt\n"
        "#   ...or install this repository's package in editable mode:\n"
        "pip install -e .\n```"
    )
    st.stop()

try:  # plotly is an optional extra of the package
    import plotly.graph_objects as go
except ImportError as exc:  # pragma: no cover
    go = None
    PLOTLY_ERROR = str(exc)
else:
    PLOTLY_ERROR = None


# ==========================================================================
# Presentation helpers (kept version-tolerant across Streamlit releases)
# ==========================================================================
def render_figure(fig: Any) -> None:
    """Render a Plotly figure across Streamlit API generations."""
    try:
        st.plotly_chart(fig, width="stretch")
    except TypeError:  # Streamlit < 1.49
        try:
            st.plotly_chart(fig, use_container_width=True)
        except TypeError:  # pragma: no cover - very old Streamlit
            st.plotly_chart(fig)


def eng(value: float, unit: str = "") -> str:
    """Format a (possibly astronomically large or small) number for display."""
    if value is None or (isinstance(value, float) and not math.isfinite(value)):
        return "out of floating-point range"
    if value == 0:
        return f"0 {unit}".strip()
    exp = math.floor(math.log10(abs(value)))
    if -3 <= exp < 5:
        return f"{value:,.4g} {unit}".strip()
    mant, ex = f"{value / 10 ** exp:.3f}", int(exp)
    return f"{mant} × 10^{ex} {unit}".strip()


def safe_radius(E_nb: float, delta_T: float, theta_c: float, sc: ReferenceScales) -> tuple[float, float]:
    """Return (R_d, log10 R_d), overflow-safe.

    R_d = r0 * exp(K sqrt(e) / (tau theta_c)) can exceed the float range for
    large sources.  The package's ``vacuum_destruction_radius`` is used for the
    ordinary case; when it overflows we report log10 R_d rather than raising,
    which is the more informative answer anyway.
    """
    e = E_nb / sc.E0
    tau = delta_T / sc.T0
    exponent = sc.K * math.sqrt(e) / (tau * theta_c)
    log10_rd = math.log10(sc.r0) + exponent / math.log(10.0)
    if log10_rd > 308.0:
        return math.inf, log10_rd
    try:
        return float(np.asarray(vacuum_destruction_radius(E_nb, theta_c, delta_T, scales=sc))), log10_rd
    except (OverflowError, ValueError):
        return sc.r0 * math.exp(exponent), log10_rd


# ==========================================================================
# Figure builders (cached: they are pure functions of their arguments)
# ==========================================================================
@st.cache_data(show_spinner=False)
def decay_figure(
    E_nb: float,
    delta_T: float,
    scales: tuple[float, float, float, float],
    x_max: float,
    n: int = 400,
) -> Any:
    """|theta_S| against distance for the chosen source and a few larger ones."""
    E0, T0, r0, K = scales
    sc = ReferenceScales(E0=E0, T0=T0, r0=r0, K=K)
    xs = np.linspace(1.05, max(x_max, 1.2), n)
    e_ref = E_nb / E0
    fig = go.Figure()
    for mult, style in ((1.0, None), (2.0, "dash"), (0.5, "dot")):
        e = e_ref * mult
        with np.errstate(divide="ignore", invalid="ignore"):
            y = sc.K * np.sqrt(e) / ((delta_T / T0) * np.log(xs))
        fig.add_trace(
            go.Scatter(
                x=xs,
                y=y,
                mode="lines",
                name=f"e = {e:.3g}" + (" (selected)" if style is None else ""),
                line=dict(width=3 if style is None else 1.6, dash=style),
            )
        )
    fig.update_layout(
        title=f"Field decay with distance  (tau = {delta_T / T0:.3g})",
        xaxis_title="dimensionless distance  x = r / r0",
        yaxis_title="|theta_S|",
        template="plotly_white",
        hovermode="closest",
    )
    return fig


@st.cache_data(show_spinner=False)
def surface_figure(
    second_axis: str,
    other_value: float,
    scales: tuple[float, float, float, float],
    x_range: tuple[float, float],
    sec_range: tuple[float, float],
    grid: int = 70,
    log_x: bool = True,
    log_z: bool = True,
) -> Any:
    """3-D field surface, same construction as ``visualization.plot_surface_3d``.

    ``second_axis='e'``  -> surface over (distance, source energy)
    ``second_axis='tau'`` -> the package's own (distance, thermal gradient) surface
    """
    E0, T0, r0, K = scales
    sc = ReferenceScales(E0=E0, T0=T0, r0=r0, K=K)
    x_lo, x_hi = x_range
    s_lo, s_hi = sec_range
    x_lo = max(x_lo, 1.001)

    if log_x:
        xs = np.logspace(np.log10(x_lo), np.log10(x_hi), grid)
    else:
        xs = np.linspace(x_lo, x_hi, grid)
    secs = np.linspace(s_lo, s_hi, grid)
    SEC, X = np.meshgrid(secs, xs)

    if second_axis == "e":
        e, tau = np.clip(SEC, 1e-9, None), other_value
        sec_label = "source energy  e = E_nb / E0"
        title = f"Field surface over distance and energy  (tau = {tau:.3g})"
    else:
        e, tau = other_value, np.clip(SEC, 1e-9, None)
        sec_label = "thermal gradient  tau = Delta_T / T0"
        title = f"Field surface over distance and thermal gradient  (e = {e:.3g})"

    with np.errstate(divide="ignore", invalid="ignore"):
        Z = sc.K * np.sqrt(e) / (tau * np.log(X))
    Zc = np.clip(Z, 1e-12, None)
    Zshow = np.log10(Zc) if log_z else Zc

    fig = go.Figure(
        data=[
            go.Surface(
                x=xs,
                y=secs,
                z=Zshow.T,
                colorscale="Viridis",
                colorbar=dict(title="log10 |θ_S|" if log_z else "|θ_S|"),
                hovertemplate=(
                    "x = %{x:.3f}<br>" + sec_label.split("  ")[0] + " = %{y:.3g}"
                    + "<br>value = %{z:.3f}<extra></extra>"
                ),
            )
        ]
    )
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title="distance  x = r / r0",
            yaxis_title=sec_label,
            zaxis_title="log10 |theta_S|" if log_z else "|theta_S|",
        ),
        template="plotly_white",
    )
    return fig


@st.cache_data(show_spinner=False)
def ratio_figure(x1: float, x2: float) -> Any:
    """SUG (logarithmic) versus inverse-square range-extension cost."""
    xs = np.logspace(np.log10(max(x1, 1.0)), np.log10(x2), 60)
    sug = (np.log(xs) / np.log(x1)) ** 2
    inv_sq = (xs / x1) ** 4  # a 1/r^2 field needs E ~ x^4
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=xs, y=sug, name="SUG: E2/E1 = (ln x2 / ln x1)^2",
                   line=dict(width=3))
    )
    fig.add_trace(
        go.Scatter(x=xs, y=inv_sq, name="inverse-square field: E2/E1 = (x2/x1)^4",
                   line=dict(width=2, dash="dash"))
    )
    fig.add_vline(x=x2, line_dash="dot", line_color="grey")
    fig.update_layout(
        title="Cost of extending the destruction threshold (normalised to E1 = 1)",
        xaxis_title="dimensionless distance  x = r / r0",
        yaxis_title="required energy ratio  E2 / E1",
        yaxis_type="log",
        template="plotly_white",
    )
    return fig


# ==========================================================================
# Sidebar
# ==========================================================================

with st.sidebar:
    st.markdown("### Reference scales")
    st.caption("The units of the theory. Changing them rescales e, tau and x "
               "simultaneously and leaves every prediction invariant.")

    presets = {
        "Unit / laboratory (E0=T0=r0=1)": NUCLEAR_BLAST,
        "Laboratory  (1e6, 100, 1)": LABORATORY,
        "Stellar  (1e26, 1e4, 1e11)": STELLAR,
        "Deep space  (1e20, 2.7255, 1e9)": DEEP_SPACE,
    }
    preset_name = st.selectbox("Preset", list(presets), index=0)
    preset = presets[preset_name]

    with st.expander("Fine-tune (optional)"):
        E0 = st.number_input("Reference energy  E0", min_value=1e-30, value=float(preset.E0),
                             format="%.6g", help="Same units as E_nb.")
        T0 = st.number_input("Reference gradient  T0", min_value=1e-30, value=float(preset.T0),
                             format="%.6g", help="Same units as Delta_T.")
        r0 = st.number_input("Reference length  r0", min_value=1e-30, value=float(preset.r0),
                             format="%.6g", help="Same units as r. The field is undefined for r <= r0.")
        K = st.number_input("Calibration constant  K", min_value=0.0, value=float(preset.K),
                            format="%.6g", help="Sole free parameter. K = 1 is a placeholder, not a fit.")

    st.markdown("### Source and geometry")
    E_nb = st.number_input(
        "Released energy  E_nb", min_value=1e-30, value=1.0e6, format="%.6g",
        help="Energy released by the source, in the same units as E0.",
    )
    delta_T = st.number_input(
        "Thermal gradient  Delta_T", min_value=1e-30, value=100.0, format="%.6g",
        help="Local temperature contrast. Postulate IV: a larger gradient damps the field.",
    )
    r = st.number_input(
        "Distance  r", min_value=1e-30, value=10.0, format="%.6g",
        help="Distance from the source. Must exceed r0: x = 1 is a singularity.",
    )

    st.markdown("### Material threshold")
    theta_c = st.number_input(
        "Critical threshold  theta_c", min_value=1e-30, value=1.0, format="%.6g",
        help="Field value above which matter no longer holds its bound state.",
    )

    st.markdown("### Display")
    log_y = st.checkbox("Logarithmic field axis", value=True)

scales_obj = ReferenceScales(E0=E0, T0=T0, r0=r0, K=K)
scales_tuple = (float(E0), float(T0), float(r0), float(K))
e_dimless = E_nb / E0
tau_dimless = delta_T / T0
x_dimless = r / r0
in_core = x_dimless <= 1.0


# ==========================================================================
# Header
# ==========================================================================
st.title("Sayan Universal Gradient (SUG) Theory -- interactive explorer")
st.caption(
    "A proposed, unvalidated framework. Outputs are model values, not measurements. "
    "Repository: github.com/sayan9168/Sayan-Universal-Gradient-Theory  |  "
    "DOI: 10.5281/zenodo.22723906  |  `pip install sayan-gradient`"
)
st.info(
    "**K has not been calibrated to data.** Until one anchor event fixes K, SUG "
    "predicts *shapes and ratios* (notably Prediction P2), not absolute values. "
    "This app lets you explore those shapes; it does not validate them."
)

tab_field, tab_surface, tab_p2, tab_calib, tab_about = st.tabs(
    ["Θ_S field & limits", "3D field surface", "P2 parameter-free ratio",
     "Calibration of K", "About"]
)

if PLOTLY_ERROR is not None:
    st.warning(f"Plotly is not installed, so interactive figures are disabled: {PLOTLY_ERROR}")


# ==========================================================================
# Tab 1 -- the operator, the destruction radius, the breaking energy
# ==========================================================================
with tab_field:
    st.latex(
        r"\theta_S(x) = K\,\frac{\sqrt{e}}{\tau\,\ln x}, \qquad"
        r"e=\frac{E_{nb}}{E_0},\quad \tau=\frac{\Delta T}{T_0},\quad"
        r"x=\frac{r}{r_0} > 1"
    )

    dim_cols = st.columns(4)
    dim_cols[0].metric("Dimensionless energy  e", eng(e_dimless))
    dim_cols[1].metric("Dimensionless gradient  tau", eng(tau_dimless))
    dim_cols[2].metric("Dimensionless distance  x", eng(x_dimless))
    dim_cols[3].metric("ln x", "undefined" if x_dimless <= 1.0 else f"{math.log(x_dimless):.5f}")

    st.markdown("#### Observables")

    # --- the field -----------------------------------------------------
    if in_core:
        st.error(
            f"**Source-core singularity:** r = {eng(r)} <= r0 = {eng(r0)}, so "
            "x = r/r0 <= 1 and ln x <= 0. The continuum SUG field is *undefined* "
            "here (it diverges as x -> 1+). Pick a distance larger than r0; this "
            "is a stated boundary of the model (open question O3), not a bug."
        )
        theta_val = None
    else:
        theta_val = float(np.asarray(theta_s(E_nb, delta_T, r, scales=scales_obj)))
        # Built by concatenation rather than one f-string: the LaTeX braces
        # and the format braces fight each other inside an f-string.
        st.latex(
            r"\theta_S = " + f"{theta_val:.6g}" + r" \qquad = K\,\frac{\sqrt{"
            + f"{e_dimless:.6g}" + r"}}{" + f"{tau_dimless:.6g}" + r"}\ln("
            + f"{x_dimless:.6g}" + r")}"
        )

    c1, c2, c3 = st.columns(3)
    c1.metric(
        "|theta_S| at r",
        "undefined (x <= 1)" if theta_val is None else f"{theta_val:.6g}",
        help="The central operator. Diverges at x = 1 by construction.",
    )
    R_d, log10_Rd = safe_radius(E_nb, delta_T, theta_c, scales_obj)
    c2.metric(
        "Vacuum destruction radius  R_d",
        eng(R_d) if math.isfinite(R_d) else f"> 10^308  (log10 R_d = {log10_Rd:.4g})",
        delta=f"log10 R_d = {log10_Rd:.4f}",
        delta_color="off",
        help="Radius at which theta_S falls to theta_c. R_d = r0 exp(K sqrt(e)/(tau theta_c)). "
             "It is a property of the source and the material, not of the distance r.",
    )
    c3.metric(
        "Energy breaking threshold  E_c",
        "undefined (r <= r0)" if in_core else eng(energy_breaking_threshold(r, theta_c, delta_T, scales=scales_obj)),
        help="Source energy needed to carry theta_c out to distance r.",
    )

    st.markdown(
        "<div style='font-size:0.85em;color:#666'>R_d depends on E_nb, Delta_T and "
        "theta_c but <b>not</b> on the distance at which you evaluate it -- the "
        "threshold radius is a property of the source and the material, not of r. "
        "E_c is the inverse statement at the chosen r.</div>",
        unsafe_allow_html=True,
    )

    # --- contour integral and gradient ---------------------------------
    st.markdown("#### Related quantities along the same ray")
    g1, g2, g3 = st.columns(3)
    try:
        if in_core:
            raise ValueError("segment must start beyond r0")
        contour = theta_s_line_integral(E_nb, delta_T, r0 * 1.05, r, scales=scales_obj)
        g1.metric("Contour constant  Theta_S(r0*1.05 -> r)", f"{contour:.6g}",
                  help="(K r0 sqrt(e)/tau) [li(x_b) - li(x_a)]; li = Ei(ln x).")
    except (ValueError, OverflowError) as exc:
        g1.metric("Contour constant  Theta_S", "undefined", help=str(exc))
    try:
        if in_core:
            raise ValueError("x <= 1")
        grad = float(np.asarray(theta_s_gradient(E_nb, delta_T, r, scales=scales_obj)))
        g2.metric("Radial gradient  dtheta_S/dr", f"{grad:.6g}",
                  help="-theta_S(r) / (r ln x): the field's local rate of decay.")
    except (ValueError, OverflowError) as exc:
        g2.metric("Radial gradient  dtheta_S/dr", "undefined", help=str(exc))
    if not in_core:
        log_decay_len = r * math.log(x_dimless)
        g3.metric("Logarithmic decay length  r ln x", eng(log_decay_len),
                  help="Diverges as r -> infinity: SUG has no fixed length scale.")
    else:
        g3.metric("Logarithmic decay length", "undefined", help="requires x > 1")

    # --- field decay figure --------------------------------------------
    if go is not None:
        st.markdown("#### Field decay with distance")
        x_max = st.select_slider(
            "Distance axis maximum  x_max",
            options=[2.0, 3.0, 10.0, 30.0, 1e2, 3e2, 1e3, 3e3, 1e4, 1e5, 1e6],
            value=float(min([o for o in [2.0, 3.0, 10.0, 30.0, 1e2, 3e2, 1e3, 3e3, 1e4, 1e5, 1e6]
                             if o >= max(2.0, x_dimless)],
                            key=lambda o: abs(math.log10(o) - math.log10(max(2.0, x_dimless))))),
        )
        fig = decay_figure(E_nb, delta_T, scales_tuple, float(x_max))
        if log_y:
            fig.update_yaxes(type="log")
        render_figure(fig)
        st.caption(
            "All curves fall logarithmically (Postulate P-II). Doubling the energy "
            "raises the field by only sqrt(2) (P-III) -- note the unequal spacing."
        )


# ==========================================================================
# Tab 2 -- 3-D surface
# ==========================================================================
with tab_surface:
    st.markdown(
        "Field magnitude over distance and a second control parameter. This is the "
        "same construction as `sayan_gradient.visualization.plot_surface_3d`; the "
        "second axis is switchable so the surface can be read over *energy* "
        "(the requested view) or over *thermal gradient* (the package default)."
    )
    if go is None:
        st.error("Install plotly to view the 3-D surface: pip install plotly")
    else:
        c1, c2, c3 = st.columns([1.2, 1, 1])
        second_axis = c1.radio("Second axis", ["Source energy  e", "Thermal gradient  tau"], index=0)
        log_x = c2.toggle("Log-spaced x axis", value=True,
                          help="The field varies over decades in x; log spacing resolves "
                               "the near-source structure.")
        log_z = c3.toggle("log10 z-scale", value=True,
                          help="Plot log10|theta_S| when the dynamic range is large.")
        use_package = False
        if second_axis.startswith("Thermal"):
            use_package = st.toggle(
                "Call sayan_gradient.visualization.plot_surface_3d()", value=True,
                help="The package's own (distance x thermal gradient) surface. "
                     "Turn off to apply the log-spaced x / log10 z options.",
            )

        is_energy_axis = second_axis.startswith("Source energy")
        if is_energy_axis:
            other = tau_dimless
            sec_label = "e = E_nb / E0"
            sec_range = (max(1e-6, 0.1 * e_dimless), max(5.0 * e_dimless, 2.0 * e_dimless))
            sec_default = float(e_dimless)
        else:
            other = e_dimless
            sec_label = "tau = Delta_T / T0"
            sec_range = (0.05, max(5.0, 3.0 * tau_dimless))
            sec_default = float(tau_dimless)

        with st.expander("Surface range", expanded=is_energy_axis):
            x_lo = st.number_input("x minimum", min_value=1.0001, value=1.05, format="%.6f")
            x_hi = st.number_input("x maximum", value=float(max(10.0, min(1e4, x_dimless * 2))),
                                   format="%.6g")
            sec_lo = st.number_input(f"{sec_label} minimum", value=float(sec_range[0]), format="%.6g")
            sec_hi = st.number_input(f"{sec_label} maximum", value=float(sec_range[1]), format="%.6g")
            other_val = st.number_input(
                "Fixed value of the other axis",
                value=float(sec_default), format="%.6g",
                help="tau (in the same units as T0) when the surface is over energy; "
                     "e (in the same units as E0) when it is over thermal gradient.",
            )
            if x_hi <= x_lo:
                st.error("x maximum must exceed x minimum.")
            elif sec_hi <= sec_lo:
                st.error(f"{sec_label} maximum must exceed its minimum.")
            elif use_package:
                fig = plot_surface_3d(
                    energy=float(other_val), x_range=(float(x_lo), float(x_hi)),
                    tau_range=(float(sec_lo), float(sec_hi)),
                    grid_size=(70, 70), scales=scales_obj, backend="plotly",
                )
                render_figure(fig)
                st.caption("Rendered by `sayan_gradient.visualization.plot_surface_3d` "
                           "with the selected reference scales.")
            else:
                fig = surface_figure(
                    "e" if is_energy_axis else "tau",
                    float(other_val), scales_tuple,
                    (float(x_lo), float(x_hi)), (float(sec_lo), float(sec_hi)),
                    log_x=log_x, log_z=log_z,
                )
                render_figure(fig)
                st.caption(
                    "Rotate with the mouse. The field diverges towards x = 1+ and falls "
                    "hyperbolically with increasing tau; along the energy axis it rises "
                    "only as sqrt(e) (P-III), which is why the surface flattens."
                )


# ==========================================================================
# Tab 3 -- Prediction P2
# ==========================================================================
with tab_p2:
    st.latex(r"\frac{E_2}{E_1} \;=\; \left(\frac{\ln x_2}{\ln x_1}\right)^{2}")
    st.markdown(
        "**Prediction P2 -- the parameter-free test.** Extending a destruction "
        "threshold from $x_1$ to $x_2$ costs released energy in this ratio. "
        "It contains **no $K$ and no $\\theta_c$**, and no choice of reference "
        "scales, so it can be tested before the theory is calibrated. It is the "
        "cleanest handle SUG offers -- and the easiest to kill."
    )

    c1, c2, c3 = st.columns(3)
    r1 = c1.number_input("Initial distance  r1", min_value=float(r0) * 1.0000001,
                         value=float(r0) * 10.0, format="%.6g",
                         help="In the same units as r0.")
    r2 = c2.number_input("Target distance  r2", min_value=float(r0) * 1.0000001,
                         value=float(r0) * 100.0, format="%.6g",
                         help="In the same units as r0. Must exceed r1.")
    c3.markdown(
        f"<div style='font-size:0.85em;color:#666'>Both distances are in the units of "
        f"<code>r0 = {eng(r0)}</code>, so only the ratio <code>x = r/r0</code> enters "
        f"Eq. (P2).</div>",
        unsafe_allow_html=True,
    )
    x1, x2 = r1 / r0, r2 / r0

    if r2 <= r1:
        st.error("The target distance r2 must exceed the initial distance r1.")
    else:
        ratio = float(np.asarray(parameter_free_energy_ratio(r1, r2, r0)))
        inv_sq = (r2 / r1) ** 4  # a 1/r^2 field requires E ~ x^4
        m1, m2, m3 = st.columns(3)
        m1.metric("x1 = r1 / r0", f"{x1:.6g}")
        m2.metric("x2 = r2 / r0", f"{x2:.6g}")
        m3.metric("P2 energy ratio  E2 / E1", f"{ratio:.6g}",
                  help="Independent of K and theta_c.")
        st.latex(
            rf"\frac{{E_2}}{{E_1}} = \left(\frac{{\ln {x2:.6g}}}{{\ln {x1:.6g}}}\right)^{{2}}"
            rf" = {ratio:.6g}"
        )
        d1, d2 = st.columns(2)
        d1.metric("Same test for an inverse-square field", f"{inv_sq:.6g}",
                  help="If the field fell as 1/r^2, E_c would grow as x^4.")
        d2.metric("SUG asks for this much less energy", f"{inv_sq / ratio:.4g}x",
                  help="Ratio of the two requirements -- the discriminating quantity.")

        if go is not None:
            render_figure(ratio_figure(float(x1), float(x2)))

        st.markdown("#### Cost of successive decades")
        rows = []
        for k in range(0, 8):
            a = 10.0 ** k
            if a < x1:
                continue
            rows.append(
                {
                    "range extension": f"{a:g} -> {10 * a:g}",
                    "x1": a,
                    "x2": 10 * a,
                    "SUG  E2/E1": round(float(parameter_free_energy_ratio(a, 10 * a, 1.0)), 4),
                    "inverse-square  E2/E1": (10.0) ** 4,
                }
            )
        if rows:
            try:
                st.dataframe(rows, width="stretch", hide_index=True)
            except TypeError:  # Streamlit < 1.49
                st.dataframe(rows, use_container_width=True, hide_index=True)
        st.caption(
            "The SUG cost of a fixed multiplicative range extension *decreases* as the "
            "range grows -- the signature of a logarithm. A power-law field instead "
            "demands a constant 10^4 per decade."
        )


# ==========================================================================
# Tab 4 -- calibration
# ==========================================================================
with tab_calib:
    st.markdown("#### One anchor event fixes K")
    st.latex(r"K = \frac{\theta_c\,\tau\,\ln x_c}{\sqrt{e}}")
    c1, c2, c3 = st.columns(3)
    with c1:
        r_obs = st.number_input("Observed threshold radius  R_d", min_value=float(r0) * 1.0000001,
                                value=float(r0) * 10.0, format="%.6g")
        theta_obs = st.number_input("...at threshold  theta_c", min_value=1e-30,
                                    value=float(theta_c), format="%.6g")
    with c2:
        E_anchor = st.number_input("Source energy  E_nb", min_value=1e-30, value=float(E_nb),
                                   format="%.6g", key="anchor_E")
        dT_anchor = st.number_input("Thermal gradient  Delta_T", min_value=1e-30,
                                    value=float(delta_T), format="%.6g", key="anchor_dT")
    with c3:
        st.metric("x_obs = R_d / r0", f"{r_obs / r0:.6g}")
        k_anchor = (theta_obs * (dT_anchor / T0) * math.log(r_obs / r0)) / math.sqrt(E_anchor / E0)
        st.metric("Implied calibration constant  K", f"{k_anchor:.6g}",
                  help="Solves the destruction-radius inversion for K.")
        st.caption("This is a one-parameter fit. It cannot test the framework; "
                   "it only removes the free constant.")
    if k_anchor > 0:
        R_pred, _ = safe_radius(E_anchor, dT_anchor, theta_obs,
                                ReferenceScales(E0=E0, T0=T0, r0=r0, K=k_anchor))
        st.success(f"Round-trip check: with K = {k_anchor:.6g}, the same event gives "
                   f"R_d = {eng(R_pred)} (input was {eng(r_obs)}).")

    st.markdown("#### Many events: weighted least squares")
    st.caption("theta_S = K p with p = sqrt(e)/(tau ln x), so K is linear in the model "
               "and has a closed-form weighted estimator. Enter one event per row; "
               "leave the table empty to skip.")
    try:
        default_rows = [
            {"E_nb": 1.0e6, "Delta_T": 100.0, "r": 10.0, "theta_obs": 0.217, "sigma": 0.02},
            {"E_nb": 4.0e6, "Delta_T": 100.0, "r": 20.0, "theta_obs": 0.212, "sigma": 0.02},
        ]
        edited = st.data_editor(
            default_rows,
            num_rows="dynamic",
            column_config={
                "E_nb": st.column_config.NumberColumn(format="%.6g"),
                "Delta_T": st.column_config.NumberColumn(format="%.6g"),
                "r": st.column_config.NumberColumn(format="%.6g", min_value=0.0),
                "theta_obs": st.column_config.NumberColumn(format="%.6g"),
                "sigma": st.column_config.NumberColumn(format="%.6g", min_value=1e-12),
            },
            key="calib_table",
        )
        if edited and len(edited) > 0:
            try:
                k_fit, k_err = calibrate_k(
                    [row["E_nb"] for row in edited],
                    [row["Delta_T"] for row in edited],
                    [row["r"] for row in edited],
                    [row["theta_obs"] for row in edited],
                    scales=scales_obj,
                )
                p1, p2_ = st.columns(2)
                p1.metric("Weighted-least-squares  K", f"{k_fit:.6g}")
                p2_.metric("Standard error  sigma_K", f"{k_err:.6g}")
                model = [k_fit * math.sqrt(row["E_nb"] / E0) /
                         ((row["Delta_T"] / T0) * math.log(row["r"] / r0)) for row in edited]
                resid = [(row["theta_obs"] - m) / row["sigma"]
                         for row, m in zip(edited, model)]
                chi2 = sum(v * v for v in resid)
                dof = max(len(edited) - 1, 1)
                st.write(f"chi^2 = {chi2:.4g} on {dof} degree(s) of freedom "
                         f"(chi^2/dof = {chi2 / dof:.3g}); a correct model gives ~1.")
            except (ValueError, RuntimeError, ZeroDivisionError) as exc:
                st.warning(f"Calibration skipped: {exc}. Every row needs r > r0, "
                           "E_nb > 0, Delta_T > 0, sigma > 0, and at least one row.")
    except Exception as exc:  # pragma: no cover - very old Streamlit without data_editor
        st.info(f"Editable table unavailable in this Streamlit version ({exc}).")

    st.warning(
        "These rows are placeholders to demonstrate the estimator, not data. "
        "A K fitted to invented points is still uncalibrated -- see the paper's "
        "validation roadmap."
    )


# ==========================================================================
# Tab 5 -- about
# ==========================================================================
with tab_about:
    st.markdown(
        """
#### The framework in one line

A single dimensionless scalar field couples released energy, thermal gradient
and distance, and decays **logarithmically** rather than as an inverse square.

$$\\theta_S(x) = K\\,\\frac{\\sqrt{e}}{\\tau\\,\\ln x}, \\qquad
e=\\frac{E_{nb}}{E_0},\\; \\tau=\\frac{\\Delta T}{T_0},\\; x=\\frac{r}{r_0}$$

#### Derived limits

| Quantity | Expression | Depends on r? |
|---|---|---|
| Field at r | `theta_S = K sqrt(e) / (tau ln x)` | yes |
| Vacuum destruction radius | `R_d = r0 exp(K sqrt(e) / (tau theta_c))` | no |
| Energy breaking threshold | `E_c = E0 (tau theta_c ln x / K)^2` | yes |
| Contour constant | `Theta_S(a->b) = (K r0 sqrt(e)/tau)[li(x_b) - li(x_a)]` | via endpoints |
| Parameter-free ratio (P2) | `E2/E1 = (ln x2 / ln x1)^2` | ratio only |

#### Honest limitations

1. **K is uncalibrated.** Only shapes and ratios are predictive; no absolute
   radius or energy is claimed.
2. **Inverse-square tension.** Logarithmic decay must be reconciled with the
   `1/r^2` spread of radiative flux, or the field must be reinterpreted as
   acting on a derived rather than a raw observable.
3. **Source-core singularity.** The divergence at `x = 1` needs a physical
   prescription for `r0` and a cut-off.
4. **Square-root energy response** is postulated, not derived; the paper gives
   the `E^alpha` generalisation, under which P2 stays parameter-free.
5. **theta_c has no microphysical formula** and must be supplied per material.
6. **No data.** Nothing in this app has been tested against an experiment.

#### Code availability

* Repository -- <https://github.com/sayan9168/Sayan-Universal-Gradient-Theory>
* Archived snapshot (Zenodo) -- <https://doi.org/10.5281/zenodo.22723906>
* PyPI -- `pip install sayan-gradient` (MIT licence, Python >= 3.9)
* Paper source -- `paper/sug_theory_arxiv.tex` (arXiv physics.gen-ph)

SUG is an original, speculative proposal. It has not been peer reviewed and has
not been validated against observation.
"""
    )
