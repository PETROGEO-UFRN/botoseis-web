import numpy as np
import numpy.typing as np_types
from scipy import ndimage

EPS: float = 3.8090232

def applyGaussianAgcGain(
    gatherAmplitudes: np_types.NDArray,
    wagc: float,
    intervalTimeSamples: float
) -> np_types.NDArray:
    """
    Calculates Gaussian Automatic Gain Control (GAGC) of a seismic gather.

    Parameters
    ----------
    gatherAmplitudes : np_types.NDArray
        Array of gather amplitudes [2D array]
    wagc : float
        Window length for AGC in seconds.
    intervalTimeSamples : float
        Time step between samples in seconds.
    """
    halfWindowSamples = round(wagc / intervalTimeSamples)

    # *** Define the variance/decay of the Gaussian curve based on the window size
    decayScalar = EPS / halfWindowSamples

    # *** Array of relative distances from the center of the window
    sampleOffsets = np.arange(-halfWindowSamples + 1, halfWindowSamples)

    # *** Bell curve weights using the decay scalar and distances
    gaussianWeights = np.exp(
        -((decayScalar**2) * sampleOffsets * sampleOffsets)
    )

    # *** Moving energy average weighted by the Gaussian curve
    localWeightedEnergy = ndimage.convolve1d(
        gatherAmplitudes**2,
        gaussianWeights,
        mode='constant',
        cval=0.0,
        axis=0
    )

    # *** Extract Root Weighted Energy and apply gain
    rootWeightedEnergy = np.sqrt(localWeightedEnergy)

    return np.divide(
        gatherAmplitudes,
        rootWeightedEnergy,
        out=np.zeros_like(gatherAmplitudes),
        where=rootWeightedEnergy!=0
    )
