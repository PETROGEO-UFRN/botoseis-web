"""Unit tests for the pure BasicPlot transforms (no Bokeh, no SU fixture)."""
import numpy as np
import pytest

from plotServer.constants.VISUALIZATION import FIRST_TIME_SAMPLE, STRETCH_FACTOR
from plotServer.plots.BasicPlot.transforms import (
    check_data,
    check_x_positions,
    image_x_extent,
    rescale_for_wiggle,
    time_sample_instants,
    wiggle_fill_polygons,
    wiggle_polylines,
)


class TestCheckData:
    def test_accepts_2d_array(self):
        check_data(np.zeros((3, 4)))  # no raise

    def test_rejects_non_array(self):
        with pytest.raises(TypeError):
            check_data([[1, 2], [3, 4]])

    def test_rejects_non_2d(self):
        with pytest.raises(ValueError):
            check_data(np.arange(10))


class TestCheckXPositions:
    def test_accepts_matching_1d(self):
        check_x_positions(np.array([1.0, 2.0, 3.0]), num_traces=3)  # no raise

    def test_rejects_non_array(self):
        with pytest.raises(TypeError):
            check_x_positions([1, 2, 3], num_traces=3)

    def test_rejects_2d(self):
        with pytest.raises(ValueError):
            check_x_positions(np.zeros((2, 2)), num_traces=2)

    def test_rejects_size_mismatch(self):
        with pytest.raises(ValueError):
            check_x_positions(np.array([1.0, 2.0]), num_traces=5)


class TestTimeSampleInstants:
    def test_length_and_endpoints(self):
        t = time_sample_instants(num_time_samples=5, interval_time_samples=0.004)
        assert t.shape == (5,)
        assert t[0] == pytest.approx(FIRST_TIME_SAMPLE)
        assert t[-1] == pytest.approx(FIRST_TIME_SAMPLE + 4 * 0.004)

    def test_uniform_spacing(self):
        t = time_sample_instants(10, 0.002)
        assert np.allclose(np.diff(t), 0.002)

    def test_single_sample(self):
        t = time_sample_instants(1, 0.004)
        assert t.shape == (1,)
        assert t[0] == pytest.approx(FIRST_TIME_SAMPLE)


class TestImageXExtent:
    def test_single_trace(self):
        x, dw = image_x_extent(np.array([7.0]))
        assert x == pytest.approx(6.0)
        assert dw == pytest.approx(2.0)

    def test_uniform_offsets(self):
        # Offsets 1..4 -> centered glyph covering one spacing of padding.
        x, dw = image_x_extent(np.array([1.0, 2.0, 3.0, 4.0]))
        assert x == pytest.approx(0.5)
        assert dw == pytest.approx(4.0)


class TestRescaleForWiggle:
    def test_single_all_zero_trace_no_nan(self):
        data = np.zeros((4, 1))
        out = rescale_for_wiggle(data, np.array([1.0]))
        assert not np.isnan(out).any()
        assert np.array_equal(out, data)

    def test_single_trace_normalized(self):
        data = np.array([[0.0], [2.0], [-4.0]])
        out = rescale_for_wiggle(data, np.array([1.0]))
        assert np.max(np.abs(out)) == pytest.approx(1.0)

    def test_flat_multitrace_zero_std_no_nan(self):
        data = np.ones((4, 3))  # std along time is 0 for every trace
        out = rescale_for_wiggle(data, np.array([1.0, 2.0, 3.0]))
        assert not np.isnan(out).any()
        assert np.array_equal(out, data)

    def test_multitrace_uses_spacing_and_stretch(self):
        rng = np.random.default_rng(0)
        data = rng.standard_normal((20, 3))
        x_positions = np.array([0.0, 2.0, 4.0])
        out = rescale_for_wiggle(data, x_positions)
        expected = data / np.max(np.std(data, axis=0)) * 2.0 * STRETCH_FACTOR
        assert np.allclose(out, expected)


class TestWigglePolylines:
    def test_shapes_and_offsetting(self):
        data = np.array([[1.0, 10.0], [2.0, 20.0]])
        x_positions = np.array([5.0, 9.0])
        t = np.array([0.0, 0.1])
        out = wiggle_polylines(data, x_positions, t)
        assert set(out) == {"xs", "ys"}
        assert len(out["xs"]) == 2
        assert len(out["ys"]) == 2
        # Each polyline x = amplitude + its trace position.
        assert np.allclose(out["xs"][0], [1.0 + 5.0, 2.0 + 5.0])
        assert np.allclose(out["xs"][1], [10.0 + 9.0, 20.0 + 9.0])
        assert np.allclose(out["ys"][0], t)


class TestWiggleFillPolygons:
    def test_polygon_length_and_positive_clip(self):
        data = np.array([[-1.0, 1.0], [2.0, -2.0]])
        x_positions = np.array([0.0, 3.0])
        t = np.array([0.0, 0.1])
        out = wiggle_fill_polygons(data, x_positions, t)
        assert len(out["xs"]) == 2
        # Each polygon walks down the baseline and back up the (reversed) wiggle.
        assert out["xs"][0].shape == (4,)
        assert out["ys"][0].shape == (4,)
        # Negative amplitudes are clipped to the baseline (x == trace position).
        # Trace 0: amplitudes [-1, 2] clipped to [0, 2]; reversed-appended part.
        assert out["xs"][0].min() >= 0.0
