from ..BaseVisualization import BasePlotOptionsState


class VelanPlotOptionsState(BasePlotOptionsState):
    first_cdp: int
    last_cdp: int
    number_of_gathers_per_time: int

    first_velocity_value: float
    last_velocity_value: float
    velocity_step_size: float

    # not from user input
    width_time_samples: float

    def __init__(
        self,
        **custom_states
    ):
        default_state_values = {
            "first_cdp": 100,
            "last_cdp": 500,
            "number_of_gathers_per_time": 50,

            "first_velocity_value": 1000,
            "last_velocity_value": 4000,
            "velocity_step_size": 25,
        }
        merged_velan_states = {
            **default_state_values,
            **custom_states,
        }
        super().__init__(
            has_gather_key=True,
            num_loadedgathers=1,

            width_time_samples=100,

            **merged_velan_states
        )

        self.gather_index_start = self.first_cdp
