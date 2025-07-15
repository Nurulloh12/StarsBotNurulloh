# handlers/admin/panel.py

from aiogram import Router, types, F
from config import settings
from keyboards.admin import admin_main_menu

router = Router()

# 🔒 Faqat adminlar uchun panel
@router.message(F.text == "/admin")
async def admin_panel(message: types.Message):
    user_id = message.from_user.id

    # ✅ Faqat adminlar kirishi mumkin
    if user_id in settings.admin_ids:
        await message.answer(
            text="🔐 Admin panelga xush kelibsiz!",
            reply_markup=admin_main_menu()
        )
    else:
        await message.answer("⛔️ Siz admin emassiz!")
