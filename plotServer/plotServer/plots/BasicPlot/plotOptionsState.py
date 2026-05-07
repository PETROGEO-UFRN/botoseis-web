from ..shared.BasePlotOptionsState import BasePlotOptionsState


class PlotOptionsState(BasePlotOptionsState):
    def __init__(self, has_gather_key: bool = False) -> None:
        super().__init__(has_gather_key=has_gather_key)
