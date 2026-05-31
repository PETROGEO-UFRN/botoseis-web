from os import path
from requests import get

from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.document.document import Document

from ...velocityModel import Visualization
from ...constants import ENV, FOLDERS, URL_PATHS
from ..loadTemplate import loadTemplate
from ..RestAPIConsumer import RestAPIConsumer


def velocity_model_app_factory() -> Application:
    def __get_request_arguments(document: Document) -> tuple[str, str]:
        session_context = document.session_context
        request = session_context.request
        arguments = request.arguments

        auth_token = request.cookies.get('Authorization', '')
        workflowId = arguments.get('workflowId', [b''])[0].decode('utf-8')

        return auth_token, workflowId

    def modify_document(document: Document) -> None:
        auth_token, workflowId = __get_request_arguments(
            document
        )

        restAPIConsumer = RestAPIConsumer(
            workflowId=workflowId,
            auth_token=auth_token
        )
        absolute_file_path = restAPIConsumer.find_su_file_path(
            origin='output'
        )
        picks_by_cdp = restAPIConsumer.load_picks()
        visualization = Visualization(
            filename=absolute_file_path,
            picks_by_cdp=picks_by_cdp,
        )
        plot = visualization.plot
        template_variables = {
            "STATIC_PATH": URL_PATHS.STATIC_FILES,
            "IS_DEVELOPMENT": ENV.IS_DEVELOPMENT,
        }
        html_template = loadTemplate(
            FOLDERS.VELOCITY_MODEL_TEMPLATE_PATH,
            template_variables
        )

        document.template = html_template
        document.add_root(plot)

    # *** Create a new Bokeh Application
    bokeh_app = Application(
        FunctionHandler(func=modify_document),
    )

    return bokeh_app
