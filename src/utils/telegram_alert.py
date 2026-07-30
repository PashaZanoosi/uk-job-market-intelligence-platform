import os
import requests

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)

CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID"
)

def send_message(message: str):
    if not BOT_TOKEN or not CHAT_ID:

        print(
            "Telegram credentials not found."
        )

        return False

    url = (
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    )

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:

        response = requests.post(

            url,

            json=payload,

            timeout=30

        )

        response.raise_for_status()

        return True

    except Exception as e:

        print(
            "Telegram Error:",
            e
        )
        return False