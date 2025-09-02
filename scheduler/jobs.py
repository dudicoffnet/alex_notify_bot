
from zoneinfo import ZoneInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot
from aiogram.types import FSInputFile
from utils.pdf_generator import generate_pdf
import aiohttp, asyncio

TZ = ZoneInfo("Europe/Minsk")

def setup_scheduler(bot: Bot, chat_id: int, health_url: str) -> AsyncIOScheduler:
    sched = AsyncIOScheduler(timezone=TZ)

    async def send_pdf():
        path = generate_pdf("data/report.pdf")
        await bot.send_document(chat_id, FSInputFile(path), caption="📄 Автоотчёт PDF")

    async def self_ping():
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(health_url, timeout=10) as r:
                    await r.text()
        except Exception:
            pass

    sched.add_job(lambda: asyncio.create_task(send_pdf()), CronTrigger(hour=10, minute=0))
    sched.add_job(lambda: asyncio.create_task(send_pdf()), CronTrigger(hour=23, minute=0))
    sched.add_job(lambda: asyncio.create_task(self_ping()), CronTrigger(minute="*/5"))

    sched.start()
    return sched
