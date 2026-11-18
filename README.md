# News Autoposter — автопостинг новостей в Telegram с локальной LLM

Бот собирает свежие новости из RSS-лент, пишет по выбранной новости короткий аналитический пост с помощью локальной языковой модели и публикует его в Telegram-канал по расписанию.

## Как работает

```
RSS-ленты ──► parser.py ──► generator.py ──► publisher.py ──► Telegram-канал
             (свежие,        (пост через       (Bot API;
              без повторов)   LM Studio)        ошибки — админу)
                     ▲
              main.py: APScheduler, публикация в 9:00, 12:00, 16:00, 20:00 МСК
```

- **parser.py** — читает ленты через `feedparser`, отбрасывает новости старше 8 часов и уже опубликованные (хеши заголовков в `seen_news.json`).
- **generator.py** — отправляет заголовок и анонс в LM Studio (OpenAI-совместимый API, по умолчанию `qwen2.5-14b-instruct`) и получает готовый пост.
- **publisher.py** — публикует пост через Telegram Bot API и сообщает администратору об ошибках.
- **main.py** — публикует первый пост сразу при запуске, дальше работает по расписанию.

## Запуск

1. Установите [LM Studio](https://lmstudio.ai/), загрузите модель и включите локальный сервер (порт 1234).
2. Создайте бота у @BotFather и добавьте его администратором в канал.
3. Настройте окружение:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # впишите токен, канал и свой Telegram ID
python main.py
```

Источники, расписание и текст промпта меняются в `config.py`.

## Стек

Python · feedparser · requests · APScheduler · LM Studio (Qwen 2.5) · Telegram Bot API
