import pytest

from server.app.database.connection import database
from ..conftest import _app
from ..mock.Mock import Mock


class TestProjectRouter:
    url_prefix = "/project"
    client = pytest.client
    mock = Mock()
    created_projects: list[dict] = []

    @pytest.fixture(scope='class', autouse=True)
    def _init_and_clean_database(self):
        """Fixture to set up and clean up the database for the test class."""
        with _app.app_context():
            database.drop_all()
            database.create_all()
            self.mock.loadUser()
            self.mock.loadSession()

        yield
        with _app.app_context():
            database.drop_all()
            database.create_all()

    def test_empty_get(self):
        response = self.client.get(
            f"{self.url_prefix}/list",
        )
        assert response.status_code == 200
        assert response.json == []

    def test_create_new_project(self):
        for i in range(3):
            expected_response_data = {
                "name": f'NEW PROJECT-{i}',
                "userId": self.mock.user['id']
            }
            response = self.client.post(
                f"{self.url_prefix}/create",
                json={
                    "name": f'NEW PROJECT-{i}',
                },
            )
            assert response.status_code == 200
            assert isinstance(response.json['id'], int)
            assert expected_response_data['name'] == response.json['name']
            assert expected_response_data['userId'] == response.json['userId']
            self.created_projects.append(response.json)

    def test_list_projects(self):
        response = self.client.get(
            f"{self.url_prefix}/list",
        )
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert response.json == self.created_projects

    def test_update_project_name(self):
        for project in self.created_projects:
            new_name = f"new_project_name_{project['id']}"
            project['name'] = new_name
            response = self.client.put(
                f"{self.url_prefix}/update/{project['id']}",
                json={
                    "name": new_name,
                },
            )
            project['modified_at'] = response.json['modified_at']
            assert response.status_code == 200
            assert response.json == project

    def test_invalid_token_project(self):
        self.client.set_cookie("Authorization", "!NV4L1dT0k3N")
        for project in self.created_projects:
            response = self.client.delete(
                f"{self.url_prefix}/delete/{project['id']}",
                headers={
                    "Authorization": "!NV4L1dT0k3N"
                }
            )
            assert response.status_code == 401

    def test_delete_project(self):
        self.mock.loadSession()
        for project in self.created_projects:
            response = self.client.delete(
                f"{self.url_prefix}/delete/{project['id']}",
            )
            assert response.status_code == 200
            assert response.json == project
