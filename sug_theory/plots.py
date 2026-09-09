"""
Figure generation for the SUG framework.

Run from the repository root::

    python -m sug_theory.plots --outdir figures

produces the PNG figures referenced throughout the documentation.
"""

from __future__ import annotations

import argparse
import os

import numpy as np

from .constants import ReferenceScales
from .operators import theta_s, theta_critical_radius, theta_critical_energy


def _new_axes():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7.2, 5.0), dpi=150)
    return fig, ax


def _style(ax, xlabel: str, ylabel: str, title: str):
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.set_facecolor("#fafafa")


def figure_field_decay(outdir: str, sc: ReferenceScales):
    """Fig. 1 -- SUG field magnitude vs dimensionless distance for several energies."""
    fig, ax = _new_axes()
    x = np.linspace(1.05, 12.0, 600)
    tau = 1.0
    for e in (0.5, 1.0, 2.0, 4.0):
        E_nb = e * sc.E0
        delta_T = tau * sc.T0
        r = x * sc.r0
        y = theta_s(E_nb, delta_T, r, scales=sc)
        ax.plot(x, y, lw=2, label=f"e = {e}")
    _style(
        ax,
        "dimensionless distance x = r / r0",
        "SUG field magnitude |θ_S|",
        "SUG field decay with distance (τ = 1)",
    )
    ax.legend(title="source energy (dimensionless)")
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "fig_field_decay.png"))
    ax.cla()
    import matplotlib.pyplot as plt

    plt.close(fig)


def figure_temperature_energy_map(outdir: str, sc: ReferenceScales):
    """Fig. 2 -- heatmap of |θ_S| over a thermal-gradient / distance plane."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7.2, 5.4), dpi=150)
    e = 1.0
    E_nb = e * sc.E0
    taus = np.linspace(0.2, 3.0, 220)
    xs = np.linspace(1.05, 10.0, 240)
    TAU, X = np.meshgrid(taus, xs)
    theta = sc.K * np.sqrt(e) / (TAU * np.log(X))
    im = ax.pcolormesh(X, TAU, theta, shading="auto", cmap="magma")
    cs = ax.contour(X, TAU, theta, levels=8, colors="white", linewidths=0.5, alpha=0.6)
    ax.clabel(cs, inline=True, fontsize=7)
    fig.colorbar(im, ax=ax, label="|θ_S|")
    ax.set_xlabel("dimensionless distance x")
    ax.set_ylabel("dimensionless thermal gradient τ")
    ax.set_title("Thermal–distance energy map (e = 1)")
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "fig_thermal_energy_map.png"))
    plt.close(fig)


def figure_vacuum_destruction_radius(outdir: str, sc: ReferenceScales):
    """Fig. 3 -- vacuum destruction radius vs source energy for thresholds."""
    fig, ax = _new_axes()
    tau = 1.0
    e = np.linspace(0.1, 10.0, 400)
    for thc in (0.2, 0.5, 1.0, 2.0):
        rad = [
            theta_critical_radius(ei * sc.E0, tau * sc.T0, thc, scales=sc) / sc.r0
            for ei in e
        ]
        ax.plot(e, rad, lw=2, label=f"θ_c = {thc}")
    _style(
        ax,
        "dimensionless source energy e",
        "vacuum destruction radius x_d = R_d / r0",
        "Predicted vacuum destruction radius (τ = 1)",
    )
    ax.legend(title="material threshold")
    ax.set_yscale("log")
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "fig_vacuum_destruction_radius.png"))
    ax.cla()
    import matplotlib.pyplot as plt

    plt.close(fig)


def figure_breaking_energy(outdir: str, sc: ReferenceScales):
    """Fig. 4 -- breaking energy vs distance for several thresholds."""
    fig, ax = _new_axes()
    tau = 1.0
    x = np.linspace(1.2, 10.0, 400)
    for thc in (0.5, 1.0, 2.0):
        e_b = [
            theta_critical_energy(xi * sc.r0, tau * sc.T0, thc, scales=sc) / sc.E0
            for xi in x
        ]
        ax.plot(x, e_b, lw=2, label=f"θ_c = {thc}")
    _style(
        ax,
        "dimensionless distance x",
        "breaking energy e_b = E_b / E0",
        "Energy-breaking threshold vs distance (τ = 1)",
    )
    ax.legend(title="material threshold")
    ax.set_yscale("log")
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "fig_breaking_energy.png"))
    ax.cla()
    import matplotlib.pyplot as plt

    plt.close(fig)


def _generate_all(outdir: str) -> list[str]:
    os.makedirs(outdir, exist_ok=True)
    sc = ReferenceScales(E0=1.0, T0=1.0, r0=1.0, K=1.0)
    figure_field_decay(outdir, sc)
    figure_temperature_energy_map(outdir, sc)
    figure_vacuum_destruction_radius(outdir, sc)
    figure_breaking_energy(outdir, sc)
    return sorted(os.listdir(outdir))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate SUG figures.")
    parser.add_argument("--outdir", default="figures", help="output directory")
    args = parser.parse_args()
    files = _generate_all(args.outdir)
    print(f"Wrote {len(files)} figure(s) to '{args.outdir}':")
    for f in files:
        print(f"  - {f}")


if __name__ == "__main__":
    main()
