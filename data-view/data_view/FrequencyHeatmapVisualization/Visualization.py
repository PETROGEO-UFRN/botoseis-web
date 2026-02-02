import numpy as np
from bokeh.plotting import figure
from bokeh.models import GlyphRenderer, ColumnDataSource
from typing import Callable

from ..BaseVisualization.factories import plotFactory
from .heatmapRendererFactory import heatmapRendererFactory


class Visualization:
    plots: figure
    source: ColumnDataSource
    renderer: GlyphRenderer

    def __init__(
        self,
        subscribeListener: Callable[
            [Callable[[dict], None]],
            None
        ],
    ):
        self.source = ColumnDataSource(data=dict(x=[], y=[]))

        self.plot = plotFactory(
            y_label="Magnitude",
            x_label="Frequency (Hz)",
            y_flipped=False
        )

        self.renderer = heatmapRendererFactory(
            plot=self.plot,
            source=self.source,
        )

        subscribeListener(self.updateHeatmap)

    def updateHeatmap(self, data):
        gather = data
        number_samples, number_traces = gather.shape
        interval_time_samples = 0.004  # 4 ms

        frequencies_axis = np.fft.rfftfreq(
            number_samples,
            interval_time_samples
        )

        complex_frequencies_by_trace = np.fft.rfft(gather, axis=0)
        # *** +ℝ Real positive frequencies map
        frequencies_by_trace = np.abs(complex_frequencies_by_trace)

        self.source.data = {'image': [frequencies_by_trace]}

        self.renderer.glyph.dw = number_traces
        self.renderer.glyph.dh = frequencies_axis[-1]
