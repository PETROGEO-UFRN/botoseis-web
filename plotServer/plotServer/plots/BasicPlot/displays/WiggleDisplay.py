import numpy.typing as np_types
from bokeh.models import ColumnDataSource, GlyphRenderer
from bokeh.plotting import figure

from .. import transforms
from ...shared.renderers.wiggleRendererFactory import wiggleRendererFactory
from ....constants.VISUALIZATION import MAX_TRACES_LINE_HAREA

FILL_COLOR = "black"


class WiggleDisplay:
    """The wiggle-trace representation of a seismic section: one polyline per
    trace plus filled positive lobes.

    Owns both the line and the fill ColumnDataSources/glyphs on a given figure
    (they are one representation, toggled together). Recomputing the wiggle
    geometry is only worthwhile when visible, so updates are cached and the
    sources are (re)built lazily on show — that policy lives here, in the wiggle
    domain, rather than leaking into the Visualization.
    """

    line_source: ColumnDataSource
    line_renderer: GlyphRenderer
    fill_source: ColumnDataSource
    fill_renderer: GlyphRenderer

    def __init__(
        self,
        plot: figure,
        data: np_types.NDArray,
        x_positions: np_types.NDArray,
        instants: np_types.NDArray,
        *,
        visible: bool = False,
    ) -> None:
        self._visible = visible

        # Line renderer first, fill second, so fill draws on top of the lines.
        self.line_source = ColumnDataSource(data={"xs": [], "ys": []})
        self.line_renderer = wiggleRendererFactory(
            plot=plot,
            source=self.line_source,
            isVisible=visible,
        )
        self.fill_source = ColumnDataSource(data={"xs": [], "ys": []})
        self.fill_renderer = plot.patches(
            xs="xs",
            ys="ys",
            source=self.fill_source,
            color=FILL_COLOR,
            line_width=0,
            visible=visible,
        )

        # Populate now (even though wiggle may start hidden) so no source ships
        # with empty columns.
        self._cache = (data, x_positions, instants)
        self._rebuild()

    def set_visible(self, visible: bool) -> None:
        self._visible = visible
        self.line_renderer.visible = visible
        self.fill_renderer.visible = visible
        if visible:
            self._rebuild()

    def update(
        self,
        data: np_types.NDArray,
        x_positions: np_types.NDArray,
        instants: np_types.NDArray,
    ) -> None:
        self._cache = (data, x_positions, instants)
        if self._visible:
            self._rebuild()

    def _rebuild(self) -> None:
        data, x_positions, instants = self._cache
        rescaled = transforms.rescale_for_wiggle(data, x_positions)
        self.line_source.data = transforms.wiggle_polylines(
            rescaled, x_positions, instants
        )
        self.fill_source.data = self._fill_data(rescaled, x_positions, instants)

    @staticmethod
    def _fill_data(rescaled, x_positions, instants) -> dict[str, list]:
        # Too many traces makes the filled-area polygons unreadable and slow;
        # render nothing rather than choking the browser.
        if rescaled.shape[1] > MAX_TRACES_LINE_HAREA:
            return {"xs": [], "ys": []}
        return transforms.wiggle_fill_polygons(rescaled, x_positions, instants)
