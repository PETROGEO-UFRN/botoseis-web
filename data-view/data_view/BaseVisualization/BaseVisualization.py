import numpy as np
import numpy.typing as np_types
from seismicio.Models.SuDataModel import SuFile

from ..constants.VISUALIZATION import FIRST_TIME_SAMPLE
from .get_sufile import get_stack_sufile, get_multi_gather_sufile
from .BasePlotOptionsState import BasePlotOptionsState


class BaseVisualization:
    sufile: SuFile
    plot_options_state: BasePlotOptionsState
    gather_offsets: np_types.NDArray | None

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

    def getShotGathersData(
        self,
        index_start: int | None = None
    ):
        if not index_start:
            index_start = self.plot_options_state.gather_index_start
        index_stop = index_start + self.plot_options_state.num_loadedgathers
        # ! igather VS gather
        selected_gathers = self.sufile.igather[
            index_start:index_stop
        ]

        last_time_sample = \
            FIRST_TIME_SAMPLE + \
            (self.plot_options_state.num_time_samples - 1) * \
            self.plot_options_state.interval_time_samples

        width_time_samples = np.abs(
            last_time_sample - FIRST_TIME_SAMPLE
        )
        self.plot_options_state.updatePlotOptionsState(
            width_time_samples=width_time_samples,
        )

        if (index_stop - 1 == index_start):
            # *** Single gather
            self.gather_offsets = selected_gathers.headers["offset"]
        else:
            # *** Multiple gathers
            self.gather_offsets = None
        return selected_gathers.data

    def getBaseData(self) -> np_types.NDArray:
        """
        Get Numpy NDArray for data section on display

        Handles stack or sectioned data (shot gathers) 
        """
        # *** "gather_keyword"  must exist for shot gathers
        if self.sufile.gather_keyword:
            data = self.getShotGathersData()
        else:
            data = self.sufile.traces
            self.gather_offsets = None
        return data

    def handle_state_change(self):
        raise NotImplementedError(
            """
            Missing custom handle_state_change() for this Visualization
            handle_state_change() method must be re-implmented when extending BaseVisualization
            """
        )
