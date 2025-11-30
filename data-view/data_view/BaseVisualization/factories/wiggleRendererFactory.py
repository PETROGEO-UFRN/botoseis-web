from bokeh.plotting import figure
from bokeh.models import GlyphRenderer, ColumnDataSource

WIGGLE_COLOR = "black"


def wiggleRendererFactory(
    plot: figure,
    source: ColumnDataSource,
    is_visible: bool = True,
) -> GlyphRenderer:
    renderer = plot.multi_line(
        xs="xs",
        ys="ys",
        source=source,
        color=WIGGLE_COLOR,
        visible=is_visible,
    )

    return renderer
