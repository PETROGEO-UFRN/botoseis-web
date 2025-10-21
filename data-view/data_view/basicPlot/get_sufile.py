from seismicio import readsu

SECOND_IN_MICRO_SECONDS = 1e6


def get_stack_sufile(plot_options: dict, filename: str):
    # Read seismic data
    # -----------------
    sufile = readsu(filename)

    # Data from current seismic data
    # ------------------------------
    plot_options["num_time_samples"] = sufile.num_samples
    plot_options["interval_time_samples"] = \
        sufile.headers.dt[0] / SECOND_IN_MICRO_SECONDS

    return sufile


def get_multi_gather_sufile(plot_options: dict, filename: str, gather_key: str):
    """
    plot_options:
    - [write] num_gathers, num_time_samples, interval_time_samples
    """
    # Read seismic data
    # -----------------
    sufile = readsu(filename, gather_key)

    # Data from current seismic data
    # ------------------------------
    plot_options["num_gathers"] = sufile.num_gathers
    plot_options["num_time_samples"] = sufile.num_samples
    plot_options["interval_time_samples"] = sufile.headers.dt[0] / \
        SECOND_IN_MICRO_SECONDS

    return sufile
