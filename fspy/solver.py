from typing import Union, Literal, Optional, List

import orjson
import requests

from .response_models import SessionsListResponse, SesssionCreateResponse, FlareSolverOK, GetRequestResponse
from .solver_exceptions import UnsupportedProxySchema, FlareSolverError


def _check_proxy_url(proxy_url: str) -> None:
    if not proxy_url.startswith("http://") and not proxy_url.startswith("https://") and not proxy_url.startswith("socks4://") and not proxy_url.startswith("socks5://"):
        raise UnsupportedProxySchema(f"Supported proxy schemas: ['http(s), socks4, socks5']. Yours: {proxy_url.split('://', 1)[0]}")


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
    def sessions(self) -> List[str]:
        """
        Get session ids as a list.
        :rtype: List[str]
        :return: All session ids as a list
        """
        payload = {
            "cmd": "sessions.list"
        }
        response = self.req_session.post(self.flare_solverr_url, json=payload)
        response_dict = orjson.loads(response.content)

        if response_dict["status"] != "ok":
            raise FlareSolverError.from_dict(response_dict)
        return SessionsListResponse.from_dict(response_dict).sessions

    @property
    def _sessions_raw(self) -> SessionsListResponse:
        """
        Get the whole response as SessionsListResponse object.
        :rtype: SessionsListResponse
        :return: A class containing OK messages and sessions as a list.
        """
        payload = {
            "cmd": "sessions.list"
        }
        response = self.req_session.post(self.flare_solverr_url, json=payload)
        response_dict = orjson.loads(response.content)

        if response_dict["status"] != "ok":
            raise FlareSolverError.from_dict(response_dict)
        return SessionsListResponse.from_dict(response_dict)

    def create_session(self, session_id: str = None, proxy_url: str = None) -> SesssionCreateResponse:
        """
        Create a session. This will launch a new browser instance which will retain cookies.
        :param session_id: String. Optional.
        :param proxy_url: String. Optional. Must include proxy schema. ("http://", "socks4://", "socks5://")
        :type session_id: str
        :type proxy_url: str
        :rtype: SesssionCreateResponse
        :return: FlareSolverr sessions.create response as a class.
        """
        payload = {
            "cmd": "sessions.create",
        }
        if session_id:
            payload["session"] = session_id
        if proxy_url:
            _check_proxy_url(proxy_url)
            payload["proxy"] = {"url": proxy_url}
        response = self.req_session.post(self.flare_solverr_url, json=payload)
        response_dict = orjson.loads(response.content)

        if response_dict["status"] != "ok":
            raise FlareSolverError.from_dict(response_dict)
        return SesssionCreateResponse.from_dict(response_dict)

    def destroy_session(self, session_id: str) -> FlareSolverOK:
        """
        Destroy an existing FlareSolverr session.
        :param session_id: Required. String.
        :type session_id: str
        :rtype: FlareSolverOK
        :return: Class containing OK message.
        """
        payload = {
            "cmd": "sessions.destroy",
            "session": session_id
        }

        response = self.req_session.post(self.flare_solverr_url, json=payload)
        response_dict = orjson.loads(response.content)

        if response_dict["status"] != "ok":
            raise FlareSolverError.from_dict(response_dict)
        return FlareSolverOK.from_dict(response_dict)

    def request_get(
            self,
            url: str,
            session: Optional[str] = None,
            session_ttl_minutes: Optional[int] = None,
            max_timeout: int = 60000,
            cookies: Optional[List[dict]] = None,
            return_only_cookies: bool = False,
            proxy_url: Optional[str] = None
    ) -> GetRequestResponse:
        payload = {
            "cmd": "request.get",
            "url": url,
            "maxTimeout": max_timeout,
            "returnOnlyCookies": return_only_cookies
        }
        if session:
            payload["session"] = session
        if session_ttl_minutes:
            payload["session_ttl_minutes"] = session_ttl_minutes
        if cookies:
            payload["cookies"] = cookies
        if proxy_url:
            _check_proxy_url(proxy_url)
            payload["proxy"] = {"url": proxy_url}

        response = self.req_session.post(self.flare_solverr_url, json=payload)
        response_dict = orjson.loads(response.content)

        if response_dict["status"] != "ok":
            raise FlareSolverError.from_dict(response_dict)
        return GetRequestResponse.from_dict(response_dict)
