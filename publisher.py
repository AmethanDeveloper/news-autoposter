import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID, YOUR_ID

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

def send_post(text: str, channel: str = TELEGRAM_CHANNEL_ID) -> bool:
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": channel,
        "text": text,
        "disable_web_page_preview": False,
    }
    try:
        r = requests.post(url, json=payload, timeout=15)
        if r.status_code == 200:
            print(f"Опубликовано в {channel}")
            return True
        else:
            print(f"Ошибка Telegram: {r.text}")
            return False
    except Exception as e:
        print(f"Исключение: {e}")
        return False

def notify_admin(text: str):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": YOUR_ID, "text": f"Бот: {text}"}
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass