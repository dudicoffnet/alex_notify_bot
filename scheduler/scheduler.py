
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from utils.pdf_generator import generate_pdf
from aiogram import Bot
import os

def setup_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler()
    
    async def send_pdf():
        generate_pdf()
        chat_id = int(os.getenv("YOUR_CHAT_ID"))
        with open("data/report.pdf", "rb") as f:
            await bot.send_document(chat_id, f, caption="📄 Автоотчёт PDF")

    scheduler.add_job(send_pdf, CronTrigger(hour=10, minute=0))
    scheduler.add_job(send_pdf, CronTrigger(hour=23, minute=0))
    scheduler.start()
