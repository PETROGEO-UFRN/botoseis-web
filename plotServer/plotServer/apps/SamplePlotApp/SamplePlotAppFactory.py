from bokeh.document import Document
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from ..bridgeModelFactory import bridgeModelFactory
from .SamplePlot import SamplePlot
from .bridgeCallbackFactory import bridgeCallbackFactory


def SamplePlotAppFactory() -> Application:
    def modify_document(document: Document):
        request = document.session_context.request
        workflowId = request.arguments.get('workflowId', [b'demo'])[0].decode('utf-8')
        plot = SamplePlot(workflowId=workflowId)
        document.add_root(plot.plot)
        bridgeModelFactory(document=document, callback=bridgeCallbackFactory(plot=plot))
    return Application(FunctionHandler(func=modify_document))
