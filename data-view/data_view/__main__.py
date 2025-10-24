from pathlib import Path
from tornado import autoreload

from .constants import ENV
from .server import server_factory


def __watch_folder(folder: str) -> None:
    """Watch all files (recursively) in a folder for changes."""
    for filepath in Path(folder).rglob("*"):
        if filepath.is_file():
            autoreload.watch(str(filepath))


# *** Run the Bokeh server application
if __name__ == '__main__':
    server = server_factory()

    server.start()
    print("IS_DEVELOPMENT: ", ENV.IS_DEVELOPMENT)

    if ENV.IS_DEVELOPMENT:
        __watch_folder("data_view/public")
        __watch_folder("data_view/templates")
        autoreload.start()

    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()
