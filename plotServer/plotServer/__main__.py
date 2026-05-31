from bokeh.util.browser import view
from tornado import autoreload
from pathlib import Path

from .server import serverFactory
from .config.urls import baseServerURL
from .config.isDevelopment import isDevelopment


def __watch_folder(folder_name: str) -> None:
    """Watch all files (recursively) in a folder for changes."""
    for filepath in Path(folder_name).rglob("*"):
        if filepath.is_file():
            autoreload.watch(str(filepath))


if __name__ == '__main__':
    print(
        f'Opening Tornado app with embedded Bokeh application on {baseServerURL}'
    )
    server = serverFactory()

    if isDevelopment:
        __watch_folder("plotServer")
        autoreload.start()

    server.start()

    server.io_loop.add_callback(view, baseServerURL)
    server.io_loop.start()
