import base64
import json

from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.document.document import Document

from ..bridgeModelFactory import bridgeModelFactory
from ...services.RestAPIConsumer import RestAPIConsumer
from ...plots.Velan import Visualization, VelanPlotOptionsState
from .bridgeCallbackFactory import bridgeCallbackFactory

REQUIRED_SETUP_KEYS = ('first_cdp', 'last_cdp', 'number_of_gathers_per_time')


def VelanAppFactory() -> Application:
    def __getRequestArguments(document: Document):
        request = document.session_context.request
        arguments = request.arguments
        auth_token_morsel = request.cookies.get('Authorization')
        auth_token = auth_token_morsel.value if auth_token_morsel else ''
        workflowId = arguments.get('workflowId', [b''])[0].decode('utf-8')

        setup_b64 = arguments.get('setup', [b''])[0].decode('utf-8')
        if not setup_b64:
            raise ValueError("setup query param is required for velan")

        try:
            setup = json.loads(base64.b64decode(setup_b64))
        except Exception as exc:
            raise ValueError(f"Invalid setup param: {exc}") from exc

        for key in REQUIRED_SETUP_KEYS:
            if key not in setup:
                raise ValueError(f"Missing required setup key: {key}")

        return workflowId, auth_token, setup

    def modify_document(document: Document):
        workflowId, auth_token, setup = __getRequestArguments(document)
        if not workflowId:
            raise ValueError("workflowId query param is required")

        consumer = RestAPIConsumer(workflowId=workflowId, auth_token=auth_token)
        absolute_file_path = consumer.find_su_file_path(origin='output')
        if not absolute_file_path:
            raise ValueError(f"SU file path not found for workflowId={workflowId}")

        picks = consumer.load_picks(times_key='y', velocities_key='x')

        # first_cdp arrives as user-visible 1-based; convert to 0-based gather_index_start
        setup['first_cdp'] = int(setup['first_cdp']) - 1
        plot_options_state = VelanPlotOptionsState(**setup)

        visualization = Visualization(
            filename=absolute_file_path,
            plot_options_state=plot_options_state,
            loaded_picks=picks,
        )

        document.add_root(visualization.plots_row)
        bridgeModelFactory(
            document=document,
            callback=bridgeCallbackFactory(
                visualization=visualization,
                consumer=consumer,
            ),
        )

    return Application(FunctionHandler(func=modify_document))
