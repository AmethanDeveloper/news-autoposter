import requests
from config import LM_STUDIO_URL, LM_MODEL, POST_PROMPT

def generate_post(title: str, summary: str):
    prompt = POST_PROMPT.format(title=title, summary=summary)

    payload = {
        "model": LM_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Ты опытный редактор новостного Telegram-канала."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.75,
        "max_tokens": 450,
        "stream": False,
    }

    try:
        response = requests.post(LM_STUDIO_URL, json=payload, timeout=120)
        response.raise_for_status()
        text = response.json()["choices"][0]["message"]["content"].strip()
        print(f"Сгенерировано {len(text)} символов")
        return text
    except requests.exceptions.ConnectionError:
        print("LM Studio не запущен!")
        return None
    except Exception as e:
        print(f"Ошибка генерации: {e}")
        return None