import pytest

from server.app.database.connection import database
from ...conftest import _app
from ...mock.Mock import Mock


class TestProgramRouter:
    url_prefix = "/programs"
    client = pytest.client
    mock = Mock()
    created_programs: list[dict] = []

    #! this fixture implementation shall be checked to be
    #! fully adopted on ent-to-end tests at this app
    @pytest.fixture(autouse=True, scope='class')
    def _init_and_clean_database(self):
        with _app.app_context():
            database.drop_all()
            database.create_all()
            self.mock.loadUser()
            self.mock.loadSession()
            self.mock.loadProgramGroup()

        yield
        with _app.app_context():
            database.drop_all()
            database.create_all()

    def test_empty_get(self):
        response = self.client.get(
            f"{self.url_prefix}/list/{self.mock.programGroup['id']}",
        )
        assert response.status_code == 200
        assert response.json == []

    def test_create_new_program_with_inexistent_group(self):
        expected_response_data = {
            "Error": "Program Group does not exist"
        }
        response = self.client.post(
            f"{self.url_prefix}/create/9999",
            data={
                "name": "NOTSUFILTER",
                "description": "description of NOTSUFILTER",
                "path_to_executable_file": "notsufilter",
            },
        )
        assert response.status_code == 404
        assert response.json['Error'] == expected_response_data['Error']

    def test_create_new_program_with_json(self):
        expected_response_data = {
            "Error": "No body, JSON is not accepted for this route"
        }
        response = self.client.post(
            f"{self.url_prefix}/create/{self.mock.programGroup['id']}",
            json={
                "name": "NOTSUFILTER",
                "description": "description of NOTSUFILTER",
                "path_to_executable_file": "notsufilter",
            },
        )
        assert response.status_code == 415
        assert response.json['Error'] == expected_response_data['Error']

    def test_create_new_program(self):
        for i in range(3):
            expected_response_data = {
                "name": f"NOTSUFILTER - {i}",
                "description": "description of NOTSUFILTER",
                "path_to_executable_file": "notsufilter",
                "groupId": self.mock.programGroup['id']
            }
            response = self.client.post(
                f"{self.url_prefix}/create/{self.mock.programGroup['id']}",
                data={
                    "name": f"NOTSUFILTER - {i}",
                    "description": "description of NOTSUFILTER",
                    "path_to_executable_file": "notsufilter",
                },
            )
            assert response.status_code == 200
            assert isinstance(response.json['id'], int)
            assert response.json['name'] == expected_response_data['name']
            assert response.json['description'] == expected_response_data['description']
            assert response.json['path_to_executable_file'] == expected_response_data['path_to_executable_file']
            assert response.json['groupId'] == expected_response_data['groupId']
            self.created_programs.append(response.json)

    def test_list_program_groups(self):
        response = self.client.get(
            f"{self.url_prefix}/list/{self.mock.programGroup['id']}",
        )
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) == len(self.created_programs)

        for index, program in enumerate(self.created_programs):
            assert response.status_code == 200
            assert isinstance(response.json[index]['id'], int)
            assert response.json[index]['id'] == program['id']
            assert response.json[index]['name'] == program['name']
            assert response.json[index]['description'] == program['description']
            assert response.json[index]['path_to_executable_file'] == program['path_to_executable_file']
            assert response.json[index]['groupId'] == program['groupId']

    def test_delete_program(self):
        for program in self.created_programs:
            response = self.client.delete(
                f"{self.url_prefix}/delete/{program['id']}",
            )
            assert response.status_code == 200
            assert isinstance(response.json['id'], int)
            assert response.json['id'] == program['id']
            assert response.json['name'] == program['name']
            assert response.json['description'] == program['description']
            assert response.json['path_to_executable_file'] == program['path_to_executable_file']
            assert response.json['groupId'] == program['groupId']
