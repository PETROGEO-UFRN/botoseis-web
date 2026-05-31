"""Wiring tests for BandwidthAppFactory.modify_document.

The handler-level test in test_bokeh_script_handler.py only exercises Bokeh's
script generation (server_document). The actual file-path resolution ->
Visualization construction runs lazily inside modify_document when a session
opens, so it is covered here by driving modify_document directly against a real
Bokeh Document with RestAPIConsumer mocked.
"""
import importlib
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from bokeh.document import Document
from bokeh.models import ColumnDataSource

# Import the *module* (not the package attr) to get a stable patch target: the
# package __init__ rebinds the name `BandwidthAppFactory` to the function.
BF = importlib.import_module(
    "plotServer.apps.BandwidthApp.BandwidthAppFactory"
)

NUM_SAMPLES = 723  # marmousi_4ms_stack.su


def _make_doc(arguments: dict, cookies: dict | None = None) -> Document:
    """A Document whose session_context.request exposes Bokeh-style args.

    Bokeh reads request args as {name: [bytes, ...]}. session_context is a
    zero-arg callable internally; stubbing _session_context is enough to drive
    modify_document outside a live server (validated on Bokeh 3.8.2).
    """
    doc = Document()
    request = SimpleNamespace(arguments=arguments, cookies=cookies or {})
    doc._session_context = lambda: SimpleNamespace(request=request)
    return doc


def _spectrum_sources(doc: Document):
    return [
        s
        for s in doc.select({"type": ColumnDataSource})
        if "x" in s.data and "y" in s.data
    ]


def test_modify_document_builds_spectrum(marmousi_stack_path):
    app = BF.BandwidthAppFactory()
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
    sources = _spectrum_sources(doc)
    assert len(sources) == 1
    assert len(sources[0].data["x"]) == (NUM_SAMPLES // 2) + 1  # rfft length


def test_modify_document_missing_workflowId_raises():
    app = BF.BandwidthAppFactory()
    handler = app.handlers[0]
    args = {"workflowId": [b""]}
    # Must fail before any file lookup is attempted.
    with patch.object(BF.RestAPIConsumer, "find_su_file_path") as mocked:
        doc = _make_doc(args)
        with pytest.raises(ValueError, match="workflowId"):
            handler.modify_document(doc)
    mocked.assert_not_called()


def test_modify_document_missing_file_raises():
    app = BF.BandwidthAppFactory()
    handler = app.handlers[0]
    args = {"workflowId": [b"demo"]}
    with patch.object(
        BF.RestAPIConsumer, "find_su_file_path", return_value=None
    ):
        doc = _make_doc(args)
        with pytest.raises(ValueError, match="SU file path not found"):
            handler.modify_document(doc)
