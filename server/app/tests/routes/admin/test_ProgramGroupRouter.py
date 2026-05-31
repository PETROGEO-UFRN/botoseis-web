import pytest

from server.app.database.connection import database
from ...conftest import _app
from ...mock.Mock import Mock


class TestProgramGroupRouter:
    url_prefix = "/programs/groups"
    client = pytest.client
    mock = Mock()
    created_groups: list[dict] = []

    #! this fixture implementation shall be checked to be
    #! fully adopted on ent-to-end tests at this app
    @pytest.fixture(autouse=True, scope='class')
    def _init_and_clean_database(self):
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

    def test_create_new_program_group(self):
        for i in range(3):
            expected_response_data = {
                "name": f"NEW PROGRAM GROUP - {i}",
                "description": "some description",
                "programs": [],
            }
            response = self.client.post(
                f"{self.url_prefix}/create",
                json={
                    "name": f"NEW PROGRAM GROUP - {i}",
                    "description": "some description",
                },
            )
            assert response.status_code == 200
            assert isinstance(response.json['id'], int)
            assert response.json['name'] == expected_response_data['name']
            assert response.json['description'] == expected_response_data['description']
            self.created_groups.append(response.json)

    def test_update_program_group_name(self):
        for index, group in enumerate(self.created_groups):
            expected_response_data = {
                "id": group['id'],
                "name": f"GROUP {group['id']} new name",
                "description": group['description'],
                "programs": [],
            }
            response = self.client.put(
                f"{self.url_prefix}/update/{group['id']}",
                json={
                    "name": f"GROUP {group['id']} new name",
                },
            )

            assert response.status_code == 200
            assert response.json == expected_response_data
            self.created_groups[index]['name'] = response.json['name']

    def test_update_program_group_description(self):
        for index, group in enumerate(self.created_groups):
            expected_response_data = {
                "id": group['id'],
                "name": group['name'],
                "description": "some new updated description",
                "programs": [],
            }
            response = self.client.put(
                f"{self.url_prefix}/update/{group['id']}",
                json={
                    "description": "some new updated description",
                },
            )

            assert response.status_code == 200
            assert response.json == expected_response_data
            self.created_groups[index]['description'] = response.json['description']

    def test_list_program_groups(self):
        response = self.client.get(
            f"{self.url_prefix}/list",
        )
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) == len(self.created_groups)

        for index, group in enumerate(self.created_groups):
            assert response.status_code == 200
            assert isinstance(response.json[index]['id'], int)
            assert response.json[index]['id'] == group['id']
            assert response.json[index]['name'] == group['name']
            assert response.json[index]['description'] == group['description']
            assert response.json[index]['programs'] == group['programs']

    def test_delete_program(self):
        for program_group in self.created_groups:
            response = self.client.delete(
                f"{self.url_prefix}/delete/{program_group['id']}",
            )
            assert response.status_code == 200
            assert isinstance(response.json['id'], int)
            assert response.json['id'] == program_group['id']
            assert response.json['name'] == program_group['name']
            assert response.json['description'] == program_group['description']
            assert response.json['programs'] == program_group['programs']
