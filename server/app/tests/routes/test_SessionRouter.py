import pytest
import base64
import json

from server.app.database.connection import database
from ..conftest import _app
from ..Mock import Mock, DEFAULT_PASSWORD


class TestSessionRouter:
    url_prefix = "/session"
    client = pytest.client
    mock = Mock()
    created_projects: list[dict] = []
    session_token: str = ""

    @pytest.fixture(scope='class', autouse=True)
    def _init_and_clean_database(self):
        """Fixture to set up and clean up the database for the test class."""
        with _app.app_context():
            database.drop_all()
            database.create_all()
            self.mock.loadUser()

        yield
        with _app.app_context():
            database.drop_all()
            database.create_all()

    def test_create_session(self):
        response = self.client.post(
            f"{self.url_prefix}/",
            json={
                "email": self.mock.user["email"],
                "password": DEFAULT_PASSWORD,
            }
        )
        assert response.status_code == 200
        assert response.json["message"] == "Logged in"

        set_cookie_header = response.headers.get("Set-Cookie")
        assert set_cookie_header is not None
        assert set_cookie_header.startswith("Authorization=")
        # *** check JWT format
        cookie_value = set_cookie_header.split("=", 1)[1].split(";", 1)[0]
        parts = cookie_value.split(".")
        assert len(parts) == 3, (
            "Token should have 3 parts: header.payload.signature"
        )
        assert all(parts), "JWT parts must be non-empty"
        self.session_token = cookie_value

    def test_validate_session(self):
        response = self.client.get(
            f"{self.url_prefix}/validate",
            headers={"Cookie": self.session_token}
        )
        assert response.status_code == 204
        assert response.json == None
