import json
from os import path
from requests import get
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.document.document import Document

from ..constants import ENV, FOLDERS, URL_PATHS
from ..velan import Visualization, VelanPlotOptionsState

from .loadTemplate import loadTemplate
from .create_bridge_model import create_bridge_model
from .addFinishLoadingEvent import addFinishLoadingEvent


def velan_app_factory() -> Application:
    def __find_file_path(
        auth_token: str,
        workflowId: int,
    ) -> None | str:
        api_url = f"{ENV.BASE_API_URL}/su-file-path/{workflowId}/show-path/output"

        cookies = {
            "Authorization": f"Bearer {auth_token}"
        }

        response = get(api_url, cookies=cookies)

        if response.status_code != 200:
            return None

        absolute_file_path = path.join(
            "..",
            "server",
            response.json()["file_path"],
        )

        return absolute_file_path

    def __get_request_arguments(document: Document) -> tuple[str, str]:
        session_context = document.session_context
        request = session_context.request
        arguments = request.arguments

        auth_token = request.cookies.get('Authorization', '')
        velan_starter_props = json.loads(
            request.cookies.get('velan_starter_props', '')
        )
        workflowId = arguments.get('workflowId', [b''])[0].decode('utf-8')

        return auth_token, workflowId, velan_starter_props

    def modify_document(document: Document) -> None:
        auth_token, workflowId, velan_starter_props = __get_request_arguments(
            document
        )

        absolute_file_path = __find_file_path(
            auth_token=auth_token,
            workflowId=int(workflowId),
        )

        # *** server uses 0 based index
        velan_starter_props["first_cdp"] -= 1
        velan_starter_props["last_cdp"] -= 1
        plot_options_state = VelanPlotOptionsState(
            **velan_starter_props
        )
        visualization = Visualization(
            filename=absolute_file_path,
            plot_options_state=plot_options_state,
        )
        plots_row = visualization.plots_row
        addFinishLoadingEvent(plots_row)

        state_changer_bridge_model = create_bridge_model(
            visualization=visualization
        )

        # *** server uses 0 based index
        template_variables = {
            "STATIC_PATH": URL_PATHS.STATIC_FILES,
            "IS_DEVELOPMENT": ENV.IS_DEVELOPMENT,
            "has_gather_key": True,
            "is_velan": True,
            "total_gathers_amount": plot_options_state.num_gathers,
            "first_cdp": plot_options_state.first_cdp + 1,
            "last_cdp": plot_options_state.last_cdp + 1,
            "number_of_gathers_per_time": plot_options_state.number_of_gathers_per_time
        }
        html_template = loadTemplate(
            FOLDERS.VELAN_TEMPLATE_PATH,
            template_variables
        )

        document.template = html_template
        document.add_root(plots_row)
        document.add_root(state_changer_bridge_model)

    # *** Create a new Bokeh Application
    bokeh_app = Application(
        FunctionHandler(func=modify_document),
    )

    return bokeh_app
