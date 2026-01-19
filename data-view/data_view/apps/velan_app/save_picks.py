import re


def __removeBrackets(text: str):
    text = re.sub(r"[\[\]\n]", "", text)
    return re.sub(r" +", ",", text)


def save_picks(picks: dict[int, list[float]]):
    # todo: get api/helper-file/read .dat file content
    # todo: send api/helper-file/create .dat file
    # todo: run "with open" in memory
    with open("./table.dat", "w") as file:
        cdps = picks.keys()
        file.write("cdp=")
        for index, key in enumerate(cdps):
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
