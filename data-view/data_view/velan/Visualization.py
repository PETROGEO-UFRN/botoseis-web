import numpy as np
import numpy.typing as np_types
from typing import Literal
from seismicio.Models.SuDataModel import SuFile

from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.models import GlyphRenderer, ColumnDataSource

from ..BaseVisualization import BaseVisualization
from .VelanPlotOptionsState import VelanPlotOptionsState
from .data_operations import operations
from .factories import (
    plotFactory,
    semblancePlotRendererFactory,
    imagePlotRendererFactory,
)

FIRST_TIME_SAMPLE = 0.0
GATHER_KEY = "cdp"
SMUTE = 1.5


class Visualization(BaseVisualization):
    sufile: SuFile
    cdp_gather_offsets: np_types.NDArray
    velocities: np_types.NDArray

    plots_row: row
    sources: dict[
        Literal["raw_cdp", "semblance", "nmo", "picking"],
        ColumnDataSource
    ]
    plots: dict[
        Literal["raw_cdp", "semblance", "nmo"],
        figure
    ]
    renderers: dict[
        Literal["raw_cdp", "semblance", "nmo"],
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
        self.sources["picking"] = ColumnDataSource(data={"x": [], "y": []})

        super().__init__(
            filename=filename,
            plot_options_state=plot_options_state,
            gather_key=GATHER_KEY,
        )

        data = self.__getBaseData()
        width_offsets = np.abs(
            self.cdp_gather_offsets[0] - self.cdp_gather_offsets[-1]
        )
        coherence_matrix = self.__get_semblance_coherence_matrix(data)

        self.sources["raw_cdp"] = ColumnDataSource(
            data={"image": [data]}
        )
        self.plots["raw_cdp"] = plotFactory(
            x_label="Offset (m)",
            y_label="Time (s)",
        )
        self.renderers["raw_cdp"] = imagePlotRendererFactory(
            plot=self.plots["raw_cdp"],
            source=self.sources["raw_cdp"],
            picks_source=self.sources["picking"],
            offsets=self.cdp_gather_offsets,
            first_time_sample=FIRST_TIME_SAMPLE,
            width_time_samples=self.plot_options_state.width_time_samples,
            width_offsets=width_offsets,
        )

        self.sources["semblance"] = ColumnDataSource(
            data={"image": [coherence_matrix]}
        )
        self.plots["semblance"] = plotFactory(
            x_label="Velocities (m/s)",
        )
        self.renderers["semblance"] = semblancePlotRendererFactory(
            plot=self.plots["semblance"],
            source=self.sources["semblance"],
            picks_source=self.sources["picking"],
            velocities=self.velocities,
            first_time_sample=FIRST_TIME_SAMPLE,
            width_time_samples=self.plot_options_state.width_time_samples,
            first_velocity_value=self.plot_options_state.first_velocity_value,
            last_velocity_value=self.plot_options_state.last_velocity_value,
        )

        self.sources["nmo"] = ColumnDataSource(
            data={"image": [data]}
        )
        self.plots["nmo"] = plotFactory(
            x_label="Offset (m)",
        )
        self.renderers["nmo"] = imagePlotRendererFactory(
            plot=self.plots["nmo"],
            source=self.sources["nmo"],
            picks_source=self.sources["picking"],
            offsets=self.cdp_gather_offsets,
            first_time_sample=FIRST_TIME_SAMPLE,
            width_time_samples=self.plot_options_state.width_time_samples,
            width_offsets=width_offsets,
        )
        self.plots_row = row(
            self.plots["raw_cdp"],
            self.plots["semblance"],
            self.plots["nmo"],
            sizing_mode="stretch_both",
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

        coherence_matrix = operations.semblance(
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

    def apply_nmo(self):
        data = self.sources["raw_cdp"].data["image"][0]
        picks_times = self.sources["picking"].data["y"]
        picks_velocities = self.sources["picking"].data["x"],
        interpolated_velocities_trace = operations.velocity_picks_to_trace(
            npicks=len(picks_times),
            tnmo=picks_times,
            vnmo=picks_velocities,
            t0_data=FIRST_TIME_SAMPLE,
            dt=self.plot_options_state.interval_time_samples,
            nt=data.shape[0],
        )
        nmo_corrected_data = operations.apply_nmo(
            ntracescmp=data.shape[1],
            nt=data.shape[0],
            t0_data=FIRST_TIME_SAMPLE,
            dt=self.plot_options_state.interval_time_samples,
            cmpdata=data,
            offsets=self.cdp_gather_offsets,
            vnmo_trace=interpolated_velocities_trace,
            smute=SMUTE,
        )
        self.sources["nmo"].data = {"image": [nmo_corrected_data]}

    def handle_state_change(self):
        data = self.__getBaseData()
        coherence_matrix = self.__get_semblance_coherence_matrix(data)
        self.sources["semblance"].data = {"image": [coherence_matrix]}
        self.renderers["semblance"].glyph.update(
            dh=self.plot_options_state.width_time_samples,
        )
