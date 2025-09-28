from pathlib import Path
from tornado import autoreload
from .server import app_factory, server_factory, IS_DEVELOPMENT


def __watch_folder(folder: str) -> None:
    """Watch all files (recursively) in a folder for changes."""
    for filepath in Path(folder).rglob("*"):
        if filepath.is_file():
            autoreload.watch(str(filepath))


# *** Run the Bokeh server application
if __name__ == '__main__':
    server = server_factory(
        bokeh_app=app_factory()
    )

    server.start()
    print("IS_DEVELOPMENT: ", IS_DEVELOPMENT)

    if IS_DEVELOPMENT:
        __watch_folder("data_view/public")
        __watch_folder("data_view/templates")
        autoreload.start()

    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()
