"""Unit tests for WiggleDisplay using synthetic arrays (no SU fixture, no server)."""
import numpy as np

from plotServer.constants.VISUALIZATION import MAX_TRACES_LINE_HAREA
from plotServer.plots.BasicPlot.displays import WiggleDisplay
from plotServer.plots.BasicPlot.transforms import time_sample_instants
from plotServer.plots.shared.plotFactory import plotFactory

DT = 0.004


def _data(num_time_samples=20, num_traces=5, seed=0):
    rng = np.random.default_rng(seed)
    return rng.standard_normal((num_time_samples, num_traces))


def _make(data=None, visible=False):
    data = _data() if data is None else data
    x_positions = np.arange(1, data.shape[1] + 1)
    instants = time_sample_instants(data.shape[0], DT)
    return WiggleDisplay(plotFactory(), data, x_positions, instants, visible=visible)


def test_hidden_by_default_but_sources_populated():
    disp = _make(_data(num_traces=5))
    assert disp.line_renderer.visible is False
    assert disp.fill_renderer.visible is False
    # No empty columns ship even though wiggle starts hidden.
    assert len(disp.line_source.data["xs"]) == 5


def test_toggling_on_right_after_construction_does_not_raise():
    # Regression for the AttributeError crash from the old PlotManager.
    disp = _make(_data(num_traces=5))
    disp.set_visible(True)  # must not raise
    assert disp.line_renderer.visible is True
    assert disp.fill_renderer.visible is True
    assert len(disp.line_source.data["xs"]) == 5
    assert len(disp.fill_source.data["xs"]) == 5


def test_set_visible_off_hides_both():
    disp = _make(visible=True)
    disp.set_visible(False)
    assert disp.line_renderer.visible is False
    assert disp.fill_renderer.visible is False


def test_fill_suppressed_over_threshold_but_lines_kept():
    num_traces = MAX_TRACES_LINE_HAREA + 10
    disp = _make(_data(num_time_samples=5, num_traces=num_traces), visible=True)
    assert len(disp.line_source.data["xs"]) == num_traces
    assert disp.fill_source.data["xs"] == []


def test_fill_present_under_threshold():
    disp = _make(_data(num_traces=4), visible=True)
    assert len(disp.fill_source.data["xs"]) == 4


def test_update_while_visible_rebuilds():
    disp = _make(_data(num_traces=3), visible=True)
    disp.update(_data(num_traces=6, seed=9), np.arange(1, 7), time_sample_instants(20, DT))
    assert len(disp.line_source.data["xs"]) == 6
