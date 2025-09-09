from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.utils.markdown import hbold
import asyncio
import os

TOKEN = os.getenv("TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
UPLOAD_SECRET = os.getenv("UPLOAD_SECRET")
TIMEZONE = os.getenv("TIMEZONE")

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
router = Router()
dp.include_router(router)

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Бот запущен и работает!")

@router.message(Command("ping"))
async def cmd_ping(message: Message):
    await message.answer("pong")

@router.message(Command("sendzip"))
async def cmd_sendzip(message: Message):
    if message.from_user.id != OWNER_ID:
        await message.answer("⛔ Нет доступа")
        return
    file = FSInputFile(path="alex_notify_bot_v28.zip", filename="alex_notify_bot_v28.zip")
    await bot.send_document(chat_id=message.chat.id, document=file, caption="Готовый ZIP архив")

@router.message(Command("reportpdf"))
async def cmd_reportpdf(message: Message):
    if message.from_user.id != OWNER_ID:
        await message.answer("⛔ Нет доступа")
        return
    await message.answer("PDF отчёты временно отключены. Используй ZIP.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())