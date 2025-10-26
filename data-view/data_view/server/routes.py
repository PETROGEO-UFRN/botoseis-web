from bokeh.application import Application
from data_view import apps

routes: dict[str, Application] = {
    "/": apps.basic_plot_app_factory(),
    "/velan": apps.velan_app_factory()
}
