from bokeh.plotting import figure

from ..shared.plotFactory import plotFactory


class Visualization:
    plot: figure

    def __init__(self):
        self.plot = plotFactory(
            xAxisLabel="Wavenumber",
            yAxisLabel="Frequency (Hz)",
            isYAxisFlipped=False,
        )
        self.plot.title.text = "FK (placeholder)"
