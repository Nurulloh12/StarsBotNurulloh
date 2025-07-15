# handlers/admin/statistics.py

from aiogram import Router, types
from aiogram.filters import Command
from database.user import get_total_users
from config import settings

router = Router()

@router.message(Command("stat"))
async def show_statistics(message: types.Message):
    if message.from_user.id not in settings.admin_ids:
        return await message.answer("⛔ Siz admin emassiz.")
    
    total_users = await get_total_users()
    
    await message.answer(
        f"📊 <b>Statistika:</b>\n\n"
        f"👥 Umumiy foydalanuvchilar: <b>{total_users}</b>"
    )
