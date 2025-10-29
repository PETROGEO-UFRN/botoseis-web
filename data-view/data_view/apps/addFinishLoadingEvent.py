from bokeh.plotting import figure
from bokeh.models import CustomJS


def addFinishLoadingEvent(plot: figure) -> None:
    """
    Add event to bokeh plot to notify when loading is finished.

    This function adds a CustomJS callback to the plot's tags property.
    When the tags are updated, it triggers the `window.finishLoading` function
    on the client side, passing the tags as an argument.

    Args:
            plot: Bokeh plot object to which the event will be added.
    """
    plot.js_on_change(
        "tags",
        CustomJS(
            # *** This event will be triggered on client-side by any update on "plot.tags"
            # *** "window.finishLoading" should be available on client-side
            # *** "cb_obj" is provided by bokeh
            # *** "cb_obj" = "plot.tags" new value
            code="""
			try {
				window.finishLoading(cb_obj.tags)
				// Clear the tags locally to prevent re-triggering
				cb_obj.tags = []
			} catch (error) {
				console.error('Error in finishLoading at bokeh callback: ', error)
			}
			"""
        ),
    )
