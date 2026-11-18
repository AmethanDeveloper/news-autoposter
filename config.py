import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")
YOUR_ID = int(os.getenv("ADMIN_ID", "0"))

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHANNEL_ID:
    raise SystemExit("Заполните TELEGRAM_BOT_TOKEN и TELEGRAM_CHANNEL_ID в файле .env (см. .env.example)")

LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1/chat/completions")
LM_MODEL = os.getenv("LM_MODEL", "qwen2.5-14b-instruct")

SCHEDULE_HOURS = [9, 12, 16, 20]

RSS_FEEDS = [
    "https://feeds.bbcrussian.com/russian/rss.xml",
    "https://rss.dw.com/rdf/rss-ru-all",
    "https://meduza.io/rss/all",
    "https://lenta.ru/rss/news",
    "https://tass.ru/rss/v2.xml",
]

POST_PROMPT = """Ты редактор аналитического Telegram-канала о геополитике и внешней политике.

Напиши пост на основе этой новости. Требования:
- 3-5 предложений, ёмко и по делу
- Добавь краткий аналитический комментарий
- 2-3 тематических эмодзи
- Никаких заголовков, звёздочек, markdown-разметки
- Пиши живым языком

Заголовок: {title}
Содержание: {summary}

Только текст поста, ничего лишнего."""