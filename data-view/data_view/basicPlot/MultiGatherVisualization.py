import time

import numpy.typing as npt
from seismicio.Models.SuDataModel import SuFile

from ..transforms.clip import apply_clip_from_perc
from ..transforms.gain import apply_gain


class MultiGatherVisualization:

    def __init__(self, filename: str, gather_key: str) -> None:

        self.state: dict[str, int | float | str | None] = {
            "gather_index_start": 0,  # zero-based indexing
            "num_loadedgathers": 1,
            "percentile_clip": 100,
            "gain_option": "None",
            "wagc": 0.5,
            "num_gathers": None,
            "interval_time_samples": None,
            "num_time_samples": None,
        }

    @staticmethod
    def _optionally_apply_pencentile_clip(data: npt.NDArray, percentile: None | int) -> npt.NDArray:
        if (percentile is None) or percentile == 100:
            return data
        return apply_clip_from_perc(data, percentile)

    @staticmethod
    def _optionally_apply_gain(data: npt.NDArray, gain_option: str, wagc: float, dt: float) -> npt.NDArray:
        if gain_option == "None":
            return data
        return apply_gain(data, gain_option, wagc, dt)

    def handle_state_change(self):
        # WARNING: this function expects the index or slice to be correct
        start_time = time.perf_counter()
        print("CALL handle_state_change")

        gather_index_stop = self.state["gather_index_start"] + \
            self.state["num_loadedgathers"]

        if self.state["gather_index_start"] == gather_index_stop - 1:
            # *** Single gather

            data = self.sufile.igather[self.state["gather_index_start"]].data

            data = self._optionally_apply_gain(
                data,
                gain_option=self.state["gain_option"],
                wagc=self.state["wagc"],
                dt=self.state["interval_time_samples"],
            )
            data = self._optionally_apply_pencentile_clip(
                data,
                self.state["percentile_clip"]
            )

            self.seismic_plot_wrapper.update_plot(
                data=data,
                x_positions=self.sufile.igather[
                    self.state["gather_index_start"]
                ].headers["offset"],
                interval_time_samples=self.state["interval_time_samples"],
                gather_key="Offset [m]",
            )

    # changes between Stack and MultiGather classes:
    #   - data assignment at "handle_state_change"
    #       - 1 path for stack
    #       - 1 path for single-gather
    #       - 1 path for multi-gather
    #   - update_plot parameters, different for single-gather
    #       - different x_positions
    #       - different gather_key
    #           - gather_key miss on multi-gather?
        else:
            # *** Multiple gathers

            data = self.sufile.igather[self.state["gather_index_start"]: gather_index_stop].data

            data = self._optionally_apply_gain(
                data,
                gain_option=self.state["gain_option"],
                wagc=self.state["wagc"],
                dt=self.state["interval_time_samples"],
            )
            data = self._optionally_apply_pencentile_clip(
                data,
                self.state["percentile_clip"]
            )

            self.seismic_plot_wrapper.update_plot(
                data=data,
                x_positions=None,
                interval_time_samples=self.state["interval_time_samples"],
            )

        end_time = time.perf_counter()
        print(f"elapsed time: {end_time - start_time} seconds")
