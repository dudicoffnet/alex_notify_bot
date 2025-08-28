
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile

import os

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

async def send_report():
    while True:
        now = datetime.now().strftime("%H:%M")
        if now == "10:00":
            if os.path.exists("report.pdf"):
                await bot.send_document(CHAT_ID, document=FSInputFile("report.pdf"), caption="📄 Утренний отчёт")
        if now == "23:00":
            if os.path.exists("backup.zip"):
                await bot.send_document(CHAT_ID, document=FSInputFile("backup.zip"), caption="📦 Вечерний ZIP")
        await asyncio.sleep(60)

async def main():
    asyncio.create_task(send_report())
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
