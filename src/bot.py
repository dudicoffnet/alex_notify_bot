# Логика запуска
import asyncio
from src.handlers import router
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
USER_ID = int(os.getenv("USER_ID"))

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)

async def run_bot():
    await dp.start_polling(bot)