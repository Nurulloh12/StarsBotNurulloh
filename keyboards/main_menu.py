# keyboards/user/main_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def user_main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="👤 Hisobim"),
                KeyboardButton(text="⭐️ Ballarim"),
            ],
            [
                KeyboardButton(text="🔗 Referal havola"),
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Kerakli bo‘limni tanlang"
    )
