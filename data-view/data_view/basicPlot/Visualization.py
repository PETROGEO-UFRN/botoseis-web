import time
import numpy.typing as np_types
from bokeh.palettes import Greys256, BuRd9, RdGy11
from typing import Literal
from seismicio.Models.SuDataModel import SuFile

from ..transforms.clip import apply_clip_from_perc
from ..transforms.gain import apply_gain

from .get_sufile import get_stack_sufile, get_multi_gather_sufile
from .PlotOptionsState import PlotOptionsState
from .PlotManager import PlotManager


class Visualization:
    sufile: SuFile
    x_positions: np_types.NDArray | None
    plot_options_state: PlotOptionsState
    plot_manager: PlotManager

    def __init__(
        self,
        filename: str,
        plot_options_state: PlotOptionsState,
        gather_key: str | None = None,
    ) -> None:
        self.plot_options_state = plot_options_state
        if gather_key:
            self.sufile: SuFile = get_multi_gather_sufile(
                plot_options=self.plot_options_state.__dict__,
                filename=filename,
                gather_key=gather_key,
            )
        else:
            self.sufile = get_stack_sufile(
                plot_options=self.plot_options_state.__dict__,
                filename=filename,
            )

        # !!! check if "gather_keyword" exist
        # !!! is must exist for shot gathers
        if self.sufile.gather_keyword:
            data = self.__getDataForShotGathers()
        else:
            data = self.sufile.traces
            self.x_positions = None
        self.plot_manager = PlotManager(
            data=data,
            interval_time_samples=self.plot_options_state.interval_time_samples,
        )

    @staticmethod
    def __optionally_apply_pencentile_clip(data: np_types.NDArray, percentile: None | int) -> np_types.NDArray:
        if (percentile is None) or percentile == 100:
            return data
        return apply_clip_from_perc(data, percentile)

    @staticmethod
    def __optionally_apply_gain(data: np_types.NDArray, gain_option: str, wagc: float, dt: float) -> np_types.NDArray:
        if gain_option == None:
            return data
        return apply_gain(data, gain_option, wagc, dt)

    def __getDataForShotGathers(self):
        gather_index_start = self.plot_options_state.gather_index_start
        gather_index_stop = gather_index_start + \
            self.plot_options_state.num_loadedgathers

        data = self.sufile.igather[
            gather_index_start:gather_index_stop
        ].data

        if (gather_index_stop - 1 == gather_index_start):
            # *** Single gather
            self.x_positions = self.sufile.igather[
                gather_index_start
            ].headers["offset"]
            return data

        # *** Multiple gathers
        self.x_positions = None
        return data

    def handle_palette_change(
        self,
        selectedPalette: Literal["grey", "BuRd", "RdGy"]
    ):
        if selectedPalette == "grey":
            return self.plot_manager.updateImagePalette(Greys256)
        if selectedPalette == "BuRd":
            return self.plot_manager.updateImagePalette(BuRd9)
        if selectedPalette == "RdGy":
            return self.plot_manager.updateImagePalette(RdGy11)

    def toogle_visibility_by_type(
        self,
        renderer_type: Literal["toggle_image", "toggle_wiggle", "toggle_areas"]
    ) -> bool:
        if renderer_type == "toggle_image":
            is_visible = not self.plot_manager.is_image_visible
            self.plot_manager.is_image_visible = is_visible
            self.plot_manager.image_renderer.visible = is_visible
            return is_visible
        if renderer_type == "toggle_wiggle":
            is_visible = not self.plot_manager.is_wiggle_visible
            self.plot_manager.is_wiggle_visible = is_visible
            self.plot_manager.wiggle_renderer.visible = is_visible
            return is_visible
        if renderer_type == "toggle_areas":
            is_visible = not self.plot_manager.is_areas_visible
            self.plot_manager.is_areas_visible = is_visible
            self.plot_manager.areas_renderer.visible = is_visible
            return is_visible

    def handle_state_change(self):
        start_time = time.perf_counter()
        print("CALL handle_state_change")

        # !!! check if "gather_keyword" exist
        # !!! is must exist for shot gathers
        if self.sufile.gather_keyword:
            data = self.__getDataForShotGathers()
        else:
            data = self.sufile.traces
            self.x_positions = None

        data = self.__optionally_apply_gain(
            data,
            gain_option=self.plot_options_state.gain_option,
            wagc=self.plot_options_state.wagc,
            dt=self.plot_options_state.interval_time_samples,
        )
        data = self.__optionally_apply_pencentile_clip(
            data,
            self.plot_options_state.percentile_clip
        )

        self.plot_manager.update_plot(
            data=data,
            x_positions=self.x_positions,
            interval_time_samples=self.plot_options_state.interval_time_samples,
        )

        end_time = time.perf_counter()
        print(f"elapsed time: {end_time - start_time} seconds")
