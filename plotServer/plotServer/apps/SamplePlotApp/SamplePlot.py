from bokeh.plotting import figure
from bokeh.models import ColumnDataSource


class SamplePlot:
    def __init__(self, workflowId: str):
        self.counter = 0
        self.source = ColumnDataSource(data={'x': [0], 'y': [0]})
        self.plot = figure(
            title=f"Sample plot - workflowId={workflowId}",
            x_axis_label="ping #",
            y_axis_label="value",
        )
        self.plot.line('x', 'y', source=self.source)

    def handle_ping(self):
        from random import randint
        self.counter += 1
        self.source.stream({'x': [self.counter], 'y': [randint(0, 10)]}, rollover=20)
