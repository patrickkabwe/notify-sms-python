import json
from dataclasses import dataclass
from typing import Dict, List, TypeVar

T = TypeVar("T")


class APIResponse[T](Dict):
    """APIResponse is the response from the Notify SMS API."""

    success: str
    message: str
    payload: T
    error: dict

    def __str__(self):
        return json.dumps(self.__dict__)


class AuthResponse(Dict):
    """AuthResponse is the response from the Notify SMS API."""

    token: str

    def __str__(self):
        return json.dumps(self.__dict__)


@dataclass
class Tracker:
    """Tracker is the response from the Notify SMS API."""

    _id: str
    title: str
    autoApprove: bool
    status: str
    active: bool
    createdOn: str
    lastModifiedOn: str

    def __str__(self):
        return json.dumps(self.__dict__)


@dataclass
class Sender:
    """Sender is the response from the Notify SMS API."""

    _id: str
    title: str
    description: str
    tracker: Tracker
    status: str
    active: bool
    user: str
    createdOn: str
    lastModifiedOn: str

    def __str__(self):
        return json.dumps(self.__dict__)


class SendersAPIResponse(Dict):
    """SenderAPIResponse is the response from the Notify SMS API."""

    data: List[Sender]

    def __str__(self):
        return json.dumps(self.__dict__)
