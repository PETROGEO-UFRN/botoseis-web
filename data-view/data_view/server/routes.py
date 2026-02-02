from bokeh.application import Application
from data_view import apps

appsObserver = apps.AppsObserver()

routes: dict[str, Application] = {
    "/": apps.basic_plot_app_factory(),
    "/velan": apps.velan_app_factory(appsObserver),
    "/bandwidth": apps.bandwidth_app_factory(appsObserver),
    "/frequency-heatmap": apps.frequency_heatmap_app_factory(appsObserver),
    "/model": apps.velocity_model_app_factory(),
}
