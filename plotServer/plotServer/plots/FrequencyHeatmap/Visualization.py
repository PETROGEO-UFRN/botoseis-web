from bokeh.plotting import figure

from ..shared.plotFactory import plotFactory


class Visualization:
    plot: figure

    def __init__(self):
        self.plot = plotFactory(
            xAxisLabel="Trace",
            yAxisLabel="Frequency (Hz)",
            isYAxisFlipped=False,
        )
        self.plot.title.text = "FrequencyHeatmap (placeholder)"
