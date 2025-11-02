import colorcet

from bokeh.plotting import figure
from bokeh.models import GlyphRenderer
import numpy as np
import numpy.typing as np_types


def semblancePlotRendererFactory(
    plot: figure,
    coherence_matrix: np_types.NDArray,
    velocities: np_types.NDArray,

    first_time_sample: float,
    width_time_samples: float,

    first_velocity_value: float,
    last_velocity_value: float,
) -> GlyphRenderer:
    width_velocities = np.abs(last_velocity_value - first_velocity_value)

    renderer = plot.image(
        image=[coherence_matrix],
        x=velocities[0],
        y=first_time_sample,
        dw=width_velocities,
        dh=width_time_samples,
        anchor="bottom_left",
        origin="bottom_left",
        palette=colorcet.rainbow4,
    )

    return renderer
