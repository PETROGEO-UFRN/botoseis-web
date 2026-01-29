import colorcet

from bokeh.plotting import figure
from bokeh.models import GlyphRenderer, ColumnDataSource


def velocityModelRendererFactory(
    plot: figure,
    source: ColumnDataSource,

    first_cdp: int,
    last_cdp: int,

    first_time_sample: float,
    total_time: float,
) -> GlyphRenderer:
    renderer = plot.image(
        image='image',
        source=source,

        x=first_cdp,
        y=first_time_sample,
        dw=last_cdp - first_cdp,
        dh=total_time,

        palette=colorcet.rainbow4,
    )

    return renderer
