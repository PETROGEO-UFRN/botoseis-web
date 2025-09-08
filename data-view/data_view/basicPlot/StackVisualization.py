import time

import numpy.typing as npt
from bokeh.layouts import column, row
from bokeh.models import Paragraph
from seismicio.Models.SuDataModel import SuFile

from ..widgets import widgets
from ..transforms.clip import apply_clip_from_perc
from ..transforms.gain import apply_gain
from .get_sufile import get_stack_sufile


class StackVisualization:

    def __init__(self, filename: str) -> None:

        self.state: dict[str, int | float | str | None] = {
            "percentile_clip": 100,
            "gain_option": "None",
            "wagc": 0.5,
            "interval_time_samples": None,
            "num_time_samples": None,
        }

        self.sufile: SuFile = get_stack_sufile(self.state, filename)

        self.seismic_plot_wrapper = widgets.create_seismic_plot_wrapper(
            self.state,
            self.sufile
        )
        self.seismic_plot_wrapper.toggle_wiggle_visible(False)

        percentile_clip_input = widgets.create_percentile_clip_input(
            self.state,
            self.handle_state_change,
        )
        gain_option_picker = widgets.create_gain_option_picker(
            self.state,
            self.handle_state_change,
        )
        wagc_input = widgets.create_wagc_input(
            self.state,
            self.handle_state_change,
        )

        left_tools_column = column(
            row(Paragraph(text="Image"), self.seismic_plot_wrapper.image_switch),
            row(Paragraph(text="Wiggle"), self.seismic_plot_wrapper.wiggle_switch),
            row(Paragraph(text="Areas"), self.seismic_plot_wrapper.areas_switch),
            percentile_clip_input,
            gain_option_picker,
            wagc_input,
        )
        row_tools_figure = row(
            children=[left_tools_column, self.seismic_plot_wrapper.plot],
            sizing_mode="stretch_both"
        )
        self.root_layout = column(
            children=[row_tools_figure],
            sizing_mode="stretch_both"
        )

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
        start_time = time.perf_counter()
        print("CALL handle_state_change")

        data = self.sufile.traces

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
