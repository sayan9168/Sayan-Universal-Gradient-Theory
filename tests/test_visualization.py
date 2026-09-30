"""Unit tests for sayan_gradient.visualization module."""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pytest

from sayan_gradient import ReferenceScales, Source2D
from sayan_gradient.visualization import (
    plot_breaking_energy,
    plot_deep_space_field_2d,
    plot_field_decay,
    plot_surface_3d,
    plot_thermal_energy_map,
    plot_vacuum_destruction_radius,
)

SC = ReferenceScales(E0=1.0, T0=1.0, r0=1.0, K=1.0)


@pytest.mark.parametrize("backend", ["matplotlib", "plotly"])
def test_plot_field_decay(backend):
    fig = plot_field_decay(energies=[1.0, 2.0], tau=1.0, scales=SC, backend=backend)
    if backend == "matplotlib":
        assert isinstance(fig, plt.Figure)
        plt.close(fig)
    else:
        assert isinstance(fig, go.Figure)


@pytest.mark.parametrize("backend", ["matplotlib", "plotly"])
def test_plot_thermal_energy_map(backend):
    fig = plot_thermal_energy_map(energy=1.0, scales=SC, backend=backend, grid_size=(30, 30))
    if backend == "matplotlib":
        assert isinstance(fig, plt.Figure)
        plt.close(fig)
    else:
        assert isinstance(fig, go.Figure)


@pytest.mark.parametrize("backend", ["matplotlib", "plotly"])
def test_plot_vacuum_destruction_radius(backend):
    fig = plot_vacuum_destruction_radius(thresholds=[0.5, 1.0], tau=1.0, scales=SC, backend=backend, num_points=50)
    if backend == "matplotlib":
        assert isinstance(fig, plt.Figure)
        plt.close(fig)
    else:
        assert isinstance(fig, go.Figure)


@pytest.mark.parametrize("backend", ["matplotlib", "plotly"])
def test_plot_breaking_energy(backend):
    fig = plot_breaking_energy(thresholds=[0.5, 1.0], tau=1.0, scales=SC, backend=backend, num_points=50)
    if backend == "matplotlib":
        assert isinstance(fig, plt.Figure)
        plt.close(fig)
    else:
        assert isinstance(fig, go.Figure)


@pytest.mark.parametrize("backend", ["matplotlib", "plotly"])
def test_plot_surface_3d(backend):
    fig = plot_surface_3d(energy=1.0, grid_size=(15, 15), scales=SC, backend=backend)
    if backend == "matplotlib":
        assert isinstance(fig, plt.Figure)
        plt.close(fig)
    else:
        assert isinstance(fig, go.Figure)


@pytest.mark.parametrize("backend", ["matplotlib", "plotly"])
def test_plot_deep_space_field_2d(backend):
    sources = [Source2D(x=0.0, y=0.0, energy=50.0)]
    fig = plot_deep_space_field_2d(sources, grid_res=40, scales=SC, backend=backend)
    if backend == "matplotlib":
        assert isinstance(fig, plt.Figure)
        plt.close(fig)
    else:
        assert isinstance(fig, go.Figure)
