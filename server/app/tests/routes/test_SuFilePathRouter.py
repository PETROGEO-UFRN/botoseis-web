import pytest

from server.app.database.connection import database
from ..conftest import _app
from ..Mock import Mock


class TestSuFilePathRouter:
    url_prefix = "/su-file-path"
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

            self.mock.loadSuFileLink()
        yield
        with _app.app_context():
            database.drop_all()
            database.create_all()

    def test_show_path_with_inexistent_workflow(self):
        expeted_response_data = {
            "Error": "No instance found for this id"
        }
        response = self.client.get(
            f"{self.url_prefix}/99/show-path/input",
        )
        assert response.status_code == 404
        assert response.json["Error"] == expeted_response_data["Error"]

    def test_show_path_with_unset_input(self):
        expeted_response_data = {
            "Error": "No input file found for this workflow"
        }
        response = self.client.get(
            f"{self.url_prefix}/{self.mock.workflow['id']}/show-path/input",
        )
        assert response.status_code == 424
        # *** create other function to load workflow input
        assert response.json["Error"] == expeted_response_data["Error"]

    def test_show_path(self):
        self.mock.linkSuFileInputToWorkflow()
        expected_file_path = "/home/jorb/code/CloudSeis/server/static/root@email.com/1/marmousi_4ms_stack.su"

        response = self.client.get(
            f"{self.url_prefix}/{self.mock.workflow['id']}/show-path/input",
        )
        assert response.status_code == 200
        assert response.json["file_path"] == expected_file_path
