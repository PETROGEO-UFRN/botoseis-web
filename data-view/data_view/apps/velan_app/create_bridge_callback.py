from ...basicPlot import Visualization as BasicVisualization
from ...velan import Visualization as VelanVisualization

from .RestAPIConsumer import RestAPIConsumer


def create_bridge_callback(restAPIConsumer: RestAPIConsumer):
    def bridge_callback(
        visualization: BasicVisualization | VelanVisualization,
        flat_new_state_options: dict[str, any]
    ):
        # *** remove and process triggers that are not accepted by "updatePlotOptionsState()"
        if "save_picks_triger" in flat_new_state_options:
            restAPIConsumer.save_picks(
                visualization.picking_data
            )
            flat_new_state_options.pop("save_picks_triger")

        if "nmo_trigger" in flat_new_state_options:
            if flat_new_state_options["nmo_trigger"]:
                visualization.apply_nmo()
            else:
                visualization.remove_nmo()
            flat_new_state_options.pop("nmo_trigger")

        if "reuse_picks" in flat_new_state_options:
            visualization.reuse_picks()
            flat_new_state_options.pop("reuse_picks")

        if "semblance_plot_hover" in flat_new_state_options:
            hover_coordinates = flat_new_state_options["semblance_plot_hover"]
            visualization.update_time_curve_source(
                index_in_plot_pair=hover_coordinates["index_in_plot_pair"],
                selected_time=hover_coordinates["y"],
                selected_velocity=hover_coordinates["x"],
            )
            flat_new_state_options.pop("semblance_plot_hover")

        visualization.plots_row.tags = list(
            flat_new_state_options.keys()
        )
    return bridge_callback
