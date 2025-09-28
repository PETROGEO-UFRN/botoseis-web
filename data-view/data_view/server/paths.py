from pathlib import Path

INDEX_TEMPLATE_PATH = (
    Path(__file__).parent.parent / "templates" / "index.html"
).resolve()


STATIC_URL_PATH = "/public/"

STATIC_FILES_PATH = (Path(__file__).parent.parent / "public").resolve()
