from seismicio import readsu


def get_stack_sufile(state: dict, filename: str):
    # Read seismic data
    # -----------------
    sufile = readsu(filename)

    # Data from current seismic data
    # ------------------------------
    state["num_time_samples"] = sufile.num_samples
    state["interval_time_samples"] = sufile.headers.dt[0] / 1000000  # µs → s

    return sufile


def get_sufile(state: dict, filename: str, gather_key: str):
    """
    State:
    - [write] num_gathers, num_time_samples, interval_time_samples
    """
    state["gather_index_start"] = 0
    state["num_loadedgathers"] = 1

    # Read seismic data
    # -----------------
    sufile = readsu(filename, gather_key)

    # Data from current seismic data
    # ------------------------------
    state["num_gathers"] = sufile.num_gathers
    state["num_time_samples"] = sufile.num_samples
    state["interval_time_samples"] = sufile.headers.dt[0] / 1000000  # µs → s

    return sufile
