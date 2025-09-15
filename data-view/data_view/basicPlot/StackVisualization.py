import time
import numpy.typing as np_types
from seismicio.Models.SuDataModel import SuFile

from ..transforms.clip import apply_clip_from_perc
from ..transforms.gain import apply_gain

from .get_sufile import get_stack_sufile, get_multi_gather_sufile
from .PlotOptionsState import PlotOptionsState
from .PlotManager import PlotManager


class Visualization:
    sufile: SuFile
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

        self.plot_manager = PlotManager(
            data=self.sufile.traces,
            interval_time_samples=self.plot_options_state.interval_time_samples,
        )

    @staticmethod
    def __optionally_apply_pencentile_clip(data: np_types.NDArray, percentile: None | int) -> np_types.NDArray:
        if (percentile is None) or percentile == 100:
            return data
        return apply_clip_from_perc(data, percentile)

    @staticmethod
    def __optionally_apply_gain(data: np_types.NDArray, gain_option: str, wagc: float, dt: float) -> np_types.NDArray:
        if gain_option == "None":
            return data
        return apply_gain(data, gain_option, wagc, dt)

    def handle_state_change(self):
        start_time = time.perf_counter()
        print("CALL handle_state_change")

        data = self.sufile.traces

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
            x_positions=None,
            interval_time_samples=self.plot_options_state.interval_time_samples,
        )

        end_time = time.perf_counter()
        print(f"elapsed time: {end_time - start_time} seconds")
