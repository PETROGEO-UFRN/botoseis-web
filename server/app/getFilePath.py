from os import getcwd


def getProgramFilePath(unique_filename):
    file_path = getcwd() + '/static/custom_programs/' + unique_filename
    return file_path
