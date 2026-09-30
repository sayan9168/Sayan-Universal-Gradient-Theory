"""Visualization tools for Sayan Universal Gradient Theory.

Supports publication-quality static figures with Matplotlib and interactive
visualizations with Plotly:
- Radial field decay curves (:func:`plot_field_decay`)
- 2D Thermal-distance energy contour maps (:func:`plot_thermal_energy_map`)
- Vacuum destruction radius limits (:func:`plot_vacuum_destruction_radius`)
- Breaking energy threshold scaling (:func:`plot_breaking_energy`)
- 3D interactive field surface (:func:`plot_surface_3d`)
- 2D deep space multi-source field map (:func:`plot_deep_space_field_2d`)
"""

from __future__ import annotations

from typing import Any, Literal, Optional, Sequence, Union

import numpy as np

from .core import ArrayLike, ReferenceScales
from .operators import (
    Source2D,
    spatial_field_2d,
    theta_critical_energy,
    theta_critical_radius,
    theta_s,
)


def _check_matplotlib():
    try:
        import matplotlib.pyplot as plt
        return plt
    except ImportError as exc:
        raise ImportError(
            "Matplotlib is required for static plots. Install with: pip install matplotlib"
        ) from exc


def _check_plotly():
    try:
        import plotly.graph_objects as go
        return go
    except ImportError as exc:
        raise ImportError(
            "Plotly is required for interactive plots. Install with: pip install plotly"
        ) from exc


def plot_field_decay(
    energies: Sequence[float] = (0.5, 1.0, 2.0, 4.0),
    tau: float = 1.0,
    x_range: tuple[float, float] = (1.05, 12.0),
    num_points: int = 500,
    scales: ReferenceScales | None = None,
    backend: Literal["matplotlib", "plotly"] = "matplotlib",
    title: str = "SUG Field Decay with Distance",
) -> Any:
    """Plot SUG field magnitude |θ_S| vs dimensionless distance for different energies.

    Parameters
    ----------
    energies : Sequence of float
        Dimensionless energies e = E_nb / E0.
    tau : float, default 1.0
        Dimensionless thermal gradient tau = Delta_T / T0.
    x_range : tuple of (float, float), default (1.05, 12.0)
        Range of dimensionless distance x = r / r0.
    num_points : int, default 500
        Number of grid points.
    scales : ReferenceScales, optional
        Reference scales.
    backend : {"matplotlib", "plotly"}, default "matplotlib"
        Plotting backend.
    title : str
        Figure title.

    Returns
    -------
    matplotlib.figure.Figure or plotly.graph_objects.Figure
    """
    sc = scales if scales is not None else ReferenceScales()
    xs = np.linspace(x_range[0], x_range[1], num_points)

    if backend == "matplotlib":
        plt = _check_matplotlib()
        fig, ax = plt.subplots(figsize=(7.5, 5.0), dpi=150)
        ax.set_facecolor("#fafafa")

        for e in energies:
            r = xs * sc.r0
            E_nb = e * sc.E0
            dT = tau * sc.T0
            y = theta_s(E_nb, dT, r, scales=sc)
            ax.plot(xs, y, lw=2.2, label=f"e = {e:.1f}")

        ax.set_xlabel("Dimensionless distance $x = r / r_0$", fontsize=11)
        ax.set_ylabel("Field magnitude $|\\theta_S|$", fontsize=11)
        ax.set_title(f"{title} ($\\tau = {tau}$)", fontsize=12, fontweight="bold")
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend(title="Source Energy $e$")
        fig.tight_layout()
        return fig

    if backend == "plotly":
        go = _check_plotly()
        fig = go.Figure()
        for e in energies:
            r = xs * sc.r0
            E_nb = e * sc.E0
            dT = tau * sc.T0
            y = theta_s(E_nb, dT, r, scales=sc)
            fig.add_trace(go.Scatter(x=xs, y=y, mode="lines", name=f"e = {e:.1f}", line=dict(width=2.5)))

        fig.update_layout(
            title=f"{title} (τ = {tau})",
            xaxis_title="Dimensionless distance x = r / r0",
            yaxis_title="Field magnitude |θ_S|",
            template="plotly_white",
        )
        return fig

    raise ValueError(f"Unknown backend '{backend}'. Supported: 'matplotlib', 'plotly'.")


def plot_thermal_energy_map(
    energy: float = 1.0,
    x_range: tuple[float, float] = (1.05, 10.0),
    tau_range: tuple[float, float] = (0.2, 3.0),
    grid_size: tuple[int, int] = (200, 200),
    scales: ReferenceScales | None = None,
    backend: Literal["matplotlib", "plotly"] = "matplotlib",
    cmap: str = "magma",
) -> Any:
    """Plot 2D heatmap/contours of |θ_S| over the (thermal gradient, distance) plane.

    Parameters
    ----------
    energy : float, default 1.0
        Dimensionless source energy e = E_nb / E0.
    x_range : tuple of (float, float), default (1.05, 10.0)
        Range of dimensionless distance x.
    tau_range : tuple of (float, float), default (0.2, 3.0)
        Range of dimensionless thermal gradient tau.
    grid_size : tuple of (int, int), default (200, 200)
        Mesh resolution (nx, ntau).
    scales : ReferenceScales, optional
        Reference scales.
    backend : {"matplotlib", "plotly"}, default "matplotlib"
        Plotting backend.
    cmap : str, default "magma"
        Colormap name.

    Returns
    -------
    matplotlib.figure.Figure or plotly.graph_objects.Figure
    """
    sc = scales if scales is not None else ReferenceScales()
    xs = np.linspace(x_range[0], x_range[1], grid_size[0])
    taus = np.linspace(tau_range[0], tau_range[1], grid_size[1])
    TAU, X = np.meshgrid(taus, xs)

    # Compute theta_S: K * sqrt(e) / (tau * ln(x))
    THETA = sc.K * np.sqrt(energy) / (TAU * np.log(X))

    if backend == "matplotlib":
        plt = _check_matplotlib()
        fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=150)
        im = ax.pcolormesh(X, TAU, THETA, shading="auto", cmap=cmap)
        cs = ax.contour(X, TAU, THETA, levels=10, colors="white", linewidths=0.7, alpha=0.6)
        ax.clabel(cs, inline=True, fontsize=8, fmt="%.2f")
        cbar = fig.colorbar(im, ax=ax)
        cbar.set_label("Field magnitude $|\\theta_S|$", fontsize=11)
        ax.set_xlabel("Dimensionless distance $x = r / r_0$", fontsize=11)
        ax.set_ylabel("Dimensionless thermal gradient $\\tau = \\Delta T / T_0$", fontsize=11)
        ax.set_title(f"Thermal–Distance Energy Map ($e = {energy:.1f}$)", fontsize=12, fontweight="bold")
        fig.tight_layout()
        return fig

    if backend == "plotly":
        go = _check_plotly()
        fig = go.Figure(
            data=go.Contour(
                z=THETA.T,
                x=xs,
                y=taus,
                colorscale="Magma",
                contours=dict(showlabels=True, labelfont=dict(size=11, color="white")),
                colorbar=dict(title="|θ_S|"),
            )
        )
        fig.update_layout(
            title=f"Thermal–Distance Energy Map (e = {energy:.1f})",
            xaxis_title="Dimensionless distance x = r / r0",
            yaxis_title="Dimensionless thermal gradient τ = ΔT / T0",
            template="plotly_white",
        )
        return fig

    raise ValueError(f"Unknown backend '{backend}'. Supported: 'matplotlib', 'plotly'.")


def plot_vacuum_destruction_radius(
    thresholds: Sequence[float] = (0.2, 0.5, 1.0, 2.0),
    tau: float = 1.0,
    e_range: tuple[float, float] = (0.1, 10.0),
    num_points: int = 400,
    scales: ReferenceScales | None = None,
    backend: Literal["matplotlib", "plotly"] = "matplotlib",
) -> Any:
    """Plot predicted vacuum destruction radius vs dimensionless source energy.

    Demonstrates Postulate P1: log(R_c) is strictly linear in sqrt(e).
    """
    sc = scales if scales is not None else ReferenceScales()
    es = np.linspace(e_range[0], e_range[1], num_points)

    if backend == "matplotlib":
        plt = _check_matplotlib()
        fig, ax = plt.subplots(figsize=(7.5, 5.0), dpi=150)
        ax.set_facecolor("#fafafa")

        for thc in thresholds:
            rads = [
                theta_critical_radius(ei * sc.E0, tau * sc.T0, thc, scales=sc) / sc.r0
                for ei in es
            ]
            ax.plot(es, rads, lw=2.2, label=f"$\\theta_c = {thc}$")

        ax.set_yscale("log")
        ax.set_xlabel("Dimensionless source energy $e = E_{nb} / E_0$", fontsize=11)
        ax.set_ylabel("Destruction radius $x_c = R_c / r_0$ (log scale)", fontsize=11)
        ax.set_title(f"Predicted Vacuum Destruction Limits ($\\tau = {tau}$)", fontsize=12, fontweight="bold")
        ax.grid(True, which="both", linestyle="--", alpha=0.35)
        ax.legend(title="Threshold $\\theta_c$")
        fig.tight_layout()
        return fig

    if backend == "plotly":
        go = _check_plotly()
        fig = go.Figure()
        for thc in thresholds:
            rads = [
                theta_critical_radius(ei * sc.E0, tau * sc.T0, thc, scales=sc) / sc.r0
                for ei in es
            ]
            fig.add_trace(go.Scatter(x=es, y=rads, mode="lines", name=f"θ_c = {thc}", line=dict(width=2.5)))

        fig.update_layout(
            title=f"Predicted Vacuum Destruction Limits (τ = {tau})",
            xaxis_title="Dimensionless source energy e = E_nb / E0",
            yaxis_title="Destruction radius x_c = R_c / r0",
            yaxis_type="log",
            template="plotly_white",
        )
        return fig

    raise ValueError(f"Unknown backend '{backend}'. Supported: 'matplotlib', 'plotly'.")


def plot_breaking_energy(
    thresholds: Sequence[float] = (0.5, 1.0, 2.0),
    tau: float = 1.0,
    x_range: tuple[float, float] = (1.2, 10.0),
    num_points: int = 400,
    scales: ReferenceScales | None = None,
    backend: Literal["matplotlib", "plotly"] = "matplotlib",
) -> Any:
    """Plot breaking energy threshold vs distance."""
    sc = scales if scales is not None else ReferenceScales()
    xs = np.linspace(x_range[0], x_range[1], num_points)

    if backend == "matplotlib":
        plt = _check_matplotlib()
        fig, ax = plt.subplots(figsize=(7.5, 5.0), dpi=150)
        ax.set_facecolor("#fafafa")

        for thc in thresholds:
            ebs = [
                theta_critical_energy(xi * sc.r0, tau * sc.T0, thc, scales=sc) / sc.E0
                for xi in xs
            ]
            ax.plot(xs, ebs, lw=2.2, label=f"$\\theta_c = {thc}$")

        ax.set_yscale("log")
        ax.set_xlabel("Dimensionless distance $x = r / r_0$", fontsize=11)
        ax.set_ylabel("Breaking energy $e_b = E_b / E_0$ (log scale)", fontsize=11)
        ax.set_title(f"Energy-Breaking Threshold vs Distance ($\\tau = {tau}$)", fontsize=12, fontweight="bold")
        ax.grid(True, which="both", linestyle="--", alpha=0.35)
        ax.legend(title="Threshold $\\theta_c$")
        fig.tight_layout()
        return fig

    if backend == "plotly":
        go = _check_plotly()
        fig = go.Figure()
        for thc in thresholds:
            ebs = [
                theta_critical_energy(xi * sc.r0, tau * sc.T0, thc, scales=sc) / sc.E0
                for xi in xs
            ]
            fig.add_trace(go.Scatter(x=xs, y=ebs, mode="lines", name=f"θ_c = {thc}", line=dict(width=2.5)))

        fig.update_layout(
            title=f"Energy-Breaking Threshold vs Distance (τ = {tau})",
            xaxis_title="Dimensionless distance x = r / r0",
            yaxis_title="Breaking energy e_b = E_b / E0",
            yaxis_type="log",
            template="plotly_white",
        )
        return fig

    raise ValueError(f"Unknown backend '{backend}'. Supported: 'matplotlib', 'plotly'.")


def plot_surface_3d(
    energy: float = 1.0,
    x_range: tuple[float, float] = (1.1, 10.0),
    tau_range: tuple[float, float] = (0.2, 3.0),
    grid_size: tuple[int, int] = (60, 60),
    scales: ReferenceScales | None = None,
    backend: Literal["plotly", "matplotlib"] = "plotly",
) -> Any:
    """Generate interactive 3D surface plot of the SUG field."""
    sc = scales if scales is not None else ReferenceScales()
    xs = np.linspace(x_range[0], x_range[1], grid_size[0])
    taus = np.linspace(tau_range[0], tau_range[1], grid_size[1])
    TAU, X = np.meshgrid(taus, xs)
    THETA = sc.K * np.sqrt(energy) / (TAU * np.log(X))

    if backend == "plotly":
        go = _check_plotly()
        fig = go.Figure(
            data=[
                go.Surface(
                    z=THETA.T,
                    x=xs,
                    y=taus,
                    colorscale="Viridis",
                    colorbar=dict(title="|θ_S|"),
                )
            ]
        )
        fig.update_layout(
            title=f"3D SUG Field Surface (e = {energy:.1f})",
            scene=dict(
                xaxis_title="Distance x = r / r0",
                yaxis_title="Thermal Gradient τ = ΔT / T0",
                zaxis_title="Field Magnitude |θ_S|",
            ),
            template="plotly_white",
        )
        return fig

    if backend == "matplotlib":
        plt = _check_matplotlib()
        from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

        fig = plt.figure(figsize=(9, 6), dpi=150)
        ax = fig.add_subplot(111, projection="3d")
        surf = ax.plot_surface(X, TAU, THETA, cmap="viridis", edgecolor="none", alpha=0.9)
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label="$|\\theta_S|$")
        ax.set_xlabel("Distance $x$")
        ax.set_ylabel("Thermal gradient $\\tau$")
        ax.set_zlabel("Field $|\\theta_S|$")
        ax.set_title(f"3D SUG Field Surface ($e = {energy:.1f}$)")
        return fig

    raise ValueError(f"Unknown backend '{backend}'.")


def plot_deep_space_field_2d(
    sources: Sequence[Source2D | tuple[float, float, float]],
    x_bounds: tuple[float, float] = (-20.0, 20.0),
    y_bounds: tuple[float, float] = (-20.0, 20.0),
    grid_res: int = 250,
    delta_T: float = 1.0,
    scales: ReferenceScales | None = None,
    backend: Literal["matplotlib", "plotly"] = "matplotlib",
    title: str = "Deep Space SUG Field Distribution",
) -> Any:
    """Plot 2D spatial map of multiple high-energy sources in deep space."""
    sc = scales if scales is not None else ReferenceScales()
    xs = np.linspace(x_bounds[0], x_bounds[1], grid_res)
    ys = np.linspace(y_bounds[0], y_bounds[1], grid_res)
    X, Y = np.meshgrid(xs, ys)

    field = spatial_field_2d(sources, X, Y, delta_T=delta_T, scales=sc)

    src_xs = [s.x if isinstance(s, Source2D) else s[0] for s in sources]
    src_ys = [s.y if isinstance(s, Source2D) else s[1] for s in sources]
    src_es = [s.energy if isinstance(s, Source2D) else s[2] for s in sources]

    if backend == "matplotlib":
        plt = _check_matplotlib()
        fig, ax = plt.subplots(figsize=(8, 6.5), dpi=150)
        im = ax.pcolormesh(X, Y, np.log10(np.clip(field, 1e-4, None)), shading="auto", cmap="inferno")
        cbar = fig.colorbar(im, ax=ax)
        cbar.set_label("$\\log_{10}(|\\theta_S|)$", fontsize=11)

        # Plot source markers
        ax.scatter(src_xs, src_ys, color="cyan", edgecolors="white", s=80, marker="*", label="Sources", zorder=5)
        for i, (sx, sy, se) in enumerate(zip(src_xs, src_ys, src_es)):
            ax.annotate(f"S{i+1}: {se:.0f}E0", (sx + 0.5, sy + 0.5), color="white", fontsize=9, weight="bold")

        ax.set_xlabel("X (r0 units)", fontsize=11)
        ax.set_ylabel("Y (r0 units)", fontsize=11)
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.legend(loc="upper right")
        fig.tight_layout()
        return fig

    if backend == "plotly":
        go = _check_plotly()
        fig = go.Figure(
            data=go.Heatmap(
                z=np.log10(np.clip(field, 1e-4, None)),
                x=xs,
                y=ys,
                colorscale="Inferno",
                colorbar=dict(title="log10(|θ_S|)"),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=src_xs,
                y=src_ys,
                mode="markers+text",
                text=[f"S{i+1} ({se}E0)" for i, se in enumerate(src_es)],
                textposition="top center",
                marker=dict(symbol="star", size=14, color="cyan", line=dict(color="white", width=1)),
                name="Sources",
            )
        )
        fig.update_layout(
            title=title,
            xaxis_title="X (r0 units)",
            yaxis_title="Y (r0 units)",
            template="plotly_white",
        )
        return fig

    raise ValueError(f"Unknown backend '{backend}'.")
