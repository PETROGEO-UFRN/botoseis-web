"""Unit tests for plotServer.plots.Bandwidth.Visualization.

Current scope: the whole stacked SU file is FFT'd along time and averaged
across every trace into a single aggregate magnitude spectrum. These tests
require the marmousi_4ms_stack.su fixture; without it the file is skipped (see
the `marmousi_stack_path` session fixture in conftest.py).

(Per-gather spectra with pagination are deferred to BasicPlot integration and
are intentionally not covered here.)
"""
import numpy as np
import pytest

from plotServer.plots.Bandwidth import Visualization

# Properties of THE fixture (marmousi_4ms_stack.su), enforced by the
# marmousi_stack_path fixture guard in conftest.py: 724 samples, dt 0.004 s.
NUM_SAMPLES = 724
NYQUIST_HZ = 125.0  # 1 / (2 * 0.004)


@pytest.fixture
def viz(marmousi_stack_path):
    return Visualization(filename=str(marmousi_stack_path))


class TestBandwidthVisualizationOutput:
    def test_x_and_y_have_equal_length(self, viz):
        assert len(viz.source.data["x"]) == len(viz.source.data["y"])

    def test_rfft_output_length_matches_whole_file(self, viz):
        # rfft length over the full section = N // 2 + 1
        assert len(viz.source.data["x"]) == (NUM_SAMPLES // 2) + 1

    def test_frequency_axis_starts_at_dc(self, viz):
        assert viz.source.data["x"][0] == pytest.approx(0.0)

    def test_frequency_axis_top_is_nyquist(self, viz):
        x = viz.source.data["x"]
        bin_width = x[1] - x[0]
        # N=723 is odd, so the top bin sits one bin below Nyquist.
        assert x[-1] == pytest.approx(NYQUIST_HZ, abs=bin_width)

    def test_magnitudes_are_real_and_non_negative(self, viz):
        y = viz.source.data["y"]
        assert np.isrealobj(y)
        assert (y >= 0).all()

    def test_legend_is_attached(self, viz):
        assert len(viz.plot.legend) > 0

    def test_no_placeholder_title(self, viz):
        title = viz.plot.title
        assert (title is None) or (title.text in (None, ""))


class TestBandwidthAggregation:
    def test_spectrum_matches_manual_fft(self, marmousi_stack_path):
        """The plotted spectrum equals mean(|rfft(traces, axis=0)|, axis=1)."""
        from seismicio import readsu

        sufile = readsu(str(marmousi_stack_path))
        expected = np.mean(np.abs(np.fft.rfft(sufile.traces, axis=0)), axis=1)

        viz = Visualization(filename=str(marmousi_stack_path))
        assert np.allclose(viz.source.data["y"], expected)
