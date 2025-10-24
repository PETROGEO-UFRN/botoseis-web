from typing import Literal
from os import path
from requests import get
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.document.document import Document


from ..basicPlot import Visualization, PlotOptionsState
from ..constants import ENV, FOLDERS, URL_PATHS
from .loadTemplate import loadTemplate
from .create_bridge_model import create_bridge_model


def app_factory() -> Application:
    def __find_file_path(
        auth_token: str,
        workflowId: int,
        origin: Literal["input", "output"]
    ) -> None | str:
        api_url = f"{ENV.BASE_API_URL}/su-file-path/{workflowId}/show-path/output"
        if origin == "input":
            api_url = api_url.replace("/output", "/input")
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

    def __get_request_arguments(document: Document) -> tuple[str, str, str, str]:
        session_context = document.session_context
        request = session_context.request
        arguments = request.arguments

        auth_token = request.cookies.get('Authorization', '')
        gather_key: str = arguments.get('gather_key', [b''])[0].decode('utf-8')
        workflowId = arguments.get('workflowId', [b''])[0].decode('utf-8')
        origin = arguments.get('origin', [b''])[0].decode('utf-8')
        return (
            origin,
            auth_token,
            workflowId,
            gather_key,
        )

    def modify_document(document: Document) -> None:
        (
            origin,
            auth_token,
            workflowId,
            gather_key
        ) = __get_request_arguments(document)

        absolute_file_path = __find_file_path(
            auth_token=auth_token,
            workflowId=int(workflowId),
            origin=origin
        )

        plot_options_state = PlotOptionsState(has_gather_key=bool(gather_key))
        visualization = Visualization(
            gather_key=gather_key or None,
            filename=absolute_file_path,
            plot_options_state=plot_options_state,
        )
        plot = visualization.plot_manager.plot

        state_changer_bridge_model = create_bridge_model(
            visualization=visualization
        )

        template_variables = {
            "STATIC_PATH": URL_PATHS.STATIC_FILES,
            "IS_DEVELOPMENT": ENV.IS_DEVELOPMENT,
            "has_gather_key": gather_key,
        }
        if gather_key:
            template_variables["total_gathers_amount"] = plot_options_state.num_gathers
        html_template = loadTemplate(
            FOLDERS.BASIC_PLOT_TEMPLATE_PATH,
            template_variables
        )

        document.template = html_template
        document.add_root(plot)
        document.add_root(state_changer_bridge_model)

    # *** Create a new Bokeh Application
    bokeh_app = Application(
        FunctionHandler(func=modify_document),
    )

    return bokeh_app
