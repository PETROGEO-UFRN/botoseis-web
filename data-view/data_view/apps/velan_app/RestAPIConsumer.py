import orjson
from os import path
from requests import get, post
from typing import Literal

from ...constants import ENV


class RestAPIConsumer():
    lineId: int
    workflowId: int

    cookies: dict[Literal['a'], str]

    def __init__(
        self,
        workflowId,
        auth_token,
    ):
        self.workflowId = workflowId
        self.cookies = {
            "Authorization": f"Bearer {auth_token}"
        }

    def find_file_path(self) -> None | str:
        request_url = f"{ENV.BASE_API_URL}/su-file-path/{self.workflowId}/show-path/output"

        response = get(
            url=request_url,
            cookies=self.cookies
        )

        if response.status_code != 200:
            return None

        absolute_file_path = path.join(
            "..",
            "server",
            response.json()["file_path"],
        )

        return absolute_file_path

    def save_picks(
        self,
        picks: dict[int, list[float]],
    ):
        request_url = f"{ENV.BASE_API_URL}/helper-file/generate/{self.workflowId}/table"

        json_bytes = orjson.dumps(
            {"picks": picks},
            option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_NON_STR_KEYS
        )

        response = post(
            url=request_url,
            cookies=self.cookies,
            data=json_bytes,
            headers={"Content-Type": "application/json"}
        )
        import pdb
        pdb.set_trace()
        print(response)
