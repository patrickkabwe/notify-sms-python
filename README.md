## Notify Bulk SMS Library Documentation

## Introduction

https://www.olympusmedia.co.zm

Notify is a bulk SMS Module for sending SMS's accross local zambian phone numbers. It is embedded in [GameBox - Download the app here.](https://play.google.com/store/apps/details?id=com.microtech.gamebox)

## Instructions

Download GameBox and Sign Up. [GameBox - Download the app here.](https://play.google.com/store/apps/details?id=com.microtech.gamebox)
Place your username and password in .env file as

```python
NOTIFY_SMS_USERNAME="2609xxxxxxx"
NOTIFY_SMS_PASSWORD="***********"
```

## ⚙️ Installation

Before you begin, ensure you have Go installed on your system. This module requires Go version 1.21 or **higher** to run.

```go
pip install notify_sms_py
```

## ⚡️ Quickstart

### Get Sender

Returns all the senders(business name) you created on your profile

```python
from notify_sms_py import notify_sms

client = notify_sms.NewClient(
    username="26097xxxxxx",
    password="*********"
)
res = client.get_senders()

print(res)


```

### Send SMS to Contact(s)

Sends sms to a list of recipients defined as contacts

```python
from notify_sms_py import notify_sms

client = notify_sms.NewClient(
    username="26097xxxxxx",
    password="*********"
)

res = client.send_to_contacts(contacts=["+26097xxxxxx"], message="Hello Patrick from Notify SMS", sender_id="1234888888888888888888")

print(res)

```

## 🎯 Features

- Send SMS to channel
- Send SMS to contact groups
- Send SMS to contacts
- Check SMS balance(WIP) - Coming soon

## 👍 Contribute

If you want to say Thank You and/or support the active development of Notify SMS:

- Add a GitHub Star to the project.
- Tweet about the project on your 𝕏 (Twitter).
- Write a review or tutorial on [Medium](https://www,medium.com), [Dev.to](https://www.dev.to) or personal blog.
