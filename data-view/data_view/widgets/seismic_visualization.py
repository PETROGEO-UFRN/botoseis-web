from bokeh.models import Switch

from ..core.SeismicPlotWrapper import SeismicPlotWrapper


def create_seismic_plot_wrapper(state: dict, sufile):
    """
    State:
    - [read] num_loadedgathers
    """
    if sufile.gather_keyword is None:
        seismic_plot_wrapper = SeismicPlotWrapper(
            data=sufile.traces,
            x_positions=None,
            interval_time_samples=state["interval_time_samples"],
        )
    else:
        if state["num_loadedgathers"] == 1:
            # Single gather
            seismic_plot_wrapper = SeismicPlotWrapper(
                data=sufile.igather[state["gather_index_start"]].data,
                x_positions=sufile.igather[
                    state["gather_index_start"]
                ].headers["offset"],
                interval_time_samples=state["interval_time_samples"],
                gather_key="Offset [m]",
            )
        else:
            # Multiple gathers
            seismic_plot_wrapper = SeismicPlotWrapper(
                data=sufile.igather[
                    state["gather_index_start"]:
                    state["gather_index_start"] +
                    state["num_loadedgathers"]
                ].data,
                x_positions=None,
                interval_time_samples=state["interval_time_samples"],
            )

    # Toggle visibility
    wiggle_switch = Switch(active=True)
    image_switch = Switch(active=True)
    areas_switch = Switch(active=True)
    seismic_plot_wrapper.assign_wiggle_switch(wiggle_switch)
    seismic_plot_wrapper.assign_image_switch(image_switch)
    seismic_plot_wrapper.assign_area_switch(areas_switch)

    return seismic_plot_wrapper
