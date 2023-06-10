from typing import Union, Literal, Optional, List

import orjson
import requests

from .response_models import FlareSolverError, SessionsListResponse, SesssionCreateResponse, FlareSolverOK
from .solver_exceptions import UnsupportedProxySchema


class FlareSolverrError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class FlareSolverr:
    def __init__(
            self,
            host: str = "127.0.0.1",
            port: Optional[Union[str, int]] = "8191",
            http_schema: Literal["http", "https"] = "http",
            additional_headers: dict = None,
            v: str = "v1"
    ) -> None:
        self.req_session = requests.Session()
        ah = additional_headers if additional_headers is not None else {}
        self.req_session.headers.update = {"Content-Type": "application/json", **ah}

        self.host = host
        self.port = str(port) if port is not None else None
        self.http_schema = http_schema
        self.v = v
        self.flare_solverr_url = f"{http_schema}://{host}{':' + self.port if port is not None else ''}/{v}"

    @property
    def sessions(self) -> Union[List[str], FlareSolverError]:
        """
        Get session ids as a list.
        Returns 'FlareSolverNotOK' object if flaresolverr status != 'ok'
        """
        payload = {
            "cmd": "sessions.list"
        }
        response = self.req_session.post(self.flare_solverr_url, json=payload)
        response_dict = orjson.loads(response.content)

        if response_dict["status"] != "ok":
            return FlareSolverError.from_dict(response_dict)
        return SessionsListResponse.from_dict(response_dict).sessions

    @property
    def _sessions_raw(self) -> Union[SessionsListResponse, FlareSolverError]:
        """
        Get the whole response as SessionsListResponse object.
        Returns 'FlareSolverNotOK' object if flaresolverr status != 'ok'
        """
        payload = {
            "cmd": "sessions.list"
        }
        response = self.req_session.post(self.flare_solverr_url, json=payload)
        response_dict = orjson.loads(response.content)

        if response_dict["status"] != "ok":
            return FlareSolverError.from_dict(response_dict)
        return SessionsListResponse.from_dict(response_dict)

    def create_session(self, session_id: str = None, proxy_url: str = None) -> Union[SesssionCreateResponse, FlareSolverError]:
        """
        Create a session. This will launch a new browser instance which will retain cookies.
        :param session_id: String. Optional.
        :param proxy_url: String. Optional. Must include proxy schema. ("http://", "socks4://", "socks5://")
        :return:
        """
        payload = {
            "cmd": "sessions.create",
        }
        if session_id:
            payload["session"] = session_id
        if proxy_url:
            if not proxy_url.startswith("http://") and not proxy_url.startswith("https://") and not proxy_url.startswith("socks4://") and not proxy_url.startswith("socks5://"):
                raise UnsupportedProxySchema(f"Supported proxy schemas: ['http(s), socks4, socks5']. Yours: {proxy_url.split('://', 1)[0]}")
            payload["proxy"] = proxy_url
        response = self.req_session.post(self.flare_solverr_url, json=payload)
        response_dict = orjson.loads(response.content)

        if response_dict["status"] != "ok":
            return FlareSolverError.from_dict(response_dict)
        return SesssionCreateResponse.from_dict(response_dict)

    def destroy_session(self, session_id: str) -> Union[FlareSolverOK, FlareSolverError]:
        """
        Destroy an existing FlareSolverr session.
        :param session_id: Required. String.
        :return: Union[FlareSolverOK, FlareSolverError]
        """
        payload = {
            "cmd": "sessions.destroy",
            "session": session_id
        }

        response = self.req_session.post(self.flare_solverr_url, json=payload)
        response_dict = orjson.loads(response.content)

        if response_dict["status"] != "ok":
            return FlareSolverError.from_dict(response_dict)
        return FlareSolverOK.from_dict(response_dict)
