import json
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.document.document import Document

from ...constants import ENV, FOLDERS, URL_PATHS
from ...velan import Visualization, VelanPlotOptionsState

from ..loadTemplate import loadTemplate
from ..create_bridge_model import create_bridge_model
from ..addFinishLoadingEvent import addFinishLoadingEvent
from .create_bridge_callback import create_bridge_callback
from ..RestAPIConsumer import RestAPIConsumer
from ..AppsObserver import AppsObserver


def velan_app_factory(appsObserver: AppsObserver) -> Application:
    def __get_request_arguments(document: Document) -> tuple[str, str]:
        session_context = document.session_context
        request = session_context.request
        arguments = request.arguments

        auth_token = request.cookies.get('Authorization', '')
        velan_starter_props = json.loads(
            request.cookies.get('velan_starter_props', '')
        )
        workflowId = arguments.get('workflowId', [b''])[0].decode('utf-8')

        # *** convert client 1 based index to server 0 based index
        velan_starter_props["first_cdp"] -= 1
        velan_starter_props["last_cdp"] -= 1

        return auth_token, workflowId, velan_starter_props

    def modify_document(document: Document) -> None:
        auth_token, workflowId, velan_starter_props = __get_request_arguments(
            document
        )

        # *** Load external data
        restAPIConsumer = RestAPIConsumer(
            workflowId=workflowId,
            auth_token=auth_token
        )
        picks = restAPIConsumer.load_picks(
            # *** keys compatible with bokeh data source
            times_key='y',
            velocities_key='x',
        )
        absolute_file_path = restAPIConsumer.find_su_file_path()

        # *** Build plot
        plot_options_state = VelanPlotOptionsState(
            **velan_starter_props
        )
        visualization = Visualization(
            filename=absolute_file_path,
            plot_options_state=plot_options_state,
            loaded_picks=picks,
            onUpdateDispatcher=lambda data: appsObserver.publish(
                workflowId,
                data
            ),
        )
        plots_row = visualization.plots_row

        # *** Set client events
        addFinishLoadingEvent(plots_row)
        state_changer_bridge_model = create_bridge_model(
            visualization=visualization,
            callback=create_bridge_callback(
                restAPIConsumer=restAPIConsumer
            )
        )

        # *** Render HTML
        template_variables = {
            "workflowId": workflowId,

            "STATIC_PATH": URL_PATHS.STATIC_FILES,
            "IS_DEVELOPMENT": ENV.IS_DEVELOPMENT,
            "has_gather_key": True,
            "is_velan": True,
            "total_gathers_amount": plot_options_state.num_gathers,
            "number_of_gathers_per_time": plot_options_state.number_of_gathers_per_time,

            # *** convert back server 0 based index to client 1 based index
            "first_cdp": plot_options_state.first_cdp + 1,
            "last_cdp": plot_options_state.last_cdp + 1
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
