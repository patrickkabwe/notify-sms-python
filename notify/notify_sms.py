import re
from dataclasses import dataclass
from typing import Any, Dict, List

import requests

from notify.notify_types import APIResponse, AuthResponse, SendersAPIResponse


@dataclass
class Config:
    """Config is the configuration for the Notify SMS API."""

    user_name: str
    password: str

    def __post_init__(self):

        if not self.user_name:
            raise ValueError("Username is required")
        match = re.search(r"^(\+)?(\d{12})$", self.user_name)
        if not match:
            raise ValueError("Invalid username")
        if not self.password:
            raise ValueError("Password is required")


class NewClient:
    """
    NewClient is a client for the Notify SMS API.
    """

    base_url = "https://production.olympusmedia.co.zm/api/v1"
    token = None

    def __init__(self, config: Config):
        self.config = config
        self.__auth()

    def __auth(self):
        try:
            endpoint = f"{self.base_url}/authentication/web/login?error_context=CONTEXT_API_ERROR_JSON"

            payload = {
                "username": self.config.user_name,
                "password": self.config.password,
            }
            response = requests.post(endpoint, json=payload, timeout=5)
            response.raise_for_status()
            dict_response: APIResponse[AuthResponse] = response.json()
            self.token = dict_response["payload"]["token"]
            return self.token
        except requests.exceptions.RequestException as e:
            raise e

    def get_senders(self):
        """GetSenders returns a list of senders."""
        endpoint = f"{self.base_url}/notify/sender-ids/fetch?error_context=CONTEXT_API_ERROR_JSON"
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}",
            }
            response = requests.get(endpoint, timeout=5, headers=headers)
            response.raise_for_status()
            res: APIResponse[SendersAPIResponse] = response.json()
            return res
        except requests.exceptions.RequestException as e:
            raise e

    def send_to_contacts(self, sender_id: str, message: str, contacts: List[str]):
        """SendToContacts sends a sms message to a list of contacts."""
        try:
            payload = {
                "reciepientType": "NOTIFY_RECIEPIENT_TYPE_CUSTOM",
                "senderId": sender_id,
                "message": message,
                "reciepients": contacts,
            }
            return self.send_sms(payload)
        except requests.exceptions.RequestException as e:
            raise e

    def send_to_channel(self, sender_id: str, message: str, channel: str):
        """SendToChannel sends a sms message to a channel."""
        try:
            payload = {
                "reciepientType": "NOTIFY_RECIEPIENT_TYPE_CHANNEL",
                "senderId": sender_id,
                "message": message,
                "channel": channel,
            }
            return self.send_sms(payload)
        except requests.exceptions.RequestException as e:
            raise e

    def send_to_contact_group(self, sender_id: str, message: str, contact_group: str):
        """SendToContactGroup sends a sms message to a contact group."""
        try:
            payload = {
                "reciepientType": "NOTIFY_RECIEPIENT_TYPE_CHANNEL",
                "senderId": sender_id,
                "message": message,
                "contactGroup": contact_group,
            }
            return self.send_sms(payload)
        except requests.exceptions.RequestException as e:
            raise e

    def send_sms(self, json_payload: Any):
        """SendSms sends a message to a list of contacts."""
        try:
            endpoint = f"{self.base_url}/notify/channels/messages/compose?error_context=CONTEXT_API_ERROR_JSON"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}",
            }
            response = self.make_request("POST", endpoint, json_payload, headers)
            return response
        except requests.exceptions.RequestException as e:
            raise e

    def make_request(
        self, method: str, endpoint: str, payload: Any, headers: Dict[str, str]
    ):
        """MakeRequest sends a message to a list of contacts."""
        try:
            response = requests.request(
                method, endpoint, json=payload, timeout=5, headers=headers
            )
            response.raise_for_status()
            res: APIResponse[Any] = response.json()
            if res["success"] is False:
                if res["error"]:
                    raise requests.exceptions.RequestException(
                        res["error"]["message"], response=response
                    )
                raise requests.exceptions.RequestException(
                    res["message"], response=response
                )
            return res
        except requests.exceptions.RequestException as e:
            raise e
