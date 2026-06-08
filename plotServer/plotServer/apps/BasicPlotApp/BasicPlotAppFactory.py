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
        auth_token = request.cookies.get('Authorization') or ''
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

        try:
            gather_key = setup.get('gather_key') if setup else None

            if gather_key:
                plot_options_state = PlotOptionsState(has_gather_key=True)
                plot_options_state.updatePlotOptionsState(
                    # first_cdp arrives 0-based (the gather to show); no -1.
                    gather_index_start=max(0, int(setup.get('first_cdp', 0))),
                    num_loadedgathers=int(setup.get('number_of_gathers_per_time', 1)),
                )
            else:
                plot_options_state = PlotOptionsState(has_gather_key=False)

            visualization = Visualization(
                filename=absolute_file_path,
                plot_options_state=plot_options_state,
                gather_key=gather_key,
            )

            document.add_root(visualization.plot)
            bridgeModelFactory(
                document=document,
                callback=bridgeCallbackFactory(visualization=visualization),
            )
        except Exception as exc:
            import traceback
            traceback.print_exc()
            raise

    return Application(FunctionHandler(func=modify_document))
