import base64
import json

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

        setup_b64 = arguments.get('setup', [b''])[0].decode('utf-8')
        setup: dict = {}
        if setup_b64:
            try:
                setup = json.loads(base64.b64decode(setup_b64))
            except Exception:
                setup = {}

        return workflowId, auth_token, origin, setup

    def modify_document(document: Document):
        workflowId, auth_token, origin, setup = __getRequestArguments(document)
        if not workflowId:
            raise ValueError("workflowId query param is required")

        consumer = RestAPIConsumer(workflowId=workflowId, auth_token=auth_token)
        absolute_file_path = consumer.find_su_file_path(origin=origin)
        if not absolute_file_path:
            raise ValueError(f"SU file path not found for workflowId={workflowId}")

        gather_key = setup.get('gather_key') if setup else None

        if gather_key:
            plot_options_state = PlotOptionsState(has_gather_key=True)
            plot_options_state.updatePlotOptionsState(
                gather_index_start=int(setup.get('first_cdp', 1)) - 1,
                num_loadedgathers=int(setup.get('number_of_gathers_per_time', 1)),
            )
            visualization = Visualization(
                filename=absolute_file_path,
                plot_options_state=plot_options_state,
                gather_key=gather_key,
            )
        else:
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
