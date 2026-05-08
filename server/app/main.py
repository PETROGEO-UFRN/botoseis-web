from .create_app import create_app
from dotenv import load_dotenv


if __name__ == "main":
    load_dotenv()
    app = create_app("DEVELOPMENT")

    app.run(debug=True)
