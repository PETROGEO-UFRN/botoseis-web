import numpy as np
import numpy.typing as np_types
from typing import Literal
from seismicio.Models.SuDataModel import SuFile

from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.models import GlyphRenderer, ColumnDataSource

from ..BaseVisualization import BaseVisualization
from .VelanPlotOptionsState import VelanPlotOptionsState
from .data_operations import semblance
from .factories import (
    plotFactory,
    semblancePlotRendererFactory
)

FIRST_TIME_SAMPLE = 0.0
GATHER_KEY = "cdp"


class Visualization(BaseVisualization):
    sufile: SuFile
    cdp_gather_offsets: np_types.NDArray
    velocities: np_types.NDArray

    plots_row: row
    plots: dict[
        Literal["wiggle", "semblance", "image"],
        figure
    ]
    sources: dict[
        Literal["wiggle", "semblance", "image"],
        ColumnDataSource
    ]
    renderers: dict[
        Literal["wiggle", "semblance", "image"],
        GlyphRenderer
    ]

    def __init__(
        self,
        filename: str,
        plot_options_state: VelanPlotOptionsState,
    ) -> None:
        self.plots = dict()
        self.sources = dict()
        self.renderers = dict()

        super().__init__(
            filename=filename,
            plot_options_state=plot_options_state,
            gather_key=GATHER_KEY,
        )

        data = self.__getBaseData()
        coherence_matrix = self.__get_semblance_coherence_matrix(data)

        self.plots["semblance"] = plotFactory(
            x_label="Velocities (m/s)",
            y_label="Time (s)",
        )
        self.sources["semblance"] = ColumnDataSource(
            data={"image": [coherence_matrix]}
        )
        self.renderers["semblance"] = semblancePlotRendererFactory(
            plot=self.plots["semblance"],
            source=self.sources["semblance"],
            velocities=self.velocities,
            first_time_sample=FIRST_TIME_SAMPLE,
            width_time_samples=self.plot_options_state.width_time_samples,
            first_velocity_value=self.plot_options_state.first_velocity_value,
            last_velocity_value=self.plot_options_state.last_velocity_value,
        )
        self.plots_row = row(
            self.plots["semblance"],
            tags=[]
        )

    def __getBaseData(self):
        selected_gathers = self.sufile.gather[
            self.plot_options_state.gather_index_start
        ]

        cdp_gather_data = selected_gathers.data
        self.cdp_gather_offsets = selected_gathers.headers["offset"]

        last_time_sample = \
            FIRST_TIME_SAMPLE + \
            (self.plot_options_state.num_time_samples - 1) * \
            self.plot_options_state.interval_time_samples

        self.plot_options_state.width_time_samples = np.abs(
            last_time_sample - FIRST_TIME_SAMPLE
        )

        self.plot_options_state.updatePlotOptionsState(
            width_time_samples=self.plot_options_state.width_time_samples,
        )
        return cdp_gather_data

    def __get_semblance_coherence_matrix(self, data: np_types.NDArray):
        self.velocities = np.arange(
            self.plot_options_state.first_velocity_value,
            self.plot_options_state.last_velocity_value + 1,
            self.plot_options_state.velocity_step_size,
            dtype=float
        )

        num_time_samples = data.shape[0]
        num_traces = data.shape[1]

        coherence_matrix = semblance(
            sucmpdata=data,
            offsets=self.cdp_gather_offsets,
            velocities=self.velocities,
            t0_data=FIRST_TIME_SAMPLE,
            dt=self.plot_options_state.interval_time_samples,
            nt=num_time_samples,
            num_traces=num_traces,
            velocities_length=len(self.velocities),
        )
        return coherence_matrix

    def handle_state_change(self):
        data = self.__getBaseData()
        coherence_matrix = self.__get_semblance_coherence_matrix(data)
        self.sources["semblance"].data = {"image": [coherence_matrix]}
        self.renderers["semblance"].glyph.update(
            dh=self.plot_options_state.width_time_samples,
        )
