"""Wiring tests for BandwidthAppFactory.modify_document.

Bandwidth reads no file -- it builds an empty plot and subscribes to the
observer feed -- so these drive modify_document directly against a real Bokeh
Document with no RestAPIConsumer involved.
"""
import importlib
from types import SimpleNamespace

import numpy as np
import pytest
from bokeh.document import Document
from bokeh.models import ColumnDataSource

# Import the *module* (not the package attr) for a stable reference.
BF = importlib.import_module(
    "plotServer.apps.BandwidthApp.BandwidthAppFactory"
)


def _make_doc(arguments: dict, cookies: dict | None = None) -> Document:
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


class _RecordingObserver:
    """Captures subscribe() so the test can invoke the registered callback
    directly -- exactly what AppsObserver would deliver on next tick."""

    def __init__(self):
        self.calls = []

    def subscribe(self, workflowId, document, callback):
        self.calls.append((workflowId, document, callback))


def test_modify_document_builds_empty_plot_and_bridge():
    app = BF.BandwidthAppFactory()
    handler = app.handlers[0]
    doc = _make_doc({"workflowId": [b"demo"]})
    handler.modify_document(doc)

    # An (empty) spectrum source exists and the figure is a root.
    sources = _spectrum_sources(doc)
    assert len(sources) == 1
    assert list(sources[0].data["x"]) == []


def test_modify_document_missing_workflowId_raises():
    app = BF.BandwidthAppFactory()
    handler = app.handlers[0]
    doc = _make_doc({"workflowId": [b""]})
    with pytest.raises(ValueError, match="workflowId"):
        handler.modify_document(doc)


def test_subscribes_to_observer_and_updates_on_publish():
    observer = _RecordingObserver()
    app = BF.BandwidthAppFactory(observer)
    handler = app.handlers[0]
    doc = _make_doc({"workflowId": [b"demo"]})
    handler.modify_document(doc)

    # Subscribed for this workflow + this document.
    assert len(observer.calls) == 1
    workflowId, sub_doc, callback = observer.calls[0]
    assert workflowId == "demo"
    assert sub_doc is doc

    # A published section recomputes the spectrum to that section's length.
    traces = np.zeros((100, 5), dtype=np.float32)
    traces[1, :] = 1.0
    callback([{"traces": traces, "dt": 0.004}])

    sources = _spectrum_sources(doc)
    assert len(sources) == 1
    assert len(sources[0].data["x"]) == (100 // 2) + 1
