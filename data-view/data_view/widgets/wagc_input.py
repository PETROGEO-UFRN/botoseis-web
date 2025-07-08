from bokeh.models import NumericInput
from collections.abc import Callable


def create_wagc_input(
    state: dict,
    handle_state_change: Callable,
) -> NumericInput:
    """
    State:
    - [read, write] percentile_clip
    """
    wagc_input = NumericInput(
        mode="float",
        title="Automatic gain control window (seconds):",
        value=0.5,
    )

    def callback(attr: str, old: int | float, new: int | float) -> None:
        print(f"\nCALLBACK wagc_input. new={new}")
        wagc = float(new)
        state["wagc"] = wagc
        handle_state_change()

    wagc_input.on_change("value", callback)
    return wagc_input
