from typing import get_args
from numpy import ndarray


class BasePlotOptionsState():
    # Paremeters for stack files or multi-gather files
    interval_time_samples: int | None
    num_time_samples: int | None

    # Parameters for multi-gather files only
    gather_index_start: int | None
    num_loadedgathers: int | None
    num_gathers: int | None

    def __init__(
        self,
        has_gather_key: bool = False,
        **custom_states
    ) -> None:
        default_options = {
            "interval_time_samples": None,
            "num_time_samples": None,
        }
        merged_options = {
            **default_options,
            **custom_states
        }
        self.updatePlotOptionsState(
            **merged_options
        )

        if has_gather_key:
            self.updatePlotOptionsState(
                gather_index_start=0,  # zero-based indexing
                num_loadedgathers=1,
                num_gathers=None,
            )

        baseClassAnnotations = BasePlotOptionsState.__annotations__
        self.__annotations__.update(baseClassAnnotations)

    def __to_extected_number_type(self, key: str, value: str):
        """
        Expected to fail when expected type is.
            #   - String
            #   - Multi layer types
        """
        annotation = self.__annotations__.get(key, str)
        expected_type = get_args(annotation)[0]

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
                # Parameters for multi-gather files only:
                - gather_index_start: int | None
                - num_loadedgathers: int | None
                - num_gathers: int | None
        """
        for plot_option_key, plot_option_value in plot_options_new_state.items():
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
                # Expected to fail when expected type is a non numerical type:
                plot_option_value = plot_option_value
            setattr(self, plot_option_key, plot_option_value)
