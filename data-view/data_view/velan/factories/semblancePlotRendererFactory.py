import colorcet
import numpy as np
import numpy.typing as np_types
from typing import Callable

from bokeh.plotting import figure
from bokeh.models import GlyphRenderer, ColumnDataSource, HoverTool, CustomJS, CrosshairTool

from .pickingFactory import pickingFactory

CROSSHAIR_COLOR = "red"
CROSSHAIR_LINE_WIDTH = 1


def semblancePlotRendererFactory(
    plot: figure,
    source: ColumnDataSource,
    picks_source: ColumnDataSource,
    on_pick_update: Callable,
    index_in_plot_pair: int,

    velocities: np_types.NDArray,

    first_time_sample: float,
    width_time_samples: float,

    first_velocity_value: float,
    last_velocity_value: float,
) -> GlyphRenderer:
    width_velocities = np.abs(last_velocity_value - first_velocity_value)

    renderer = plot.image(
        image="image",
        source=source,
        x=velocities[0],
        y=first_time_sample,
        dw=width_velocities,
        dh=width_time_samples,
        anchor="bottom_left",
        origin="bottom_left",
        palette=colorcet.rainbow4,
    )
    pickingFactory(
        plot=plot,
        picks_source=picks_source,
        on_pick_update=on_pick_update,
    )

    nativeCrosshair = CrosshairTool(
        dimensions='height',
        line_alpha=CROSSHAIR_LINE_WIDTH,
        line_color=CROSSHAIR_COLOR,
    )

    hover_callback = CustomJS(
        args={
            "picks_source": picks_source,
            "nativeCrosshair": nativeCrosshair
        },
        code=f"""
            try {{
                // cb_data contains the geometry of the hover event
                const geometry = cb_data.geometry
                const hasPicks = picks_source.data.x.length > 0

                window.semblancePlotHoverCallback({{
                    index_in_plot_pair: {index_in_plot_pair},
                    hasPicks,
                    geometry,
                    nativeCrosshair,
                }})

            }} catch (error) {{
                console.error(
                    'Error in semblancePlotHoverCallback at bokeh callback: ',
                    error
                )
            }}
        """
    )

    hover = HoverTool(
        tooltips=[("(x,y)", "($x, $y)")],
        callback=hover_callback,
        mode='mouse'
    )

    plot.add_tools(hover)
    plot.add_tools(nativeCrosshair)

    return renderer
