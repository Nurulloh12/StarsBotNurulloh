# fake_test.py
import asyncio
from database.user import add_user, add_referral_star, get_user_stars

# 👤 Yangi foydalanuvchi
new_user_id = 999123  # Har safar yangicha qilib o‘zgartiring
full_name = "Test Foydalanuvchi"

# 👥 Kimning referali edi?
referal_id = 7293959501  # Sizning (adminning) ID

async def main():
    await add_user(new_user_id, full_name, referal_id)
    await add_referral_star(referal_id)

    stars = await get_user_stars(referal_id)
    print(f"✅ Referalga berilgan yulduzlar soni: {stars}")

asyncio.run(main())
