"""Unit tests for ImageDisplay using synthetic arrays (no SU fixture, no server).

ImageDisplay attaches to a throwaway figure and takes prepared NumPy data, so
its rendering behavior is testable in isolation.
"""
import numpy as np
import pytest

from plotServer.plots.BasicPlot.displays import ImageDisplay
from plotServer.plots.BasicPlot.transforms import image_x_extent, time_sample_instants
from plotServer.plots.shared.colormaps import getColormap
from plotServer.plots.shared.plotFactory import plotFactory

DT = 0.004


def _data(num_time_samples=20, num_traces=5, seed=0):
    rng = np.random.default_rng(seed)
    return rng.standard_normal((num_time_samples, num_traces))


def _instants(num_time_samples=20):
    return time_sample_instants(num_time_samples, DT)


def _make(data=None, x_positions=None, visible=True):
    data = _data() if data is None else data
    if x_positions is None:
        x_positions = np.arange(1, data.shape[1] + 1)
    return ImageDisplay(
        plotFactory(), data, x_positions, _instants(data.shape[0]), visible=visible
    )


def test_visible_by_default():
    assert _make().renderer.visible is True


def test_source_holds_data():
    data = _data()
    assert np.array_equal(_make(data).source.data["image"][0], data)


def test_glyph_positioned_from_offsets():
    x_positions = np.array([10.0, 20.0, 30.0, 40.0])
    disp = _make(_data(num_traces=4), x_positions=x_positions)
    expected_x, expected_dw = image_x_extent(x_positions)
    assert disp.renderer.glyph.x == pytest.approx(expected_x)
    assert disp.renderer.glyph.dw == pytest.approx(expected_dw)


def test_set_visible():
    disp = _make()
    disp.set_visible(False)
    assert disp.renderer.visible is False


def test_set_palette():
    disp = _make()
    disp.set_palette(getColormap("red_black"))
    assert disp.renderer.glyph.color_mapper.palette == getColormap("red_black")


def test_update_changes_source_and_reposition():
    disp = _make(_data(num_traces=4))
    new_data = _data(num_traces=6, seed=7)
    new_x = np.arange(1, 7)
    disp.update(new_data, new_x, _instants())
    assert np.array_equal(disp.source.data["image"][0], new_data)
    expected_x, expected_dw = image_x_extent(new_x)
    assert disp.renderer.glyph.x == pytest.approx(expected_x)
    assert disp.renderer.glyph.dw == pytest.approx(expected_dw)
