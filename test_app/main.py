from notify_sms_py import notify_sms


def main():
    client = notify_sms.NewClient(
        password="password",
        username="username"
    )