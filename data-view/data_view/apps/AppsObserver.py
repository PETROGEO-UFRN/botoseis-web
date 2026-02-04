from typing import Callable
from bokeh.document.document import Document


class AppsObserver():
    """
    Allow cross app communication.

    Connects multiple tabs, allows data cross tab action triggering and data sharing between them.
    """

    subscribers: dict[
        int | str,
        tuple[
            Document,
            Callable[[dict], None]
        ]
    ]

    def __init__(self):
        self.subscribers = {}

    def subscribe(
        self,
        workflowId: int | str,
        document: Document,
        callback: Callable[[dict], None]
    ) -> None:
        subscriber = (document, callback)
        if workflowId not in self.subscribers:
            self.subscribers[workflowId] = []
        self.subscribers[workflowId].append(subscriber)

        # *** Auto-cleanup when the session/tab is closed
        document.on_session_destroyed(
            lambda _: self.unsubscribe(workflowId, subscriber)
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
    ):
        """
        Broadcast data to all other apps sharing the same workflowId.

        Document calling "emit" can be also subscribied for multi-directional 
        communication but shall not receive data emitted by itself.
        """
        if workflowId not in self.subscribers:
            return

        for document, callback in self.subscribers[workflowId]:
            # *** Use add_next_tick_callback to ensure thread-safety for the target document
            # document.add_next_tick_callback(lambda: callback(data))
            document.add_next_tick_callback(
                lambda callback=callback, dataList=dataList: callback(dataList)
            )
