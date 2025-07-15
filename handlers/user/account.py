# handlers/user/account.py

from aiogram import Router, types, F
from database.user import get_user_stars
from keyboards.user.main_menu import user_main_menu

router = Router()

# 🔹 1. 👤 Hisobim tugmasi logikasi
@router.message(F.text == "👤 Hisobim")
async def show_account(message: types.Message):
    user = message.from_user

    await message.answer(
        text=(
            f"🙋‍♂️ Ismingiz: <b>{user.full_name}</b>\n"
            f"🆔 Telegram ID: <code>{user.id}</code>"
        ),
        reply_markup=user_main_menu()
    )

# 🔹 2. ⭐️ Ballarim tugmasi logikasi
@router.message(F.text == "⭐️ Ballarim")
async def show_stars(message: types.Message):
    user_id = message.from_user.id
    stars = await get_user_stars(user_id)

    await message.answer(
        text=f"⭐️ Sizda {stars} ta yulduzcha mavjud!",
        reply_markup=user_main_menu()
    )

# 🔹 3. 🔗 Referal havola tugmasi logikasi
@router.message(F.text == "🔗 Referal havola")
async def show_ref_link(message: types.Message):
    user_id = message.from_user.id
    bot_username = (await message.bot.me()).username
    ref_link = f"https://t.me/{bot_username}?start={user_id}"

    await message.answer(
        text=(
            f"📢 Do‘stlaringizni taklif qilish uchun ushbu havolani ulashing:\n\n"
            f"<code>{ref_link}</code>\n\n"
            f"💡 Har bir do‘st uchun sizga 1 ⭐️ beriladi!"
        ),
        reply_markup=user_main_menu()
    )
