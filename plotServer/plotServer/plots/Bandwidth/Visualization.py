import numpy as np
from bokeh.models import ColumnDataSource, GlyphRenderer
from bokeh.plotting import figure
from seismicio import readsu

from ..shared.plotFactory import plotFactory

SECOND_IN_MICRO_SECONDS = 1e6


class Visualization:
    """Aggregate magnitude spectrum of a stacked SU file.

    Current scope: the whole output file is treated as a single stacked
    section -- FFT along time, averaged across every trace.

    Deferred (lands with BasicPlot integration): per-gather spectrum with
    real-time updates as the user paginates gathers. Pagination has no source
    yet, so it is intentionally not implemented here.
    """

    plot: figure
    source: ColumnDataSource
    renderer: GlyphRenderer

    def __init__(self, filename: str):
        sufile = readsu(filename)
        interval_time_samples = sufile.headers.dt[0] / SECOND_IN_MICRO_SECONDS

        traces = sufile.traces  # (num_time_samples, num_traces)
        number_samples = traces.shape[0]

        frequencies_axis = np.fft.rfftfreq(number_samples, interval_time_samples)
        complex_frequencies = np.fft.rfft(traces, axis=0)
        magnitudes = np.abs(complex_frequencies)
        aggregate_spectrum = np.mean(magnitudes, axis=1)

        self.source = ColumnDataSource(data=dict(
            x=frequencies_axis,
            y=aggregate_spectrum,
        ))
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
