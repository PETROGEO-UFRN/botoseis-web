import numpy as np
from bokeh.plotting import figure
from bokeh.models import GlyphRenderer, ColumnDataSource
from typing import Callable

from ..BaseVisualization.factories import plotFactory


class Visualization():
    source: ColumnDataSource
    plot: figure
    renderer: GlyphRenderer
    traces: list[float]

    def __init__(
        self,
        subscribeListener: Callable[
            [Callable[[dict], None]],
            None
        ],
    ):
        """
        Bandwidth Visualization

        :param initial_data: Seismic data for extracting bandwidth
        :type initial_data: dict
        """

        self.source = ColumnDataSource(data=dict(x=[], y=[]))

        self.plot = plotFactory(
            y_label="Magnitude",
            x_label="Frequency (Hz)",
            y_flipped=False
        )

        self.renderer = self.plot.line(
            source=self.source,
            line_width=2,
            color="navy",
            legend_label="Aggregate Spectrum"
        )

        subscribeListener(self.updateBandwidth)

    def updateBandwidth(self, data):
        gather = data
        number_samples, _ = gather.shape
        interval_time_samples = 0.004  # 4 ms

        frequencies_axis = np.fft.rfftfreq(
            number_samples,
            interval_time_samples
        )

        complex_frequencies_by_trace = np.fft.rfft(gather, axis=0)
        # *** +ℝ Real positive frequencies map
        frequencies_by_trace = np.abs(complex_frequencies_by_trace)

        aggregate_spectrum = np.mean(frequencies_by_trace, axis=1)

        self.source.data = dict(
            x=frequencies_axis,
            y=aggregate_spectrum
        )

        print("BandwidthVisualization received data:")
