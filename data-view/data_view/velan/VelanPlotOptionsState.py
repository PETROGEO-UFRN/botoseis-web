from ..BaseVisualization import BasePlotOptionsState


class VelanPlotOptionsState(BasePlotOptionsState):
    first_cdp: int
    last_cdp: int
    number_of_gathers_per_time: int

    # time_min
    first_time_sample: float
    # time_max - time_min
    width_time_samples: float

    first_velocity_value: float
    last_velocity_value: float
    # number of velocity values
    velocity_step_size: float

    def __init__(
        self,
        **custom_states
    ):
        super().__init__(
            has_gather_key=True,
            interval_time_samples=50,

            first_cdp=100,
            last_cdp=100,
            number_of_gathers_per_time=25,

            first_time_sample=0.0,
            width_time_samples=100,

            first_velocity_value=1000.0,
            last_velocity_value=5000.0,
            velocity_step_size=25.0,
            **custom_states
        )

        self.last_cdp = self.first_cdp + self.velocity_step_size
