from typing import Literal
from bokeh.models import ColumnDataSource, GlyphRenderer
from bokeh.plotting import figure
from bokeh.palettes import Palette
import numpy as np
import numpy.typing as np_types

from ..BaseVisualization import visualization_factories
from ..constants.VISUALIZATION import (
    FIRST_TIME_SAMPLE,
    MAX_TRACES_LINE_HAREA,
    STRETCH_FACTOR,
)


class PlotManager:
    plot: figure
    sources: dict[
        Literal["wiggle", "image"],
        ColumnDataSource
    ]
    renderers: dict[
        Literal["wiggle", "image", "hareas"],
        GlyphRenderer
    ]
    is_visible: dict[
        Literal["wiggle", "image"],
        bool
    ]
    __patches_source: dict[str, str]

    def __init__(
        self,
        data: np_types.NDArray,
        interval_time_samples: float,
        x_positions: np_types.NDArray | None = None,
        gather_key: str | None = None,
    ):
        self.sources = dict()
        self.renderers = dict()
        self.is_visible = dict()
        self.is_visible["image"] = True
        self.is_visible["wiggle"] = False

        self._check_data(data)
        num_time_samples = data.shape[0]
        num_traces = data.shape[1]
        if x_positions is None:
            x_positions = np.arange(start=1, stop=num_traces + 1)
        self._check_x_positions(x_positions, num_traces)
        last_time_sample = (
            FIRST_TIME_SAMPLE +
            (num_time_samples - 1) *
            interval_time_samples
        )
        time_sample_instants = np.linspace(
            start=FIRST_TIME_SAMPLE,
            stop=last_time_sample,
            num=num_time_samples
        )

        self.plot = visualization_factories.plotFactory(
            y_label="Time (s)",
            gather_key=gather_key,
        )

        width_time_samples = np.abs(
            time_sample_instants[0] - time_sample_instants[-1]
        )

        self.sources["image"] = ColumnDataSource(data={"image": [data]})
        # Amplitudes rescaled (data for wiggle renderers)
        data_rescaled = self._rescale_data(data, x_positions)
        self.sources["wiggle"] = ColumnDataSource(
            data=self.__compute_wiggle_source_data(
                data_rescaled,
                x_positions,
                time_sample_instants
            )
        )

        self.renderers["image"] = visualization_factories.imageRendererFactory(
            plot=self.plot,
            source=self.sources["image"],

            offsets=x_positions,
            first_time_sample=FIRST_TIME_SAMPLE,
            width_time_samples=width_time_samples,
            is_visible=self.is_visible["image"],
        )
        # wiggle_renderer shall be created after image_renderer.
        # Bokeh places the most recently created renderer on top.
        # If image is placed on top, wiggle will be invisible.
        self.renderers["wiggle"] = visualization_factories.wiggleRendererFactory(
            plot=self.plot,
            source=self.sources["wiggle"],
            is_visible=self.is_visible["wiggle"],
        )

        if self.is_visible["wiggle"]:
            self.__patches_source = {
                "data": data_rescaled,
                "x_positions": x_positions,
                "time_sample_instants": time_sample_instants,
            }
            self.add_patches()

    def updateImagePalette(self, palette: Palette):
        self.renderers["image"].glyph.color_mapper.palette = palette

    @staticmethod
    def _check_data(data):
        if type(data).__module__ != np.__name__:
            raise TypeError("data must be a numpy array")
        if len(data.shape) != 2:
            raise ValueError("data must be a 2D array")

    @staticmethod
    def _check_x_positions(x_positions, num_traces):
        if type(x_positions).__module__ != np.__name__:
            raise TypeError("x_positions must be a numpy array")
        if len(x_positions.shape) != 1:
            raise ValueError("x_positions must be a 1D array")
        if x_positions.size != num_traces:
            raise ValueError(
                "The size of x_positions must be equal to the number of "
                "columns in data, that is, it must be equal to the number "
                "of traces"
            )

    @staticmethod
    def _rescale_data(data: np_types.NDArray, x_positions: np_types.NDArray):
        # if there is only one trace, no need to rescale
        if data.shape[1] == 1:
            # normalize between -1 and 1
            return data / np.max(np.abs(data))

        # Minimum trace horizontal spacing
        trace_x_spacing = np.min(np.diff(x_positions))

        # Rescale data by trace_x_spacing and stretch_factor
        data_max_std = np.max(np.std(data, axis=0))
        data_rescaled = data / data_max_std * trace_x_spacing * STRETCH_FACTOR
        return data_rescaled

    @staticmethod
    def __compute_wiggle_source_data(
        data: np_types.NDArray,
        x_positions: np_types.NDArray,
        time_sample_instants: np_types.NDArray,
    ):
        num_traces = data.shape[1]

        xs_list = []
        ys_list = []
        for trace_index in range(num_traces):
            x_position = x_positions[trace_index]
            amplitudes = data[:, trace_index]

            # construct CDS for line render
            xs_list.append(amplitudes + x_position)
            ys_list.append(time_sample_instants)

        data_repositioned = data + x_positions
        xs_list = data_repositioned.T.tolist()
        ys_list = [time_sample_instants for _ in range(num_traces)]
        return {"xs": xs_list, "ys": ys_list}

    def remove_patches(self):
        """Remove patches glyph renderers from this plot"""
        self.plot.renderers = list(
            filter(lambda gl: gl.name != "H", self.plot.renderers)
        )

    def add_patches(self):
        data = self.__patches_source["data"]
        x_positions = self.__patches_source["x_positions"]
        time_sample_instants = self.__patches_source["time_sample_instants"]

        num_time_samples = data.shape[0]
        num_traces = data.shape[1]

        # Cancel if there are too many traces
        if num_traces > MAX_TRACES_LINE_HAREA:
            return

        data_positive = np.clip(data, a_min=0, a_max=None)
        y_value = np.concatenate(
            [time_sample_instants, time_sample_instants[::-1]]
        )
        xs = []
        ys = []
        for x_pos, trace in zip(x_positions, data_positive.T):
            x_poly = np.concatenate([
                # *** Baseline (Vertical)
                np.full(num_time_samples, x_pos),
                # *** Wiggle (Reversed)
                (x_pos + trace)[::-1]
            ])

            xs.append(x_poly)
            ys.append(y_value)

        self.plot.patches(
            xs=xs,
            ys=ys,
            color="black",
            name="H",
            line_width=0,
            visible=self.is_visible["wiggle"],
        )

    def _update_image_glyph(self, x_positions: np_types.NDArray, time_sample_instants: np_types.NDArray):
        num_traces = x_positions.size
        first_time_sample = time_sample_instants[0]
        width_time_samples = np.abs(
            time_sample_instants[0] - time_sample_instants[-1]
        )
        if num_traces == 1:
            self.renderers["image"].glyph.update(
                x=x_positions[0] - 1,
                dw=2,
                y=first_time_sample,
                dh=width_time_samples,
            )
        else:
            width_x_positions = np.abs(x_positions[0] - x_positions[-1])
            distance_first_x_positions = x_positions[1] - x_positions[0]
            distance_last_x_positions = x_positions[-1] - x_positions[-2]
            self.renderers["image"].glyph.update(
                x=x_positions[0] - distance_first_x_positions / 2,
                dw=(
                    width_x_positions +
                    (distance_first_x_positions + distance_last_x_positions) /
                    2
                ),
                y=first_time_sample,
                dh=width_time_samples,
            )

    def update_plot(
        self,
        data: np_types.NDArray,
        x_positions: np_types.NDArray | None,
        interval_time_samples: float,
    ):
        self._check_data(data)
        num_time_samples = data.shape[0]
        num_traces = data.shape[1]
        if x_positions is None:
            x_positions = np.arange(start=1, stop=num_traces + 1)
        self._check_x_positions(x_positions, num_traces)
        last_time_sample = (
            FIRST_TIME_SAMPLE +
            (num_time_samples - 1) *
            interval_time_samples
        )
        time_sample_instants = np.linspace(
            start=FIRST_TIME_SAMPLE,
            stop=last_time_sample,
            num=num_time_samples
        )

        if self.is_visible["image"]:
            self.sources["image"].data = {"image": [data]}
            self._update_image_glyph(x_positions, time_sample_instants)

        if self.is_visible["wiggle"]:
            data_rescaled = self._rescale_data(data, x_positions)
            self.sources["wiggle"].data = self.__compute_wiggle_source_data(
                data_rescaled,
                x_positions,
                time_sample_instants
            )
            self.remove_patches()
            self.__patches_source = {
                "data": data_rescaled,
                "x_positions": x_positions,
                "time_sample_instants": time_sample_instants,
            }
            self.add_patches()
