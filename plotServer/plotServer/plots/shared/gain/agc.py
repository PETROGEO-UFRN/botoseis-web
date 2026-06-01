import numpy as np
import numpy.typing as np_types
from scipy import ndimage

def applyAgcGain(
    gatherAmplitudes: np_types.NDArray,
    wagc: float,
    intervalTimeSamples: float
) -> np_types.NDArray:
    """
    Calculates Simple Automatic Gain Control (AGC) of a seismic gather.

    Parameters
    ----------
    gatherAmplitudes : np_types.NDArray
        Array of gather amplitudes [2D array]
    wagc : float
        Window length for AGC in seconds.
    intervalTimeSamples : float
        Time step between samples in seconds.
    """
    # *** At least one sample each side, so the averaging window is never empty
    # *** (round() can hit 0 when wagc is small relative to the sample interval).
    half_window_samples = max(round(wagc / intervalTimeSamples), 1)

    # *** Define the physical window dimensions
    fullWindowSamples = 2 * half_window_samples

    # *** Rectangular filter (weights sum to 1.0 to compute a true mean)
    averagingWeights = np.ones(fullWindowSamples) / fullWindowSamples

    # *** Moving energy average
    # *** Apply the 1D filter down the time axis (axis=0)
    # *** mode='constant' with cval=0.0 safely pads the top and bottom with zeros
    localMeanSquaredEnergy = ndimage.convolve1d(
        gatherAmplitudes**2,
        averagingWeights,
        mode='constant',
        cval=0.0,
        axis=0
    )

    # *** Extract RMS and apply gain
    rootMeanSquareEnergy = np.sqrt(localMeanSquaredEnergy)

    return np.divide(
        gatherAmplitudes,
        rootMeanSquareEnergy,
        out=np.zeros_like(gatherAmplitudes),
        where=rootMeanSquareEnergy!=0
    )
