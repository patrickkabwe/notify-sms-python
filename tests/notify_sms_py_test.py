import os

import pytest
import requests
from dotenv import load_dotenv
from unittest import mock
from notify_sms_py import notify_sms

load_dotenv()

INVALID_PHONE_NUMBER = "+2609786134"
VALID_PHONE_NUMBER = os.environ.get("NOTIFY_SMS_USERNAME", "260978613411")
VALID_TEST_CONTACT = os.environ.get("NOTIFY_SMS_TEST_CONTACT", "+260978619511")
VALID_PASSWORD = os.environ.get("NOTIFY_SMS_PASSWORD", "password")
VALID_SENDER_ID = os.environ.get("NOTIFY_SMS_SENDER_ID", "5e7d5e5b4e1f5f0011e4e3c6")


@pytest.fixture
def auth_client():
    mock_post_request = mock.Mock()
    mock_post_request.return_value = mock.Mock(
        status_code=200,
        json=mock.Mock(
            return_value={
                "success": True,
                "payload": {
                    "token": "eyJ0eXAiOiJKV"
                }
            }
        )
    )

    with mock.patch("requests.post", mock_post_request):
        auth_client = notify_sms.NewClient(username=VALID_PHONE_NUMBER, password=VALID_PASSWORD)

    return auth_client


def test_invalid_notify_sms_client():
    """Test invalid notify_sms client."""
    mock_request_exception = requests.exceptions.RequestException

    with mock.patch("requests.post") as mock_post:
        mock_post.side_effect = mock_request_exception
        pytest.raises(
            mock_request_exception,
            notify_sms.NewClient,
            username="260923421211",
            password="password",
        )
        pytest.raises(ValueError, notify_sms.NewClient, username="", password="")
        pytest.raises(
            ValueError,
            notify_sms.NewClient,
            username=VALID_PHONE_NUMBER,
            password="",
        )
        pytest.raises(
            ValueError, notify_sms.NewClient, username=INVALID_PHONE_NUMBER, password=""
        )
        pytest.raises(ValueError, notify_sms.NewClient, username="", password="password")


def test_valid_notify_sms_client(auth_client):
    """Test valid notify_sms client."""
    assert auth_client.base_url == "https://production.olympusmedia.co.zm/api/v1"
    assert auth_client.username == VALID_PHONE_NUMBER
    assert auth_client.password == VALID_PASSWORD
    assert auth_client.token is not None


def test_get_senders(auth_client):
    """Test get senders."""

    mock_get_request = mock.Mock()
    mock_get_request.return_value = mock.Mock(
        status_code=200,
        json=mock.Mock(
            return_value={
                "success": True,
                "payload": {
                    "data": [
                        {
                            "_id": "5e7d5e5b4e1f5f0011e4e3c6",
                            "title": "Olympus Media",
                            "description": "Olympus Media",
                            "tracker": {
                                "_id": "5e7d5e5b4e1f5f0011e4e3c5",
                                "title": "Olympus Media",
                                "autoApprove": False,
                                "status": "STATUS_ACCEPTED",
                                "active": True,
                                "createdOn": "2024-03-26T14:17:55.000Z",
                                "lastModifiedOn": "2024-03-26T14:17:55.000Z",
                            },
                            "status": "STATUS_ACCEPTED",
                            "active": True,
                            "user": "5e7d5e5b4e1f5f0011e4e3c4",
                            "createdOn": "2024-03-26T14:17:55.000Z",
                            "lastModifiedOn": "2024-03-26T14:17:55.000Z",
                        }
                    ]
                }
            }
        )
    )

    with mock.patch("requests.get", mock_get_request):
        senders = auth_client.get_senders()
        assert senders["payload"]["data"] is not None
        assert senders["success"] is True


def test_send_to_contacts(auth_client):
    """Test send to contacts."""
    auth_client.send_to_contacts = mock.Mock(
        return_value={
            "success": True,
            "message": "message has been queued successfully",
            "payload": {}
        }
    )

    response = auth_client.send_to_contacts(
        sender_id=VALID_SENDER_ID,
        message="Hello, Patrick from Python SDK",
        contacts=[VALID_TEST_CONTACT],
    )

    auth_client.send_to_contacts.assert_called_with(
        sender_id=VALID_SENDER_ID,
        message="Hello, Patrick from Python SDK",
        contacts=[VALID_TEST_CONTACT],
    )
    assert response["success"] is True
    assert response['message'] == "message has been queued successfully"


def test_invalid_send_to_contacts(auth_client):
    """Test invalid send to contacts."""
    auth_client._NewClient__send_sms = mock.Mock(side_effect=requests.exceptions.RequestException)
    request_exception = requests.exceptions.RequestException
    pytest.raises(
        request_exception,
        auth_client.send_to_contacts,
        sender_id="",
        message="Hello, Patrick from Python SDK",
        contacts=[VALID_TEST_CONTACT],
    )
    pytest.raises(
        request_exception,
        auth_client.send_to_contacts,
        sender_id=VALID_SENDER_ID,
        message="",
        contacts=[VALID_TEST_CONTACT],
    )
    pytest.raises(
        request_exception,
        auth_client.send_to_contacts,
        sender_id=VALID_SENDER_ID,
        message="Hello, Patrick from Python SDK",
        contacts=[],
    )
    pytest.raises(
        request_exception,
        auth_client.send_to_contacts,
        sender_id=VALID_SENDER_ID,
        message="Hello, Patrick from Python SDK",
        contacts=[""],
    )


def test_send_to_channel(auth_client):
    """Test send to channel."""
    auth_client.send_to_channel = mock.Mock(
        return_value={
            "success": True,
            "message": "message has been queued successfully",
            "payload": {}
        }
    )

    response = auth_client.send_to_channel(
        sender_id=VALID_SENDER_ID,
        message="Hello, Patrick from Python SDK",
        channel="test_channel",
    )

    auth_client.send_to_channel.assert_called_with(
        sender_id=VALID_SENDER_ID,
        message="Hello, Patrick from Python SDK",
        channel="test_channel",
    )
    assert response["success"] is True
    assert response['message'] == "message has been queued successfully"


def test_invalid_send_to_channel(auth_client):
    #  We could not process your request at this moment, if error persists, Please contact us at support@microtech.co.zm
    request_exception = requests.exceptions.RequestException
    auth_client._NewClient__send_sms = mock.Mock(side_effect=requests.exceptions.RequestException)
    pytest.raises(
        request_exception,
        auth_client.send_to_channel,
        sender_id=VALID_SENDER_ID,
        message="",
        channel="test_channel"
    )

    pytest.raises(
        request_exception,
        auth_client.send_to_channel,
        sender_id=VALID_SENDER_ID,
        message="test message",
        channel=""
    )
