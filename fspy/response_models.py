from dataclasses import dataclass
from typing import List

@dataclass
class SessionsListResponse(slots=True):
    startTimestamp: int
    endTimestamp: int
    version: str
    status: str
    message: str
    sessions: List[str]
    
    @classmethod
    def from_dict(cls, dct: dict):
        return SessionsListResponse(**dct)
