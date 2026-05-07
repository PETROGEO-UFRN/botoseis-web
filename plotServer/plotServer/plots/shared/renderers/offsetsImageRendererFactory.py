import numpy as np
import numpy.typing as np_types

from bokeh.palettes import Greys256
from bokeh.plotting import figure
from bokeh.models import GlyphRenderer, ColumnDataSource

DEFAULT_PALETTE = Greys256


def offsetsImageRendererFactory(
    plot: figure,
    source: ColumnDataSource,

    offsets: np_types.NDArray,
    first_time_sample: float,
    widthTimeSamples: float,

    isVisible: bool = True,
    palette: any = DEFAULT_PALETTE,
) -> GlyphRenderer:
    tracesAmount = source.data["image"][0].shape[1]

    if tracesAmount == 1:
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
        dh=widthTimeSamples,
        anchor="bottom_left",
        origin="bottom_left",
        palette=palette,
        visible=isVisible
    )

    return renderer
