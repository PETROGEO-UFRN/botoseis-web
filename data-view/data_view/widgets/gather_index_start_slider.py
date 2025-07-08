from bokeh.models import Slider


def create_gather_index_start_slider(state: dict, update_func) -> Slider:
    """
    State
    - [read] num_gathers, num_loadedgathers
    - [read, write] gather_index_start
    """
    gather_index_start_slider = Slider(
        start=1,
        end=state["num_gathers"],
        value=state["gather_index_start"] + 1,
        step=1,
        title="Gather sequential number",
        width=1000,
    )

    def callback(attr: str, old, new):
        print(f"\nCALLBACK gather_index_start. new={new}")

        gather_index_start: int = round(new) - 1

        # if exceeding to the right
        gather_index_stop = gather_index_start + state["num_loadedgathers"]
        if gather_index_stop > state["num_gathers"]:
            print("EXCEEDED")
            gather_index_start = state["num_gathers"] - state["num_loadedgathers"]
            gather_index_stop = state["num_gathers"]
            gather_index_start_slider.value = gather_index_start + 1
            return

        state["gather_index_start"] = gather_index_start
        update_func()

    gather_index_start_slider.on_change("value_throttled", callback)

    return gather_index_start_slider
