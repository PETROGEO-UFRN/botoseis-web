from seismicio.Models.SuDataModel import SuFile


from .get_sufile import get_stack_sufile, get_multi_gather_sufile
from .BasePlotOptionsState import BasePlotOptionsState


class BaseVisualization:
    sufile: SuFile
    plot_options_state: BasePlotOptionsState

    def __init__(
        self,
        filename: str,
        plot_options_state: BasePlotOptionsState,
        gather_key: str | None = None,
    ) -> None:
        self.plot_options_state = plot_options_state
        if gather_key:
            self.sufile: SuFile = get_multi_gather_sufile(
                plot_options=self.plot_options_state.__dict__,
                filename=filename,
                gather_key=gather_key,
            )
        else:
            self.sufile = get_stack_sufile(
                plot_options=self.plot_options_state.__dict__,
                filename=filename,
            )

    def handle_state_change(self):
        raise NotImplementedError(
            """
            Missing custom handle_state_change() for this Visualization
            handle_state_change() method must be re-implmented when extending BaseVisualization
            """
        )
