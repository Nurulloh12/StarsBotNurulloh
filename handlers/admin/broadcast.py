# handlers/admin/broadcast.py

from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database.user import get_all_users
from keyboards.admin import confirm_cancel_kb, admin_main_menu

router = Router()

# 📤 Xabar yuborish FSM holati
class BroadcastState(StatesGroup):
    waiting_for_text = State()
    confirm_send = State()

# 🧾 Admin xabar yuborishni boshlaydi
@router.message(F.text == "📤 Xabar yuborish")
async def ask_broadcast_text(message: types.Message, state: FSMContext):
    await message.answer("📝 Reklama matnini yuboring:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(BroadcastState.waiting_for_text)

# ✉️ Reklama matni qabul qilinadi
@router.message(BroadcastState.waiting_for_text)
async def confirm_broadcast_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)

    await message.answer(
        f"Quyidagi xabar yuborilsinmi?\n\n{message.text}",
        reply_markup=confirm_cancel_kb()
    )
    await state.set_state(BroadcastState.confirm_send)

# ✅ TASDIQLAYMAN bosilganda
@router.message(BroadcastState.confirm_send, F.text == "✅ Tasdiqlayman")
async def send_broadcast(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")
    users = await get_all_users()

    sent = 0
    for user_id in users:
        try:
            await message.bot.send_message(chat_id=user_id, text=text)
            sent += 1
        except Exception:
             pass
    await message.answer(
        f"✅ Xabar {sent} ta foydalanuvchiga yuborildi!",
        reply_markup=admin_main_menu()
    )
    await state.clear()

# ❌ BEKOR QILISH bosilganda
@router.message(BroadcastState.confirm_send, F.text == "❌ Bekor qilish")
async def cancel_broadcast(message: types.Message, state: FSMContext):
    await message.answer("❌ Xabar yuborish bekor qilindi.", reply_markup=admin_main_menu())
    await state.clear()
