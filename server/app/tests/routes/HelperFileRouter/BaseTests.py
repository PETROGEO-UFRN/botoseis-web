import pytest
from os import path

from server.app.database.connection import database
from ...conftest import _app
from ...Mock import Mock


class BaseTests:
    url_prefix = "/helper-file"
    client = pytest.client
    mock = Mock()
    created_file_link = dict()
    # *** used as subpath, set by derived classes
    data_type = ""

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
        yield
        with _app.app_context():
            database.drop_all()
            database.create_all()

    def test_empty_get(self):
        response = self.client.get(
            f"{self.url_prefix}/list/{self.mock.project['id']}/{self.data_type}s",
        )
        assert response.status_code == 200
        assert response.json == []

    def test_list_files_with_inexistent_project(self):
        expeted_response_data = {
            "Error": "No instance found for this id"
        }
        response = self.client.get(
            f"{self.url_prefix}/list/99/{self.data_type}s",
        )
        assert response.status_code == 404
        assert response.json["Error"] == expeted_response_data["Error"]

    def test_create_file_with_no_file(self):
        expeted_response_data = {
            "Error": "No file part in the request"
        }
        response = self.client.post(
            f"{self.url_prefix}/create/{self.mock.project['id']}/{self.data_type}",
        )

        assert response.status_code == 400
        assert response.json["Error"] == expeted_response_data["Error"]

    def test_create_file_with_inexistent_workflow(self):
        expeted_response_data = {
            "Error": "No instance found for this id"
        }
        with open(self.mock.base_marmousi_stack_path, "rb") as file:
            response = self.client.post(
                f"{self.url_prefix}/create/99/{self.data_type}",
                data={
                    "file": (file, path.basename(file.name))
                },
                content_type="multipart/form-data"
            )
        assert response.status_code == 404
        assert response.json["Error"] == expeted_response_data["Error"]

    def test_create_file(self):
        with open(self.mock.base_marmousi_stack_path, "rb") as file:
            file_path = path.basename(file.name)
            expeted_response_data = {
                "fileLink": {
                    "path": file_path,
                    "projectId": self.mock.project['id'],
                    "data_type": self.data_type,
                }
            }
            response = self.client.post(
                f"{self.url_prefix}/create/{self.mock.project['id']}/{self.data_type}",
                data={
                    "file": (file, file_path)
                },
                content_type="multipart/form-data"
            )
        assert response.status_code == 200
        assert isinstance(response.json["fileLink"]["id"], int)
        assert response.json["fileLink"]["projectId"] == expeted_response_data["fileLink"]["projectId"]
        assert response.json["fileLink"]["data_type"] == expeted_response_data["fileLink"]["data_type"]
        self.created_file_link["id"] = response.json["fileLink"]["id"]
        self.created_file_link["projectId"] = response.json["fileLink"]["projectId"]
        self.created_file_link["data_type"] = response.json["fileLink"]["data_type"]

    def test_list_files(self):
        response = self.client.get(
            f"{self.url_prefix}/list/{self.mock.project['id']}/{self.data_type}s",
            content_type="multipart/form-data"
        )

        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) == 1
        assert isinstance(response.json[0]["id"], int)
        assert response.json[0]["projectId"] == self.created_file_link["projectId"]
        assert response.json[0]["data_type"] == self.created_file_link["data_type"]
