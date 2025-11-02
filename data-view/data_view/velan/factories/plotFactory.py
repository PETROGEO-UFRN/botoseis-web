from bokeh.plotting import figure


def plotFactory(
    x_label: str,
    y_label: str,
):
    plot = figure(
        active_drag=None,
        x_axis_label=x_label,
        x_axis_location="above",
        y_axis_label=y_label,
    )

    plot.x_range.range_padding = 0.0
    plot.y_range.range_padding = 0.0
    plot.y_range.flipped = True

    return plot
