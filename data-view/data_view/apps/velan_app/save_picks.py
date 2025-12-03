import numpy.typing as np_types


def __removeBrackets(text: str):
    return text.replace("[", "").replace("]", "")


def save_picks(picks: dict[int, list[float]]):
    # todo: get api/helper-file/read .dat file content
    # todo: send api/helper-file/create .dat file
    # todo: run "with open" in memory
    # import pdb
    # pdb.set_trace()
    with open("./table.dat", "w") as file:
        cdps = picks.keys()
        for index, key in enumerate(cdps):
            file.write("cdp=")
            file.write(f"{key+1}")
            if index+1 < len(cdps):
                file.write(",")
        file.write("\n")

        for picks_by_cdp in picks.values():
            file.write("tnmo=")
            file.write(__removeBrackets(f'{picks_by_cdp["y"]}'))
            file.write("\n")
            file.write("vnmo=")
            file.write(__removeBrackets(f'{picks_by_cdp["x"]}'))
            file.write("\n")
