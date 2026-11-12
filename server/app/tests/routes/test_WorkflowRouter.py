import pytest

from ..conftest import reset_database
from ..mock.Mock import Mock


class TestWorkflowRouter:
    url_prefix = "/workflow"
    client = pytest.client
    mock = Mock()
    created_workflows: list[dict] = []

    @pytest.fixture(autouse=True, scope='class')
    def _init_and_clean_database(self):
        reset_database()
        self.mock.loadUser()
        self.mock.loadSession()
        self.mock.loadProject()
        self.mock.loadLine()

        yield
        reset_database()

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

    def test_update_post_processing(self):
        # *** Precondition: records created by test_create_new_workflow_at_line and test_create_new_workflow_at_project
        assert len(self.created_workflows) == 6, "expected 6 workflows from test_create_new_workflow_at_line and test_create_new_workflow_at_project"
        for workflow in self.created_workflows:
            expected_options = {
                "key": "tab-vizualizer",
                "options": {"gain": 2, "label": "stack", "clip": 0.5, "flip": True},
            }
            response = self.client.put(
                f"{self.url_prefix}/update/{workflow['id']}/post-processing",
                json=expected_options,
            )
            assert response.status_code == 200
            assert response.json == {"post_processing_options": expected_options}
            workflow["post_processing_options"] = expected_options

    def test_update_post_processing_with_invalid_body(self):
        # *** Precondition: records created by test_create_new_workflow_at_line and test_create_new_workflow_at_project
        assert len(self.created_workflows) == 6, "expected 6 workflows from test_create_new_workflow_at_line and test_create_new_workflow_at_project"
        workflow_id = self.created_workflows[0]['id']
        response = self.client.put(
            f"{self.url_prefix}/update/{workflow_id}/post-processing",
            json={"key": "tab-vizualizer", "options": {"nested": {"gain": 2}}},
        )
        assert response.status_code == 422
        assert response.json['Error'] == {
            "options": ["Value for key 'nested' at 'options' must be a primite. Got dict."]
        }

        response = self.client.put(
            f"{self.url_prefix}/update/{workflow_id}/post-processing",
            json={"options": {}},
        )
        assert response.status_code == 422
        assert response.json['Error'] == {"key": ["Missing data for required field."]}

    def test_invalid_token_workflow(self):
        # *** Precondition: records created by test_create_new_workflow_at_line and test_create_new_workflow_at_project
        assert len(self.created_workflows) == 6, "expected 6 workflows from test_create_new_workflow_at_line and test_create_new_workflow_at_project"
        self.client.set_cookie("Authorization", "!NV4L1dT0k3N")
        for workflow in self.created_workflows:
            response = self.client.delete(
                f"{self.url_prefix}/delete/{workflow['id']}",
            )
            assert response.status_code == 401

    def test_delete_workflow(self):
        # *** Precondition: records created by test_create_new_workflow_at_line and test_create_new_workflow_at_project
        assert len(self.created_workflows) == 6, "expected 6 workflows from test_create_new_workflow_at_line and test_create_new_workflow_at_project"
        self.mock.loadSession()
        for workflow in self.created_workflows:
            response = self.client.delete(
                f"{self.url_prefix}/delete/{workflow['id']}",
            )
            assert response.status_code == 200
            assert response.json == workflow
