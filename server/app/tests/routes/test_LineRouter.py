import pytest

from server.app.database.connection import database
from ..conftest import _app
from ..mock.Mock import Mock


class TestLineRouter:
    url_prefix = "/line"
    client = pytest.client
    mock = Mock()
    created_lines: list[dict] = []

    #! this fixture implementation shall be checked to be
    #! fully adopted on ent-to-end tests at this app
    @pytest.fixture(autouse=True, scope='class')
    def _init_and_clean_database(self):
        with _app.app_context():
            database.drop_all()
            database.create_all()
            self.mock.loadUser()
            self.mock.loadSession()
            self.mock.loadProject()
            self.mock.loadWorkflow()

        yield
        with _app.app_context():
            database.drop_all()
            database.create_all()

    def test_empty_get(self):
        response = self.client.get(
            f"{self.url_prefix}/list/{self.mock.project['id']}",
        )
        assert response.status_code == 200
        assert response.json == []

    def test_create_new_line(self):
        for i in range(3):
            expected_response_data = {
                "name": f'NEW LINE-{i}',
                "projectId": self.mock.project['id']
            }
            response = self.client.post(
                f"{self.url_prefix}/create/{self.mock.project['id']}",
                json={
                    "name": f'NEW LINE-{i}',
                    "projectId": self.mock.project['id']
                },
            )
            assert response.status_code == 200
            assert isinstance(response.json['id'], int)
            assert expected_response_data['name'] == response.json['name']
            assert expected_response_data['projectId'] == response.json['projectId']
            self.created_lines.append(response.json)

    def test_list_lines(self):
        response = self.client.get(
            f"{self.url_prefix}/list/{self.mock.project['id']}",
        )
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert response.json == self.created_lines

    def test_update_line_name(self):
        for line in self.created_lines:
            expected_response_data = {
                "id": line['id'],
                "projectId": self.mock.project['id'],
                "name": f"new_line_name_{line['id']}",
                "workflows": []
            }
            response = self.client.put(
                f"{self.url_prefix}/update/{line['id']}",
                json={
                    "name": f"new_line_name_{line['id']}",
                },
            )

            assert response.status_code == 200
            assert response.json == expected_response_data

    def test_invalid_token_line(self):
        self.client.set_cookie("Authorization", "!NV4L1dT0k3N")
        for line in self.created_lines:
            response = self.client.delete(
                f"{self.url_prefix}/delete/{line['id']}",
                headers={
                    "Authorization": "!NV4L1dT0k3N"
                }
            )
            assert response.status_code == 401

    def test_delete_line(self):
        self.mock.loadSession()
        for line in self.created_lines:
            response = self.client.delete(
                f"{self.url_prefix}/delete/{line['id']}",
            )
            assert response.status_code == 200
