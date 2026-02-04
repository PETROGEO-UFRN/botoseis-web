import numpy as np
from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.models import GlyphRenderer, ColumnDataSource
from typing import Callable

from ..BaseVisualization.factories import plotFactory


class Visualization():
    plots_row: row

    plots: list[figure]
    sources: list[ColumnDataSource]
    renderers: list[GlyphRenderer]

    def __init__(
        self,
        subscribeListener: Callable[
            [Callable[[dict], None]],
            None
        ],
    ):
        self.plots = []
        self.sources = []
        self.renderers = []

        self.plots_row = row(
            sizing_mode="stretch_both"
        )

        subscribeListener(self.updateBandwidth)

    def createNewPlotSet(self):
        self.sources.append(ColumnDataSource(data=dict(x=[], y=[])))
        self.plots.append(
            plotFactory(
                y_label="Magnitude",
                x_label="Frequency (Hz)",
                y_flipped=False
            )
        )
        self.renderers.append(
            self.plots[-1].line(
                source=self.sources[-1],
                line_width=2,
                color="navy",
                legend_label="Aggregate Spectrum"
            )
        )
        self.plots_row.children = self.plots

    def updateBandwidth(self, dataList: list[dict]):
        for index, data in enumerate(dataList):
            # *** Create required amount of plots sets on the first load
            if index >= len(self.plots):
                self.createNewPlotSet()
                if index != 0:
                    self.plots[index].yaxis.axis_label = None

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

            self.sources[index].data = dict(
                x=frequencies_axis,
                y=aggregate_spectrum
            )
