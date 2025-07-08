import numpy.typing as npt
from bokeh.models import ColumnDataSource, GlyphRenderer, Switch
import numpy as np
import numpy.typing as npt
from bokeh.plotting import figure


MAX_TRACES_LINE_HAREA = 10


class SeismicPlotWrapper:

    image_switch: Switch | None = None
    wiggle_switch: Switch | None = None
    areas_switch: Switch | None = None

    def __init__(
        self,
        data: npt.NDArray,
        x_positions: npt.NDArray | None,
        interval_time_samples: float,
        time_unit: str = "s",
        stretch_factor: float = 0.15,
        color: str = "black",
        gather_key: str | None = None,
    ):
        # Input checks
        # ------------
        self._check_stretch_factor(stretch_factor)
        self._check_data(data)
        num_time_samples = data.shape[0]
        num_traces = data.shape[1]
        if x_positions is None:
            x_positions = np.arange(start=1, stop=num_traces + 1)
        else:
            self._check_x_positions(x_positions, num_traces)

        # Create and set up figure object
        # -------------------------------
        self.plot: figure = figure(
            x_axis_location="above",
            height=800,
            width=1000,
            sizing_mode="stretch_both",
            active_drag=None,
        )

        # Adjust ranges
        self.plot.x_range.range_padding = 0.0
        self.plot.y_range.range_padding = 0.0
        self.plot.y_range.flipped = True

        # Adjust axes labels
        if gather_key:
            self.plot.xaxis.axis_label = gather_key
        else:
            self.plot.xaxis.axis_label = "trace sequential number"
        if time_unit == "s":
            self.plot.yaxis.axis_label = "Time (s)"
        elif time_unit == "ms":
            self.plot.yaxis.axis_label = "Time (ms)"

        # Amplitudes rescaled (data for wiggle renderers)
        data_rescaled = self._rescale_data(data, x_positions, stretch_factor)

        # Time sample instants (data for all renderers)
        first_time_sample = 0.0
        # ! REVOKE THIS CHANGE
        last_time_sample = first_time_sample + \
            (num_time_samples - 1) * interval_time_samples
        time_sample_instants = np.linspace(
            start=first_time_sample, stop=last_time_sample, num=num_time_samples
        )

        # Create ColumnDataSource objects
        # -------------------------------

        # Create image source
        self.image_source = ColumnDataSource(data={"image": [data]})

        # Create wiggle renderer's source
        self.wiggle_source = ColumnDataSource(
            data=self._compute_wiggle_source_data(
                data_rescaled, x_positions, time_sample_instants
            )
        )

        # Add renderers
        # -------------

        # --- Add (single) image renderer ---
        # auxiliary data for image renderer parameters
        width_time_sample_instants = np.abs(
            time_sample_instants[0] - time_sample_instants[-1]
        )
        if num_traces == 1:
            self.image_renderer: GlyphRenderer = self.plot.image(
                image="image",
                source=self.image_source,
                x=x_positions[0] - 1,
                y=first_time_sample,
                dw=2,
                dh=width_time_sample_instants,
                palette="Greys256",
                anchor="bottom_left",
                origin="bottom_left",
            )
        else:
            # more auxiliary data for image renderer parameters
            width_x_positions = np.abs(x_positions[0] - x_positions[-1])
            distance_first_x_positions = x_positions[1] - x_positions[0]
            distance_last_x_positions = x_positions[-1] - x_positions[-2]
            self.image_renderer: GlyphRenderer = self.plot.image(
                image="image",
                source=self.image_source,
                x=x_positions[0] - distance_first_x_positions / 2,
                y=first_time_sample,
                # ! REVOKE THIS CHANGE
                dw=width_x_positions +
                (distance_first_x_positions + distance_last_x_positions) / 2,
                dh=width_time_sample_instants,
                palette="Greys256",
                anchor="bottom_left",
                origin="bottom_left",
            )

        # Add (single) wiggle renderer
        self.wiggle_renderer: GlyphRenderer = self.plot.multi_line(
            xs="xs",
            ys="ys",
            source=self.wiggle_source,
            color=color,
            visible=self.wiggle_switch.active if self.wiggle_switch else True,
        )

        # Add (multiple) harea renderers
        self._add_hareas(data_rescaled, x_positions, time_sample_instants)

        self._set_up_renderers_on_trace_excess(num_traces)

    @staticmethod
    def _check_stretch_factor(stretch_factor):
        if not isinstance(stretch_factor, (int, float)):
            raise TypeError("stretch_factor must be a number")

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
    def _rescale_data(data: npt.NDArray, x_positions: npt.NDArray, stretch_factor: int):
        # if there is only one trace, no need to rescale
        if data.shape[1] == 1:
            # normalize between -1 and 1
            return data / np.max(np.abs(data))

        # Minimum trace horizontal spacing
        trace_x_spacing = np.min(np.diff(x_positions))

        # Rescale data by trace_x_spacing and stretch_factor
        data_max_std = np.max(np.std(data, axis=0))

        data_rescaled = data / data_max_std * trace_x_spacing * stretch_factor
        return data_rescaled

    @staticmethod
    def _compute_wiggle_source_data(
        data: npt.NDArray,
        x_positions: npt.NDArray,
        time_sample_instants: npt.NDArray,
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

    def _add_hareas(
        self,
        data: npt.NDArray,
        x_positions: npt.NDArray,
        time_sample_instants: npt.NDArray,
    ):

        num_time_samples = data.shape[0]
        num_traces = data.shape[1]

        # Cancel if there are too many traces
        if num_traces > MAX_TRACES_LINE_HAREA:
            return

        amplitudes_zeros = np.zeros(shape=(num_time_samples,))

        for trace_index in range(num_traces):
            x_position = x_positions[trace_index]
            amplitudes = data[:, trace_index]

            amplitudes_positive = np.clip(amplitudes, a_min=0, a_max=None)

            # Add harea glyph renderer
            self.plot.harea(
                x1=amplitudes_zeros + x_position,
                x2=amplitudes_positive + x_position,
                y=time_sample_instants,
                color="black",
                name="H",
                visible=self.areas_switch.active if self.areas_switch else True,
            )

    def _update_image_glyph(self, x_positions: npt.NDArray, time_sample_instants: npt.NDArray):
        num_traces = x_positions.size
        first_time_sample = time_sample_instants[0]
        width_time_sample_instants = np.abs(
            time_sample_instants[0] - time_sample_instants[-1]
        )
        if num_traces == 1:
            self.image_renderer.glyph.update(
                x=x_positions[0] - 1,
                dw=2,
                y=first_time_sample,
                dh=width_time_sample_instants,
            )
        else:
            width_x_positions = np.abs(x_positions[0] - x_positions[-1])
            distance_first_x_positions = x_positions[1] - x_positions[0]
            distance_last_x_positions = x_positions[-1] - x_positions[-2]
            self.image_renderer.glyph.update(
                x=x_positions[0] - distance_first_x_positions / 2,
                # ! REVOKE THIS CHANGE
                dw=width_x_positions +
                (distance_first_x_positions + distance_last_x_positions) / 2,
                y=first_time_sample,
                dh=width_time_sample_instants,
            )

    def update_plot(
        self,
        data: npt.NDArray,
        x_positions: npt.NDArray | None,
        interval_time_samples: float,
        time_unit="s",
        stretch_factor=0.15,
        color="black",
        gather_key: str | None = None,
    ):
        # Input checks
        # ------------
        self._check_stretch_factor(stretch_factor)
        self._check_data(data)
        num_time_samples = data.shape[0]
        num_traces = data.shape[1]
        if x_positions is None:
            x_positions = np.arange(start=1, stop=num_traces + 1)
        else:
            self._check_x_positions(x_positions, num_traces)

        # Hold off all requests to repaint the plot
        self.plot.hold_render = True

        # Amplitudes rescaled (data for wiggle renderers)
        data_rescaled = self._rescale_data(data, x_positions, stretch_factor)

        # Time sample instants (data for all renderers)
        first_time_sample = 0.0
        # ! REVOKE THIS CHANGE
        last_time_sample = first_time_sample + \
            (num_time_samples - 1) * interval_time_samples
        time_sample_instants = np.linspace(
            start=first_time_sample, stop=last_time_sample, num=num_time_samples
        )

        # Update visualization
        # --------------------

        # Update image renderer's source
        self._update_image_source(data)
        # Update image renderer's glyph
        self._update_image_glyph(x_positions, time_sample_instants)

        # Update wiggle renderer's source
        self._update_wiggle_source(
            data_rescaled, x_positions,
            time_sample_instants
        )

        # Update harea renderers
        self._remove_hareas()
        self._add_hareas(data_rescaled, x_positions, time_sample_instants)

        # Update plot setup
        # -----------------
        # Adjust axes labels
        if gather_key:
            self.plot.xaxis.axis_label = gather_key
        else:
            self.plot.xaxis.axis_label = "trace sequential number"
        if time_unit == "s":
            self.plot.yaxis.axis_label = "Time (s)"
        elif time_unit == "ms":
            self.plot.yaxis.axis_label = "Time (ms)"

        self._set_up_renderers_on_trace_excess(num_traces)

        # Stop holding off requests to repaint the plot
        self.plot.hold_render = False

    def _update_image_source(self, data: npt.NDArray):
        self.image_source.data = {"image": [data]}

    def _update_wiggle_source(
        self,
        data_rescaled: npt.NDArray,
        x_positions: npt.NDArray,
        time_sample_instants: npt.NDArray,
    ):
        self.wiggle_source.data = self._compute_wiggle_source_data(
            data_rescaled, x_positions, time_sample_instants
        )

    def _remove_hareas(self):
        """Remove all harea glyph renderers from this plot"""
        self.plot.renderers = list(
            filter(lambda gl: gl.name != "H", self.plot.renderers)
        )

    def _set_up_renderers_on_trace_excess(self, num_traces: int):
        # If there are too many traces...
        if num_traces > MAX_TRACES_LINE_HAREA:
            # deactivate area widget
            if self.areas_switch:
                self.areas_switch.update(active=False, disabled=True)
        else:
            # harea is allowed
            if self.areas_switch is not None:
                self.areas_switch.disabled = False

    def assign_wiggle_switch(self, switch: Switch):
        """Link the `active` attribute of a Switch instance (either a
        Switch or CheckBox instance) to the visibility of the line renderer"""
        self.wiggle_switch = switch
        self.wiggle_switch.active = self.wiggle_renderer.visible
        self.wiggle_switch.js_link(
            "active",
            self.wiggle_renderer,
            "visible"
        )

    def assign_area_switch(self, switch: Switch):
        """Link the `active` attribute of a Switch instance (either a
        Switch or CheckBox instance) to the visibility of the area renderer"""

        def harea_switch_handler(attr, old, new: bool):
            self.areas_switch.disabled = True
            with self.plot.hold(render=True):
                for gl in filter(lambda gl: gl.name == "H", self.plot.renderers):
                    gl.visible = new
            self.areas_switch.disabled = False

        self.areas_switch = switch
        self.areas_switch.on_change("active", harea_switch_handler)

    def assign_image_switch(self, switch: Switch):
        """Link the `active` attribute of a Switch instance (either a
        Switch or CheckBox instance) to the visibility of the image renderer"""
        self.image_switch = switch
        self.image_switch.active = self.image_renderer.visible
        self.image_switch.js_link("active", self.image_renderer, "visible")

    def toggle_wiggle_visible(self, value: bool) -> None:
        self.wiggle_renderer.visible = value
        self.wiggle_switch.active = value
