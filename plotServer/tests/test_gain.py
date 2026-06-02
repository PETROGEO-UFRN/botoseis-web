"""Unit tests for the shared gain pipeline (primary consumer is BasicPlot)."""
import numpy as np
import pytest

from plotServer.plots.shared.gain import applyGain
from plotServer.plots.shared.gain.agc import applyAgcGain
from plotServer.plots.shared.gain.perc import applyPercentileClipping

DT = 0.004


def _data(seed=0):
    rng = np.random.default_rng(seed)
    return rng.standard_normal((50, 8))


class TestApplyGainDispatch:
    def test_none_values_are_skipped(self):
        data = _data()
        out = applyGain(
            data,
            gain={"AGC": None, "GAUSSIAN_AGC": None, "PERCENTILE_CLIPPING": None},
            intervalTimeSamples=DT,
        )
        assert np.array_equal(out, data)

    def test_does_not_mutate_input(self):
        data = _data()
        original = data.copy()
        applyGain(
            data,
            gain={"AGC": 0.1, "GAUSSIAN_AGC": None, "PERCENTILE_CLIPPING": 90},
            intervalTimeSamples=DT,
        )
        assert np.array_equal(data, original)

    def test_agc_changes_data(self):
        data = _data()
        out = applyGain(
            data,
            gain={"AGC": 0.1, "GAUSSIAN_AGC": None, "PERCENTILE_CLIPPING": None},
            intervalTimeSamples=DT,
        )
        assert not np.array_equal(out, data)


class TestAgcGuards:
    def test_tiny_window_does_not_produce_nan(self):
        # wagc << dt would round the half-window to 0 in the old code -> NaN.
        data = _data()
        out = applyAgcGain(data, wagc=0.0001, intervalTimeSamples=DT)
        assert not np.isnan(out).any()
        assert out.shape == data.shape


class TestPercentileClipping:
    def test_clips_to_percentile(self):
        data = _data()
        out = applyPercentileClipping(data, percentile=50)
        bound = np.percentile(np.absolute(data), 50)
        assert out.max() <= bound + 1e-9
        assert out.min() >= -bound - 1e-9

    def test_out_of_range_percentile_is_clamped(self):
        data = _data()
        # 150 is invalid for np.percentile; clamped to 100 -> no clipping.
        out = applyPercentileClipping(data, percentile=150)
        assert np.allclose(out, data)
