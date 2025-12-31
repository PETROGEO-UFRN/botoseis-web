import math
import numpy as np
import numpy.typing as np_types
from typing import Literal

from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.models import GlyphRenderer, ColumnDataSource

from ..BaseVisualization import BaseVisualization, visualization_factories
from ..constants.VISUALIZATION import FIRST_TIME_SAMPLE, VELAN_GATHER_KEY, SMUTE
from .VelanPlotOptionsState import VelanPlotOptionsState
from .data_operations import operations
from .factories import (
    NMOCurveRendererFactory,
    semblancePlotRendererFactory
)

EMPTY_PICKING_DATA = {"x": [], "y": []}


class Visualization(BaseVisualization):
    plots_row: row
    picking_data: dict[
        int,
        dict[Literal["x", "y"], list[float]]
    ]
    sources: dict[
        Literal[
            "cdp_1",
            "semblance_1",
            "nmo_1",
            "picking_1",
            "curve_1",
            "cdp_2",
            "semblance_2",
            "nmo_2",
            "picking_2",
            "curve_2",
        ],
        ColumnDataSource
    ]
    plots: dict[
        Literal["cdp_1", "semblance_1", "cdp_2", "semblance_2"],
        figure
    ]
    renderers: dict[
        Literal["cdp_1", "semblance_1", "cdp_2", "semblance_2"],
        GlyphRenderer
    ]
    velocities: np_types.NDArray
    # *** last_selected_gather is used for not triggering picker data updates
    # *** while changing selected gathers
    last_selected_gather: int

    def __init__(
        self,
        filename: str,
        plot_options_state: VelanPlotOptionsState,
    ) -> None:
        self.plots = dict()
        self.sources = dict()
        self.renderers = dict()
        self.picking_data = dict()
        self.sources["picking_1"] = ColumnDataSource(data=EMPTY_PICKING_DATA)
        self.sources["picking_2"] = ColumnDataSource(data=EMPTY_PICKING_DATA)
        self.sources["curve_1"] = ColumnDataSource(data=EMPTY_PICKING_DATA)
        self.sources["curve_2"] = ColumnDataSource(data=EMPTY_PICKING_DATA)

        super().__init__(
            filename=filename,
            plot_options_state=plot_options_state,
            gather_key=VELAN_GATHER_KEY,
        )

        self.last_selected_gather = self.plot_options_state.gather_index_start
        self.velocities = np.arange(
            self.plot_options_state.first_velocity_value,
            self.plot_options_state.last_velocity_value + 1,
            self.plot_options_state.velocity_step_size,
            dtype=float
        )

        # *** duplicate everything
        for index in [1, 2]:
            cdp_key = f"cdp_{index}"
            semblance_key = f"semblance_{index}"
            picking_key = f"picking_{index}"
            curve_key = f"curve_{index}"

            current_gather_index = self.__get_current_gather_index(index)
            data = self.getShotGathersData(index_start=current_gather_index)
            coherence_matrix = self.__get_semblance_coherence_matrix(data)

            shared_image_renderer_parameters = {
                "offsets": self.gather_offsets,
                "first_time_sample": FIRST_TIME_SAMPLE,
                "width_time_samples": self.plot_options_state.width_time_samples,
            }
            self.sources[cdp_key] = ColumnDataSource(data={"image": [data]})
            self.plots[cdp_key] = visualization_factories.plotFactory(
                x_label="Offset (m)",
                y_label="Time (s)" if index == 1 else None,
            )
            self.renderers[cdp_key] = visualization_factories.imageRendererFactory(
                plot=self.plots[cdp_key],
                source=self.sources[cdp_key],
                **shared_image_renderer_parameters
            )
            NMOCurveRendererFactory(
                plot=self.plots[cdp_key],
                source=self.sources[curve_key],
            )

            self.sources[semblance_key] = ColumnDataSource(
                data={"image": [coherence_matrix]}
            )
            self.plots[semblance_key] = visualization_factories.plotFactory(
                x_label="Velocities (m/s)"
            )
            self.renderers[semblance_key] = semblancePlotRendererFactory(
                plot=self.plots[semblance_key],
                source=self.sources[semblance_key],
                picks_source=self.sources[picking_key],
                on_pick_update=self.save_picks_in_memory,
                index_in_plot_pair=index,

                velocities=self.velocities,
                first_time_sample=FIRST_TIME_SAMPLE,
                width_time_samples=self.plot_options_state.width_time_samples,
                first_velocity_value=self.plot_options_state.first_velocity_value,
                last_velocity_value=self.plot_options_state.last_velocity_value,
            )

        self.plots_row = row(
            self.plots["cdp_1"],
            self.plots["semblance_1"],
            self.plots["cdp_2"],
            self.plots["semblance_2"],
            sizing_mode="stretch_both",
            tags=[]
        )

    def update_time_curve_source(
        self,
        index_in_plot_pair,
        selected_time: float | None,
        selected_velocity: float | None,
    ):
        curve_key = f"curve_{index_in_plot_pair}"

        # *** Comparing directly to "None" avoiding edge cases where the values can be "0"
        if selected_time == None or selected_velocity == None:
            self.sources[curve_key].data = {"x": [], "y": []}
            return

        ys = []
        for offset in self.gather_offsets:
            y = (selected_time ** 2) + (offset ** 2) / (selected_velocity ** 2)
            ys.append(math.sqrt(y))
        curve_source_data = {"x": self.gather_offsets, "y": ys}
        self.sources[curve_key].data = curve_source_data

    def __get_current_gather_index(self, plot_index):
        if plot_index == 1:
            return self.plot_options_state.gather_index_start
        return self.plot_options_state.gather_index_start + \
            self.plot_options_state.number_of_gathers_per_time

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

    def save_picks_in_memory(self):
        if self.last_selected_gather != self.plot_options_state.gather_index_start:
            return
        for index in [1, 2]:
            picking_key = f"picking_{index}"
            current_gather_index = self.__get_current_gather_index(index)
            # *** Picking data must be converted to dict again
            # *** If not converted, data will not be accepted back by CollumnDataSource
            # *** Bokeh does not allow setting CollumnDataSource data with another CollumnDataSource data
            self.picking_data[current_gather_index] = dict(
                self.sources[picking_key].data
            )

    def apply_nmo(self):
        for index in [1, 2]:
            cdp_key = f"cdp_{index}"
            picking_key = f"picking_{index}"
            if len(self.sources[picking_key].data["y"]):
                data = self.sources[cdp_key].data["image"][0]
                interpolated_velocities_trace = operations.velocity_picks_to_trace(
                    npicks=len(self.sources[picking_key].data["y"]),
                    tnmo=self.sources[picking_key].data["y"],
                    vnmo=self.sources[picking_key].data["x"],
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
                self.sources[cdp_key].data = {"image": [nmo_corrected_data]}

    def handle_state_change(self):
        for index in [1, 2]:
            cdp_key = f"cdp_{index}"
            semblance_key = f"semblance_{index}"
            picking_key = f"picking_{index}"
            current_gather_index = self.__get_current_gather_index(index)

            data = self.getShotGathersData(index_start=current_gather_index)
            coherence_matrix = self.__get_semblance_coherence_matrix(data)
            self.sources[semblance_key].data = {"image": [coherence_matrix]}
            self.renderers[semblance_key].glyph.update(
                dh=self.plot_options_state.width_time_samples,
            )
            self.sources[cdp_key].data = {"image": [data]}
            self.renderers[cdp_key].glyph.update(
                dh=self.plot_options_state.width_time_samples,
            )
            if current_gather_index in self.picking_data:
                self.sources[picking_key].data = self.picking_data[current_gather_index]
            else:
                self.sources[picking_key].data = EMPTY_PICKING_DATA
        self.last_selected_gather = self.plot_options_state.gather_index_start
