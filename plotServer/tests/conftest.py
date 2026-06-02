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


# Exact dimensions of the canonical marmousi_4ms_stack.su (the copy in
# PETROGEO-UFRN/mock_large_files that CI checks out). Tests assert against these
# fixed numbers, so the guard below fails loudly with one clear message if a
# different SU file is present rather than letting wrong constants cascade into
# many cryptic failures.
MARMOUSI_NUM_SAMPLES = 724
MARMOUSI_NUM_TRACES = 457


@pytest.fixture(scope="session")
def marmousi_stack_path() -> Path:
    """Path to the local SU fixture used by Bandwidth/FrequencyHeatmap/FK and
    BasicPlot tests.

    Tests that depend on real seismic data should request this fixture; if the
    file is missing they are skipped with a clear message rather than failing.
    Populate plotServer/tests/fixtures/ per the README in that directory.

    The file is verified to be the canonical marmousi_4ms_stack.su: a wrong copy
    fails here with one explicit message instead of producing many confusing
    dimension-mismatch failures downstream.
    """
    if not MARMOUSI_STACK.exists():
        pytest.skip(
            f"SU fixture not found at {MARMOUSI_STACK}. "
            "See plotServer/tests/fixtures/README.md to populate."
        )

    from seismicio import readsu

    shape = readsu(str(MARMOUSI_STACK)).traces.shape
    expected = (MARMOUSI_NUM_SAMPLES, MARMOUSI_NUM_TRACES)
    if shape != expected:
        raise RuntimeError(
            f"Unexpected SU fixture at {MARMOUSI_STACK}: traces shape {shape}, "
            f"expected {expected}. This is not the canonical marmousi_4ms_stack.su "
            "(PETROGEO-UFRN/mock_large_files). Replace it; see "
            "plotServer/tests/fixtures/README.md."
        )
    return MARMOUSI_STACK
