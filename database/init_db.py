# database/init_db.py

import aiosqlite

# 📌 Bazani yaratish funksiyasi
async def create_db():
    async with aiosqlite.connect("starsbot.db") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT,
            referal_id INTEGER,
            stars INTEGER DEFAULT 0
        )
        """)
        await db.commit()


