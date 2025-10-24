import time
import numpy.typing as np_types
from typing import Literal

from ..BaseVisualization import BaseVisualization
from ..transforms.clip import apply_clip_from_perc
from ..transforms.gain import apply_gain

from .PlotOptionsState import PlotOptionsState
from .PlotManager import PlotManager
from .get_plot_palette import get_plot_pallete


class Visualization(BaseVisualization):
    x_positions: np_types.NDArray | None
    plot_options_state: PlotOptionsState
    plot_manager: PlotManager

    def __init__(
        self,
        filename: str,
        plot_options_state: PlotOptionsState,
        gather_key: str | None = None,
    ) -> None:
        super().__init__(
            filename,
            plot_options_state,
            gather_key,
        )

        data = self.getBaseData()

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

    def handle_palette_change(
        self,
        selectedPalette: Literal[
            "grey", "red_black", "red_blue", "blue_red", "BuRd", "RdGy"
        ]
    ):
        return self.plot_manager.updateImagePalette(
            get_plot_pallete(selectedPalette)
        )

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
            is_visible = not self.plot_manager.is_hareas_visible
            self.plot_manager.is_hareas_visible = is_visible
            if is_visible:
                self.plot_manager.add_hareas()
                return is_visible
            self.plot_manager.remove_hareas()
            return is_visible

    def handle_state_change(self):
        start_time = time.perf_counter()
        print("CALL handle_state_change")

        data = self.getBaseData()

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
