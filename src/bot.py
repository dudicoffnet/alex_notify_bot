import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from src.handlers import router

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)

async def run_bot():
    print("✅ Бот запущен, ожидает команды...")
    await dp.start_polling(bot)
