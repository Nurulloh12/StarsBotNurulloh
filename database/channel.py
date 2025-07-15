# database/channel.py

import aiosqlite

# 📌 Kanalni qo‘shish
async def add_channel(channel_username: str):
    async with aiosqlite.connect("data.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE
            )
        """)
        await db.execute("INSERT OR IGNORE INTO channels (username) VALUES (?)", (channel_username,))
        await db.commit()


# ❌ Kanalni o‘chirish
async def delete_channel(channel_username: str):
    async with aiosqlite.connect("data.db") as db:
        await db.execute("DELETE FROM channels WHERE username = ?", (channel_username,))
        await db.commit()


# 📥 Barcha kanallarni olish
async def get_channels() -> list[str]:
    async with aiosqlite.connect("data.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE
            )
        """)
        cursor = await db.execute("SELECT username FROM channels")
        rows = await cursor.fetchall()
        return [row[0] for row in rows]


# 🔎 Kanal borligini tekshirish
async def channel_exists(channel_username: str) -> bool:
    async with aiosqlite.connect("data.db") as db:
        cursor = await db.execute("SELECT 1 FROM channels WHERE username = ?", (channel_username,))
        return await cursor.fetchone() is not None

# database/channel.py

async def remove_channel(username: str) -> bool:
    async with aiosqlite.connect("data.db") as db:
        result = await db.execute("DELETE FROM channels WHERE username = ?", (username,))
        await db.commit()
        return result.rowcount > 0
