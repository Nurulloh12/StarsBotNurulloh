from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from keyboards.admin import admin_main_menu, confirm_cancel_kb
from database.channel import add_channel, get_channels, remove_channel
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router = Router()

# 📥 Kanal ulash uchun holatlar
class ChannelState(StatesGroup):
    waiting_for_username = State()
    waiting_for_confirmation = State()
    remove_selection = State()  # ❌ Kanal uzish uchun state

# 📡 "Kanal ulash" tugmasi bosilganda
@router.message(F.text == "📡 Kanal ulash")
async def start_channel_linking(message: types.Message, state: FSMContext):
    await message.answer("🔗 Kanal usernameni yuboring (masalan: @starsbot)", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(ChannelState.waiting_for_username)

# 🔠 Kanal username qabul qilish
@router.message(StateFilter(ChannelState.waiting_for_username))
async def receive_channel_username(message: types.Message, state: FSMContext):
    channel_username = message.text.strip()

    if not channel_username.startswith("@") or " " in channel_username:
        return await message.answer("❌ Noto‘g‘ri format. Masalan: @starsbot")

    await state.update_data(channel_username=channel_username)
    await state.set_state(ChannelState.waiting_for_confirmation)

    await message.answer(
        f"🔄 Ushbu kanalni ulaysizmi: {channel_username}?",
        reply_markup=confirm_cancel_kb()
    )

# ✅ Tasdiqlash / ❌ Bekor qilish
@router.message(StateFilter(ChannelState.waiting_for_confirmation))
async def confirm_channel_link(message: types.Message, state: FSMContext):
    data = await state.get_data()
    username = data.get("channel_username")

    if message.text == "✅ Tasdiqlayman":
        await add_channel(username)
        await message.answer("✅ Kanal muvaffaqiyatli ulandi!", reply_markup=admin_main_menu())
    else:
        await message.answer("❌ Bekor qilindi.", reply_markup=admin_main_menu())

    await state.clear()

# ❌ "Kanal uzish" tugmasi bosilganda
@router.message(F.text == "❌ Kanal uzish")
async def start_channel_unlink(message: types.Message, state: FSMContext):
    channels = await get_channels()

    if not channels:
        return await message.answer("ℹ️ Ulab qo‘yilgan hech qanday kanal yo‘q.", reply_markup=admin_main_menu())

    builder = ReplyKeyboardBuilder()
    for channel in channels:
        builder.button(text=channel)
    builder.button(text="⬅️ Orqaga")
    builder.adjust(1)

    await message.answer("❌ Qaysi kanalni uzmoqchisiz?", reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(ChannelState.remove_selection)

# ✂️ Kanal tanlab o‘chirish
@router.message(StateFilter(ChannelState.remove_selection))
async def confirm_remove_channel(message: types.Message, state: FSMContext):
    text = message.text.strip()

    if text == "⬅️ Orqaga":
        await message.answer("🔙 Bosh menuga qaytdingiz.", reply_markup=admin_main_menu())
        return await state.clear()

    success = await remove_channel(text)
    if success:
        await message.answer(f"✅ {text} kanali o‘chirildi.", reply_markup=admin_main_menu())
    else:
        await message.answer(f"❌ {text} kanal topilmadi yoki o‘chirilmadi.", reply_markup=admin_main_menu())

    await state.clear()
