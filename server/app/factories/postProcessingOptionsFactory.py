import json


def createPostProcessingOptions(
        key: str | None = "tab-vizualizer",
        options: dict[str, str | int | float | None] | None = {},
):
    """
    Create stringfied JSON formated to fit as workflow post processing settings

    By default, create stringfied json set to vizualizer

    ### Parameter
        - key: Define wich client-side program shall be used at the end of the workflow
            - Default: "tab-vizualizer"
        - options: Dict settings passed to the client-side program. Dict format depends on wich key is used   
            - Default: empty dict
    """
    return json.dumps({
        "key": key,
        "options": options
    })
