import colorcet
import numpy as np
import numpy.typing as np_types
from typing import Callable

from bokeh.plotting import figure
from bokeh.models import GlyphRenderer, ColumnDataSource, CrosshairTool

from .pickingFactory import pickingFactory

CROSSHAIR_COLOR = "red"
CROSSHAIR_LINE_WIDTH = 1


def semblancePlotRendererFactory(
    plot: figure,
    source: ColumnDataSource,
    picks_source: ColumnDataSource,
    on_pick_update: Callable,

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
    plot.add_tools(nativeCrosshair)

    return renderer
