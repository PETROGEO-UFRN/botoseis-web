import pytest
from os import path

from server.app.database.connection import database
from ...conftest import _app
from ...mock.Mock import Mock


class BaseTests:
    url_prefix = "/helper-file"
    client = pytest.client
    mock = Mock()
    stored_file_link = dict()
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
            self.mock.loadLine()
        yield
        with _app.app_context():
            database.drop_all()
            database.create_all()

    def test_empty_get(self):
        response = self.client.get(
            f"{self.url_prefix}/list/{self.mock.line['id']}/{self.data_type}s",
        )
        assert response.status_code == 200
        assert response.json == []

    def test_list_files_with_inexistent_line(self):
        expeted_response_data = {
            "Error": "No instance found for this id"
        }
        response = self.client.get(
            f"{self.url_prefix}/list/99/{self.data_type}s",
        )
        assert response.status_code == 404
        assert response.json["Error"] == expeted_response_data["Error"]

    def test_upload_file_with_no_file(self):
        expeted_response_data = {
            'Error': {
                'file': ['Missing data for required field.']
            }
        }
        response = self.client.post(
            f"{self.url_prefix}/upload/{self.mock.line['id']}/{self.data_type}",
        )
        assert response.status_code == 422
        assert response.json["Error"] == expeted_response_data["Error"]

    def test_upload_file_with_inexistent_line(self):
        expeted_response_data = {
            "Error": "No instance found for this id"
        }
        with open(self.mock.base_marmousi_stack_path, "rb") as file:
            response = self.client.post(
                f"{self.url_prefix}/upload/99/{self.data_type}",
                data={
                    "file": (file, path.basename(file.name))
                },
                content_type="multipart/form-data"
            )
        assert response.status_code == 404
        assert response.json["Error"] == expeted_response_data["Error"]

    def test_upload_file(self):
        with open(self.mock.base_marmousi_stack_path, "rb") as file:
            file_path = path.basename(file.name)
            expeted_response_data = {
                "fileLink": {
                    "path": file_path,
                    "data_type": self.data_type,
                    "lineId": self.mock.line['id'],
                }
            }
            response = self.client.post(
                f"{self.url_prefix}/upload/{self.mock.line['id']}/{self.data_type}",
                data={
                    "file": (file, file_path)
                },
                content_type="multipart/form-data"
            )
        assert response.status_code == 200
        assert isinstance(response.json["fileLink"]["id"], int)
        assert response.json["fileLink"]["data_type"] == expeted_response_data["fileLink"]["data_type"]
        assert response.json["fileLink"]["lineId"] == expeted_response_data["fileLink"]["lineId"]
        self.stored_file_link["id"] = response.json["fileLink"]["id"]
        self.stored_file_link["data_type"] = response.json["fileLink"]["data_type"]
        self.stored_file_link["lineId"] = response.json["fileLink"]["lineId"]

    def test_list_files(self):
        response = self.client.get(
            f"{self.url_prefix}/list/{self.mock.line['id']}/{self.data_type}s",
            content_type="multipart/form-data"
        )

        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) == 1
        assert isinstance(response.json[0]["id"], int)
        assert response.json[0]["data_type"] == self.stored_file_link["data_type"]
        assert response.json[0]["lineId"] == self.stored_file_link["lineId"]
