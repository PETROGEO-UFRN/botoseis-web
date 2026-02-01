from bokeh.plotting import figure


def plotFactory(
    x_label: str = None,
    y_label: str | None = None,
    gather_key: str | None = None,
    y_flipped: bool = True,
):
    plot = figure(
        active_drag=None,
        x_axis_label=x_label,
        x_axis_location="above",
        y_axis_label=y_label,
        sizing_mode="stretch_both",
        tags=[]
    )

    plot.toolbar.logo = None
    plot.x_range.range_padding = 0.0
    plot.y_range.range_padding = 0.0
    plot.y_range.flipped = y_flipped

    # Adjust axes labels
    if gather_key:
        plot.xaxis.axis_label = gather_key
    else:
        plot.xaxis.axis_label = "trace sequential number"
    if x_label:
        plot.xaxis.axis_label = x_label

    return plot
