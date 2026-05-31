from copy import deepcopy
import pytest

from server.app.database.connection import database
from ..conftest import _app
from ..mock.Mock import Mock


class TestCommandRouter:
    url_prefix = "/command"
    client = pytest.client
    mock = Mock()
    created_commands: list[dict] = []

    @pytest.fixture(autouse=True, scope='class')
    def _init_and_clean_database(self):
        with _app.app_context():
            database.drop_all()
            database.create_all()
            self.mock.loadUser()
            self.mock.loadSession()
            self.mock.loadProject()
            self.mock.loadLine()
            self.mock.loadWorkflow()
            self.mock.loadProgramGroup()
            self.mock.loadProgram()

        yield
        with _app.app_context():
            database.drop_all()
            database.create_all()

    def test_empty_get(self):
        expected_response_data = {
            "Error": "No instance found for this id"
        }
        response = self.client.get(
            f"{self.url_prefix}/show/1",
        )
        assert response.status_code == 404
        assert response.json['Error'] == expected_response_data['Error']

    def test_create_new_command_with_inexistent_workflow(self):
        expected_response_data = {
            "Error": "No instance found for this id"
        }
        response = self.client.post(
            f"{self.url_prefix}/create/{self.mock.workflow['id'] + 99}",
            json={
                "name": "NO EXISTING PARENT",
                "parameters": "SUDEFAULT",
                "program_id": self.mock.program['id'],
            },
        )

        assert response.status_code == 404
        assert response.json['Error'] == expected_response_data['Error']

    def test_create_new_command_with_inexistent_program(self):
        expected_response_data = {
            "Error": "Program does not exist"
        }
        response = self.client.post(
            f"{self.url_prefix}/create/{self.mock.workflow['id']}",
            json={
                "name": "NO EXISTING PARENT",
                "parameters": "SUDEFAULT",
                "program_id": 99,
            },
        )

        assert response.status_code == 404
        assert response.json['Error'] == expected_response_data['Error']

    def test_create_new_command(self):
        for i in range(3):
            expected_response_data = {
                "name": f"NEW COMMAND-{i}",
                "workflowId": self.mock.workflow['id'],
                "parameters": "SUDEFAULT",
                "program_id": self.mock.program['id'],
            }
            response = self.client.post(
                f"{self.url_prefix}/create/{self.mock.workflow['id']}",
                json={
                    "name": f"NEW COMMAND-{i}",
                    "parameters": "SUDEFAULT",
                    "program_id": self.mock.program['id'],
                },
            )
            assert response.status_code == 200
            assert isinstance(response.json['id'], int)
            assert response.json['name'] == expected_response_data['name']
            assert response.json['is_active'] == True
            self.created_commands.append(response.json)

    def test_show_command(self):
        for command in self.created_commands:
            response = self.client.get(
                f"{self.url_prefix}/show/{command['id']}",
            )
            assert response.status_code == 200
            assert isinstance(response.json['id'], int)
            assert response.json['id'] == command['id']
            assert response.json['name'] == command['name']
            assert response.json['is_active'] == command['is_active']

    # todo: this test as well as its domains need repair
    def test_update_command_parameters(self):
        for index, command in enumerate(self.created_commands):
            expected_response_data = {
                "parameters": f"SUDEFAULT-updated-{command['id']}",
            }
            response = self.client.put(
                f"{self.url_prefix}/update/{command['id']}/parameters",
                json={
                    "parameters": f"SUDEFAULT-updated-{command['id']}",
                },
            )
            assert response.status_code == 200
            assert isinstance(response.json['id'], int)
            assert response.json['id'] == command['id']
            assert response.json['name'] == command['name']
            assert response.json['is_active'] == command['is_active']
            assert response.json['parameters'] == expected_response_data['parameters']
            self.created_commands[index] = response.json

    def test_update_command_is_active(self):
        for index, command in enumerate(self.created_commands):
            response = self.client.put(
                f"{self.url_prefix}/update/{command['id']}/is_active",
            )
            assert response.status_code == 200
            assert isinstance(response.json['id'], int)
            assert response.json['id'] == command['id']
            assert response.json['name'] == command['name']
            assert response.json['is_active'] == (not command['is_active'])
            assert response.json['parameters'] == command['parameters']
            self.created_commands[index] = response.json

    def test_update_order_command(self):
        order = [command["id"] for command in self.created_commands]
        # *** swap first and last item from command order
        order[0], order[-1] = order[-1], order[0]
        expected_response_data = deepcopy(self.created_commands)
        expected_response_data[0], expected_response_data[-1] = expected_response_data[-1], expected_response_data[0]

        response = self.client.put(
            f"{self.url_prefix}/order/{self.mock.workflow['id']}",
            json={
                "newOrder": order,
            },
        )
        assert response.status_code == 200
        assert isinstance(response.status_code, int)
        assert isinstance(response.json, list)
        for index, command in enumerate(expected_response_data):
            assert isinstance(response.json[index]['id'], int)
            assert response.json[index]["id"] == order[index]
            assert response.json[index]["program_id"] == command["program_id"]
            assert response.json[index]["workflowId"] == command["workflowId"]
            assert response.json[index]["name"] == command["name"]
            assert response.json[index]["is_active"] == command["is_active"]
            assert response.json[index]["parameters"] == command["parameters"]
        self.created_commands = expected_response_data

    def test_delete_command_with_invalid(self):
        self.client.set_cookie("Authorization", "!NV4L1dT0k3N")
        for command in self.created_commands:
            response = self.client.delete(
                f"{self.url_prefix}/delete/{command['id']}",
                headers={
                    "Authorization": "!NV4L1DT0K3N"
                }
            )
            assert response.status_code == 401

    def test_delete_command(self):
        self.mock.loadSession()
        for command in self.created_commands:
            response = self.client.delete(
                f"{self.url_prefix}/delete/{command['id']}",
            )
            assert response.status_code == 200
