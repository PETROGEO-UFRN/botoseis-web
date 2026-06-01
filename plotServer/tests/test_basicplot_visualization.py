"""Unit tests for plotServer.plots.BasicPlot.Visualization in stack mode.

Visualization now orchestrates data + gain + geometry and composes two display
objects (ImageDisplay, WiggleDisplay). These integration-level tests require the
marmousi_4ms_stack.su fixture (skipped if absent, like the Bandwidth tests).
Detailed display behavior is covered fixture-free in test_image_display.py /
test_wiggle_display.py; pure math in test_basicplot_transforms.py.
"""
import numpy as np
import pytest
from bokeh.models import Plot

from plotServer.constants.VISUALIZATION import MAX_TRACES_LINE_HAREA
from plotServer.plots.BasicPlot import Visualization, PlotOptionsState
from plotServer.plots.BasicPlot.transforms import image_x_extent
from plotServer.plots.shared.colormaps import getColormap

# marmousi_4ms_stack.su: traces shape (723, 574), dt = 0.004 s
NUM_SAMPLES = 723
NUM_TRACES = 574


@pytest.fixture
def viz(marmousi_stack_path):
    state = PlotOptionsState(has_gather_key=False)
    return Visualization(
        filename=str(marmousi_stack_path),
        plot_options_state=state,
        gather_key=None,
    )


class TestConstruction:
    def test_owns_figure_directly(self, viz):
        assert isinstance(viz.plot, Plot)

    def test_composes_two_displays(self, viz):
        assert viz.image is not None
        assert viz.wiggle is not None

    def test_image_source_matches_file_shape(self, viz):
        assert viz.image.source.data["image"][0].shape == (NUM_SAMPLES, NUM_TRACES)

    def test_interval_time_samples_loaded(self, viz):
        assert viz.plot_options_state.interval_time_samples == pytest.approx(0.004)

    def test_stack_mode_has_no_offsets(self, viz):
        assert viz.gather_offsets is None

    def test_image_positioned_from_offsets_on_first_paint(self, viz):
        # Stack mode falls back to arange(1, n+1); regression that the first paint
        # already places the glyph from those positions.
        expected_x, expected_dw = image_x_extent(np.arange(1, NUM_TRACES + 1))
        assert viz.image.renderer.glyph.x == pytest.approx(expected_x)
        assert viz.image.renderer.glyph.dw == pytest.approx(expected_dw)


class TestInteractions:
    def test_image_visibility_delegates(self, viz):
        viz.updateImageVisibility(False)
        assert viz.image.renderer.visible is False

    def test_wiggle_visibility_does_not_raise(self, viz):
        # Regression for the old AttributeError crash when toggling wiggle on
        # before any pagination.
        viz.updateWiggleVisibility(True)
        assert viz.wiggle.line_renderer.visible is True
        assert viz.wiggle.fill_renderer.visible is True
        assert len(viz.wiggle.line_source.data["xs"]) == NUM_TRACES

    def test_fill_empty_over_trace_threshold(self, viz):
        assert NUM_TRACES > MAX_TRACES_LINE_HAREA
        viz.updateWiggleVisibility(True)
        assert viz.wiggle.fill_source.data["xs"] == []

    def test_colormap_update(self, viz):
        viz.updateColormap("red_black")
        assert viz.image.renderer.glyph.color_mapper.palette == getColormap("red_black")

    def test_update_gain_merges_into_state(self, viz):
        viz.updateGain({"AGC": 0.2})
        assert viz.gain["AGC"] == 0.2
        assert viz.gain["PERCENTILE_CLIPPING"] == 100  # untouched default


class TestRenderPipeline:
    def test_prepare_render_applies_active_gain(self, viz):
        raw = viz.getBaseData()
        viz.gain = {"AGC": 0.1, "GAUSSIAN_AGC": None, "PERCENTILE_CLIPPING": None}
        data, x_positions, instants = viz._prepare_render()
        assert data.shape == raw.shape
        assert not np.array_equal(data, raw)
        assert x_positions.shape == (NUM_TRACES,)
        assert instants.shape == (NUM_SAMPLES,)

    def test_gain_update_repaints_image(self, viz):
        before = viz.image.source.data["image"][0].copy()
        viz.updateGain({"AGC": 0.1})
        after = viz.image.source.data["image"][0]
        assert not np.array_equal(before, after)
