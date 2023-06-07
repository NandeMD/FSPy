from dataclasses import dataclass
from typing import List


@dataclass
class FlareSolverNotOK:
    status: str
    version: str
    message: str

    @classmethod
    def from_dict(cls, dct):
        return FlareSolverNotOK(
            dct["status"],
            dct["version"],
            dct["message"]
        )


@dataclass
class SessionsListResponse:
    startTimestamp: int
    endTimestamp: int
    version: str
    status: str
    message: str
    sessions: List[str]

    @classmethod
    def from_dict(cls, dct):
        return SessionsListResponse(
            dct["startTimestamp"],
            dct["endTimestamp"],
            dct["version"],
            dct["status"],
            dct["message"],
            dct["sessions"]
        )
