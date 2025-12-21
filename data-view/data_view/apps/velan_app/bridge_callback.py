from ...basicPlot import Visualization as BasicVisualization
from ...velan import Visualization as VelanVisualization

from .save_picks import save_picks


def bridge_callback(
    visualization: BasicVisualization | VelanVisualization,
    flat_new_state_options: dict[str, any]
):
    if "save_picks_triger" in flat_new_state_options:
        save_picks(visualization.picking_data)
        # *** remove "palette" once it will not be accepted by "updatePlotOptionsState()"
        flat_new_state_options.pop("save_picks_triger")
    if "apply_nmo_triger" in flat_new_state_options:
        visualization.apply_nmo()
        # *** remove "palette" once it will not be accepted by "updatePlotOptionsState()"
        flat_new_state_options.pop("apply_nmo_triger")
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
