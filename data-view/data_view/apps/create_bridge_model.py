from bokeh.models import ColumnDataSource

from ..basicPlot import Visualization as BasicVisualization
from ..velan import Visualization as VelanVisualization
from .save_picks import save_picks


def create_bridge_model(
    visualization: BasicVisualization | VelanVisualization
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

        for toggle_key in ["toggle_image", "toggle_wiggle"]:
            if toggle_key in flat_new_state_options:
                visualization.toogle_visibility_by_type(toggle_key)
                # *** remove "toggle_key" once it will not be accepted by "updatePlotOptionsState()"
                flat_new_state_options.pop(toggle_key)

        if "palette" in flat_new_state_options:
            visualization.handle_palette_change(
                flat_new_state_options["palette"]
            )
            # *** remove "palette" once it will not be accepted by "updatePlotOptionsState()"
            flat_new_state_options.pop("palette")

        if (not flat_new_state_options):
            return

        # ! workarround to bypass difference beetwen different Visualization classes
        # ! This chunk handles loading feedback
        if hasattr(visualization, "plot_manager"):
            visualization.plot_manager.plot.tags = list(
                flat_new_state_options.keys()
            )
        else:
            if "save_picks_triger" in flat_new_state_options:
                print("*** *** RUN save_picks_triger *** ***")
                save_picks(visualization.picking_data)
                flat_new_state_options.pop("save_picks_triger")
            if "apply_nmo_triger" in flat_new_state_options:
                visualization.apply_nmo()
                flat_new_state_options.pop("apply_nmo_triger")

            visualization.plots_row.tags = list(
                flat_new_state_options.keys()
            )

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
