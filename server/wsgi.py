from server.app.create_app import create_app

if __name__ == "__main__":
    app = create_app("PRODUCTION")
    app.run()
