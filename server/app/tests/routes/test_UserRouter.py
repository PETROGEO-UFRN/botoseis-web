import pytest

from server.app.database.connection import database
from ..conftest import _app
from ..mock.Mock import Mock, DEFAULT_PASSWORD


class TestUserRouter:
    url_prefix = "/user"
    client = pytest.client
    mock = Mock()
    created_users: list[dict] = []

    @pytest.fixture(scope='class', autouse=True)
    def _init_and_clean_database(self):
        """Fixture to set up and clean up the database for the test class."""
        with _app.app_context():
            database.drop_all()
            database.create_all()

        yield
        with _app.app_context():
            database.drop_all()
            database.create_all()

    def test_empty_get(self):
        """Test that listing users returns empty list if no users exist."""
        response = self.client.get(f"{self.url_prefix}/list")
        assert response.status_code == 200
        assert response.json == []

    def test_weak_password(self):
        """Test creating a user with a weak password returns a validation error."""
        expected_response_data = {
            "Error": {
                "password": ["Invalid Credentials"]
            }
        }
        response = self.client.post(
            f"{self.url_prefix}/create",
            json={
                "name": "weak_password_name",
                "email": "weak_password@email.com",
                "password": "weak",
            },
        )
        assert response.status_code == 422
        assert response.json == expected_response_data

    def test_create_new_user(self):
        """Test creating multiple new users with valid data."""
        for i in range(3):
            expected_response_data = {
                "name": f'user_{i}',
                "email": f'user_{i}@email.com'
            }
            response = self.client.post(
                f"{self.url_prefix}/create",
                json={
                    "name": expected_response_data["name"],
                    "email": expected_response_data["email"],
                    "password": DEFAULT_PASSWORD
                }
            )
            assert response.status_code == 200
            assert isinstance(response.json['id'], str)
            # *** shoud never return the password
            assert "password" not in response.json
            assert expected_response_data['name'] == response.json['name']
            assert expected_response_data['email'] == response.json['email']
            self.created_users.append(response.json)

    def test_list_users(self):
        """Test that listing users returns the users that were created."""
        response = self.client.get(f"{self.url_prefix}/list")
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert response.json == self.created_users

    def test_update_user(self):
        """Test updating a user's name with a valid session token."""
        for user in self.created_users:
            self.mock.loadSession(email=user['email'])
            response = self.client.put(
                f"{self.url_prefix}/update",
                json={"name": f"updated_{user['name']}"},
            )
            assert response.status_code == 200
            assert response.json['name'] == f"updated_{user['name']}"

    def test_invalid_token_user(self):
        """Test updating a user with an invalid token."""
        for _ in self.created_users:
            self.client.set_cookie("Authorization", "!NV4L1dT0k3N")
            response = self.client.delete(
                f"{self.url_prefix}/delete",
                headers={"Authorization": "!NV4L1dT0k3N"}
            )
            assert response.status_code == 401

    def test_delete_user(self):
        """Test deleting users with a valid session token."""
        for user in self.created_users:
            self.mock.loadSession(email=user['email'])
            response = self.client.delete(
                f"{self.url_prefix}/delete",
            )
            assert response.status_code == 200
            assert response.json['email'] == user['email']
