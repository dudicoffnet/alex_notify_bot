from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import logging
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
USER_ID = int(os.getenv("USER_ID", "0"))
TIMEZONE = os.getenv("TIMEZONE", "Europe/Minsk")

dp = Dispatcher()
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Бот-уведомитель запущен. Используй /report для отчёта.")

@dp.message(Command("report"))
async def cmd_report(message: Message):
    await message.answer("📝 Здесь будет PDF-отчёт (имитация).")

@dp.message(Command("ping"))
async def cmd_ping(message: Message):
    await message.answer("🏓 Бот работает.")

async def scheduler_task():
    await bot.send_message(USER_ID, "⏰ Это сообщение отправлено по расписанию.")

async def main():
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    scheduler.add_job(scheduler_task, "cron", hour=10, minute=0)
    scheduler.add_job(scheduler_task, "cron", hour=23, minute=0)
    scheduler.start()

    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())