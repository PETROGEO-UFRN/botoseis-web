"""Pure, Bokeh-free geometry/transform helpers for the BasicPlot renderers.

These functions take and return plain NumPy arrays / dicts so they can be unit
tested with synthetic data, without a Bokeh document or an SU fixture. The
``Visualization`` owns the figure and renderers and calls into these for all
geometry/amplitude math and input validation.
"""
import numpy as np
import numpy.typing as np_types

from ...constants.VISUALIZATION import FIRST_TIME_SAMPLE, STRETCH_FACTOR


def check_data(data) -> None:
    """Validate that ``data`` is a 2D NumPy array (raises otherwise)."""
    if type(data).__module__ != np.__name__:
        raise TypeError("data must be a numpy array")
    if len(data.shape) != 2:
        raise ValueError("data must be a 2D array")


def check_x_positions(x_positions, num_traces: int) -> None:
    """Validate that ``x_positions`` is a 1D NumPy array with one entry per trace."""
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


def time_sample_instants(
    num_time_samples: int,
    interval_time_samples: float,
) -> np_types.NDArray:
    """Time (in seconds) of each sample row, from ``FIRST_TIME_SAMPLE``."""
    last_time_sample = (
        FIRST_TIME_SAMPLE + (num_time_samples - 1) * interval_time_samples
    )
    return np.linspace(
        start=FIRST_TIME_SAMPLE,
        stop=last_time_sample,
        num=num_time_samples,
    )


def image_x_extent(x_positions: np_types.NDArray) -> tuple[float, float]:
    """Left edge ``x`` and width ``dw`` of the image glyph, in trace-position units.

    Mirrors the placement done by ``offsetsImageRendererFactory`` so the image
    stays aligned with the trace offsets when the data is repaginated.
    """
    if x_positions.size == 1:
        return float(x_positions[0] - 1), 2.0

    width_x_positions = np.abs(x_positions[0] - x_positions[-1])
    distance_first = x_positions[1] - x_positions[0]
    distance_last = x_positions[-1] - x_positions[-2]
    x = x_positions[0] - distance_first / 2
    dw = width_x_positions + (distance_first + distance_last) / 2
    return float(x), float(dw)


def rescale_for_wiggle(
    data: np_types.NDArray,
    x_positions: np_types.NDArray,
) -> np_types.NDArray:
    """Rescale amplitudes so wiggle traces sit at their x positions without overlap.

    Guards against all-zero data (single trace) and all-zero standard deviation
    (flat section), which would otherwise divide by zero and produce NaNs.
    """
    if data.shape[1] == 1:
        # Single trace: normalize between -1 and 1.
        max_abs = np.max(np.abs(data))
        if max_abs == 0:
            return data.copy()
        return data / max_abs

    # Minimum horizontal spacing between adjacent traces.
    trace_x_spacing = np.min(np.diff(x_positions))
    data_max_std = np.max(np.std(data, axis=0))
    if data_max_std == 0:
        return data.copy()
    return data / data_max_std * trace_x_spacing * STRETCH_FACTOR


def wiggle_polylines(
    data_rescaled: np_types.NDArray,
    x_positions: np_types.NDArray,
    time_sample_instants: np_types.NDArray,
) -> dict[str, list]:
    """Build the ``{xs, ys}`` multi_line source: one polyline per trace."""
    num_traces = data_rescaled.shape[1]
    data_repositioned = data_rescaled + x_positions
    return {
        "xs": list(data_repositioned.T),
        "ys": [time_sample_instants for _ in range(num_traces)],
    }


def wiggle_fill_polygons(
    data_rescaled: np_types.NDArray,
    x_positions: np_types.NDArray,
    time_sample_instants: np_types.NDArray,
) -> dict[str, list]:
    """Build the ``{xs, ys}`` patch source filling positive amplitudes per trace."""
    num_time_samples = data_rescaled.shape[0]
    data_positive = np.clip(data_rescaled, a_min=0, a_max=None)
    y_value = np.concatenate(
        [time_sample_instants, time_sample_instants[::-1]]
    )
    xs = []
    ys = []
    for x_pos, trace in zip(x_positions, data_positive.T):
        x_poly = np.concatenate([
            # Baseline (vertical) at the trace position.
            np.full(num_time_samples, x_pos),
            # Wiggle outline, reversed to close the polygon.
            (x_pos + trace)[::-1],
        ])
        xs.append(x_poly)
        ys.append(y_value)
    return {"xs": xs, "ys": ys}
