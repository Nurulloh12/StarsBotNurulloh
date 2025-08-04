from aiogram import Router, types
from aiogram.filters import Command

from database.user import get_total_users, get_star_stats
from keyboards.admin import admin_main_menu
from config import settings

router = Router()

@router.message(Command("stat"))
async def show_statistics(message: types.Message):
    if message.from_user.id not in settings.admin_ids:
        return await message.answer("⛔️ Siz admin emassiz.")

    total_users = await get_total_users()
    total_stars, avg_stars = await get_star_stats()

    await message.answer(
        f"📊 <b>Statistika:</b>\n\n"
        f"👥 Umumiy foydalanuvchilar: <b>{total_users}</b>\n"
        f"⭐ Umumiy yulduzlar: <b>{total_stars}</b>\n"
        f"📈 O‘rtacha yulduzlar: <b>{avg_stars}</b>",
        reply_markup=admin_main_menu()
    )