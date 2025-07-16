import aiosqlite

DB_PATH = "database/database.db"

# 🔹 1. Foydalanuvchini bazaga qo‘shish (faqat yangi bo‘lsa)
async def add_user(user_id: int, full_name: str, referal_id: int = None):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,)) as cursor:
            exists = await cursor.fetchone()
        if not exists:
            await db.execute("""
                INSERT INTO users (user_id, full_name, referal_id, stars)
                VALUES (?, ?, ?, 0)
            """, (user_id, full_name, referal_id))
            await db.commit()

# 🔹 2. Referalga 1 yulduz qo‘shish
async def add_referral_star(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE users SET stars = stars + 1 WHERE user_id = ?
        """, (user_id,))
        await db.commit()

# 🔹 3. Foydalanuvchining yulduzlari
async def get_user_stars(user_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT stars FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

# 🔹 4. Foydalanuvchilar ro‘yxati
async def get_all_users() -> list[int]:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT user_id FROM users") as cursor:
            return [row[0] async for row in cursor]

# 🔹 5. Statistika: umumiy va o‘rtacha yulduzlar
async def get_star_stats():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT stars FROM users") as cursor:
            rows = await cursor.fetchall()
            total = sum(row[0] for row in rows)
            average = total / len(rows) if rows else 0
            return total, round(average, 2)

# 🔹 6. Umumiy foydalanuvchilar soni
async def get_total_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0

# 🔹 7. Foydalanuvchi bazada borligini tekshirish
async def is_user_exists(user_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,)) as cursor:
            return await cursor.fetchone() is not None
