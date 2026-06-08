from typing import Callable
from bokeh.document.document import Document


class AppsObserver():
    """
    Allow cross app communication.

    Connects multiple tabs, allows data cross tab action triggering and data
    sharing between them.

    The latest payload per workflowId is cached so a tab that connects *after*
    the data was produced (e.g. a Bandwidth tab opened while BasicPlot is
    already running) is handed the current section as soon as it subscribes,
    instead of waiting for the next publish.
    """

    subscribers: dict[
        int | str,
        list[tuple[
            Document,
            Callable[[list[dict]], None]
        ]]
    ]
    last_payloads: dict[int | str, list[dict]]

    def __init__(self):
        self.subscribers = {}
        self.last_payloads = {}

    def subscribe(
        self,
        workflowId: int | str,
        document: Document,
        callback: Callable[[list[dict]], None]
    ) -> None:
        subscriber = (document, callback)
        if workflowId not in self.subscribers:
            self.subscribers[workflowId] = []
        self.subscribers[workflowId].append(subscriber)

        # *** Auto-cleanup when the session/tab is closed
        document.on_session_destroyed(
            lambda _: self.unsubscribe(workflowId, subscriber)
        )

        # *** Replay the latest section so a late-joining tab syncs immediately
        if workflowId in self.last_payloads:
            dataList = self.last_payloads[workflowId]
            document.add_next_tick_callback(
                lambda callback=callback, dataList=dataList: callback(dataList)
            )

    def unsubscribe(
        self,
        workflowId: int | str,
        subscriber: tuple[Document, Callable[[dict], None]]
    ) -> None:
        if workflowId in self.subscribers:
            self.subscribers[workflowId].remove(subscriber)
            if not self.subscribers[workflowId]:
                self.subscribers.pop(workflowId)

    def publish(
        self,
        workflowId: int | str,
        dataList: list[dict],
        origin_document: Document | None = None,
    ):
        """
        Broadcast data to all other apps sharing the same workflowId.

        The document calling "publish" can also be subscribed (for
        multi-directional communication) but shall not receive data emitted by
        itself: pass its document as ``origin_document`` to skip it.
        """
        # Cache as the current section even if nobody is subscribed yet, so a
        # later subscriber gets it on connect.
        self.last_payloads[workflowId] = dataList

        if workflowId not in self.subscribers:
            return

        for document, callback in self.subscribers[workflowId]:
            if origin_document is not None and document is origin_document:
                continue
            # *** Use add_next_tick_callback to ensure thread-safety for the target document
            document.add_next_tick_callback(
                lambda callback=callback, dataList=dataList: callback(dataList)
            )
