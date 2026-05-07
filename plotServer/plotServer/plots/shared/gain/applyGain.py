from typing import TypedDict
from numpy import typing as np_types

from .agc import applyAgcGain
from .gaussianAgc import applyGaussianAgcGain
from .perc import applyPercentileClipping

class GainType(TypedDict):
    """
    A dictionary defining the supported types of gain that can
    be applied to seismic data.
    """
    AGC: float
    GAUSSIAN_AGC: float
    PERCENTILE_CLIPPING: float

def applyGain(
    data: np_types.NDArray,
    gain: GainType,
    intervalTimeSamples: float,
) -> np_types.NDArray:
    """
    Applies the specified gain to the input data.
    \nChecks for gain values, not keys.
    \nIn case of None or 0 values, the gain will be skipped.

    Parameters
    ----------
    data: np_types.NDArray
        Input data array [2D array]
    gain: GainType [dict]
        Dictionary containing the gain values.
    intervalTimeSamples: float
        Time step between samples in seconds.

    Returns: np_types.NDArray
        The gained data array.
    """
    newData = data.copy()

    if gain['AGC']:
        newData = applyAgcGain(newData, gain['AGC'], intervalTimeSamples)

    if gain['GAUSSIAN_AGC']:
        newData = applyGaussianAgcGain(newData, gain['GAUSSIAN_AGC'], intervalTimeSamples)

    if gain['PERCENTILE_CLIPPING']:
        newData = applyPercentileClipping(newData, gain['PERCENTILE_CLIPPING'])

    return newData
