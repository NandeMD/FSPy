from typing import Union, Literal, Optional, List
import requests
from .response_models import FlareSolverNotOK, SessionsListResponse
import orjson


class FlareSolverrError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class FlareSolverr:
    def __init__(
            self,
            host: str = "127.0.0.1",
            port: Optional[Union[str, int]] = "8191",
            http_schema: Literal["http", "https"] = "http",
            additional_headers: dict = {},
            v: str = "v1"
    ) -> None:
        self.req_session = requests.Session()
        self.req_session.headers.update = {"Content-Type": "application/json", **additional_headers}

        self.host = host
        self.port = str(port) if port is not None else None
        self.http_schema = http_schema
        self.v = v
        self.flare_solverr_url = f"{http_schema}://{host}{':' + self.port if port is not None else ''}/{v}"

    @property
    def sessions(self) -> Union[List[str], FlareSolverNotOK]:
        payload = {
            "cmd": "sessions.list"
        }
        response = self.req_session.post(self.flare_solverr_url, json=payload)
        response_dict = orjson.loads(response.content)

        if response_dict["status"] != "ok":
            return FlareSolverNotOK.from_dict(response_dict)
        return SessionsListResponse.from_dict(response_dict).sessions
