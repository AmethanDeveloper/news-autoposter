import feedparser
import hashlib
import json
import os
import re
from datetime import datetime, timedelta

SEEN_FILE = "seen_news.json"

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    return set()

def save_seen(seen: set):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen)[-1000:], f)

def news_id(title: str) -> str:
    return hashlib.md5(title.encode("utf-8")).hexdigest()

def fetch_news(feeds: list, max_age_hours: int = 8) -> list:
    seen = load_seen()
    fresh_news = []
    cutoff = datetime.now() - timedelta(hours=max_age_hours)

    for url in feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:15]:
                nid = news_id(entry.get("title", ""))
                if nid in seen:
                    continue

                published = entry.get("published_parsed")
                if published:
                    pub_dt = datetime(*published[:6])
                    if pub_dt < cutoff:
                        continue

                title = entry.get("title", "").strip()
                summary = re.sub(r"<[^>]+>", "", entry.get("summary", "")).strip()[:600]

                if not title:
                    continue

                fresh_news.append({
                    "id": nid,
                    "title": title,
                    "summary": summary,
                    "link": entry.get("link", ""),
                })
                seen.add(nid)

        except Exception as e:
            print(f"Ошибка парсинга {url}: {e}")

    save_seen(seen)
    print(f"Найдено свежих новостей: {len(fresh_news)}")
    return fresh_news