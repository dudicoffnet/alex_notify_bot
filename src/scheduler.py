# Планировщик
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import time
import asyncio
from aiogram import Bot
from dotenv import load_dotenv
import os

load_dotenv()
USER_ID = int(os.getenv("USER_ID"))
BASE_DIR = os.getenv("BASE_DIR")

async def send_report(bot: Bot):
    pdf_path = os.path.join(BASE_DIR, "morning.pdf")
    zip_path = os.path.join(BASE_DIR, "reports.zip")
    if os.path.exists(pdf_path):
        await bot.send_document(USER_ID, document=pdf_path)
    if os.path.exists(zip_path):
        await bot.send_document(USER_ID, document=zip_path)