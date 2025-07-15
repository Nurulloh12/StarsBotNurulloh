# init_db.py

import asyncio
import aiosqlite

async def init_db():
    async with aiosqlite.connect("database/database.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                full_name TEXT,
                referal_id INTEGER,
                stars INTEGER DEFAULT 0
            )
        """)
        await db.commit()
    print("✅ Baza yaratildi!")

if __name__ == "__main__":
    asyncio.run(init_db())
