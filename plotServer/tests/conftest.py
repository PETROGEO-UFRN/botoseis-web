import asyncio
import socket
import threading
import time
from pathlib import Path

import pytest
import requests
from bokeh.server.server import Server

from plotServer.apps import (
    BandwidthAppFactory,
    BasicPlotAppFactory,
    FKAppFactory,
    FrequencyHeatmapAppFactory,
    VelanAppFactory,
    VelocityModelAppFactory,
)
from plotServer.constants.ROUTE_PATHS import ROUTE_PATHS
from plotServer.server.BokehScriptHandler import BokehScriptHandler

FIXTURES_DIR = Path(__file__).parent / "fixtures"
MARMOUSI_STACK = FIXTURES_DIR / "marmousi_4ms_stack.su"


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@pytest.fixture(scope="session")
def bokeh_server():
    port = _free_port()
    started = threading.Event()
    error: list[BaseException] = []

    def run() -> None:
        try:
            asyncio.set_event_loop(asyncio.new_event_loop())
            server = Server(
                applications={
                    ROUTE_PATHS.BASIC_PLOT: BasicPlotAppFactory(),
                    ROUTE_PATHS.VELOCITY_MODEL: VelocityModelAppFactory(),
                    ROUTE_PATHS.VELAN: VelanAppFactory(),
                    ROUTE_PATHS.BANDWIDTH: BandwidthAppFactory(),
                    ROUTE_PATHS.FREQUENCY_HEATMAP: FrequencyHeatmapAppFactory(),
                    ROUTE_PATHS.FK: FKAppFactory(),
                },
                extra_patterns=[(r"/api/bokeh-script/(.*)", BokehScriptHandler)],
                allow_websocket_origin=[f"localhost:{port}", f"127.0.0.1:{port}"],
                port=port,
            )
            server.start()
            started.set()
            server.io_loop.start()
        except BaseException as exc:
            error.append(exc)
            started.set()

    thread = threading.Thread(target=run, daemon=True)
    thread.start()

    if not started.wait(timeout=15):
        raise RuntimeError("Bokeh server failed to start within 15s")
    if error:
        raise error[0]

    base_url = f"http://127.0.0.1:{port}"
    deadline = time.time() + 5
    while time.time() < deadline:
        try:
            requests.get(f"{base_url}/api/bokeh-script/basic-plot", timeout=1)
            break
        except requests.RequestException:
            time.sleep(0.1)
    else:
        raise RuntimeError(f"Bokeh server did not become reachable at {base_url}")

    yield base_url


@pytest.fixture(scope="session")
def marmousi_stack_path() -> Path:
    """Path to the local SU fixture used by Bandwidth/FrequencyHeatmap/FK tests.

    Tests that depend on real seismic data should request this fixture; if the
    file is missing they will be skipped with a clear message rather than fail.
    Populate plotServer/tests/fixtures/ per the README in that directory.
    """
    if not MARMOUSI_STACK.exists():
        pytest.skip(
            f"SU fixture not found at {MARMOUSI_STACK}. "
            "See plotServer/tests/fixtures/README.md to populate."
        )
    return MARMOUSI_STACK
