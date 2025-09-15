from typing import Literal
from os import path
from requests import get
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.document.document import Document
from jinja2 import Template

from ..basicPlot import Visualization, PlotOptionsState
from ..constants.paths import index_template_path, static_url_path
from .config import BASE_URL

with open(index_template_path, "r", encoding="utf-8") as file:
    html_template = Template(file.read())


def app_factory():
    def __find_file_path(auth_token: str, workflowId: int, origin: Literal["input", "output"]) -> None | str:
        api_url = f"{BASE_URL}/su-file-path/{workflowId}/show-path/output"
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

    def modify_document(document: Document) -> None:
        session_context = document.session_context
        request = session_context.request
        arguments = request.arguments

        auth_token = request.cookies.get('Authorization', '')
        gather_key: str = arguments.get('gather_key', [b''])[0].decode('utf-8')
        workflowId = arguments.get('workflowId', [b''])[0].decode('utf-8')
        origin = arguments.get('origin', [b''])[0].decode('utf-8')
        absolute_file_path = __find_file_path(
            auth_token=auth_token,
            workflowId=int(workflowId),
            origin=origin
        )
        visualization = Visualization(
            gather_key=gather_key or None,
            filename=absolute_file_path,
            plot_options_state=PlotOptionsState(gather_key=gather_key or None),
        )
        plot = visualization.plot_manager.plot

        document.template = html_template
        document.template_variables["static_path"] = static_url_path

        document.add_root(plot)

    # *** Create a new Bokeh Application
    bokeh_app = Application(
        FunctionHandler(func=modify_document),
    )

    return bokeh_app
