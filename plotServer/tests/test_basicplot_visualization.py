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

from plotServer.plots.BasicPlot import Visualization, PlotOptionsState
from plotServer.plots.BasicPlot.transforms import image_x_extent
from plotServer.plots.shared.colormaps import getColormap

# Properties of THE fixture (marmousi_4ms_stack.su), enforced by the
# marmousi_stack_path fixture guard in conftest.py: traces (724, 457), dt 0.004 s.
NUM_SAMPLES = 724
NUM_TRACES = 457


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

    def test_fill_populated_for_this_fixture(self, viz):
        # This fixture has 457 traces (< MAX_TRACES_LINE_HAREA), so the filled
        # area is rendered: one polygon per trace. The over-threshold suppression
        # path is covered fixture-free in test_wiggle_display.py.
        viz.updateWiggleVisibility(True)
        assert len(viz.wiggle.fill_source.data["xs"]) == NUM_TRACES

    def test_colormap_update(self, viz):
        viz.updateColormap("red_black")
        assert viz.image.renderer.glyph.color_mapper.palette == getColormap("red_black")

    def test_update_gain_merges_into_state(self, viz):
        viz.updateGain({"AGC": 0.2})
        assert viz.gain["AGC"] == 0.2
        assert viz.gain["PERCENTILE_CLIPPING"] == 100  # untouched default


class TestSectionChangeHook:
    """The cross-tab publish point: an optional callback fires with the current
    displayed section on first paint and on every repaint. Defaults to a no-op."""

    def test_fires_on_init_with_data_and_dt(self, marmousi_stack_path):
        calls = []
        Visualization(
            filename=str(marmousi_stack_path),
            plot_options_state=PlotOptionsState(has_gather_key=False),
            gather_key=None,
            on_section_change=lambda data, dt: calls.append((data, dt)),
        )
        assert len(calls) == 1
        data, dt = calls[0]
        assert data.shape == (NUM_SAMPLES, NUM_TRACES)
        assert dt == pytest.approx(0.004)

    def test_fires_again_on_state_change(self, marmousi_stack_path):
        calls = []
        viz = Visualization(
            filename=str(marmousi_stack_path),
            plot_options_state=PlotOptionsState(has_gather_key=False),
            gather_key=None,
            on_section_change=lambda data, dt: calls.append((data, dt)),
        )
        viz.handle_state_change()
        assert len(calls) == 2

    def test_hook_is_optional(self, viz):
        # The `viz` fixture passes no on_section_change; repaint must not raise.
        viz.handle_state_change()


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


class TestGatherNavigation:
    """Gather-mode pagination: updateGatherIndex is 0-based and clamped so a
    stale client index never wraps to the last gather (negative slice) or reads
    past the end. Reading the stack file with gather_key='cdp' gives a real
    multi-gather grouping (same as VelocityModel)."""

    @pytest.fixture
    def gather_viz(self, marmousi_stack_path):
        return Visualization(
            filename=str(marmousi_stack_path),
            plot_options_state=PlotOptionsState(has_gather_key=True),
            gather_key="cdp",
        )

    def test_num_gathers_is_known(self, gather_viz):
        assert gather_viz.plot_options_state.num_gathers > 1

    def test_update_is_zero_based(self, gather_viz):
        gather_viz.updateGatherIndex(3)
        assert gather_viz.plot_options_state.gather_index_start == 3

    def test_negative_index_clamps_to_zero(self, gather_viz):
        # Regression: gatherIndex 0 used to become -1 and wrap to the last gather.
        gather_viz.updateGatherIndex(-5)
        assert gather_viz.plot_options_state.gather_index_start == 0

    def test_overshoot_clamps_to_last_loadable(self, gather_viz):
        state = gather_viz.plot_options_state
        gather_viz.updateGatherIndex(state.num_gathers + 100)
        loaded = state.num_loadedgathers or 1
        assert state.gather_index_start == state.num_gathers - loaded
