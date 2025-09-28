from bokeh.server.server import Server
from bokeh.application import Application
from tornado.web import StaticFileHandler

from .DevAutoReloadWebSocketHandler import DevAutoReloadWebSocketHandler
from .config import IS_DEVELOPMENT
from .paths import STATIC_FILES_PATH


def server_factory(bokeh_app: Application) -> Server:
    server = Server(
        applications={
            '/': bokeh_app,
        },
        allow_websocket_origin=["*"],
        port=5006,
    )

    server._tornado.add_handlers(
        r".*",
        [(
            r"/public/(.*)",
            StaticFileHandler,
            {"path": str(STATIC_FILES_PATH)}
        )]
    )

    if IS_DEVELOPMENT:
        server._tornado.add_handlers(
            r".*",
            [(r"/ws-autoreload", DevAutoReloadWebSocketHandler)]
        )

    return server
