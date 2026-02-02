
import colorcet
from bokeh.plotting import figure
from bokeh.models import GlyphRenderer, ColumnDataSource

START_DISTANCE = 1
START_INDEX = 0


def heatmapRendererFactory(
    plot: figure,
    source: ColumnDataSource,
) -> GlyphRenderer:
    """
    Frequency-Offset Heatmap Renderer Factory
    """
    renderer = plot.image(
        image="image",
        source=source,
        x=START_INDEX,
        y=START_INDEX,
        dw=START_DISTANCE,
        dh=START_DISTANCE,
        palette=colorcet.rainbow4,
        level="image",
    )

    return renderer
