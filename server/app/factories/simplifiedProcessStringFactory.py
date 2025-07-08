from os import path


def createSimplifiedProcessString(process_output):
    commands, rest = process_output.args.split("<", 1)
    inputPath, outputPath = rest.split(">", 1)
    inputFileName = path.basename(inputPath)
    outputFileName = path.basename(outputPath)

    executionSimplifiedString = f"{commands} < {inputFileName} > {outputFileName}"
    return executionSimplifiedString
