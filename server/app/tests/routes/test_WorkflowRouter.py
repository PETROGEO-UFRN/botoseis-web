import pytest

from server.app.database.connection import database
from ..conftest import _app
from ..mock.Mock import Mock


class TestWorkflowRouter:
    url_prefix = "/workflow"
    client = pytest.client
    mock = Mock()
    created_workflows: list[dict] = []

    @pytest.fixture(autouse=True, scope='class')
    def _init_and_clean_database(self):
        with _app.app_context():
            database.drop_all()
            database.create_all()
            self.mock.loadUser()
            self.mock.loadSession()
            self.mock.loadProject()
            self.mock.loadLine()

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

    def test_create_new_workflow_with_bad_parent(self):
        expected_response_data = {
            'Error': {
                'parentType': ['Must be one of: projectId, lineId.']
            }
        }
        response = self.client.post(
            f"{self.url_prefix}/create/{self.mock.line['id']}",
            json={
                "name": f'NEW BAD WORKFLOW',
                "parentType": "badParent"
            },
        )
        assert response.status_code == 422
        assert response.json['Error'] == expected_response_data['Error']

    def test_create_new_workflow_with_inexistent_project(self):
        expected_response_data = {
            "Error": "No instance found for this id"
        }
        response = self.client.post(
            f"{self.url_prefix}/create/{self.mock.project['id'] + 99}",
            json={
                "name": f'NEW BAD WORKFLOW',
                "parentType": "projectId"
            },
        )
        assert response.status_code == 404
        assert response.json['Error'] == expected_response_data['Error']

    # todo: test bad request cases with dateset to block manual dataset
    def test_create_new_workflow_with_inexistent_line(self):
        expected_response_data = {
            "Error": "No instance found for this id"
        }
        response = self.client.post(
            f"{self.url_prefix}/create/{self.mock.line['id'] + 99}",
            json={
                "name": f'NEW BAD WORKFLOW',
                "parentType": "lineId"
            },
        )
        assert response.status_code == 404
        assert response.json['Error'] == expected_response_data['Error']

    def test_create_new_workflow_at_line(self):
        for i in range(3):
            expected_response_data = {
                "name": f'NEW WORKFLOW-{i}',
                "parentType": "lineId",
            }
            response = self.client.post(
                f"{self.url_prefix}/create/{self.mock.line['id']}",
                json={
                    "name": f'NEW WORKFLOW-{i}',
                    "parentType": "lineId"
                },
            )
            assert response.status_code == 200
            assert isinstance(response.json['id'], int)
            assert response.json['name'] == expected_response_data['name']
            # ? how will it work now ?
            assert response.json['input_file_link_id'] == None
            self.created_workflows.append(response.json)

    def test_create_new_workflow_at_project(self):
        for i in range(3):
            expected_response_data = {
                "name": f'NEW WORKFLOW-{i}',
                "parent": {
                    "parentType": "projectId",
                    "parentId": self.mock.project['id']
                },
            }
            response = self.client.post(
                f"{self.url_prefix}/create/{self.mock.project['id']}",
                json={
                    "name": f'NEW WORKFLOW-{i}',
                    "parentType": "projectId",
                },
            )
            assert response.status_code == 200
            assert isinstance(response.json['id'], int)
            assert response.json['name'] == expected_response_data['name']
            # ? how will it work now ?
            assert response.json['input_file_link_id'] == None
            self.created_workflows.append(response.json)

    def test_update_workflow_name(self):
        pass

    def test_invalid_token_workflow(self):
        self.client.set_cookie("Authorization", "!NV4L1dT0k3N")
        for workflow in self.created_workflows:
            response = self.client.delete(
                f"{self.url_prefix}/delete/{workflow['id']}",
            )
            assert response.status_code == 401

    def test_delete_workflow(self):
        self.mock.loadSession()
        for workflow in self.created_workflows:
            response = self.client.delete(
                f"{self.url_prefix}/delete/{workflow['id']}",
            )
            assert response.status_code == 200
            assert response.json == workflow
