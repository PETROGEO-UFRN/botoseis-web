from bokeh.models import NumericInput
from collections.abc import Callable


def create_percentile_clip_input(
    state: dict,
    handle_state_change: Callable,
) -> NumericInput:
    """
    State:
    - [read, write] percentile_clip
    """
    percentile_clip_input = NumericInput(
        format="0.[00]",
        mode="float",
        title="Percentile clip:",
        value=100,
    )

    def callback(attr: str, old: int | float, new: int | float) -> None:
        print(f"\nCALLBACK percentile_clip_input. new={new}")
        percentile_clip = float(new)
        if percentile_clip > 100.0:
            percentile_clip_input.value = 100.0
            return
        elif percentile_clip < 1.0:
            percentile_clip_input.value = 100.0
            return
        state["percentile_clip"] = percentile_clip
        handle_state_change()

    percentile_clip_input.on_change("value", callback)
    return percentile_clip_input
