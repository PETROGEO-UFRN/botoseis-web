from bokeh.server.server import Server
from tornado.web import StaticFileHandler

from ..constants import ENV, FOLDERS
from .DevAutoReloadWebSocketHandler import DevAutoReloadWebSocketHandler
from .routes import routes


def server_factory() -> Server:
    server = Server(
        applications=routes,
        allow_websocket_origin=["*"],
        port=5006,
    )

    server._tornado.add_handlers(
        r".*",
        [(
            r"/public/(.*)",
            StaticFileHandler,
            {"path": str(FOLDERS.STATIC_FILES_PATH)}
        )]
    )

    if ENV.IS_DEVELOPMENT:
        server._tornado.add_handlers(
            r".*",
            [(r"/ws-autoreload", DevAutoReloadWebSocketHandler)]
        )

    return server
