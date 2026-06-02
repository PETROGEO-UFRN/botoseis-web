from os import getenv
from bokeh.server.server import Server
from ..config.allowedOrigins import allowedWebSocketOrigins
from ..constants.ROUTE_PATHS import ROUTE_PATHS
from ..apps import (
    BasicPlotAppFactory,
    VelocityModelAppFactory,
    VelanAppFactory,
    BandwidthAppFactory,
    FrequencyHeatmapAppFactory,
    FKAppFactory,
)
from .BokehScriptHandler import BokehScriptHandler


def serverFactory() -> Server:
    return Server(
        applications={
            ROUTE_PATHS.BASIC_PLOT: BasicPlotAppFactory(),
            ROUTE_PATHS.VELOCITY_MODEL: VelocityModelAppFactory(),
            ROUTE_PATHS.VELAN: VelanAppFactory(),
            ROUTE_PATHS.BANDWIDTH: BandwidthAppFactory(),
            ROUTE_PATHS.FREQUENCY_HEATMAP: FrequencyHeatmapAppFactory(),
            ROUTE_PATHS.FK: FKAppFactory(),
        },
        extra_patterns=[(r'/api/bokeh-script/(.*)', BokehScriptHandler)],
        allow_websocket_origin=allowedWebSocketOrigins,
        use_xheaders=True,
        websocket_max_message_size=1024 * 1024 * 1024,
        check_unused_sessions_milliseconds=5000,
        unused_session_lifetime_milliseconds=5000,
        address=getenv('SERVER_ADDRESS', None),
        port=5006,
    )
