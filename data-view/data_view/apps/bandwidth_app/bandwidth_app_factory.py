import json
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.document.document import Document

from ...constants import ENV, FOLDERS, URL_PATHS
from ...BandwidthVisualization import Visualization

from ..loadTemplate import loadTemplate
from ..AppsObserver import AppsObserver


def bandwidth_app_factory(appsObserver: AppsObserver) -> Application:
    def __get_workflow_id(document: Document) -> str:
        session_context = document.session_context
        request = session_context.request
        arguments = request.arguments

        workflowId = arguments.get('workflowId', [b''])[0].decode('utf-8')

        return workflowId

    def modify_document(document: Document) -> None:
        workflowId = __get_workflow_id(document)

        visualization = Visualization(
            subscribeListener=lambda callback: appsObserver.subscribe(
                workflowId=workflowId,
                document=document,
                callback=callback
            ),
        )
        plots_row = visualization.plots_row

        # *** Render HTML
        template_variables = {
            "STATIC_PATH": URL_PATHS.STATIC_FILES,
            "IS_DEVELOPMENT": ENV.IS_DEVELOPMENT,
            "has_gather_key": True,
            # *** selecting a single CDP for bandwidth visualization
            # *** maybe shall selecct 2 cdps for velan pairing
            # *** => also possible for velan trigger to open 2 windows (one per cdp)
            "selected_cdp": 1,
        }
        html_template = loadTemplate(
            FOLDERS.BANDWIDTH_TEMPLATE_PATH,
            template_variables
        )

        document.template = html_template
        document.add_root(plots_row)

    # *** Create a new Bokeh Application
    bokeh_app = Application(
        FunctionHandler(func=modify_document),
    )

    return bokeh_app
