from .api import app_factory, server_factory

# *** Run the Bokeh server application
if __name__ == '__main__':
    server = server_factory(
        bokeh_app=app_factory()
    )
    server.start()
    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()
