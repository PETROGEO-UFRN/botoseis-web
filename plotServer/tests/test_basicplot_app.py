"""Wiring tests for BasicPlotAppFactory.modify_document.

Like test_bandwidth_app.py, this drives modify_document directly against a real
Bokeh Document with RestAPIConsumer mocked, since the file-path resolution and
Visualization construction run lazily when a session opens.
"""
import importlib
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from bokeh.document import Document
from bokeh.models import ColumnDataSource, Plot

from plotServer.constants.BOKEH_REACT_BRIDGE import (
    BRIDGE_FEEDBACK_MODEL_NAME,
    BRIDGE_MODEL_NAME,
)

# Import the module so the patch target is stable (the package __init__ rebinds
# the name BasicPlotAppFactory to the function).
BF = importlib.import_module(
    "plotServer.apps.BasicPlotApp.BasicPlotAppFactory"
)


def _make_doc(arguments: dict, cookies: dict | None = None) -> Document:
    doc = Document()
    request = SimpleNamespace(arguments=arguments, cookies=cookies or {})
    doc._session_context = lambda: SimpleNamespace(request=request)
    return doc


def _models_named(doc: Document, name: str):
    return list(doc.select({"name": name}))


def test_modify_document_builds_plot_and_bridge(marmousi_stack_path):
    app = BF.BasicPlotAppFactory()
    handler = app.handlers[0]
    args = {"workflowId": [b"demo"]}
    with patch.object(
        BF.RestAPIConsumer,
        "find_su_file_path",
        return_value=str(marmousi_stack_path),
    ) as mocked:
        doc = _make_doc(args)
        handler.modify_document(doc)

    mocked.assert_called_once_with(origin="output")
    # The figure was added as a root.
    assert any(isinstance(root, Plot) for root in doc.roots)
    # Both bridge models are wired.
    assert len(_models_named(doc, BRIDGE_MODEL_NAME)) == 1
    assert len(_models_named(doc, BRIDGE_FEEDBACK_MODEL_NAME)) == 1


def test_origin_query_param_is_propagated(marmousi_stack_path):
    app = BF.BasicPlotAppFactory()
    handler = app.handlers[0]
    args = {"workflowId": [b"demo"], "origin": [b"input"]}
    with patch.object(
        BF.RestAPIConsumer,
        "find_su_file_path",
        return_value=str(marmousi_stack_path),
    ) as mocked:
        doc = _make_doc(args)
        handler.modify_document(doc)
    mocked.assert_called_once_with(origin="input")


def test_modify_document_missing_workflowId_raises():
    app = BF.BasicPlotAppFactory()
    handler = app.handlers[0]
    args = {"workflowId": [b""]}
    with patch.object(BF.RestAPIConsumer, "find_su_file_path") as mocked:
        doc = _make_doc(args)
        with pytest.raises(ValueError, match="workflowId"):
            handler.modify_document(doc)
    mocked.assert_not_called()


def test_modify_document_missing_file_raises():
    app = BF.BasicPlotAppFactory()
    handler = app.handlers[0]
    args = {"workflowId": [b"demo"]}
    with patch.object(
        BF.RestAPIConsumer, "find_su_file_path", return_value=None
    ):
        doc = _make_doc(args)
        with pytest.raises(ValueError, match="SU file path not found"):
            handler.modify_document(doc)
