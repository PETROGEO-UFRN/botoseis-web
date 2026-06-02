import numpy as np
import numpy.typing as np_types
from bokeh.models import ColumnDataSource, GlyphRenderer
from bokeh.palettes import Palette
from bokeh.plotting import figure

from .. import transforms
from ...shared.renderers.offsetsImageRendererFactory import offsetsImageRendererFactory
from ....constants.VISUALIZATION import FIRST_TIME_SAMPLE


class ImageDisplay:
    """The variable-density (image) representation of a seismic section.

    Owns the image ColumnDataSource and its glyph on a given figure, and knows
    how to reposition itself when the data/offsets change and how to recolor.
    Amplitude/geometry math is delegated to :mod:`transforms`.
    """

    source: ColumnDataSource
    renderer: GlyphRenderer

    def __init__(
        self,
        plot: figure,
        data: np_types.NDArray,
        x_positions: np_types.NDArray,
        instants: np_types.NDArray,
        *,
        visible: bool = True,
    ) -> None:
        self.source = ColumnDataSource(data={"image": [data]})
        self.renderer = offsetsImageRendererFactory(
            plot=plot,
            source=self.source,
            offsets=x_positions,
            first_time_sample=FIRST_TIME_SAMPLE,
            widthTimeSamples=float(np.abs(instants[0] - instants[-1])),
            isVisible=visible,
        )

    def set_visible(self, visible: bool) -> None:
        self.renderer.visible = visible

    def set_palette(self, palette: Palette) -> None:
        self.renderer.glyph.color_mapper.palette = palette

    def update(
        self,
        data: np_types.NDArray,
        x_positions: np_types.NDArray,
        instants: np_types.NDArray,
    ) -> None:
        self.source.data = {"image": [data]}
        x, dw = transforms.image_x_extent(x_positions)
        self.renderer.glyph.update(
            x=x,
            dw=dw,
            y=instants[0],
            dh=float(np.abs(instants[0] - instants[-1])),
        )
