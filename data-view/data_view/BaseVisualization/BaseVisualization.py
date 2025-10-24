import numpy.typing as np_types
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

    def __getDataForShotGathers(self) -> np_types.NDArray:
        gather_index_start = self.plot_options_state.gather_index_start
        gather_index_stop = gather_index_start + \
            self.plot_options_state.num_loadedgathers

        data = self.sufile.igather[
            gather_index_start:gather_index_stop
        ].data

        if (gather_index_stop - 1 == gather_index_start):
            # *** Single gather
            self.x_positions = self.sufile.igather[
                gather_index_start
            ].headers["offset"]
            return data

        # *** Multiple gathers
        self.x_positions = None
        return data

    def getBaseData(self) -> np_types.NDArray:
        """
        Get Numpy NDArray for data section on display

        Handles stack or sectioned data (shot gathers) 
        """
        # !!! check if "gather_keyword" exist
        # !!! is must exist for shot gathers
        if self.sufile.gather_keyword:
            data = self.__getDataForShotGathers()
        else:
            data = self.sufile.traces
            self.x_positions = None
        return data

    def handle_state_change(self):
        raise NotImplementedError(
            "Missing custom handle_state_change() for this Visualization",
            "handle_state_change() method must be implmented for any class extending BaseVisualization"
        )
