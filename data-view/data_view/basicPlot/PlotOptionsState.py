class PlotOptionsState:
    # Paremeters for stack files or multi-gather files
    percentile_clip: float | None
    gain_option: str | None  # todo: define static strs
    wagc: float | None
    interval_time_samples: int | None
    num_time_samples: int | None

    # Parameters for multi-gather files only
    gather_index_start: int | None
    num_loadedgathers: int | None
    num_gathers: int | None

    def __init__(
        self,
        gather_key: str | None = None
    ) -> None:
        self.updatePlotOptionsState(
            percentile_clip=100,
            gain_option=None,
            wagc=0.5,
            interval_time_samples=None,
            num_time_samples=None,
        )

        if gather_key:
            self.updatePlotOptionsState(
                gather_index_start=0,  # zero-based indexing
                num_loadedgathers=1,
                num_gathers=None,
            )

    def updatePlotOptionsState(
        self,
        **plot_options_new_state
    ):
        for plot_option_key, plot_option_value in plot_options_new_state.items():
            setattr(self, plot_option_key, plot_option_value)
