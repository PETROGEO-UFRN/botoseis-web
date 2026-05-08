import base64
import json

import pytest
import requests

REGISTERED_PLOTS = ["sample-plot", "basic-plot", "velocity-model", "velan"]


@pytest.mark.parametrize("plot", REGISTERED_PLOTS)
def test_returns_200_for_each_registered_plot(bokeh_server, plot):
    res = requests.get(
        f"{bokeh_server}/api/bokeh-script/{plot}",
        params={"workflowId": "demo"},
        timeout=5,
    )
    assert res.status_code == 200
    body = res.json()
    assert "script" in body
    assert "<script" in body["script"]


def test_returns_200_with_setup_param(bokeh_server):
    setup_b64 = base64.b64encode(
        json.dumps(
            {
                "first_cdp": 100,
                "last_cdp": 500,
                "number_of_gathers_per_time": 50,
            }
        ).encode("utf-8")
    ).decode("ascii")
    res = requests.get(
        f"{bokeh_server}/api/bokeh-script/velan",
        params={"workflowId": "demo", "setup": setup_b64},
        timeout=5,
    )
    assert res.status_code == 200
    assert "script" in res.json()


def test_returns_400_when_workflowId_missing(bokeh_server):
    res = requests.get(
        f"{bokeh_server}/api/bokeh-script/basic-plot",
        timeout=5,
    )
    assert res.status_code == 400
    assert "workflowId" in res.json()["error"]


def test_returns_400_when_workflowId_empty(bokeh_server):
    res = requests.get(
        f"{bokeh_server}/api/bokeh-script/basic-plot",
        params={"workflowId": ""},
        timeout=5,
    )
    assert res.status_code == 400
    assert "workflowId" in res.json()["error"]


def test_options_preflight_returns_204(bokeh_server):
    res = requests.options(
        f"{bokeh_server}/api/bokeh-script/basic-plot",
        timeout=5,
    )
    assert res.status_code == 204


def test_response_includes_cors_headers(bokeh_server):
    res = requests.get(
        f"{bokeh_server}/api/bokeh-script/sample-plot",
        params={"workflowId": "demo"},
        timeout=5,
    )
    assert res.status_code == 200
    assert "Access-Control-Allow-Origin" in res.headers
    assert "Access-Control-Allow-Methods" in res.headers


def test_returns_404_for_unknown_plot(bokeh_server):
    res = requests.get(
        f"{bokeh_server}/api/bokeh-script/does-not-exist",
        params={"workflowId": "demo"},
        timeout=5,
    )
    assert res.status_code == 404
    assert "not found" in res.json()["error"]
