import pytest
from copy import deepcopy

from server.app.database.connection import database
from ...conftest import _app
from ...mock.Mock import Mock


class TestParameterRouter:
    url_prefix = "/programs/parameters"
    client = pytest.client
    mock = Mock()
    created_parameters: list[dict] = []

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
            self.mock.loadProgram()

        yield
        with _app.app_context():
            database.drop_all()
            database.create_all()

    def test_empty_get(self):
        expected_response_data = {
            "Error": "There are no parameters for this program"
        }
        response = self.client.get(
            f"{self.url_prefix}/list/{self.mock.program['id']}",
        )
        assert response.status_code == 200
        assert response.json == []

    def test_create_new_parameter_with_inexistent_program(self):
        expected_response_data = {
            "Error": "Program does not exist"
        }
        response = self.client.post(
            f"{self.url_prefix}/create/9999",
        )
        assert response.status_code == 404
        assert response.json['Error'] == expected_response_data['Error']

    def test_create_new_parameter(self):
        # *** parameters shall be initialized empty
        for _ in range(3):
            response = self.client.post(
                f"{self.url_prefix}/create/{self.mock.program['id']}",
            )
            assert response.status_code == 200
            assert isinstance(response.json['id'], int)
            assert response.json['name'] == ""
            assert response.json['description'] == ""
            assert response.json['input_type'] == ""
            assert response.json['isRequired'] == False
            self.created_parameters.append(response.json)

    def test_update_parameter_only_name(self):
        for index, parameter in enumerate(self.created_parameters):
            expected_response_data = deepcopy(parameter)
            expected_response_data["name"] = f"new name - {parameter['id']}"

            response = self.client.put(
                f"{self.url_prefix}/update/{parameter['id']}",
                json={
                    "name": f"new name - {parameter['id']}",
                },
            )
            assert response.status_code == 200
            assert response.json == expected_response_data
            self.created_parameters[index]["name"] = response.json["name"]

    def test_update_parameter_only_description(self):
        for index, parameter in enumerate(self.created_parameters):
            expected_response_data = deepcopy(parameter)
            expected_response_data["description"] = "New description"

            response = self.client.put(
                f"{self.url_prefix}/update/{parameter['id']}",
                json={
                    "description": "New description",
                },
            )
            assert response.status_code == 200
            assert response.json == expected_response_data
            self.created_parameters[index]["description"] = response.json["description"]

    def test_update_parameter_only_example(self):
        for index, parameter in enumerate(self.created_parameters):
            expected_response_data = deepcopy(parameter)
            expected_response_data["example"] = "New Usage Example: 0.,1.,...,1.,0."

            response = self.client.put(
                f"{self.url_prefix}/update/{parameter['id']}",
                json={
                    "example": "New Usage Example: 0.,1.,...,1.,0.",
                },
            )
            assert response.status_code == 200
            assert response.json == expected_response_data
            self.created_parameters[index]["example"] = response.json["example"]

    def test_update_parameter_only_input_type(self):
        for index, parameter in enumerate(self.created_parameters):
            expected_response_data = deepcopy(parameter)
            # ! could test allowed types
            expected_response_data["input_type"] = "string"

            response = self.client.put(
                f"{self.url_prefix}/update/{parameter['id']}",
                json={
                    "input_type": "string",
                },
            )
            assert response.status_code == 200
            assert response.json == expected_response_data
            self.created_parameters[index]["input_type"] = response.json["input_type"]

    def test_update_parameter_only_isRequired(self):
        for index, parameter in enumerate(self.created_parameters):
            expected_response_data = deepcopy(parameter)
            expected_response_data["isRequired"] = True

            response = self.client.put(
                f"{self.url_prefix}/update/{parameter['id']}",
                json={
                    "isRequired": True,
                },
            )
            assert response.status_code == 200
            assert response.json == expected_response_data
            self.created_parameters[index]["isRequired"] = response.json["isRequired"]

    def test_update_parameter_multiple_fields(self):
        for index, parameter in enumerate(self.created_parameters):
            expected_response_data = deepcopy(parameter)
            expected_response_data['description'] = "Description and type update"
            expected_response_data['input_type'] = "boolean"

            response = self.client.put(
                f"{self.url_prefix}/update/{parameter['id']}",
                json={
                    "description": "Description and type update",
                    "input_type": "boolean",
                },
            )
            assert response.status_code == 200
            assert response.json == expected_response_data
            self.created_parameters[index]["description"] = response.json["description"]
            self.created_parameters[index]["input_type"] = response.json["input_type"]

    def test_show_parameter(self):
        response = self.client.get(
            f"{self.url_prefix}/list/{self.mock.program['id']}",
        )
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) == len(self.created_parameters)

        for index, parameter in enumerate(self.created_parameters):
            assert response.status_code == 200
            assert isinstance(response.json[index]['id'], int)
            assert response.json[index]['id'] == parameter['id']
            assert response.json[index]['name'] == parameter['name']
            assert response.json[index]['description'] == parameter['description']
            assert response.json[index]['input_type'] == parameter['input_type']
            assert response.json[index]['isRequired'] == parameter['isRequired']

    def test_delete_parameter(self):
        for program in self.created_parameters:
            response = self.client.delete(
                f"{self.url_prefix}/delete/{program['id']}",
            )
            assert response.status_code == 200
            assert isinstance(response.json['id'], int)
            assert response.json['id'] == program['id']
            assert response.json['name'] == program['name']
            assert response.json['description'] == program['description']
            assert response.json['input_type'] == program['input_type']
            assert response.json['isRequired'] == program['isRequired']
