import numpy as np
from bokeh.models import GlyphRenderer, ColumnDataSource
from bokeh.plotting import figure
from seismicio import readsu

from ..BaseVisualization import visualization_factories
from ..constants.VISUALIZATION import FIRST_TIME_SAMPLE
from .velocityModelRendererFactory import velocityModelRendererFactory

SECOND_IN_MICRO_SECONDS = 1e6


class Visualization():
    plot: figure
    source: ColumnDataSource
    renderer: GlyphRenderer

    def __init__(self, filename, picks_by_cdp):
        sufile = readsu(filename, 'cdp')

        time_samples_number = sufile.headers.ns[0]
        interval_time_samples = sufile.headers.dt[0] / SECOND_IN_MICRO_SECONDS

        cdps = sufile.headers.cdp

        first_cdp = 1
        last_cdp = cdps[-1]

        velocity_grid = self.create_velocity_model_source(
            last_cdp=last_cdp,
            picks_by_cdp=picks_by_cdp,
            time_samples_number=time_samples_number,
            interval_time_samples=interval_time_samples,
        )

        self.source = ColumnDataSource(data={'image': [velocity_grid]})
        self.plot = visualization_factories.plotFactory(
            x_label="CDPs",
            y_label="Time (s)"
        )
        self.renderer = velocityModelRendererFactory(
            plot=self.plot,
            source=self.source,

            first_cdp=first_cdp,
            last_cdp=last_cdp,

            first_time_sample=FIRST_TIME_SAMPLE,
            total_time=time_samples_number * interval_time_samples
        )

    def create_velocity_model_source(
        self,
        last_cdp,
        picks_by_cdp,
        time_samples_number,
        interval_time_samples
    ):
        model_source = np.zeros((time_samples_number, last_cdp))

        time_axis = np.arange(time_samples_number) * interval_time_samples
        max_time = (time_samples_number - 1) * interval_time_samples

        picked_cdps = np.fromiter(
            picks_by_cdp.keys(),
            dtype=int
        ).tolist()
        if len(picked_cdps) < 2:
            raise IndexError("Not enogh picked cdps")

        first_picked_cdp = picked_cdps[0]
        last_picked_cdp = picked_cdps[-1]
        cdp_step_size = picked_cdps[1] - picked_cdps[0]

        for cdp, picks in picks_by_cdp.items():
            # *** add type safety on cdp
            cdp = int(cdp)
            velocity_values = picks['velocities']
            time_values = picks['times']

            time_coordinates = np.concatenate(
                ([FIRST_TIME_SAMPLE], time_values, [max_time])
            )
            velocity_coordinates = np.concatenate(
                ([velocity_values[0]], velocity_values, [velocity_values[-1]])
            )

            # *** 1d interpolation for time axis
            model_source[:, cdp:cdp+cdp_step_size] = np.interp(
                time_axis,
                time_coordinates,
                velocity_coordinates
            )[:, np.newaxis]
            # *** 2d interpolation for velocity axis
            start = max(0, cdp-cdp_step_size)
            model_source[:, start:cdp] = np.linspace(
                model_source[:, start],
                model_source[:, cdp],
                num=cdp-start,
                axis=1
            )

        # *** fill 2d model empty start (right) with first filled column
        first_picked_column = model_source[:, [first_picked_cdp]]
        model_source[:, 0:first_picked_cdp] = first_picked_column

        # *** fill 2d model empty end (left) with first filled column
        last_picked_column = model_source[:, [last_picked_cdp]]
        model_source[:, last_picked_cdp:last_cdp] = last_picked_column

        return model_source
