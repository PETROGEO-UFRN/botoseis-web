from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.document.document import Document
from jinja2 import Template


from ..basicPlot import Visualization, PlotOptionsState
from ..constants.paths import index_template_path, static_url_path

with open(index_template_path, "r", encoding="utf-8") as file:
    html_template = Template(file.read())


def app_factory():
    def modify_document(document: Document) -> None:
        visualization = Visualization(
            gather_key=None,
            filename="",
            plot_options_state=PlotOptionsState(gather_key=None),
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
