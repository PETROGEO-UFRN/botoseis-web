import numpy.typing as np_types

from bokeh.plotting import figure
from bokeh.models import GlyphRenderer, ColumnDataSource


def nmoPlotRendererFactory(
    plot: figure,
    source: ColumnDataSource,

    offsets: np_types.NDArray,
    first_time_sample: float,
    width_time_samples: float,
    width_offsets: int,
) -> GlyphRenderer:
    renderer = plot.image(
        image="image",
        source=source,
        x=offsets[0],
        y=first_time_sample,
        dw=width_offsets,
        dh=width_time_samples,
        anchor="bottom_left",
        origin="bottom_left",
        palette="Greys256",
    )

    return renderer
