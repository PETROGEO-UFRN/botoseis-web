from bokeh.plotting import figure
from bokeh.models import GlyphRenderer

import numpy as np
from numpy import typing as np_types

MAX_TRACES_FILL_AREA = 1400
WIGGLE_COLOR = "black"

MIDPOINT_INDEX_OFFSET = 0.5
"""
Used to create a fractional pseudo-index for zero-crossings.
Ensures that when NumPy sorts the arrays, the crossing coordinates
are injected chronologically between integer sample indices.
"""

def wigglePatchesRenderFactory(
	plot: figure,
	data: np_types.NDArray,
	offsetPosition: np_types.NDArray,
	timeSampleInstants: np_types.NDArray
) -> GlyphRenderer:
	dataPositioned, timesPositioned = __wigglePatchesDataFactory(
		data=data,
		offsetPosition=offsetPosition,
		timeSampleInstants=timeSampleInstants
	)
	renderer = plot.patches(
		xs=dataPositioned,
		ys=timesPositioned,
		color=WIGGLE_COLOR,
		name="H",
		line_width=0,
	)
	return renderer


def __wigglePatchesDataFactory(
	data: np_types.NDArray,
    offsetPosition: np_types.NDArray,
    timeSampleInstants: np_types.NDArray
):
    tracesAmount = data.shape[1]
    # *** Cancel if there are too many traces
    if tracesAmount > MAX_TRACES_FILL_AREA:
        return None

    dataPositioned = []
    timesPositioned = []

    for traceOffset, traceAmplitude in zip(offsetPosition, data.T):
        # *** Extract the negative side of the wiggle
        negativeAmplitudes, negativeTimes = __getSmoothNegativeTrace(
            timeSampleInstants,
            traceAmplitude,
            traceOffset
        )

        # *** Skip if the trace is entirely positive
        if not negativeAmplitudes:
            continue

        # *** Build the polygon for wiggle pathes (negative side)
        polygonOffsetCoordinates = [traceOffset] * len(negativeAmplitudes) + negativeAmplitudes[::-1]
        polygonTimeCordinates = negativeTimes + negativeTimes[::-1]

        dataPositioned.append(polygonOffsetCoordinates)
        timesPositioned.append(polygonTimeCordinates)

    return dataPositioned, timesPositioned


def __getSmoothNegativeTrace(timeSampleInstants, traceAmplitudes: np_types.NDArray, traceOffset):
    """
    Finds all negative amplitudes and calculates the exact zero-crossing interpolation
    points, returning the sorted boundary coordinates for a single trace lobe.
    \nReturns the X and Y coordinates for the negative part of a trace.
    \n(amplitude and time)
    """
    currentAmplitudes = traceAmplitudes[:-1]
    nextAmplitudes = traceAmplitudes[1:]
    currentTime = timeSampleInstants[:-1]
    nextTime = timeSampleInstants[1:]

    # ***Capture strictly negative values
    negativeMask = currentAmplitudes <= 0
    negativeIndices = np.where(negativeMask)[0]

    xs_neg = traceOffset + currentAmplitudes[negativeMask]
    ys_neg = currentTime[negativeMask]

    # *** Capture exact zero crossings
    crossingMask = (
        (currentAmplitudes < 0) & (nextAmplitudes > 0)
    ) | (
        (currentAmplitudes > 0) & (nextAmplitudes < 0)
    )
    crossingIndices = np.where(crossingMask)[0]

    # *** Linear interpolation to find the exact time at zero
    crossingTimes = (
        currentTime[crossingMask] + (
            nextTime[crossingMask] - currentTime[crossingMask]
        ) * (
            0 - currentAmplitudes[crossingMask]
        ) / (
            nextAmplitudes[crossingMask] - currentAmplitudes[crossingMask]
        )
    )

    xs_cross = np.full(len(crossingIndices), traceOffset)
    ys_cross = crossingTimes


    # *** Combine and sort to preserve the original append order
    sortOrder = np.argsort(np.concatenate(
        [negativeIndices, crossingIndices + MIDPOINT_INDEX_OFFSET]
    ))

    new_xs = np.concatenate([xs_neg, xs_cross])[sortOrder].tolist()
    new_ys = np.concatenate([ys_neg, ys_cross])[sortOrder].tolist()

    # Add the last point if it is negative (uncommented and fixed)
    if traceAmplitudes[-1] <= 0:
        new_xs.append(traceOffset + traceAmplitudes[-1])
        new_ys.append(timeSampleInstants[-1])

    return new_xs, new_ys
