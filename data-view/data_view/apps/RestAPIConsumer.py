import orjson
from os import path
from requests import get, post
from typing import Literal

from ..constants import ENV


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

    def find_su_file_path(
        self,
        origin: Literal["input", "output"] = 'output'
    ) -> None | str:
        request_url = f"{ENV.BASE_API_URL}/su-file-path/{self.workflowId}/show-path/output"
        if origin == "input":
            request_url = request_url.replace("/output", "/input")

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

    def load_picks(
        self,
        times_key: str = 'times',
        velocities_key: str = 'velocities',
    ) -> dict[int, dict[str, list[float]]]:
        request_url = f"{ENV.BASE_API_URL}/helper-file/path/{self.workflowId}/table"

        if times_key and velocities_key:
            query_params = f"times_key={times_key}&velocities_key={velocities_key}"
            request_url = f"{request_url}?{query_params}"
        try:
            response = get(
                url=request_url,
                cookies=self.cookies
            )
            picks = response.json()['picks']
            return picks
        except:
            return dict()

    def save_picks(
        self,
        picks: dict[int, dict[str, list[float]]],
    ):
        request_url = f"{ENV.BASE_API_URL}/helper-file/generate/{self.workflowId}/table"

        json_bytes = orjson.dumps(
            {"picks": picks},
            option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_NON_STR_KEYS
        )

        post(
            url=request_url,
            cookies=self.cookies,
            data=json_bytes,
            headers={"Content-Type": "application/json"}
        )
