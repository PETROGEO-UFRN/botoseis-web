from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.document.document import Document

from ..bridgeModelFactory import bridgeModelFactory
from ...services.RestAPIConsumer import RestAPIConsumer
from ...plots.Bandwidth import Visualization
from .bridgeCallbackFactory import bridgeCallbackFactory


def BandwidthAppFactory() -> Application:
    def __getRequestArguments(document: Document):
        request = document.session_context.request
        arguments = request.arguments
        auth_token = request.cookies.get('Authorization') or ''
        workflowId = arguments.get('workflowId', [b''])[0].decode('utf-8')
        return workflowId, auth_token

    def modify_document(document: Document):
        workflowId, auth_token = __getRequestArguments(document)
        if not workflowId:
            raise ValueError("workflowId query param is required")

        consumer = RestAPIConsumer(workflowId=workflowId, auth_token=auth_token)
        absolute_file_path = consumer.find_su_file_path(origin='output')
        if not absolute_file_path:
            raise ValueError(f"SU file path not found for workflowId={workflowId}")

        visualization = Visualization(filename=absolute_file_path)
        document.add_root(visualization.plot)
        bridgeModelFactory(
            document=document,
            callback=bridgeCallbackFactory(),
        )

    return Application(FunctionHandler(func=modify_document))
