from bokeh.application import Application
from ..apps import app_factory

routes: dict[str, Application] = {
    "/": app_factory()
}
