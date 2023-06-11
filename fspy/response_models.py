from dataclasses import dataclass
from typing import List


@dataclass
class FlareSolverOK:
    startTimestamp: int
    endTimestamp: int
    version: str
    status: str
    message: str

    @classmethod
    def from_dict(cls, dct):
        return cls(
            dct["startTimestamp"],
            dct["endTimestamp"],
            dct["version"],
            dct["status"],
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
        return cls(
            dct["startTimestamp"],
            dct["endTimestamp"],
            dct["version"],
            dct["status"],
            dct["message"],
            dct["sessions"]
        )


@dataclass
class SesssionCreateResponse:
    startTimestamp: int
    endTimestamp: int
    version: str
    status: str
    message: str
    session: str

    @classmethod
    def from_dict(cls, dct):
        return cls(
            dct["startTimestamp"],
            dct["endTimestamp"],
            dct["version"],
            dct["status"],
            dct["message"],
            dct["session"]
        )
