import numpy as np
import numpy.typing as np_types
from typing import Literal
from seismicio.Models.SuDataModel import SuFile

from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.models import GlyphRenderer, ColumnDataSource

from ..BaseVisualization import BaseVisualization, visualization_factories
from ..constants.VISUALIZATION import FIRST_TIME_SAMPLE, VELAN_GATHER_KEY, SMUTE
from .VelanPlotOptionsState import VelanPlotOptionsState
from .data_operations import operations
from .factories import (
    semblancePlotRendererFactory
)


class Visualization(BaseVisualization):
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
    velocities: np_types.NDArray

    def __init__(
        self,
        filename: str,
        plot_options_state: VelanPlotOptionsState,
    ) -> None:
        self.plots = dict()
        self.sources = dict()
        self.renderers = dict()
        self.sources["picking"] = ColumnDataSource(
            data={"x": [], "y": []}
        )

        super().__init__(
            filename=filename,
            plot_options_state=plot_options_state,
            gather_key=VELAN_GATHER_KEY,
        )

        self.velocities = np.arange(
            self.plot_options_state.first_velocity_value,
            self.plot_options_state.last_velocity_value + 1,
            self.plot_options_state.velocity_step_size,
            dtype=float
        )
        data = self.getBaseData()
        coherence_matrix = self.__get_semblance_coherence_matrix(data)
        shared_image_renderer_parameters = {
            "offsets": self.gather_offsets,
            "first_time_sample": FIRST_TIME_SAMPLE,
            "width_time_samples": self.plot_options_state.width_time_samples,
        }

        self.sources["raw_cdp"] = ColumnDataSource(data={"image": [data]})
        self.plots["raw_cdp"] = visualization_factories.plotFactory(
            x_label="Offset (m)",
            y_label="Time (s)",
        )
        self.renderers["raw_cdp"] = visualization_factories.imageRendererFactory(
            plot=self.plots["raw_cdp"],
            source=self.sources["raw_cdp"],
            **shared_image_renderer_parameters
        )

        self.sources["semblance"] = ColumnDataSource(
            data={"image": [coherence_matrix]}
        )
        self.plots["semblance"] = visualization_factories.plotFactory(
            x_label="Velocities (m/s)"
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

        self.sources["nmo"] = ColumnDataSource(data={"image": [data]})
        self.plots["nmo"] = visualization_factories.plotFactory(
            x_label="Offset (m)"
        )
        self.renderers["nmo"] = visualization_factories.imageRendererFactory(
            plot=self.plots["nmo"],
            source=self.sources["nmo"],
            **shared_image_renderer_parameters
        )
        self.plots_row = row(
            self.plots["raw_cdp"],
            self.plots["semblance"],
            self.plots["nmo"],
            sizing_mode="stretch_both",
            tags=[]
        )

    def __get_semblance_coherence_matrix(self, data: np_types.NDArray):
        num_time_samples = data.shape[0]
        num_traces = data.shape[1]

        coherence_matrix = operations.semblance(
            sucmpdata=data,
            offsets=self.gather_offsets,
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
        interpolated_velocities_trace = operations.velocity_picks_to_trace(
            npicks=len(self.sources["picking"].data["y"]),
            tnmo=self.sources["picking"].data["y"],
            vnmo=self.sources["picking"].data["x"],
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
            offsets=self.gather_offsets,
            vnmo_trace=interpolated_velocities_trace,
            smute=SMUTE,
        )
        self.sources["nmo"].data = {"image": [nmo_corrected_data]}

    def handle_state_change(self):
        data = self.getBaseData()
        coherence_matrix = self.__get_semblance_coherence_matrix(data)
        self.sources["semblance"].data = {"image": [coherence_matrix]}
        self.renderers["semblance"].glyph.update(
            dh=self.plot_options_state.width_time_samples,
        )
        self.sources["raw_cdp"].data = {"image": [data]}
        self.renderers["raw_cdp"].glyph.update(
            dh=self.plot_options_state.width_time_samples,
        )
        self.sources["nmo"].data = {"image": [data]}
        self.renderers["nmo"].glyph.update(
            dh=self.plot_options_state.width_time_samples,
        )
