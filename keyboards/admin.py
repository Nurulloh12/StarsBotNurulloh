from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def admin_main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Statistika"), KeyboardButton(text="📤 Xabar yuborish")],
            [KeyboardButton(text="📡 Kanal ulash"), KeyboardButton(text="❌ Kanal uzish")],
            [KeyboardButton(text="👤 Admin qo‘shish"), KeyboardButton(text="👤 Admin o‘chirish")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Admin panel"
    )
# ✅ Tasdiqlash / ❌ Bekor qilish tugmalari
def confirm_cancel_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Tasdiqlayman")],
            [KeyboardButton(text="❌ Bekor qilish")]
        ],
        resize_keyboard=True
    )