# handlers/admin/statistics.py

from aiogram import Router, F
from aiogram.types import Message
from config import settings
from database.user import get_total_users, get_star_stats
from keyboards.admin import admin_panel  # admin tugmalarini import qilamiz

router = Router()

# 🔸 Tugma bosilganda statistika chiqarish
@router.message(F.text == "📊 Statistika")
async def show_statistics(message: Message):
    if message.from_user.id not in settings.admin_ids:
        return await message.answer("⛔️ Siz admin emassiz.")

    total_users = await get_total_users()
    total_stars, avg_stars = await get_star_stats()

    text = (
        "📊 <b>Bot statistikasi:</b>\n\n"
        f"👥 Umumiy foydalanuvchilar: <b>{total_users}</b>\n"
        f"⭐ Umumiy yulduzlar: <b>{total_stars}</b>\n"
        f"📈 O‘rtacha yulduz (1 foydalanuvchiga): <b>{avg_stars}</b>"
    )

    await message.answer(text, reply_markup=admin_panel)