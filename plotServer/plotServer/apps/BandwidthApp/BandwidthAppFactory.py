from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.document.document import Document

from ..AppsObserver import AppsObserver
from ..bridgeModelFactory import bridgeModelFactory
from ...plots.Bandwidth import Visualization
from .bridgeCallbackFactory import bridgeCallbackFactory


def BandwidthAppFactory(observer: AppsObserver | None = None) -> Application:
    def __getRequestArguments(document: Document):
        request = document.session_context.request
        arguments = request.arguments
        workflowId = arguments.get('workflowId', [b''])[0].decode('utf-8')
        return workflowId

    def modify_document(document: Document):
        workflowId = __getRequestArguments(document)
        if not workflowId:
            raise ValueError("workflowId query param is required")

        # Bandwidth reads no file: it starts empty and is driven entirely by the
        # observer feed (the section another tab, e.g. BasicPlot, is showing).
        visualization = Visualization()
        document.add_root(visualization.plot)
        bridgeModelFactory(
            document=document,
            callback=bridgeCallbackFactory(),
        )

        # *** Live feed: recompute the spectrum from the section published for
        # this workflowId. AppsObserver dispatches on this document's next tick
        # (thread-safe), replays the current section on connect, and
        # auto-unsubscribes when this session closes.
        if observer is not None:
            def on_section_published(dataList: list[dict]):
                if not dataList:
                    return
                payload = dataList[-1]
                visualization.update_from_traces(
                    payload["traces"], payload["dt"]
                )

            observer.subscribe(workflowId, document, on_section_published)

    return Application(FunctionHandler(func=modify_document))
