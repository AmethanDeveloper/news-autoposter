import random
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

from parser import fetch_news
from generator import generate_post
from publisher import send_post, notify_admin
from config import RSS_FEEDS, SCHEDULE_HOURS

MOSCOW_TZ = pytz.timezone("Europe/Moscow")

def publish_one_post():
    print("\n" + "=" * 40)
    print("Запуск публикации...")

    news_list = fetch_news(RSS_FEEDS)

    if not news_list:
        msg = "Нет новых новостей."
        print(msg)
        notify_admin(msg)
        return

    item = random.choice(news_list[:5])
    print(f"Выбрана новость: {item['title']}")

    post_text = generate_post(item["title"], item["summary"])

    if not post_text:
        notify_admin("Не удалось сгенерировать пост — проверьте LM Studio")
        return

    if item["link"]:
        post_text += f"\n\n{item['link']}"

    success = send_post(post_text)

    if not success:
        notify_admin("Не удалось опубликовать пост")

    time.sleep(2)

if __name__ == "__main__":
    print("Новостной бот запускается...")
    print(f"Расписание (МСК): {SCHEDULE_HOURS}")

    publish_one_post()

    scheduler = BlockingScheduler(timezone=MOSCOW_TZ)

    for hour in SCHEDULE_HOURS:
        scheduler.add_job(
            publish_one_post,
            CronTrigger(hour=hour, minute=0, timezone=MOSCOW_TZ),
        )

    print("Планировщик запущен. Ctrl+C для остановки.")

    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("Бот остановлен.")