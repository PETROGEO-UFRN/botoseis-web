from typing import Literal

from ..BaseVisualization import BasePlotOptionsState


class PlotOptionsState(BasePlotOptionsState):
    # Filtering parameters
    # available for stack files or multi-gather files
    percentile_clip: float | None
    gain_option: Literal["agc", "gagc"] | None
    wagc: float | None

    def __init__(
        self,
        has_gather_key: bool = False
    ) -> None:
        super().__init__(
            has_gather_key=has_gather_key,

            # Custom states
            percentile_clip=100,
            gain_option=None,
            wagc=0.5,
        )

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
                # Filter parameters:
                - wagc: float | None
                - interval_time_samples: int | None
                - num_time_samples: int | None
        """
        super().updatePlotOptionsState(
            **plot_options_new_state
        )
