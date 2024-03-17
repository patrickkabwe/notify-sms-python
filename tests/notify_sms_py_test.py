import os

import pytest
import requests
from dotenv import load_dotenv

from notify_sms_py import notify_sms

load_dotenv()

INVALID_PHONE_NUMBER = "+26090020005"
VALID_PHONE_NUMBER = os.environ.get("NOTIFY_SMS_USERNAME", "")
VALID_TEST_CONTACT = os.environ.get("NOTIFY_SMS_TEST_CONTACT", "")
VALID_PASSWORD = os.environ.get("NOTIFY_SMS_PASSWORD", "")
VALID_SENDER_ID = os.environ.get("NOTIFY_SMS_SENDER_ID", "")


def test_invalid_notify_sms_client():
    """Test invalid notify_sms client."""
    pytest.raises(ValueError, notify_sms.NewClient, username="", password="")
    pytest.raises(
        ValueError, notify_sms.NewClient, username=INVALID_PHONE_NUMBER, password=""
    )
    pytest.raises(ValueError, notify_sms.NewClient, username="", password="password")


def test_valid_notify_sms_client():
    """Test valid notify_sms client."""
    client = notify_sms.NewClient(username=VALID_PHONE_NUMBER, password=VALID_PASSWORD)

    assert client.base_url == "https://production.olympusmedia.co.zm/api/v1"
    assert client.username == VALID_PHONE_NUMBER
    assert client.password == VALID_PASSWORD
    assert client.token is not None


def test_get_senders():
    """Test get senders."""
    client = notify_sms.NewClient(username=VALID_PHONE_NUMBER, password=VALID_PASSWORD)
    senders = client.get_senders()
    assert senders["payload"]["data"] is not None
    assert senders["success"] is True


def test_send_to_contacts():
    """Test send to contacts."""
    client = notify_sms.NewClient(username=VALID_PHONE_NUMBER, password=VALID_PASSWORD)
    response = client.send_to_contacts(
        sender_id=VALID_SENDER_ID,
        message="Hello, Patrick from Python SDK",
        contacts=[VALID_TEST_CONTACT],
    )
    assert response["success"] is True


def test_invalid_send_to_contacts():
    """Test invalid send to contacts."""
    client = notify_sms.NewClient(username=VALID_PHONE_NUMBER, password=VALID_PASSWORD)
    request_exception = requests.exceptions.RequestException
    pytest.raises(
        request_exception,
        client.send_to_contacts,
        sender_id="",
        message="Hello, Patrick from Python SDK",
        contacts=[VALID_TEST_CONTACT],
    )
    pytest.raises(
        request_exception,
        client.send_to_contacts,
        sender_id=VALID_SENDER_ID,
        message="",
        contacts=[VALID_TEST_CONTACT],
    )
    pytest.raises(
        request_exception,
        client.send_to_contacts,
        sender_id=VALID_SENDER_ID,
        message="Hello, Patrick from Python SDK",
        contacts=[],
    )
    pytest.raises(
        request_exception,
        client.send_to_contacts,
        sender_id=VALID_SENDER_ID,
        message="Hello, Patrick from Python SDK",
        contacts=[""],
    )


def test_send_to_channel():
    pass


def test_invalid_send_to_channel():
    pass
