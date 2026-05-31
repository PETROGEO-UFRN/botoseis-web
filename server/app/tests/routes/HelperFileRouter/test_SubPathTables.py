from .BaseTests import BaseTests
from ...mock.loadMockPicks import loadMockPicks


class TestSubPathTables(BaseTests):
    # *** used as subpath
    data_type = "table"

    def test_generate_table_file_with_no_picks(self):
        expeted_response_data = {
            'Error': {
                'picks': ['Missing data for required field.']
            }
        }
        response = self.client.post(
            f"{self.url_prefix}/generate/{self.mock.workflow['id']}/{self.data_type}",
            json={"workflowId": self.mock.workflow['id']}
        )
        assert response.status_code == 422
        assert response.json["Error"] == expeted_response_data["Error"]

    def test_generate_table_file_with_inexistent_workflow(self):
        mock_picks = loadMockPicks()

        expeted_response_data = {
            "Error": "No instance found for this id"
        }
        response = self.client.post(
            f"{self.url_prefix}/generate/99/{self.data_type}",
            json={
                "picks": mock_picks,
            }
        )
        assert response.status_code == 404
        assert response.json["Error"] == expeted_response_data["Error"]

    def test_generate_table_file(self):
        mock_picks = loadMockPicks()
        expeted_response_data = {
            "fileLink": {
                "path": '',
                "data_type": self.data_type,
                "lineId": self.mock.line['id'],
            }
        }
        response = self.client.post(
            f"{self.url_prefix}/generate/{self.mock.workflow['id']}/{self.data_type}",
            json={
                "picks": mock_picks,
            }
        )
        assert response.status_code == 200
        assert isinstance(response.json["fileLink"]["id"], int)
        assert response.json["fileLink"]["data_type"] == expeted_response_data["fileLink"]["data_type"]
        assert response.json["fileLink"]["lineId"] == expeted_response_data["fileLink"]["lineId"]
        self.stored_file_link["id"] = response.json["fileLink"]["id"]
        self.stored_file_link["data_type"] = response.json["fileLink"]["data_type"]
        self.stored_file_link["lineId"] = response.json["fileLink"]["lineId"]
