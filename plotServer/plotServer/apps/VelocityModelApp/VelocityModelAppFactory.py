from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.document.document import Document

from ..bridgeModelFactory import bridgeModelFactory
from ...services.RestAPIConsumer import RestAPIConsumer
from ...plots.VelocityModel import Visualization
from .bridgeCallbackFactory import bridgeCallbackFactory


def VelocityModelAppFactory() -> Application:
    def __getRequestArguments(document: Document):
        request = document.session_context.request
        arguments = request.arguments
        auth_token_morsel = request.cookies.get('Authorization')
        auth_token = auth_token_morsel.value if auth_token_morsel else ''
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
        picks_by_cdp = consumer.load_picks()

        visualization = Visualization(
            filename=absolute_file_path,
            picks_by_cdp=picks_by_cdp,
        )
        document.add_root(visualization.plot)
        bridgeModelFactory(
            document=document,
            callback=bridgeCallbackFactory(),
        )

    return Application(FunctionHandler(func=modify_document))
