import numpy as np
import numpy.typing as np_types

from bokeh.palettes import Greys256
from bokeh.plotting import figure
from bokeh.models import GlyphRenderer, ColumnDataSource

DEFAULT_PALETTE = Greys256
NMO_CURVE_COLOR = "red"
NMO_CURVE_WIDTH = 1


def imageRendererFactory(
    plot: figure,
    source: ColumnDataSource,

    offsets: np_types.NDArray,
    first_time_sample: float,
    width_time_samples: float,

    curve_source: ColumnDataSource | None = None,
    is_visible: bool = True,
    palette: any = DEFAULT_PALETTE,
) -> GlyphRenderer:
    num_traces = source.data["image"][0].shape[1]

    if num_traces == 1:
        x = offsets[0] - 1
        dw = 2
    else:
        dw = np.abs(offsets[0] - offsets[-1])
        distance_first_offset = offsets[1] - offsets[0]
        distance_last_offset = offsets[-1] - offsets[-2]
        x = offsets[0] - distance_first_offset / 2
        dw = dw + (distance_first_offset + distance_last_offset) / 2
    renderer = plot.image(
        image="image",
        source=source,
        x=x,
        y=first_time_sample,
        dw=dw,
        dh=width_time_samples,
        anchor="bottom_left",
        origin="bottom_left",
        palette=palette,
        visible=is_visible
    )

    if curve_source:
        plot.line(
            color=NMO_CURVE_COLOR,
            source=curve_source,
            line_width=NMO_CURVE_WIDTH,
        )

    return renderer
