from os import getenv
from bokeh.server.server import Server
from ..config.allowedOrigins import allowedWebSocketOrigins
from ..constants.ROUTE_PATHS import ROUTE_PATHS
from ..apps import BasicPlotAppFactory, VelocityModelAppFactory, VelanAppFactory
from .BokehScriptHandler import BokehScriptHandler


def serverFactory() -> Server:
    return Server(
        applications={
            ROUTE_PATHS.BASIC_PLOT: BasicPlotAppFactory(),
            ROUTE_PATHS.VELOCITY_MODEL: VelocityModelAppFactory(),
            ROUTE_PATHS.VELAN: VelanAppFactory(),
        },
        extra_patterns=[(r'/api/bokeh-script/(.*)', BokehScriptHandler)],
        allow_websocket_origin=allowedWebSocketOrigins,
        address=getenv('SERVER_ADDRESS', None),
        port=5006,
    )
