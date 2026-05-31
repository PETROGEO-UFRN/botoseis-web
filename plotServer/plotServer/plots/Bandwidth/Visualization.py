from bokeh.plotting import figure

from ..shared.plotFactory import plotFactory


class Visualization:
    plot: figure

    def __init__(self):
        self.plot = plotFactory(
            xAxisLabel="Frequency (Hz)",
            yAxisLabel="Amplitude",
            isYAxisFlipped=False,
        )
        self.plot.title.text = "Bandwidth (placeholder)"
