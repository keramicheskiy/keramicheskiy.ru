import os

import requests


def send_message(number: str, message: str) -> int:
    url = os.environ.get("WHATSAPP_API_URL")

    payload = {
        "chatId": f"{number}@c.us",
        "message": f"{message}"
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.status_code
