# main.py

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import settings  # .env dagi sozlamalar

# 🔌 Routerlar
from handlers.user import start, account
from handlers.admin import panel, broadcast, channel, statistics, admin_delete

# 🔐 Middleware (majburiy obuna)
from middlewares.check_sub import CheckSubscriptionMiddleware

# 🗄️ Bazani yaratish
from database.init_db import create_db

async def main():
    # 📦 Bazani yaratamiz
    await create_db()

    # 🤖 Botni sozlash (parse_mode endi default= bilan uzatiladi)
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # 📲 Dispatcher (router va middlewarelarni birlashtiruvchi tizim)
    dp = Dispatcher()

    # 🔐 Middleware ulaymiz (majburiy obuna)
    dp.message.middleware(CheckSubscriptionMiddleware())

    # 🔁 Routerlarni ulamiz
    dp.include_routers(
        start.router,
        account.router,
        panel.router,
        broadcast.router,
        channel.router,
        statistics.router,
        admin_delete.router,
    )

    print("✅ Bot ishga tushdi")
    await dp.start_polling(bot)

# 🚀 Ishga tushirish
if __name__ == "__main__":
    asyncio.run(main())

