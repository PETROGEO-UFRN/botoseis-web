from bokeh.plotting import figure

def plotFactory(
    xAxisLabel: str = '',
    yAxisLabel: str = '',
    axisRange: tuple | None = None,
    isYAxisFlipped: bool = True
) -> figure:
    """
    Factory function to create a Bokeh figure with common settings for seismic plots.

    Parameters
    ----------
    xAxisLabel : str, optional
        Label for the x-axis. Default is an empty string.
    yAxisLabel : str, optional
        Label for the y-axis. Default is an empty string.
    axisRange : tuple | None, optional
        Tuple specifying the bounds for the y-axis (min, max). Default is None
        (uses automatic range).
    isYAxisFlipped : bool, optional
        Whether to flip the y-axis. Default is True.

    Returns
    -------
    figure
        A Bokeh figure object configured for seismic plotting.
    """
    plot = figure(
        active_drag=None,
        x_axis_label=xAxisLabel,
        x_axis_location="above",
        y_axis_label=yAxisLabel,
        sizing_mode="stretch_both",
        tags=[]
    )

    plot.toolbar.logo = None
    plot.x_range.range_padding = 0.0
    plot.y_range.range_padding = 0.0

    plot.y_range.flipped = isYAxisFlipped
    if axisRange:
        plot.y_range.bounds = axisRange

    return plot
