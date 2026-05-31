import orjson
import numpy as np


def createPickingDict(
    file_path,
    times_key: str = 'times',
    velocities_key: str = 'velocities',
) -> dict[int, dict[str, list[float]]]:
    with open(file_path, 'r') as file:
        lines = file.read().strip().split('\n')
        cdps = np.fromstring(lines[0].split('=')[1],  sep=',', dtype=int)

        picksAsString = lines[1:]

        unpackedPicks: dict[int, dict] = dict()
        for pickLinesIndex, pickAsString in enumerate(picksAsString):
            key, valuesAsString = pickAsString.split("=")
            valuesList = np.fromstring(
                string=valuesAsString,
                sep=',',
                dtype=float
            ).tolist()

            # *** go to next cdp on each second line
            current_cdp = int(cdps[pickLinesIndex // 2])
            # *** converting cdp number to 0 index base
            current_cdp = current_cdp - 1
            if current_cdp not in unpackedPicks:
                unpackedPicks[current_cdp] = {}

            # *** Times and velocities are unpacked as x & y
            # *** for direct compatibility Bokeh implementation
            if key == 'tnmo':
                # *** times
                unpackedPicks[current_cdp][times_key] = valuesList
            if key == 'vnmo':
                # *** velocities
                unpackedPicks[current_cdp][velocities_key] = valuesList

    return unpackedPicks
