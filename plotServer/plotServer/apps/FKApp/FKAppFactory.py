from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.document.document import Document

from ..bridgeModelFactory import bridgeModelFactory
from ...plots.FK import Visualization
from .bridgeCallbackFactory import bridgeCallbackFactory


def FKAppFactory() -> Application:
    def modify_document(document: Document):
        request = document.session_context.request
        arguments = request.arguments
        workflowId = arguments.get('workflowId', [b''])[0].decode('utf-8')
        if not workflowId:
            raise ValueError("workflowId query param is required")

        visualization = Visualization()
        document.add_root(visualization.plot)
        bridgeModelFactory(
            document=document,
            callback=bridgeCallbackFactory(),
        )

    return Application(FunctionHandler(func=modify_document))
