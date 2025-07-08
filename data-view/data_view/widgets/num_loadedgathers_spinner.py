from bokeh.models import Spinner
from collections.abc import Callable


def create_num_loadedgathers_spinner(
    state: dict,
    handle_state_update: Callable,
) -> Spinner:
    """
    State
    - [read] num_gathers, gather_index_start
    - [read, write] num_loadedgathers
    """
    num_loadedgathers_spinner = Spinner(
        title="Number of gathers to load",
        low=1,
        # high=state["num_gathers"],
        step=1,
        value=state["num_loadedgathers"],
    )

    def callback(attr: str, old, new):
        print(f"\nCALLBACK num_loadedgathers. new={new}")

        num_loadedgathers: int = round(new)

        # if exceeding to the right
        gather_index_stop = state["gather_index_start"] + num_loadedgathers
        if gather_index_stop > state["num_gathers"]:
            num_loadedgathers_spinner.value = state["num_gathers"] - state["gather_index_start"]
            return

        state["num_loadedgathers"] = num_loadedgathers
        handle_state_update()

    num_loadedgathers_spinner.on_change("value_throttled", callback)

    return num_loadedgathers_spinner
