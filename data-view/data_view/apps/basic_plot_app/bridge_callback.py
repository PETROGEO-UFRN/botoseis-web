from ...basicPlot import Visualization as BasicVisualization
from ...velan import Visualization as VelanVisualization


def bridge_callback(
    visualization: BasicVisualization | VelanVisualization,
    flat_new_state_options: dict[str, any]
):
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

    visualization.plot_manager.plot.tags = list(
        flat_new_state_options.keys()
    )
