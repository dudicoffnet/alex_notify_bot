import asyncio
import logging
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# Подключаем Arial.ttf для кириллицы
pdfmetrics.registerFont(TTFont("Arial", "Arial.ttf"))

def generate_pdf():
    filename = "report.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Arial", 14)
    c.drawString(100, 750, "Полный отчёт")
    c.setFont("Arial", 10)
    c.drawString(100, 730, f"Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(100, 710, "- Новости по проектам (боты, реклама, квартиры)")
    c.drawString(100, 695, "- Напоминания и дедлайны")
    c.drawString(100, 680, "- Финансы (BYN, USD, перелёты, траты)")
    c.drawString(100, 665, "- Крипто-обновления и airdrops")
    c.showPage()
    c.save()
    return filename

async def send_pdf():
    pdf = generate_pdf()
    await bot.send_document(ADMIN_ID, types.FSInputFile(pdf), caption="Ежедневный PDF-отчёт")

async def send_zip():
    filename = "alex_notify_bot_direct_zip.zip"
    if os.path.exists(filename):
        await bot.send_document(ADMIN_ID, types.FSInputFile(filename), caption="Архив проекта")
    else:
        await bot.send_message(ADMIN_ID, "Архив проекта не найден.")

@dp.message(Command("force"))
async def cmd_force(message: types.Message):
    pdf = generate_pdf()
    await message.answer_document(types.FSInputFile(pdf), caption="PDF-отчёт по команде /force")
    await send_zip()

async def heartbeat():
    try:
        await bot.get_me()
        logging.info("Heartbeat OK")
    except Exception as e:
        logging.error(f"Heartbeat error: {e}")

async def main():
    scheduler.add_job(send_pdf, "cron", hour=10, minute=0)
    scheduler.add_job(send_zip, "cron", hour=23, minute=0)
    scheduler.add_job(heartbeat, "interval", minutes=5)
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
