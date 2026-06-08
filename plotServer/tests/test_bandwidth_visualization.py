"""Unit tests for plotServer.plots.Bandwidth.Visualization.

Bandwidth reads no file: it starts empty and is driven by the observer feed via
update_from_traces. So these tests are fixture-free -- the FFT pipeline is
exercised directly with synthetic sections.
"""
import numpy as np

from plotServer.plots.Bandwidth import Visualization
from plotServer.plots.Bandwidth.Visualization import compute_aggregate_spectrum


class TestComputeAggregateSpectrum:
    def test_x_and_y_have_equal_rfft_length(self):
        traces = np.zeros((128, 6), dtype=np.float32)
        freqs, mags = compute_aggregate_spectrum(traces, 0.004)
        assert len(freqs) == len(mags) == (128 // 2) + 1

    def test_frequency_axis_starts_at_dc_and_tops_near_nyquist(self):
        dt = 0.004
        freqs, _ = compute_aggregate_spectrum(np.zeros((128, 3)), dt)
        nyquist = 1.0 / (2 * dt)
        assert freqs[0] == 0.0
        assert freqs[-1] == nyquist  # 128 is even -> last bin is exactly Nyquist

    def test_matches_manual_fft(self):
        rng = np.random.default_rng(0)
        traces = rng.standard_normal((100, 8)).astype(np.float32)
        _, mags = compute_aggregate_spectrum(traces, 0.004)
        expected = np.mean(np.abs(np.fft.rfft(traces, axis=0)), axis=1)
        assert np.allclose(mags, expected)

    def test_magnitudes_are_real_and_non_negative(self):
        rng = np.random.default_rng(1)
        traces = rng.standard_normal((64, 4)).astype(np.float32)
        _, mags = compute_aggregate_spectrum(traces, 0.004)
        assert np.isrealobj(mags)
        assert (mags >= 0).all()


class TestVisualization:
    def test_starts_empty(self):
        viz = Visualization()
        assert list(viz.source.data["x"]) == []
        assert list(viz.source.data["y"]) == []

    def test_legend_is_attached(self):
        assert len(Visualization().plot.legend) > 0

    def test_update_from_traces_fills_and_matches_manual(self):
        viz = Visualization()
        rng = np.random.default_rng(2)
        traces = rng.standard_normal((128, 8)).astype(np.float32)

        viz.update_from_traces(traces, 0.004)

        assert len(viz.source.data["x"]) == (128 // 2) + 1
        expected = np.mean(np.abs(np.fft.rfft(traces, axis=0)), axis=1)
        assert np.allclose(viz.source.data["y"], expected)
