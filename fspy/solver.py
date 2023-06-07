from typing import Union, Literal, Optional
import requests
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
        additional_headers: Optional[dict] = None
        ) -> None:
        self.req_session = requests.Session()
        self.req_session.headers.update = {"Content-Type": "application/json", **additional_headers}
        
        self.host = host
        self.port = str(port)
        self.http_schema = http_schema
        self.flare_solverr_url = f"{http_schema}://{host}{':'+self.port if port is not None else ''}"
        
    @property
    def sessions(self):
        payload = {
            "cmd": "sessions.list"
        }
        response = self.req_session.get(self.flare_solverr_url)
        