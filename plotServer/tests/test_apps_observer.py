"""Unit tests for plotServer.apps.AppsObserver.

AppsObserver only ever touches two Document methods -- add_next_tick_callback
(to deliver) and on_session_destroyed (to auto-clean) -- so a tiny fake Document
lets us drive delivery synchronously without a live Bokeh server.
"""
from plotServer.apps.AppsObserver import AppsObserver


class FakeDocument:
    def __init__(self):
        self._ticks = []
        self._on_destroyed = None

    # *** Methods AppsObserver calls
    def add_next_tick_callback(self, callback):
        self._ticks.append(callback)

    def on_session_destroyed(self, callback):
        self._on_destroyed = callback

    # *** Test drivers
    def run_ticks(self):
        scheduled, self._ticks = self._ticks, []
        for callback in scheduled:
            callback()

    def destroy_session(self):
        if self._on_destroyed is not None:
            self._on_destroyed(self)


def _recorder():
    received = []
    return received, lambda dataList: received.append(dataList)


def test_publish_delivers_to_all_subscribers():
    observer = AppsObserver()
    doc_a, doc_b = FakeDocument(), FakeDocument()
    got_a, cb_a = _recorder()
    got_b, cb_b = _recorder()
    observer.subscribe("wf1", doc_a, cb_a)
    observer.subscribe("wf1", doc_b, cb_b)

    payload = [{"traces": "X", "dt": 0.004}]
    observer.publish("wf1", payload)
    doc_a.run_ticks()
    doc_b.run_ticks()

    assert got_a == [payload]
    assert got_b == [payload]


def test_publish_skips_origin_document():
    observer = AppsObserver()
    emitter, listener = FakeDocument(), FakeDocument()
    got_emitter, cb_emitter = _recorder()
    got_listener, cb_listener = _recorder()
    observer.subscribe("wf1", emitter, cb_emitter)
    observer.subscribe("wf1", listener, cb_listener)

    observer.publish("wf1", [{"v": 1}], origin_document=emitter)
    emitter.run_ticks()
    listener.run_ticks()

    assert got_emitter == []          # emitter never receives its own data
    assert got_listener == [[{"v": 1}]]


def test_publish_to_unknown_workflow_is_noop():
    observer = AppsObserver()
    # Must not raise even with no subscribers for the key.
    observer.publish("nobody", [{"v": 1}])


def test_workflows_are_isolated():
    observer = AppsObserver()
    doc1, doc2 = FakeDocument(), FakeDocument()
    got1, cb1 = _recorder()
    got2, cb2 = _recorder()
    observer.subscribe("wf1", doc1, cb1)
    observer.subscribe("wf2", doc2, cb2)

    observer.publish("wf1", [{"only": "wf1"}])
    doc1.run_ticks()
    doc2.run_ticks()

    assert got1 == [[{"only": "wf1"}]]
    assert got2 == []


def test_subscribe_replays_last_payload():
    # A tab that connects AFTER the data was produced still gets the current
    # section immediately (e.g. Bandwidth opened while BasicPlot is running).
    observer = AppsObserver()
    observer.publish("wf1", [{"section": 1}])  # produced before anyone listens

    got, cb = _recorder()
    late = FakeDocument()
    observer.subscribe("wf1", late, cb)
    late.run_ticks()

    assert got == [[{"section": 1}]]


def test_replayed_payload_is_the_latest():
    observer = AppsObserver()
    observer.publish("wf1", [{"section": 1}])
    observer.publish("wf1", [{"section": 2}])

    got, cb = _recorder()
    late = FakeDocument()
    observer.subscribe("wf1", late, cb)
    late.run_ticks()

    assert got == [[{"section": 2}]]


def test_no_replay_without_prior_publish():
    observer = AppsObserver()
    got, cb = _recorder()
    doc = FakeDocument()
    observer.subscribe("wf1", doc, cb)
    doc.run_ticks()
    assert got == []


def test_session_destroyed_unsubscribes():
    observer = AppsObserver()
    doc = FakeDocument()
    got, cb = _recorder()
    observer.subscribe("wf1", doc, cb)

    doc.destroy_session()
    assert "wf1" not in observer.subscribers

    # A later publish reaches no one and schedules nothing.
    observer.publish("wf1", [{"v": 1}])
    doc.run_ticks()
    assert got == []
