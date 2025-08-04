from aiogram import Router, types, F
from aiogram.filters import CommandStart
from database.user import (
    add_user,
    is_user_exists,
    add_referral_star,
    get_user_stars
)
from keyboards.user.main_menu import user_main_menu
from config import settings

router = Router()

# 🚀 Start komandasi
@router.message(CommandStart())
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name

    # 🔹 1. Referal ID ni ajratib olish
    referal_id = None
    if message.text and '=' in message.text:
        try:
            referal_id = int(message.text.split('=')[1])
        except (ValueError, IndexError):
            referal_id = None

    # 🔹 2. Foydalanuvchi bazada yo‘q bo‘lsa – yangi foydalanuvchi
    new_user = not await is_user_exists(user_id)
    await add_user(user_id, full_name, referal_id)

    # 🔹 3. Referalga ball qo‘shish va xabar berish
    if new_user and referal_id and referal_id != user_id:
        await add_referral_star(referal_id)

        # ➕ Referalga 1 ball qo‘shildi – hozirgi yulduzlar
        total_stars = await get_user_stars(referal_id)

        # 💬 Referalga bildirish yuborish
        try:
            await message.bot.send_message(
                referal_id,
                f"🎉 Sizga yangi foydalanuvchi orqali ⭐ 1 yulduz qo‘shildi!\n"
                f"Jami yulduzlaringiz: {total_stars} ta ⭐"
            )
        except:
            pass  # Referal botni bloklagan bo‘lishi mumkin

        # 👑 Adminlarga bildirish – 10 ta chaqiriqdan keyin
        if total_stars >= 10:
            for admin_id in settings.admin_ids:
                try:
                    await message.bot.send_message(
                        admin_id,
                        f"🎉 <a href='tg://user?id={referal_id}'>Foydalanuvchi</a> 10 ta do‘st chaqirdi!",
                        parse_mode="HTML"
                    )
                except:
                    pass

    # 🔹 4. Foydalanuvchiga xush kelibsiz xabari
    await message.answer(
        f"👋 Salom, {full_name}!\n\n"
        "🤖 StarsBot'ga xush kelibsiz!\n"
        "Do‘stlaringizni taklif qilib yulduzlar to‘plang ⭐️",
        reply_markup=user_main_menu()
    )

# ✅ Callback orqali "Tekshirish" bosilganda yana start ishlaydi
@router.callback_query(F.data == "check_sub")
async def recheck_subscription(callback: types.CallbackQuery):
    await start_handler(callback.message)
    await callback.answer("✅ Obuna holati tekshirildi!")
