
from aiogram import Bot, Dispatcher, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram import Router
import asyncio
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

@router.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer("✅ Бот-уведомитель активен.")

@router.message(F.text == "/ping")
async def ping_handler(message: Message):
    await message.answer("🏓 Бот работает.")

@router.message(F.text == "/report")
async def report_handler(message: Message):
    await bot.send_message(ADMIN_ID, "📝 Ежедневный отчёт: всё под контролем.")

@router.message(F.text == "/sendzip")
async def zip_handler(message: Message):
    await bot.send_document(ADMIN_ID, types.FSInputFile("README.txt"))

async def scheduled_tasks():
    await bot.send_message(ADMIN_ID, "☀️ Доброе утро! Ваш ежедневный отчёт.")
    await asyncio.sleep(1)
    await bot.send_message(ADMIN_ID, "🌙 Вечерняя сводка: день завершён.")

def setup_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(scheduled_tasks, CronTrigger(hour=10, minute=0))
    scheduler.add_job(scheduled_tasks, CronTrigger(hour=23, minute=0))
    scheduler.start()

async def main():
    setup_scheduler()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
