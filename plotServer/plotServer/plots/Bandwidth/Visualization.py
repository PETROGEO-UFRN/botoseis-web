import numpy as np
import numpy.typing as np_types
from bokeh.models import ColumnDataSource, GlyphRenderer
from bokeh.plotting import figure

from ..shared.plotFactory import plotFactory


def compute_aggregate_spectrum(
    traces: np_types.NDArray,
    interval_time_samples: float,
) -> tuple[np_types.NDArray, np_types.NDArray]:
    """FFT a (num_time_samples, num_traces) section along time and average the
    magnitudes across every trace into a single aggregate spectrum.

    Returns ``(frequencies, magnitudes)`` of equal length (rfft: N // 2 + 1).
    """
    number_samples = traces.shape[0]
    frequencies_axis = np.fft.rfftfreq(number_samples, interval_time_samples)
    complex_frequencies = np.fft.rfft(traces, axis=0)
    magnitudes = np.abs(complex_frequencies)
    aggregate_spectrum = np.mean(magnitudes, axis=1)
    return frequencies_axis, aggregate_spectrum


class Visualization:
    """Aggregate magnitude spectrum of whatever section another tab is showing.

    Bandwidth does **not** read the file itself: it starts empty and is driven
    entirely by the cross-tab observer feed (e.g. the gather currently displayed
    in BasicPlot), which calls :meth:`update_from_traces`. The observer replays
    the current section on connect, so an open BasicPlot fills it immediately.
    """

    plot: figure
    source: ColumnDataSource
    renderer: GlyphRenderer

    def __init__(self):
        self.source = ColumnDataSource(data=dict(x=[], y=[]))
        self.plot = plotFactory(
            xAxisLabel="Frequency (Hz)",
            yAxisLabel="Magnitude",
            isYAxisFlipped=False,
        )
        self.renderer = self.plot.line(
            source=self.source,
            line_width=0.5,
            color="navy",
            legend_label="Aggregate Spectrum",
        )

    def update_from_traces(
        self,
        traces: np_types.NDArray,
        interval_time_samples: float,
    ) -> None:
        """Recompute the aggregate spectrum from a section pushed by another tab
        (e.g. the gather currently displayed in BasicPlot) and repaint."""
        frequencies_axis, aggregate_spectrum = compute_aggregate_spectrum(
            traces, interval_time_samples
        )
        self.source.data = dict(x=frequencies_axis, y=aggregate_spectrum)
