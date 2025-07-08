from collections.abc import Callable
from math import isclose, sqrt, exp

import numpy as np
import numpy.typing as npt

EPS: float = 3.8090232  # exp(-EPS*EPS) = 5e-7, "noise" level


def _apply_gain_single_trace(data, gain_option: str, iwagc, nt: int):
    if gain_option == "agc":
        data = do_agc_single_trace(data, iwagc, nt)
    elif gain_option == "gagc":
        data = do_gagc_single_trace(data, iwagc, nt)
    return data


def apply_gain(data: npt.NDArray, gain_option: str, wagc: float, dt: float) -> npt.NDArray:
    apply_gain_single_trace: Callable
    if gain_option == "agc":
        apply_gain_single_trace = do_agc_single_trace
    elif gain_option == "gagc":
        apply_gain_single_trace = do_gagc_single_trace
    else:
        return data

    iwagc = round(wagc / dt)
    nt = data.shape[0]
    num_traces = data.shape[1]

    for trace_index in range(num_traces):
        trace = data[:, trace_index]
        data[:, trace_index] = apply_gain_single_trace(trace, iwagc, nt)

    return data


def do_agc_single_trace(data: npt.NDArray, iwagc: int, nt: int) -> npt.NDArray:

    # allocate room for agc'd data and square of data
    agcdata = np.zeros(nt, dtype=float)
    d2 = np.zeros(nt)

    # Compute square of data
    d2 = data * data

    # Initialize first half window and gain first sample
    _sum: float = 0.0
    for i in range(0, iwagc):
        _sum += d2[i]

    nwin: int = iwagc
    rms: float = _sum / nwin

    if rms == 0:
        agcdata[0] = 0
    else:
        agcdata[0] = data[i] / sqrt(rms)

    # ramping on : increase sum and nwin & gain data until reaching 2*iwagc-1 window
    # processing samples from 1 to iwagc-1
    for i in range(1, iwagc):
        _sum += d2[i + iwagc - 1]
        nwin += 1
        rms = _sum / nwin
        # rms = 0 implies data[i]=0
        if rms == 0:
            agcdata[i] = 0
        else:
            agcdata[i] = data[i] / sqrt(rms)

    # full 2*iagc rms window -- gain data
    # compute sum from 0 at each sample -- decreasing sum give inaccurate results, even negative RMS
    # processing samples from iwagc to nt-iwagc-1
    nwin += 1
    for i in range(iwagc, nt - iwagc):
        _sum = 0.0
        for j in range(i - iwagc, i + iwagc):
            _sum += d2[j]
        rms = _sum / nwin
        if rms == 0:
            agcdata[i] = 0
        else:
            agcdata[i] = data[i] / sqrt(rms)

    # ramping off -- decrease nwin -- gain data
    # compute sum from 0 at each sample -- decreasing sum give inaccurate results, even negative RMS
    # processing samples from nt-iwagc to nt-1
    for i in range(nt - iwagc, nt):
        _sum = 0
        for j in range(i - iwagc, nt):
            _sum += d2[j]
        nwin -= 1
        rms = _sum / nwin
        if data[i] == 0:
            agcdata[i] = 0
        else:
            agcdata[i] = data[i] / sqrt(rms)

    return agcdata


def do_gagc_single_trace(data: npt.NDArray, iwagc: int, nt: int) -> npt.NDArray:
    agcdata: npt.NDArray  # agc'd data
    w: npt.NDArray  # Gaussian window weights
    d2: npt.NDArray  # square of input data
    s: npt.NDArray  # weighted sum of squarEPSes of the data
    u: float  # related to reciprocal std dev
    usq: float  # u*u

    # Allocate room for agc'd data
    agcdata = np.zeros(nt, dtype=float)

    # Allocate and compute Gaussian window weights
    w = np.zeros(iwagc, dtype=float)  # recall iwagc is HALF window
    u = EPS / iwagc
    usq = u * u

    for i in range(1, iwagc):
        floati = float(i)
        w[i] = exp(-(usq * floati * floati))

    # Allocate sum of squares and weighted sum of squares
    d2 = np.zeros(nt)
    s = np.zeros(nt)

    # Put sum of squares of data in d2 and
    # initialize s to d2 to get center point set
    for i in range(0, nt):
        val = data[i]
        s[i] = d2[i] = val * val

    # Compute weighted sum s; use symmetry of Gaussian
    for j in range(1, iwagc):
        wtmp = w[j]
        for i in range(j, nt):
            s[i] += wtmp * d2[i - j]
        k = nt - j
        for i in range(0, k):
            s[i] += wtmp * d2[i + j]

    for i in range(0, nt):
        stmp = s[i]
        agcdata[i] = 0.0 if (not stmp) else data[i] / sqrt(stmp)

    return agcdata
