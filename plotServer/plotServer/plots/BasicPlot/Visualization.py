from typing import Literal

import numpy as np
import numpy.typing as np_types
from bokeh.plotting import figure

from ..shared.BaseVisualization import BaseVisualization
from ..shared.gain import applyGain, GainType
from ..shared.colormaps import getColormap
from ..shared.plotFactory import plotFactory
from . import transforms
from .displays import ImageDisplay, WiggleDisplay
from .plotOptionsState import PlotOptionsState


DEFAULT_GAIN: GainType = {"AGC": None, "GAUSSIAN_AGC": None, "PERCENTILE_CLIPPING": 100}
ColormapName = Literal['grey', 'red_black', 'red_blue', 'blue_red', 'BuRd', 'RdGy']


class Visualization(BaseVisualization):
    """The BasicPlot seismic section: a Bokeh figure showing the data as an image
    and/or as wiggle traces.

    Responsibilities kept here are the section's own: loading the current data
    (via BaseVisualization), applying gain, and deriving the trace positions and
    time axis. The two display representations are delegated to ImageDisplay and
    WiggleDisplay; pure math lives in :mod:`transforms`.
    """

    plot: figure
    plot_options_state: PlotOptionsState
    gain: GainType
    image: ImageDisplay
    wiggle: WiggleDisplay

    def __init__(
        self,
        filename: str,
        plot_options_state: PlotOptionsState,
        gather_key: str | None = None,
    ) -> None:
        super().__init__(filename, plot_options_state, gather_key)
        self.gain = dict(DEFAULT_GAIN)

        data, x_positions, instants = self._prepare_render()
        self.plot = plotFactory(yAxisLabel="Time (s)", isYAxisFlipped=True)
        # Image first, wiggle second, so the wiggle draws on top of the image.
        self.image = ImageDisplay(self.plot, data, x_positions, instants, visible=True)
        self.wiggle = WiggleDisplay(self.plot, data, x_positions, instants, visible=False)

    # *** Bridge actions (contract preserved) ***

    def updateColormap(self, colormap: ColormapName):
        self.image.set_palette(getColormap(colormap))

    def updateImageVisibility(self, visible: bool):
        self.image.set_visible(visible)

    def updateWiggleVisibility(self, visible: bool):
        self.wiggle.set_visible(visible)

    def updateGain(self, gain: GainType):
        self.gain = {**self.gain, **gain}
        self.handle_state_change()

    def updateGatherIndex(self, gatherIndex: int):
        self.plot_options_state.updatePlotOptionsState(gather_index_start=gatherIndex - 1)
        self.handle_state_change()

    def updateLoadCount(self, loadCount: int):
        self.plot_options_state.updatePlotOptionsState(num_loadedgathers=loadCount)
        self.handle_state_change()

    # *** Rendering ***

    def handle_state_change(self):
        data, x_positions, instants = self._prepare_render()
        self.image.update(data, x_positions, instants)
        self.wiggle.update(data, x_positions, instants)

    def _prepare_render(self) -> tuple[np_types.NDArray, np_types.NDArray, np_types.NDArray]:
        """Load the current section, apply gain, and derive trace positions and
        the time axis. Single source of truth, so first paint and every repaint
        go through the same pipeline (data + offsets + gain)."""
        data = self.getBaseData()  # also populates self.gather_offsets
        data = applyGain(
            data,
            gain=self.gain,
            intervalTimeSamples=self.plot_options_state.interval_time_samples,
        )
        transforms.check_data(data)

        x_positions = self.gather_offsets
        if x_positions is None:
            x_positions = np.arange(start=1, stop=data.shape[1] + 1)
        transforms.check_x_positions(x_positions, data.shape[1])

        instants = transforms.time_sample_instants(
            data.shape[0], self.plot_options_state.interval_time_samples
        )
        return data, x_positions, instants
