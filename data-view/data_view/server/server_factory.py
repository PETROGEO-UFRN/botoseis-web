from bokeh.server.server import Server
from bokeh.application import Application
from tornado.web import StaticFileHandler


from ..constants.paths import static_files_path


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
            {"path": str(static_files_path)}
        )]
    )

    return server
