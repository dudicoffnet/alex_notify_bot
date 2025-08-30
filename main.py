import asyncio
import logging
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone="Europe/Minsk")

def generate_pdf():
    filename = "report.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 14)
    c.drawString(100, 750, "Ежедневный отчёт")
    c.setFont("Helvetica", 10)
    c.drawString(100, 730, f"Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Живые блоки — примеры
    c.drawString(100, 710, "🚗 MercedesScanBot — активен")
    c.drawString(100, 695, "📊 Финансы — курс BYN/USD обновлён")
    c.drawString(100, 680, "✈️ Фукуок — проверка билетов выполнена")
    c.drawString(100, 665, "💰 Крипто — свежие миссии собраны")
    c.drawString(100, 650, "🏠 Дом — новости о сносе обработаны")

    c.showPage()
    c.save()
    return filename

def generate_zip():
    import zipfile
    filename = "project.zip"
    with zipfile.ZipFile(filename, "w") as zipf:
        for f in ["main.py", "requirements.txt", "Procfile", ".env.example", "README.txt"]:
            if os.path.exists(f):
                zipf.write(f)
    return filename

async def send_pdf():
    pdf = generate_pdf()
    await bot.send_document(ADMIN_ID, types.FSInputFile(pdf), caption="Автоматический PDF-отчёт")

async def send_zip():
    zf = generate_zip()
    await bot.send_document(ADMIN_ID, types.FSInputFile(zf), caption="Автоматический ZIP-архив")

@dp.message(Command("force"))
async def cmd_force(message: types.Message):
    pdf = generate_pdf()
    await message.answer_document(types.FSInputFile(pdf), caption="PDF-отчёт по команде /force")
    zf = generate_zip()
    await message.answer_document(types.FSInputFile(zf), caption="ZIP по команде /force")

async def heartbeat():
    try:
        await bot.get_me()
        logging.info("Heartbeat OK")
    except Exception as e:
        logging.error(f"Heartbeat error: {e}")

async def main():
    scheduler.add_job(send_pdf, "cron", hour=10, minute=0)   # Утренний PDF
    scheduler.add_job(send_pdf, "cron", hour=23, minute=0)   # Вечерний PDF
    scheduler.add_job(heartbeat, "interval", minutes=5)
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
