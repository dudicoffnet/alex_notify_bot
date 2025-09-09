from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram import F
import asyncio
import logging
import os
from handlers.zip_handler import router as zip_router

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
dp.include_router(zip_router)

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("✅ Бот работает. Жду команду /sendzip")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())