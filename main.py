import asyncio
import logging
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOSScheduler
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import zipfile

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
    c.drawString(100, 750, "Утренний отчёт")
    c.setFont("Arial", 10)
    c.drawString(100, 730, f"Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(100, 710, "- Новости: проекты, обновления")
    c.drawString(100, 695, "- Напоминания: задачи, дедлайны")
    c.drawString(100, 680, "- Финансы и крипто-обновления")
    c.showPage()
    c.save()
    return filename

def generate_zip():
    filename = "backup.zip"
    with zipfile.ZipFile(filename, "w") as zipf:
        zipf.writestr("readme.txt", f"Автоматический архив. Создан: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return filename

async def send_pdf():
    pdf = generate_pdf()
    await bot.send_document(ADMIN_ID, types.FSInputFile(pdf), caption="Ежедневный PDF-отчёт")

async def send_zip():
    zf = generate_zip()
    await bot.send_document(ADMIN_ID, types.FSInputFile(zf), caption="Ежедневный ZIP-архив")

@dp.message(Command("force"))
async def cmd_force(message: types.Message):
    pdf = generate_pdf()
    await message.answer_document(types.FSInputFile(pdf), caption="PDF-отчёт по команде /force")
    zf = generate_zip()
    await message.answer_document(types.FSInputFile(zf), caption="ZIP-архив по команде /force")

@dp.message(Command("archives"))
async def cmd_archives(message: types.Message):
    archives_dir = "archives"
    if not os.path.exists(archives_dir):
        await message.answer("Папка 'archives' пуста или не создана.")
        return
    files = [f for f in os.listdir(archives_dir) if f.endswith(".zip")]
    if not files:
        await message.answer("Нет доступных архивов в папке 'archives'.")
        return
    for f in files:
        await message.answer_document(types.FSInputFile(os.path.join(archives_dir, f)), caption=f"Архив проекта: {f}")

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
