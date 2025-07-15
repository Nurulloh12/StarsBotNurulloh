# config.py

from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()  # .env faylni yuklash

@dataclass
class Settings:
    bot_token: str
    admin_ids: list[int]
    channel_usernames: list[str]

# .env'dan o‘qib sozlamalarni yuklaymiz
settings = Settings(
    bot_token=os.getenv("BOT_TOKEN"),
    admin_ids=[int(i) for i in os.getenv("ADMIN_IDS", "").split(",") if i.strip()],
    channel_usernames=[ch.strip() for ch in os.getenv("CHANNELS", "").split(",") if ch.strip()]
)
