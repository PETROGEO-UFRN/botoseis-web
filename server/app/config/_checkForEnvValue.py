from os import getenv


def checkForEnvValue(key: str, defaultValue: str) -> str:
    # *** set default when env is not setted
    envValue = getenv(key)
    if envValue:
        return envValue
    return defaultValue
