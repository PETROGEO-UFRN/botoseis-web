from bokeh.models import RadioButtonGroup
from collections.abc import Callable

GAIN_OPTIONS = ["None", "agc", "wagc"]


def create_gain_option_picker(
    state: dict,
    handle_state_change: Callable,
) -> RadioButtonGroup:
    gain_option_picker = RadioButtonGroup(
        labels=GAIN_OPTIONS,
        active=0,
    )

    def callback(attr: str, old: int, new: int) -> None:
        print(f"\nCALLBACK gain_option_picker. new={new}")
        selected = GAIN_OPTIONS[new]
        state["gain_option"] = selected
        handle_state_change()

    gain_option_picker.on_change("active", callback)
    return gain_option_picker
