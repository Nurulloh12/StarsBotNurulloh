# handlers/admin/admin_delete.py

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from config import settings
from keyboards.admin import admin_main_menu

router = Router()

# 👤 Admin qo‘shish / o‘chirish FSM holatlari
class AdminState(StatesGroup):
    waiting_for_add_id = State()
    waiting_for_remove_id = State()

# ➕ Admin qo‘shish
@router.message(F.text == "👤 Admin qo‘shish")
async def ask_admin_id(message: types.Message, state: FSMContext):
    await message.answer("👤 Admin qilmoqchi bo‘lgan foydalanuvchi ID’sini yuboring:")
    await state.set_state(AdminState.waiting_for_add_id)

@router.message(AdminState.waiting_for_add_id)
async def add_admin(message: types.Message, state: FSMContext):
    try:
        admin_id = int(message.text)
        if admin_id not in settings.admin_ids:
            settings.admin_ids.append(admin_id)
            await message.answer(f"✅ {admin_id} ID adminlar ro‘yxatiga qo‘shildi.", reply_markup=admin_main_menu())
        else:
            await message.answer("⚠️ Bu foydalanuvchi allaqachon admin.")
    except ValueError:
        await message.answer("❌ Noto‘g‘ri ID. Raqam yuboring.")
    await state.clear()

# ❌ Admin o‘chirish
@router.message(F.text == "👤 Admin o‘chirish")
async def ask_remove_admin_id(message: types.Message, state: FSMContext):
    if not settings.admin_ids:
        await message.answer("📭 Hozircha adminlar yo‘q.")
        return

    admins = "\n".join(str(i) for i in settings.admin_ids)
    await message.answer(f"🗑 O‘chirmoqchi bo‘lgan admin ID’sini yuboring:\n\n{admins}")
    await state.set_state(AdminState.waiting_for_remove_id)

@router.message(AdminState.waiting_for_remove_id)
async def remove_admin(message: types.Message, state: FSMContext):
    try:
        admin_id = int(message.text)
        if admin_id in settings.admin_ids:
            settings.admin_ids.remove(admin_id)
            await message.answer(f"🗑 {admin_id} ID adminlikdan olib tashlandi.", reply_markup=admin_main_menu())
        else:
            await message.answer("❌ Bunday admin topilmadi.")
    except ValueError:
        await message.answer("❌ Noto‘g‘ri ID. Raqam yuboring.")
    await state.clear()
