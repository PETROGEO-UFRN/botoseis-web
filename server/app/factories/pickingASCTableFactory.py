import io
import re


def __removeBrackets(text: str):
    text = re.sub(r"[\[\]\n]", "", text)
    return text.replace(' ', '')


def __to1BasedIndex(value):
    return f"{int(value)+1}"


def createPickingASCTable(picks: dict[int, any]):
    file_buffer = io.StringIO()
    cdps = picks.keys()

    # *** first line, cdps declaration
    cdps_list_string = "cdp="
    for index, key in enumerate(cdps):
        hasPicksOnCDP = bool(picks[key]['x'])
        if not hasPicksOnCDP:
            continue

        cdp_number = __to1BasedIndex(key)
        cdps_list_string += cdp_number

        if index + 1 < len(cdps):
            cdps_list_string += ","
    cdps_list_string += "\n"
    # *** remove excedent comman if find it
    cdps_list_string = cdps_list_string.replace(',\n', '\n')
    file_buffer.write(cdps_list_string)

    # *** tnmo & vnmo lines
    for cdp_number, picks_by_cdp in picks.items():
        hasPicksOnCDP = bool(picks_by_cdp['x'])
        if not hasPicksOnCDP:
            continue

        cdp_number = __to1BasedIndex(cdp_number)
        times = picks_by_cdp["y"]
        velocities = picks_by_cdp["x"]

        file_buffer.write("tnmo=")
        file_buffer.write(__removeBrackets(f'{times}'))
        file_buffer.write("\n")
        file_buffer.write("vnmo=")
        file_buffer.write(__removeBrackets(f'{velocities}'))
        file_buffer.write("\n")

    # *** make StringIO instance compatible with regular file saving calls
    def save_to_disk(path):
        with open(path, 'w') as file:
            file.write(file_buffer.getvalue())

    file_buffer.save = save_to_disk

    # *** Reset buffer cursor position
    file_buffer.seek(0)

    return file_buffer
