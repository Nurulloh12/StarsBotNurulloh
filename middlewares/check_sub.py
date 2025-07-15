from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.channel import get_channels
from config import settings  # ⚠️ admin_ids ni olish uchun
from aiogram.filters.callback_data import CallbackData

class CheckSubscriptionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: types.Message, data: dict):
        from_user = event.from_user

        # ✅ Admin bo‘lsa, to‘xtatmasdan davom ettiramiz
        if from_user.id in settings.admin_ids:
            return await handler(event, data)

        channels = await get_channels()

        if not channels:
            return await handler(event, data)  # Agar kanal yo‘q bo‘lsa davom etadi

        not_joined = []

        for channel in channels:
            try:
                member = await event.bot.get_chat_member(channel, from_user.id)
                if member.status not in ("member", "creator", "administrator"):
                    not_joined.append(channel)
            except Exception:
                not_joined.append(channel)

        if not not_joined:
            return await handler(event, data)  # Hammasiga obuna bo‘lgan

        # 🔘 Inline tugmalar
        builder = InlineKeyboardBuilder()
        for ch in not_joined:
            builder.button(
                text=f"➕ Obuna bo‘lish ({ch})",
                url=f"https://t.me/{ch.lstrip('@')}"
            )

        builder.button(text="✅ Tekshirish", callback_data="check_sub")
        builder.adjust(1)

        await event.answer(
            "🔒 Davom etish uchun quyidagi kanallarga obuna bo‘ling:",
            reply_markup=builder.as_markup()
        )
        return

