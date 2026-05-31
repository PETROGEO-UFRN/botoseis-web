from typing import Callable
from bokeh.models import ColumnDataSource

from ..basicPlot import Visualization as BasicVisualization
from ..velan import Visualization as VelanVisualization


def create_bridge_model(
    visualization: BasicVisualization | VelanVisualization,
    callback: Callable[
        [
            BasicVisualization | VelanVisualization,
            dict[str, any]
        ],
        None
    ]
) -> ColumnDataSource:
    """
    Creates a Bokeh ColumnDataSource to act as a bridge for updating plot
    options state.

    Alows JavaScript on the client side to trigger updates to the plot
    options state on the server side.

    Implements a callback function that listens for changes to the data of
    a ColumnDataSource from Bokeh.
    """
    def js_bridge_update_plot_options_state(_, __, new_state_options) -> None:
        """
        Callback function to update the plot options state from the client.
        """
        flat_new_state_options = {
            key: value[0] for key, value in new_state_options.items()
        }

        callback(
            visualization=visualization,
            flat_new_state_options=flat_new_state_options
        )

        if (not flat_new_state_options):
            return

        visualization.plot_options_state.updatePlotOptionsState(
            **flat_new_state_options
        )

        visualization.handle_state_change()

    state_changer_bridge_model = ColumnDataSource(
        data=dict(),
        # *** "name" is used in the JS code to identify this model
        name="update_plot_options_trigger",
    )
    state_changer_bridge_model.on_change(
        'data',
        js_bridge_update_plot_options_state
    )

    return state_changer_bridge_model
