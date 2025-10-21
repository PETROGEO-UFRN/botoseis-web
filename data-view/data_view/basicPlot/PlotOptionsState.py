from typing import Literal, get_origin, get_args


class PlotOptionsState:
    # Paremeters for stack files or multi-gather files
    percentile_clip: float | None
    gain_option: Literal["agc", "gagc"] | None
    wagc: float | None
    interval_time_samples: int | None
    num_time_samples: int | None

    # Parameters for multi-gather files only
    gather_index_start: int | None
    num_loadedgathers: int | None
    num_gathers: int | None

    def __init__(
        self,
        has_gather_key: bool = False
    ) -> None:
        self.updatePlotOptionsState(
            percentile_clip=100,
            gain_option=None,
            wagc=0.5,
            interval_time_samples=None,
            num_time_samples=None,
        )

        if has_gather_key:
            self.updatePlotOptionsState(
                gather_index_start=190,  # zero-based indexing
                num_loadedgathers=1,
                num_gathers=None,
            )

    def __to_extected_number_type(self, key: str, value: str):
        """
        Convert property to Int or Float, as expected for each property.

        If not Int or Float (complex types), skip conversion.
        """
        annotation = self.__annotations__.get(key, str)
        expected_type = get_args(annotation)[0]

        is_multi_layer_type = bool(get_origin(expected_type))
        if is_multi_layer_type:
            return value
        return expected_type(value)

    def updatePlotOptionsState(
        self,
        **plot_options_new_state
    ):
        """
        Updates the provided keys of the state options enforcing types.

        Keeps the old value when not explicitly updating an option.

        Parameters:
            **plot_options_new_state: Keyword arguments corresponding to
                PlotOptionsState attributes. Expected keys (all optional):
                - percentile_clip: float | None
                - gain_option: Literal["agc", "gagc", None]
                - wagc: float | None
                - interval_time_samples: int | None
                - num_time_samples: int | None
                # Parameters for multi-gather files only:
                - gather_index_start: int | None
                - num_loadedgathers: int | None
                - num_gathers: int | None
        """
        for plot_option_key, plot_option_value in plot_options_new_state.items():
            setattr(self, plot_option_key, plot_option_value)
            if plot_option_value == "None" or plot_option_value is None:
                setattr(self, plot_option_key, None)
                continue

            try:
                plot_option_value = self.__to_extected_number_type(
                    plot_option_key,
                    plot_option_value
                )
            except:
                # fallback: keep as-is if conversion fails
                plot_option_value = plot_option_value
            setattr(self, plot_option_key, plot_option_value)
