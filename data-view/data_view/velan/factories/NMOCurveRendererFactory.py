from bokeh.plotting import figure
from bokeh.models import GlyphRenderer, ColumnDataSource

NMO_CURVE_COLOR = "#0066FF"
NMO_CURVE_WIDTH = 1


def NMOCurveRendererFactory(
    plot: figure,
    source: ColumnDataSource,
) -> GlyphRenderer:
    plot.line(
        source=source,
        color=NMO_CURVE_COLOR,
        line_width=NMO_CURVE_WIDTH,
    )
