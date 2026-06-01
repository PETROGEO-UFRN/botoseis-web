import numpy as np
from numpy import typing as np_types


def applyPercentileClipping(
	data: np_types.NDArray,
    percentile: float
) -> np_types.NDArray:
    """
    Apply a percentile-based clipping to input data.

    Parameters
    ----------
    data : np_types.NDArray
        Input data array.
    percentile : float
        Percentile value for clipping.

    Returns
    -------
    np_types.NDArray
        Clipped data array.
    """
    # np.percentile requires q in [0, 100]; clamp so out-of-range input from the
    # UI degrades gracefully instead of raising.
    percentile = min(max(percentile, 0), 100)
    maxTraceAmplitude = np.percentile(
        np.absolute(data),
        percentile
    )
    clippedTraces = np.clip(data, a_min=-maxTraceAmplitude, a_max=maxTraceAmplitude)
    return clippedTraces
