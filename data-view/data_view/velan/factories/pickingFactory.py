import numpy as np

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, PointDrawTool

PICKING_COLOR = "white"
PICKING_LINE_WIDTH = 1.5


def pickingFactory(
    plot: figure,
    picks_source: ColumnDataSource,
) -> None:
    def handle_picks_data_change(attr, old, new_picks_data):
        picks_source.remove_on_change(
            "data",
            handle_picks_data_change
        )

        x_sorted, y_sorted = sort_xy_pairs_by_x(
            new_picks_data["x"],
            new_picks_data["y"]
        )
        picks_source.data.update({"x": x_sorted, "y": y_sorted})
        picks_source.on_change("data", handle_picks_data_change)

    picks_scatter_renderer = plot.scatter(
        color=PICKING_COLOR,
        source=picks_source,
    )

    plot.add_tools(
        PointDrawTool(renderers=[picks_scatter_renderer])
    )
    plot.line(
        color=PICKING_COLOR,
        source=picks_source,
        line_width=PICKING_LINE_WIDTH,
    )
    picks_source.on_change("data", handle_picks_data_change)


def sort_xy_pairs_by_x(x, y):
    x_array = np.asarray(x)
    y_array = np.asarray(y)
    # *** sort by y axis
    sorted_indices = np.argsort(y_array)
    return x_array[sorted_indices], y_array[sorted_indices]
