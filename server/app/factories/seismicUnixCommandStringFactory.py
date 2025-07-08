import json


def _getParameter(parameterValues: list | str | float | int | bool) -> str:
    parameterValuesProcessString = ""
    if not isinstance(parameterValues, list):
        parameterValuesProcessString += f'{parameterValues}'
        return parameterValuesProcessString

    for index, parameterValue in enumerate(parameterValues):
        if index < len(parameterValues) - 1:
            parameterValuesProcessString += f'{parameterValue},'
            continue
        parameterValuesProcessString += f'{parameterValue}'

    return parameterValuesProcessString


def _getAllParameters(parameters) -> str:
    parametersProcessString = ""
    for parameterKey, parameterValues in parameters.items():
        if not parameterValues:
            continue
        parametersProcessString += f' {parameterKey}='
        parametersProcessString += _getParameter(parameterValues)
    return parametersProcessString


def createSemicUnixCommandString(commandsQueue: list, source_file_path: str, target_file_path: str) -> str:
    # It will generate a string based on filled fields,
    # parameters with empty values (like empty string or empty lists) will be ignored,
    # leting the command line program handle it if not mandatory
    seismicUnixProcessString = ""
    for orderedCommandsObject in commandsQueue:
        # ! this is bad naming and bad typing, must be improved
        orderedCommandsList = orderedCommandsObject.getCommands()
        for seismicUnixProgramIndex, seismicUnixProgram in enumerate(orderedCommandsList):
            if not seismicUnixProgram["is_active"]:
                continue
            seismicUnixProcessString += f'{seismicUnixProgram["name"].lower()}'
            seismicUnixProcessString += _getAllParameters(
                json.loads((seismicUnixProgram["parameters"]))
            )
            if (seismicUnixProgramIndex == 0):
                seismicUnixProcessString += f' < {source_file_path}'
            if (seismicUnixProgramIndex <= len(orderedCommandsList)-2):
                seismicUnixProcessString += ' | '
            if (seismicUnixProgramIndex == len(orderedCommandsList)-1):
                seismicUnixProcessString += f' > {target_file_path}'

    print("seismicUnixProcessString")
    print(seismicUnixProcessString)
    print("***")
    return seismicUnixProcessString
