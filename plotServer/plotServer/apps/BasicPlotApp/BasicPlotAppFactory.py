from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.document.document import Document

from ..bridgeModelFactory import bridgeModelFactory
from ...services.RestAPIConsumer import RestAPIConsumer
from ...plots.BasicPlot import Visualization, PlotOptionsState
from .bridgeCallbackFactory import bridgeCallbackFactory


def BasicPlotAppFactory() -> Application:
    def __getRequestArguments(document: Document):
        request = document.session_context.request
        arguments = request.arguments
        auth_token = request.cookies.get('Authorization')
        auth_token = auth_token.value if auth_token else ''
        workflowId = arguments.get('workflowId', [b''])[0].decode('utf-8')
        origin = arguments.get('origin', [b'output'])[0].decode('utf-8') or 'output'
        return workflowId, auth_token, origin

    def modify_document(document: Document):
        workflowId, auth_token, origin = __getRequestArguments(document)
        if not workflowId:
            raise ValueError("workflowId query param is required")

        consumer = RestAPIConsumer(workflowId=workflowId, auth_token=auth_token)
        absolute_file_path = consumer.find_su_file_path(origin=origin)
        if not absolute_file_path:
            raise ValueError(f"SU file path not found for workflowId={workflowId}")

        plot_options_state = PlotOptionsState(has_gather_key=False)
        visualization = Visualization(
            filename=absolute_file_path,
            plot_options_state=plot_options_state,
            gather_key=None,
        )
        document.add_root(visualization.plot_manager.plot)
        bridgeModelFactory(
            document=document,
            callback=bridgeCallbackFactory(visualization=visualization),
        )

    return Application(FunctionHandler(func=modify_document))
