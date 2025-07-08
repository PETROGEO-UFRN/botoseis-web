import argparse
import numpy as np
import numpy.typing as npt
from seismicio import readsu, writesu


def apply_clip_from_perc(data: npt.NDArray, value: float) -> npt.NDArray:
    data_abs = np.absolute(data)
    clip_value = np.percentile(data_abs, value)
    return np.clip(data, a_min=-clip_value, a_max=clip_value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="clip",
        description="Apply operation to sufile TONAME",
        epilog="Text at the bottom of help, epilog TONAME",
    )
    parser.add_argument("source", help="filename of the source")
    parser.add_argument("destination", help="filename of the destination")
    parser.add_argument("-p", "--perc", required=True, help="value for percentile", type=float)

    args = parser.parse_args()
    perc_value: float = args.perc
    filename_source: float = args.source
    filename_destination: float = args.destination

    sufile = readsu(filename_source)

    data_clipped = apply_clip_from_perc(sufile.traces, perc_value)

    writesu(filename_destination, data_clipped, sufile.headers)
