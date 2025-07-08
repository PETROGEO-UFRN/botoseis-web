import pytest
from os import path

from sqlalchemy import text

from server.app.database.connection import database
from ..conftest import _app
from ..Mock import Mock


class TestSuFileRouter:
    url_prefix = "/su-file"
    client = pytest.client
    mock = Mock()
    created_file_link = dict()

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

            self.mock.loadProgramGroup()
            self.mock.loadSufilterCommand()
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

    def test_list_su_files_with_inexistent_workflow(self):
        expeted_response_data = {
            "Error": "No instance found for this id"
        }
        response = self.client.get(
            f"{self.url_prefix}/list/99",
        )
        assert response.status_code == 404
        assert response.json["Error"] == expeted_response_data["Error"]

    def test_create_su_file_with_no_file(self):
        expeted_response_data = {
            "Error": "No file part in the request"
        }
        response = self.client.post(
            f"{self.url_prefix}/create/{self.mock.project['id']}",
        )

        assert response.status_code == 400
        assert response.json["Error"] == expeted_response_data["Error"]

    def test_create_su_file_with_inexistent_workflow(self):
        expeted_response_data = {
            "Error": "No instance found for this id"
        }
        with open(self.mock.base_marmousi_stack_path, "rb") as file:
            response = self.client.post(
                f"{self.url_prefix}/create/99",
                data={
                    "file": (file, path.basename(file.name))
                },
                content_type="multipart/form-data"
            )
        assert response.status_code == 404
        assert response.json["Error"] == expeted_response_data["Error"]

    def test_create_su_file(self):
        with open(self.mock.base_marmousi_stack_path, "rb") as file:
            file_path = path.basename(file.name)
            expeted_response_data = {
                "fileLink": {
                    "path": file_path,
                    "projectId": self.mock.project['id'],
                    "data_type": "su",
                }
            }
            response = self.client.post(
                f"{self.url_prefix}/create/{self.mock.project['id']}",
                data={
                    "file": (file, file_path)
                },
                content_type="multipart/form-data"
            )
        assert response.status_code == 200
        assert isinstance(response.json["fileLink"]["id"], int)
        assert response.json["fileLink"]["path"] == expeted_response_data["fileLink"]["path"]
        assert response.json["fileLink"]["projectId"] == expeted_response_data["fileLink"]["projectId"]
        assert response.json["fileLink"]["data_type"] == expeted_response_data["fileLink"]["data_type"]
        self.created_file_link["id"] = response.json["fileLink"]["id"]
        self.created_file_link["path"] = response.json["fileLink"]["path"]
        self.created_file_link["projectId"] = response.json["fileLink"]["projectId"]
        self.created_file_link["data_type"] = response.json["fileLink"]["data_type"]

    def test_list_su_files(self):
        response = self.client.get(
            f"{self.url_prefix}/list/{self.mock.project['id']}",
            content_type="multipart/form-data"
        )

        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) == 1
        assert isinstance(response.json[0]["id"], int)
        assert response.json[0]["path"] == self.created_file_link["path"]
        assert response.json[0]["projectId"] == self.created_file_link["projectId"]
        assert response.json[0]["data_type"] == self.created_file_link["data_type"]

    def test_update_su_file_with_output_unset(self):
        expeted_response_data = {
            "Error": "Output name should be set before running workflow"
        }

        response = self.client.put(
            f"{self.url_prefix}/update/{self.mock.project['id']}",
            content_type="multipart/form-data"
        )
        assert response.status_code == 424
        assert response.json["Error"] == expeted_response_data["Error"]

    def test_update_su_file_with_output_unset(self):
        expeted_response_data = {
            "Error": "Output name should be set before running workflow"
        }

        response = self.client.put(
            f"{self.url_prefix}/update/{self.mock.project['id']}",
            content_type="multipart/form-data"
        )
        assert response.status_code == 424
        assert response.json["Error"] == expeted_response_data["Error"]

    def test_update_su_file(self):
        # ! Needs documentation and/or refactoring
        # ! broken test, needs more mocking
        with _app.app_context():
            database.session.execute(
                text(
                    "UPDATE workflows_table SET output_name = :output_name WHERE id = :id"
                ),
                {"output_name": "mock_output_marmousi",
                    "id": self.mock.workflow["id"]}
            )
            database.session.execute(
                text(
                    "UPDATE workflows_table SET input_file_link_id = :input_file_link_id WHERE id = :id"
                ),
                # ! missing link id
                {"input_file_link_id": self.created_file_link["id"],
                    "id": self.mock.workflow["id"]}
            )
            database.session.commit()

        response = self.client.put(
            f"{self.url_prefix}/update/{self.mock.project['id']}",
            content_type="multipart/form-data"
        )
        assert response.status_code == 200
