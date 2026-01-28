import io
import re


def __removeBrackets(text: str):
    text = re.sub(r"[\[\]\n]", "", text)
    return text.replace(' ', '')


def createPickingASCTable(picks: dict[int, any]):
    file_buffer = io.StringIO()
    cdps = picks.keys()

    # *** first line, cdps declaration
    file_buffer.write("cdp=")
    for index, key in enumerate(cdps):
        cdp_number = f"{int(key)+1}"
        file_buffer.write(cdp_number)

        if index + 1 < len(cdps):
            file_buffer.write(",")
    file_buffer.write("\n")

    # *** tnmo & vnmo lines
    for picks_by_cdp in picks.values():
        file_buffer.write("tnmo=")
        file_buffer.write(__removeBrackets(f'{picks_by_cdp["y"]}'))
        file_buffer.write("\n")
        file_buffer.write("vnmo=")
        file_buffer.write(__removeBrackets(f'{picks_by_cdp["x"]}'))
        file_buffer.write("\n")

    # *** make StringIO instance compatible with regular file saving calls
    def save_to_disk(path):
        with open(path, 'w') as file:
            file.write(file_buffer.getvalue())
    file_buffer.save = save_to_disk

    # *** Reset buffer cursor position
    file_buffer.seek(0)

    return file_buffer
