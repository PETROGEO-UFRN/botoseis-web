from collections.abc import Callable
from bokeh.models import Paragraph


class GatherValueWrapper:

    def update_widget(self, state):
        gather_index_start = state["gather_index_start"]
        gather_index_stop = state["gather_index_start"] + state["num_loadedgathers"]

        gather_value_start = self.index_to_value_converter(gather_index_start)
        gather_value_end = self.index_to_value_converter(gather_index_stop - 1)

        self.widget.text = f"Gather {gather_value_start} to {gather_value_end}"

    def __init__(self, index_to_value_converter: Callable[[int], int]) -> None:
        self.index_to_value_converter = index_to_value_converter
        self.widget = Paragraph()
