from tornado.web import RequestHandler
from bokeh.server.server import Server
from bokeh.application import Application

from .config import IS_DEVELOPMENT


def server_factory(bokeh_app: Application) -> Server:
    class CustomRequestHandler(RequestHandler):
        def prepare(self):
            super().prepare()

    tornado_settings = {}
    if IS_DEVELOPMENT:
        tornado_settings = {
            'default_handler_class': CustomRequestHandler,
        }

    server = Server(
        {'/': bokeh_app},
        allow_websocket_origin=["*"],
        tornado_settings=tornado_settings,
        port=5006
    )

    return server
