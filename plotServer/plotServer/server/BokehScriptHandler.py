import tornado.web
from bokeh.embed import server_document
from ..config.urls import baseServerURL
from ..config.allowedOrigins import allowedHTTPOrigins
from ..constants.ROUTE_PATHS import ROUTE_PATHS


REGISTERED_APP_NAMES = frozenset(
    path.lstrip("/")
    for path in (
        ROUTE_PATHS.BASIC_PLOT,
        ROUTE_PATHS.VELOCITY_MODEL,
        ROUTE_PATHS.VELAN,
    )
)


class BokehScriptHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        for origin in allowedHTTPOrigins:
            self.set_header("Access-Control-Allow-Origin", origin)
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "GET, OPTIONS")

    def options(self, app_name):
        self.set_status(204)
        self.finish()

    def get(self, app_name):
        workflowId = self.get_argument("workflowId", "")
        if not workflowId:
            self.set_status(400)
            self.write({"error": "workflowId query param is required"})
            return
        if app_name not in REGISTERED_APP_NAMES:
            self.set_status(404)
            self.write({"error": f"App {app_name} not found"})
            return
        setup = self.get_argument("setup", "")
        bokeh_url = f"{baseServerURL}/{app_name}"
        arguments = {"workflowId": workflowId}
        if setup:
            arguments["setup"] = setup
        try:
            script = server_document(url=bokeh_url, arguments=arguments)
            self.write({"script": script})
        except Exception:
            self.set_status(500)
            self.write({"error": f"Failed to generate script for {app_name}"})
