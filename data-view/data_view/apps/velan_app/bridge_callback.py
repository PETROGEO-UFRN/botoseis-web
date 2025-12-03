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

    visualization.plots_row.tags = list(
        flat_new_state_options.keys()
    )
