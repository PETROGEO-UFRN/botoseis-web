import time
from typing import Literal
import numpy.typing as np_types

from ..shared.BaseVisualization import BaseVisualization
from ..shared.gain import applyGain, GainType
from ..shared.colormaps import getColormap
from .PlotManager import PlotManager
from .plotOptionsState import PlotOptionsState


DEFAULT_GAIN: GainType = {"AGC": None, "GAUSSIAN_AGC": None, "PERCENTILE_CLIPPING": 100}


class Visualization(BaseVisualization):
    plot_options_state: PlotOptionsState
    plot_manager: PlotManager
    gain: GainType

    def __init__(
        self,
        filename: str,
        plot_options_state: PlotOptionsState,
        gather_key: str | None = None,
    ) -> None:
        super().__init__(filename, plot_options_state, gather_key)
        self.gain = dict(DEFAULT_GAIN)
        data = self.getBaseData()
        self.plot_manager = PlotManager(
            data=data,
            interval_time_samples=self.plot_options_state.interval_time_samples,
        )

    def updateColormap(self, colormap: Literal['grey','red_black','red_blue','blue_red','BuRd','RdGy']):
        self.plot_manager.updateImagePalette(getColormap(colormap))

    def updateImageVisibility(self, visible: bool):
        self.plot_manager.is_visible["image"] = visible
        self.plot_manager.renderers["image"].visible = visible

    def updateWiggleVisibility(self, visible: bool):
        self.plot_manager.is_visible["wiggle"] = visible
        self.plot_manager.renderers["wiggle"].visible = visible
        if visible:
            self.plot_manager.add_patches()
        else:
            self.plot_manager.remove_patches()

    def updateGain(self, gain: GainType):
        self.gain = {**self.gain, **gain}
        self.handle_state_change()

    def handle_state_change(self):
        data = self.getBaseData()
        data = applyGain(
            data,
            gain=self.gain,
            intervalTimeSamples=self.plot_options_state.interval_time_samples,
        )
        self.plot_manager.update_plot(
            data=data,
            x_positions=self.gather_offsets,
            interval_time_samples=self.plot_options_state.interval_time_samples,
        )
