import numpy as np
import numpy.typing as np_types
from typing import Literal
from seismicio.Models.SuDataModel import SuFile

from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.models import GlyphRenderer

from ..BaseVisualization import BaseVisualization
from .VelanPlotOptionsState import VelanPlotOptionsState
from .data_operations import semblance
from .factories import (
    plotFactory,
    semblancePlotRendererFactory
)


class Visualization(BaseVisualization):
    sufile: SuFile
    cdp_gather_offsets: np_types.NDArray
    velocities: np_types.NDArray

    plots_row: row
    plots: dict[
        Literal["wiggle", "semblance", "image"],
        figure
    ]
    renderers: dict[
        Literal["wiggle", "semblance", "image"],
        GlyphRenderer
    ]

    def __init__(
        self,
        filename: str,
        plot_options_state: VelanPlotOptionsState,
        gather_key: str | None = None,
    ) -> None:
        self.plots = dict()
        self.renderers = dict()

        super().__init__(
            filename,
            plot_options_state,
            gather_key,
        )

        data = self.__getBaseData()

        coherence_matrix = self.__get_semblance_coherence_matrix(data)

        self.plots["semblance"] = plotFactory(
            x_label="Velocities (m/s)",
            y_label="Time (s)",
        )
        self.renderers["semblance"] = semblancePlotRendererFactory(
            plot=self.plots["semblance"],
            coherence_matrix=coherence_matrix,
            velocities=self.velocities,
            first_time_sample=self.plot_options_state.first_time_sample,
            width_time_samples=self.plot_options_state.width_time_samples,
            first_velocity_value=self.plot_options_state.first_velocity_value,
            last_velocity_value=self.plot_options_state.last_velocity_value,
        )

    def __getBaseData(self):
        first_gather_index = self.plot_options_state.first_cdp
        last_gather_index = first_gather_index + \
            self.plot_options_state.number_of_gathers_per_time

        if first_gather_index == last_gather_index:
            selected_gathers = self.sufile.gather[
                first_gather_index
            ]
        else:
            selected_gathers = self.sufile.gather[
                first_gather_index:last_gather_index
            ]

        cdp_gather_data = selected_gathers.data
        self.cdp_gather_offsets = selected_gathers.headers["offset"]

        last_time_sample = \
            self.plot_options_state.first_time_sample + \
            (self.plot_options_state.num_time_samples - 1) * \
            self.plot_options_state.interval_time_samples

        self.plot_options_state.width_time_samples = np.abs(
            last_time_sample - self.plot_options_state.first_time_sample
        )

        self.plot_options_state.updatePlotOptionsState(
            first_time_sample=self.plot_options_state.first_time_sample,
            width_time_samples=self.plot_options_state.width_time_samples,
        )
        return cdp_gather_data

    def __get_semblance_coherence_matrix(self, data: np_types.NDArray):
        self.velocities = np.arange(
            self.plot_options_state.first_velocity_value,
            self.plot_options_state.last_velocity_value + 0.1,
            self.plot_options_state.velocity_step_size,
            dtype=float
        )

        num_time_samples = data.shape[0]
        num_traces = data.shape[1]

        coherence_matrix = semblance(
            sucmpdata=data,
            offsets=self.cdp_gather_offsets,
            velocities=self.velocities,
            t0_data=self.plot_options_state.first_time_sample,
            dt=self.plot_options_state.interval_time_samples,
            nt=num_time_samples,
            num_traces=num_traces,
            velocities_length=len(self.velocities),
        )
        return coherence_matrix

    def handle_state_change(self):
        pass
