
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import zipfile
import os

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

def generate_pdf():
    path = "report.pdf"
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "📄 УТРО. АВТООТЧЁТ ОТ АЛЕКСА")
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"🕒 Время генерации: {now}")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 120, "🟢 Статус: Бот активен")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 150, "🔧 Все системы работают штатно")
    c.drawString(50, height - 170, "📊 Будет сгенерирован ZIP-архив вечером")
    c.drawString(50, 50, "🧠 Отчёт сгенерирован автоматически")
    c.save()
    return path

def generate_zip():
    zip_filename = "backup.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in os.listdir():
            if file.endswith(".py") or file.endswith(".txt"):
                zipf.write(file)
    return zip_filename

async def scheduler():
    while True:
        now = datetime.now().strftime("%H:%M")
        if now == "10:00":
            pdf_path = generate_pdf()
            await bot.send_document(CHAT_ID, FSInputFile(pdf_path), caption="📄 Утренний отчёт")
        if now == "23:00":
            zip_path = generate_zip()
            await bot.send_document(CHAT_ID, FSInputFile(zip_path), caption="📦 Вечерний архив")
        await asyncio.sleep(60)

async def main():
    asyncio.create_task(scheduler())
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
